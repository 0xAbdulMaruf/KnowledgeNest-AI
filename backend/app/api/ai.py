import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.topic import Topic
from app.llm.ollama_client import OllamaClient
from app.llm.context_builder import build_context
from app.llm.prompts import PROMPT_TEMPLATES

router = APIRouter(prefix="/api/ai", tags=["ai"])

ollama_client = OllamaClient()


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    topic_id: Optional[int] = None
    question: str
    mode: str = "answer_question"
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    answer: str
    topic_name: str
    mode: str


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

    try:
        answer = await ollama_client.generate(prompt=prompt, system=system)
    except Exception as e:
        # If Ollama is not available, provide a helpful fallback
        answer = f"I apologize, but I'm currently unable to connect to the AI service. Please try again later or check if Ollama is running.\n\nError: {str(e)}"

    return ChatResponse(answer=answer, topic_name=topic_name, mode=request.mode)


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

    async def generate():
        try:
            async for chunk in ollama_client.generate_stream(prompt=prompt, system=system):
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
