from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unit import Unit
from app.models.topic import Topic
from app.schemas.unit import UnitResponse
from app.schemas.topic import TopicDetailResponse

router = APIRouter(prefix="/api/units", tags=["units"])


@router.get("/{unit_id}", response_model=UnitResponse)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    unit_resp = UnitResponse.model_validate(unit)
    unit_resp.topics = [{"id": t.id, "name": t.name, "importance_score": t.importance_score} for t in unit.topics]
    unit_resp.topics_count = len(unit.topics)
    return unit_resp


@router.get("/{unit_id}/topics", response_model=list[TopicDetailResponse])
def get_unit_topics(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    topics = db.query(Topic).filter(Topic.unit_id == unit_id).all()
    result = []
    for t in topics:
        topic_data = TopicDetailResponse.model_validate(t)
        grouped: dict[str, list] = {}
        for r in t.resources:
            key = r.type.value
            if key not in grouped:
                grouped[key] = []
            grouped[key].append({
                "id": r.id,
                "topic_id": r.topic_id,
                "type": r.type.value,
                "title": r.title,
                "url": r.url or "",
                "content": r.content or "",
                "metadata_": r.metadata_ or {},
            })
        topic_data.resources_by_type = grouped
        result.append(topic_data)
    return result
