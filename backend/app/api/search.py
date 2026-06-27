import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.unit import Unit
from app.models.resource import Resource

router = APIRouter(prefix="/api/search", tags=["search"])


def calculate_relevance(query: str, text: str) -> float:
    """Calculate relevance score based on query match quality."""
    if not text:
        return 0.0
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Exact match gets highest score
    if query_lower == text_lower:
        return 1.0
    
    # Starts with query gets high score
    if text_lower.startswith(query_lower):
        return 0.9
    
    # Contains query as whole word gets medium score
    if f" {query_lower} " in f" {text_lower} ":
        return 0.7
    
    # Contains query gets lower score
    if query_lower in text_lower:
        return 0.5
    
    return 0.0


def has_matching_tag(tags, query: str) -> bool:
    """Check if any tag matches the query."""
    if not tags:
        return False
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except:
            return False
    query_lower = query.lower()
    return any(query_lower in str(tag).lower() for tag in tags)


@router.get("/")
def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    pattern = f"%{q}%"
    q_lower = q.lower()

    # Search subjects
    subjects = (
        db.query(Subject)
        .filter(
            or_(
                Subject.name.ilike(pattern),
                Subject.description.ilike(pattern),
                Subject.code.ilike(pattern),
            )
        )
        .all()
    )

    # Search topics
    topics = (
        db.query(Topic)
        .filter(
            or_(
                Topic.name.ilike(pattern),
                Topic.description.ilike(pattern),
            )
        )
        .all()
    )

    # Search units
    units = (
        db.query(Unit)
        .filter(
            or_(
                Unit.name.ilike(pattern),
                Unit.description.ilike(pattern),
            )
        )
        .all()
    )

    # Search resources
    resources = (
        db.query(Resource)
        .filter(
            or_(
                Resource.title.ilike(pattern),
                Resource.content.ilike(pattern),
            )
        )
        .limit(10)
        .all()
    )

    # Calculate relevance scores and filter
    def get_subject_score(s):
        score = max(
            calculate_relevance(q, s.name),
            calculate_relevance(q, s.code),
            calculate_relevance(q, s.description or ""),
        )
        if has_matching_tag(s.tags, q):
            score = max(score, 0.6)
        return score

    def get_topic_score(t):
        score = max(
            calculate_relevance(q, t.name),
            calculate_relevance(q, t.description or ""),
        )
        if has_matching_tag(t.tags, q):
            score = max(score, 0.6)
        return score

    def get_unit_score(u):
        return max(
            calculate_relevance(q, u.name),
            calculate_relevance(q, u.description or ""),
        )

    def get_resource_score(r):
        return max(
            calculate_relevance(q, r.title),
            calculate_relevance(q, r.content or ""),
        )

    # Filter and sort by relevance
    subjects_scored = [(s, get_subject_score(s)) for s in subjects]
    subjects_scored = [(s, sc) for s, sc in subjects_scored if sc > 0 or has_matching_tag(s.tags, q)]
    subjects_scored.sort(key=lambda x: x[1], reverse=True)

    topics_scored = [(t, get_topic_score(t)) for t in topics]
    topics_scored = [(t, sc) for t, sc in topics_scored if sc > 0 or has_matching_tag(t.tags, q)]
    topics_scored.sort(key=lambda x: x[1], reverse=True)

    units_scored = [(u, get_unit_score(u)) for u in units]
    units_scored = [(u, sc) for u, sc in units_scored if sc > 0]
    units_scored.sort(key=lambda x: x[1], reverse=True)

    resources_scored = [(r, get_resource_score(r)) for r in resources]
    resources_scored = [(r, sc) for r, sc in resources_scored if sc > 0]
    resources_scored.sort(key=lambda x: x[1], reverse=True)

    # Get subject names for topics and units
    subject_map = {s.id: s.name for s in db.query(Subject).all()}
    unit_map = {u.id: (u.name, u.subject_id) for u in db.query(Unit).all()}

    return {
        "query": q,
        "subjects": [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "description": s.description,
                "tags": s.tags or [],
                "relevance": round(score, 2),
                "type": "subject",
            }
            for s, score in subjects_scored[:limit]
        ],
        "topics": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "tags": t.tags or [],
                "unit_id": t.unit_id,
                "unit_name": unit_map.get(t.unit_id, (None, None))[0],
                "subject_name": subject_map.get(unit_map.get(t.unit_id, (None, None))[1]),
                "relevance": round(score, 2),
                "type": "topic",
            }
            for t, score in topics_scored[:limit]
        ],
        "units": [
            {
                "id": u.id,
                "name": u.name,
                "description": u.description,
                "subject_id": u.subject_id,
                "subject_name": subject_map.get(u.subject_id),
                "relevance": round(score, 2),
                "type": "unit",
            }
            for u, score in units_scored[:limit]
        ],
        "resources": [
            {
                "id": r.id,
                "title": r.title,
                "type": r.type.value if r.type else "unknown",
                "topic_id": r.topic_id,
                "topic_name": unit_map.get(r.topic_id, (None, None))[0],
                "relevance": round(score, 2),
                "type": "resource",
            }
            for r, score in resources_scored[:limit]
        ],
        "total_results": len(subjects_scored) + len(topics_scored) + len(units_scored) + len(resources_scored),
    }
