import base64
import hmac
import json
import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from time import monotonic
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import get_db
from app.models.topic import Topic
from app.models.unit import Unit
from app.models.subject import Subject
from app.llm.provider_client import AIProviderClient
from app.llm.context_builder import build_context, build_general_context, build_unit_context, build_subject_context
from app.llm.prompts import PROMPT_TEMPLATES

router = APIRouter(prefix="/api/ai", tags=["ai"])
logger = logging.getLogger(__name__)
_RATE_WINDOW_SECONDS = 60.0
_RATE_LIMIT = 30
_DEVELOPER_TOKEN_TTL_MINUTES = 60
_request_timestamps: dict[str, list[float]] = defaultdict(list)


AIProvider = Literal["local", "openai", "anthropic", "mimo"]
ContextScope = Literal["topic", "unit", "subject", "general"]


def enforce_rate_limit(request: Request) -> None:
    client_key = request.client.host if request.client else "unknown"
    now = monotonic()
    recent = [timestamp for timestamp in _request_timestamps[client_key] if now - timestamp < _RATE_WINDOW_SECONDS]
    if len(recent) >= _RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many AI requests. Please wait a moment and try again.")
    recent.append(now)
    _request_timestamps[client_key] = recent


def env_ai_config() -> dict[str, str]:
    provider = os.getenv("AI_PROVIDER", "local").strip().lower() or "local"
    if provider not in {"local", "openai", "anthropic", "mimo"}:
        provider = "local"
    return {
        "provider": provider,
        "base_url": os.getenv("AI_BASE_URL", "").strip(),
        "api_key": os.getenv("AI_API_KEY", "").strip(),
        "model": os.getenv("AI_MODEL", "").strip(),
    }


class AIConfigResponse(BaseModel):
    provider: str
    model: str
    api_key_configured: bool
    developer_options_enabled: bool


class DeveloperUnlockRequest(BaseModel):
    password: str = Field(min_length=1, max_length=500)


class DeveloperUnlockResponse(BaseModel):
    access_token: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    developer_token: Optional[str] = Field(default=None, max_length=500)
    topic_id: Optional[int] = None
    question: str = Field(min_length=1, max_length=8000)
    mode: Literal["answer_question", "explain_topic", "generate_quiz", "generate_mcq"] = "answer_question"
    scope: ContextScope = "topic"
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)
    # These are accepted only for an explicit Developer Options override.
    provider: Optional[AIProvider] = None
    base_url: Optional[str] = Field(default=None, max_length=500)
    api_key: Optional[str] = Field(default=None, max_length=500)
    model: Optional[str] = Field(default=None, max_length=200)


class ChatResponse(BaseModel):
    answer: str
    topic_name: str
    mode: str
    provider: str


class ConnectionTestResponse(BaseModel):
    ok: bool
    provider: str
    message: str


def resolved_ai_config(request: ChatRequest, developer_authorized: bool = False) -> dict[str, str]:
    """Use .env values by default; accept request overrides only for a developer session."""
    defaults = env_ai_config()
    if not developer_authorized:
        return defaults
    return {
        "provider": request.provider or defaults["provider"],
        "base_url": request.base_url.strip() if request.base_url else defaults["base_url"],
        "api_key": request.api_key.strip() if request.api_key else defaults["api_key"],
        "model": request.model.strip() if request.model else defaults["model"],
    }


def developer_options_configured() -> bool:
    return bool(
        os.getenv("AI_DEVELOPER_PASSWORD", "").strip()
        and os.getenv("AI_DEVELOPER_TOKEN", "").strip()
    )


def _developer_token_secret() -> bytes:
    return os.getenv("AI_DEVELOPER_TOKEN", "").strip().encode("utf-8")


def _developer_token_ttl() -> timedelta:
    try:
        minutes = max(5, int(os.getenv("AI_DEVELOPER_TOKEN_TTL_MINUTES", str(_DEVELOPER_TOKEN_TTL_MINUTES))))
    except ValueError:
        minutes = _DEVELOPER_TOKEN_TTL_MINUTES
    return timedelta(minutes=minutes)


