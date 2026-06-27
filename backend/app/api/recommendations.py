from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.topic import Topic
from app.models.unit import Unit
from app.models.subject import Subject
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

recommendation_service = RecommendationService()


def get_match_reason(source_topic: Topic, recommended_topic: Topic) -> str:
    """Generate a human-readable reason for the recommendation."""
    reasons = []
    
    # Check tag overlap
    source_tags = set(source_topic.tags or [])
    rec_tags = set(recommended_topic.tags or [])
    common_tags = source_tags & rec_tags
    if common_tags:
        reasons.append(f"Shares tags: {', '.join(list(common_tags)[:3])}")
    
    # Check same unit
    if source_topic.unit_id == recommended_topic.unit_id:
        reasons.append("Same unit")
    
    # Check similar importance
    if abs((source_topic.importance_score or 0) - (recommended_topic.importance_score or 0)) < 0.2:
        reasons.append("Similar importance level")
    
    if not reasons:
        reasons.append("Related content")
    
    return "; ".join(reasons)


@router.get("/{topic_id}")
def get_recommendations(
    topic_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    source_unit = db.query(Unit).filter(Unit.id == topic.unit_id).first()
    source_subject_id = source_unit.subject_id if source_unit else None

    all_topics = db.query(Topic).all()
    candidate_topics = all_topics

    if source_subject_id is not None:
        same_subject_topics = (
            db.query(Topic)
            .join(Unit, Topic.unit_id == Unit.id)
            .filter(Unit.subject_id == source_subject_id, Topic.id != topic_id)
            .all()
        )

        # Prefer same-subject recommendations when the subject has enough
        # content to produce a useful result set. Fall back to all topics only
        # when the subject is too small.
        if len(same_subject_topics) >= 2:
            candidate_topics = [topic, *same_subject_topics]

    similar_ids_with_scores = recommendation_service.find_similar_topics_with_scores(topic_id, candidate_topics, limit)

    # Get related topics with scores
    recommendations = []
    for similar_id, score in similar_ids_with_scores:
        t = db.query(Topic).filter(Topic.id == similar_id).first()
        if t:
            # Get unit and subject info
            unit = db.query(Unit).filter(Unit.id == t.unit_id).first()
            subject = None
            if unit:
                subject = db.query(Subject).filter(Subject.id == unit.subject_id).first()
            
            recommendations.append({
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "tags": t.tags or [],
                "unit_id": t.unit_id,
                "unit_name": unit.name if unit else None,
                "subject_name": subject.name if subject else None,
                "importance_score": t.importance_score or 0.0,
                "relevance_score": round(score * 100, 1),
                "match_reason": get_match_reason(topic, t),
            })

    return {
        "topic_id": topic_id,
        "topic_name": topic.name,
        "recommendations": recommendations,
        "total": len(recommendations),
    }
