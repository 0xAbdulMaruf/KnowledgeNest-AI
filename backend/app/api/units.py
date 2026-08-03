from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unit import Unit
from app.models.topic import Topic
from app.schemas.unit import TopicBrief, UnitResponse
from app.schemas.topic import TopicDetailResponse
from app.schemas.resource import ResourceResponse

router = APIRouter(prefix="/api/units", tags=["units"])


@router.get("/{unit_id}", response_model=UnitResponse)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    unit_resp = UnitResponse.model_validate(unit)
    unit_resp.topics = [TopicBrief.model_validate(t) for t in unit.topics]
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
        if t.unit and t.unit.subject_id:
            topic_data.subject_id = t.unit.subject_id
        grouped: dict[str, list] = {}
        for r in t.resources:
            if r.deleted_at is not None:
                continue
            key = r.type.value
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(ResourceResponse.model_validate(r))
        topic_data.resources_by_type = grouped
        result.append(topic_data)
    return result