def _issue_developer_session_token() -> str:
    expires_at = datetime.now(timezone.utc) + _developer_token_ttl()
    payload = json.dumps({"exp": expires_at.timestamp()}, separators=(",", ":")).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).rstrip(b"=")
    signature = hmac.new(_developer_token_secret(), encoded_payload, "sha256").digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=")
    return f"{encoded_payload.decode('ascii')}.{encoded_signature.decode('ascii')}"


def _verify_developer_session_token(token: str | None) -> bool:
    if not token or not developer_options_configured():
        return False
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        expected_signature = hmac.new(_developer_token_secret(), encoded_payload.encode("ascii"), "sha256").digest()
        supplied_signature = base64.urlsafe_b64decode(encoded_signature + "===")
        if not hmac.compare_digest(supplied_signature, expected_signature):
            return False
        payload = json.loads(base64.urlsafe_b64decode(encoded_payload + "===").decode("utf-8"))
        return datetime.now(timezone.utc).timestamp() < float(payload["exp"])
    except (ValueError, KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        return False


def is_developer_authorized(request: ChatRequest) -> bool:
    return _verify_developer_session_token(request.developer_token)


def has_configuration_override(request: ChatRequest) -> bool:
    return any(value is not None for value in (request.provider, request.base_url, request.api_key, request.model))


def require_valid_override_session(request: ChatRequest) -> bool:
    developer_authorized = is_developer_authorized(request)
    if has_configuration_override(request) and not developer_authorized:
        raise HTTPException(status_code=403, detail="Developer Options session is required for AI configuration overrides.")
    return developer_authorized


MAX_HISTORY_CHARS = 24000


def build_history(request: ChatRequest) -> list[tuple[str, str]]:
    """Keep recent conversation turns without allowing history to crowd out context."""
    selected: list[tuple[str, str]] = []
    total_chars = 0
    for message in reversed(request.history[-12:]):
        content = message.content.strip()
        if not content:
            continue
        remaining = MAX_HISTORY_CHARS - total_chars
        if remaining <= 0:
            break
        content = content[:remaining]
        selected.append((message.role, content))
        total_chars += len(content)
    return list(reversed(selected))


def build_ai_client(request: ChatRequest, developer_authorized: bool = False) -> AIProviderClient:
    config = resolved_ai_config(request, developer_authorized)
    return AIProviderClient(
        provider=config["provider"],
        base_url=config["base_url"] or None,
        api_key=config["api_key"] or None,
        model=config["model"] or None,
    )


def build_prompt(request: ChatRequest, topic: Topic | None, all_topics: list[Topic] | None = None, unit: Unit | None = None, subject: Subject | None = None) -> tuple[str, str, str]:
    template_config = PROMPT_TEMPLATES.get(request.mode)
    if not template_config:
        raise HTTPException(status_code=400, detail="Unsupported AI mode")

    if request.scope == "topic" and topic:
        topic_context = build_context(topic)
        topic_name = topic.name
    elif request.scope == "unit" and unit:
        topic_context = build_unit_context(unit)
        topic_name = f"{unit.name} (Unit)"
    elif request.scope == "subject" and subject:
        topic_context = build_subject_context(subject)
        topic_name = f"{subject.name} (Subject)"
    elif request.scope == "general":
        topic_context = build_general_context(all_topics or [], request.question)
        topic_name = "General Assistant"
    elif topic:
        topic_context = build_context(topic)
        topic_name = topic.name
    else:
        topic_context = build_general_context(all_topics or [], request.question)
        topic_name = "General Assistant"

    prompt = template_config["template"].format(context=topic_context, question=request.question.strip())
    return prompt, template_config["system"], topic_name


@router.get("/config", response_model=AIConfigResponse)
def get_ai_config() -> AIConfigResponse:
    config = env_ai_config()
    return AIConfigResponse(
        provider=config["provider"],
        model=config["model"],
        api_key_configured=bool(config["api_key"]),
        developer_options_enabled=developer_options_configured(),
    )


@router.post("/developer/unlock", response_model=DeveloperUnlockResponse, dependencies=[Depends(enforce_rate_limit)])
def unlock_developer(request: DeveloperUnlockRequest) -> DeveloperUnlockResponse:
    configured_password = os.getenv("AI_DEVELOPER_PASSWORD", "")
    if not developer_options_configured() or not hmac.compare_digest(request.password, configured_password):
        raise HTTPException(status_code=401, detail="Invalid developer password")
    return DeveloperUnlockResponse(access_token=_issue_developer_session_token())


def _load_scope_data(request: ChatRequest, db: Session) -> tuple[Topic | None, Unit | None, Subject | None, list[Topic] | None]:
    """Load the academic data relevant to the requested scope."""
    topic: Topic | None = None
    unit: Unit | None = None
    subject: Subject | None = None
    all_topics: list[Topic] | None = None

    if request.topic_id is not None:
        topic = (
            db.query(Topic)
            .options(joinedload(Topic.unit).joinedload(Unit.subject), selectinload(Topic.resources))
            .filter(Topic.id == request.topic_id)
            .first()
        )
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

    if request.scope == "unit" and topic and topic.unit:
        unit = (
            db.query(Unit)
            .options(joinedload(Unit.subject), selectinload(Unit.topics).selectinload(Topic.resources))
            .filter(Unit.id == topic.unit_id)
            .first()
        )
    elif request.scope == "subject" and topic and topic.unit and topic.unit.subject:
        subject = (
            db.query(Subject)
            .options(selectinload(Subject.units).selectinload(Unit.topics).selectinload(Topic.resources))
            .filter(Subject.id == topic.unit.subject_id)
            .first()
        )
    elif request.scope == "general" or topic is None:
        all_topics = (
            db.query(Topic)
            .options(joinedload(Topic.unit).joinedload(Unit.subject), selectinload(Topic.resources))
            .all()
        )

    return topic, unit, subject, all_topics


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db), _: None = Depends(enforce_rate_limit)):
    topic, unit, subject, all_topics = _load_scope_data(request, db)
    prompt, system, topic_name = build_prompt(request, topic, all_topics, unit, subject)
    developer_authorized = require_valid_override_session(request)
    config = resolved_ai_config(request, developer_authorized)
    client = build_ai_client(request, developer_authorized)
    try:
        answer = await client.generate(prompt=prompt, system=system, history=build_history(request))
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI provider request failed for provider=%s", config["provider"])
        raise HTTPException(status_code=502, detail="AI provider request failed. Check Developer Options or the server environment.") from exc
    finally:
        await client.close()

    return ChatResponse(answer=answer or "No response was returned.", topic_name=topic_name, mode=request.mode, provider=config["provider"])


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db), _: None = Depends(enforce_rate_limit)):
    topic, unit, subject, all_topics = _load_scope_data(request, db)
    prompt, system, _ = build_prompt(request, topic, all_topics, unit, subject)
    developer_authorized = require_valid_override_session(request)
    config = resolved_ai_config(request, developer_authorized)
    client = build_ai_client(request, developer_authorized)
    history = build_history(request)

    async def generate():
        try:
            async for chunk in client.generate_stream(prompt=prompt, system=system, history=history):
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
        except Exception:  # noqa: BLE001
            logger.exception("AI streaming request failed for provider=%s", config["provider"])
            yield f"data: {json.dumps({'error': 'AI provider request failed. Check Developer Options or the server environment.', 'done': True})}\n\n"
        finally:
            await client.close()

    return StreamingResponse(generate(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.post("/test-connection", response_model=ConnectionTestResponse)
async def test_connection(request: ChatRequest, _: None = Depends(enforce_rate_limit)):
    developer_authorized = require_valid_override_session(request)
    config = resolved_ai_config(request, developer_authorized)
    client = build_ai_client(request, developer_authorized)
    try:
        await client.test_connection()
        return ConnectionTestResponse(ok=True, provider=config["provider"], message="Connection successful")
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI connection test failed for provider=%s", config["provider"])
        raise HTTPException(status_code=502, detail="Connection test failed. Check Developer Options or the server environment.") from exc
    finally:
        await client.close()
