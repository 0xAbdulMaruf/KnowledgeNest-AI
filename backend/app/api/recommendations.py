from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import get_db
from app.models.topic import Topic
from app.models.unit import Unit
from app.models.subject import Subject
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

recommendation_service = RecommendationService()


@router.get("/{topic_id}")
def get_recommendations(
    topic_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    # ── Load source topic with all relationships ──────────
    topic = (
        db.query(Topic)
        .options(
            joinedload(Topic.unit).joinedload(Unit.subject),
            selectinload(Topic.resources),
        )
        .filter(Topic.id == topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # ── Load all topics eagerly (one query) ────────────────
    all_topics = (
        db.query(Topic)
        .options(
            joinedload(Topic.unit).joinedload(Unit.subject),
            selectinload(Topic.resources),
        )
        .all()
    )

    # ── Get recommendations with multi-signal scoring ─────
    similar_with_signals = recommendation_service.find_similar_topics_with_signals(
        topic_id, all_topics, limit
    )

    # ── Build response — no N+1 queries! ──────────────────
    topic_map: dict[int, Topic] = {t.id: t for t in all_topics}
    recommendations = []
    for similar_id, score, signals, reason in similar_with_signals:
        rec_topic = topic_map.get(similar_id)
        if not rec_topic:
            continue

        unit = rec_topic.unit
        subject = unit.subject if unit else None

        recommendations.append({
            "id": rec_topic.id,
            "name": rec_topic.name,
            "description": rec_topic.description,
            "tags": rec_topic.tags or [],
            "unit_id": rec_topic.unit_id,
            "unit_name": unit.name if unit else None,
            "subject_name": subject.name if subject else None,
            "importance_score": rec_topic.importance_score or 0.0,
            "relevance_score": round(score * 100, 1),
            "match_reason": reason,
        })

    return {
        "topic_id": topic_id,
        "topic_name": topic.name,
        "recommendations": recommendations,
        "total": len(recommendations),
    }
