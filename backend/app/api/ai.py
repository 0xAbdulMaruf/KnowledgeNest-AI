import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.topic import Topic
from app.llm.provider_client import AIProviderClient
from app.llm.context_builder import build_context
from app.llm.prompts import PROMPT_TEMPLATES

router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    topic_id: Optional[int] = None
    question: str
    mode: str = "answer_question"
    history: list[ChatMessage] = Field(default_factory=list)
    provider: str = "local"
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    topic_name: str
    mode: str
    provider: str


class ConnectionTestResponse(BaseModel):
    ok: bool
    provider: str
    message: str


def build_conversation_context(history: list[ChatMessage], max_messages: int = 5) -> str:
    """Build conversation context from recent message history."""
    if not history:
        return ""
    
    recent = history[-max_messages:]
    context_parts = []
    for msg in recent:
        role = "User" if msg.role == "user" else "Assistant"
        context_parts.append(f"{role}: {msg.content}")
    
    return "\n".join(context_parts)


def build_ai_client(request: ChatRequest) -> AIProviderClient:
    return AIProviderClient(
        provider=request.provider or "local",
        base_url=request.base_url,
        api_key=request.api_key,
        model=request.model,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    topic = None
    if request.topic_id is not None:
        topic = db.query(Topic).filter(Topic.id == request.topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

    template_config = PROMPT_TEMPLATES.get(request.mode)
    if not template_config:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown mode. Available: {list(PROMPT_TEMPLATES.keys())}",
        )

    if topic:
        # Build context from topic resources
        topic_context = build_context(topic)
        topic_name = topic.name
    else:
        topic_context = (
            "General academic assistant mode. The user has not selected a specific topic. "
            "Answer clearly, ask clarifying questions when needed, and keep the response relevant to study help."
        )
        topic_name = "General Assistant"
    
    # Build conversation history context
    history_context = build_conversation_context(request.history)
    
    # Combine contexts
    full_context = f"Topic Context:\n{topic_context}"
    if history_context:
        full_context += f"\n\nConversation History:\n{history_context}"
    
    prompt = template_config["template"].format(
        context=full_context,
        question=request.question,
    )
    system = template_config["system"]

    client = build_ai_client(request)

    try:
        answer = await client.generate(prompt=prompt, system=system)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI provider request failed: {str(e)}") from e

    return ChatResponse(answer=answer, topic_name=topic_name, mode=request.mode, provider=request.provider or "local")


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):
    """Stream AI response using Server-Sent Events."""
    topic = None
    if request.topic_id is not None:
        topic = db.query(Topic).filter(Topic.id == request.topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

    template_config = PROMPT_TEMPLATES.get(request.mode)
    if not template_config:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown mode. Available: {list(PROMPT_TEMPLATES.keys())}",
        )

    if topic:
        # Build context
        topic_context = build_context(topic)
    else:
        topic_context = (
            "General academic assistant mode. The user has not selected a specific topic. "
            "Answer clearly, ask clarifying questions when needed, and keep the response relevant to study help."
        )
    history_context = build_conversation_context(request.history)
    
    full_context = f"Topic Context:\n{topic_context}"
    if history_context:
        full_context += f"\n\nConversation History:\n{history_context}"
    
    prompt = template_config["template"].format(
        context=full_context,
        question=request.question,
    )
    system = template_config["system"]

    client = build_ai_client(request)

    async def generate():
        try:
            async for chunk in client.generate_stream(prompt=prompt, system=system):
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/test-connection", response_model=ConnectionTestResponse)
async def test_connection(request: ChatRequest):
    client = build_ai_client(request)
    try:
        await client.test_connection()
        return ConnectionTestResponse(ok=True, provider=request.provider or "local", message="Connection successful")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Connection test failed: {str(e)}") from e
