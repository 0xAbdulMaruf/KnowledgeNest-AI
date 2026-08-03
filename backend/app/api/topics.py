from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType
from app.schemas.topic import TopicDetailResponse
from app.schemas.resource import ResourceResponse

router = APIRouter(prefix="/api/topics", tags=["topics"])


@router.get("/{topic_id}", response_model=TopicDetailResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic_data = TopicDetailResponse.model_validate(topic)
    # Inject subject_id so the frontend can build correct breadcrumb links
    if topic.unit and topic.unit.subject_id:
        topic_data.subject_id = topic.unit.subject_id
    grouped: dict[str, list] = {}
    for r in topic.resources:
        if r.deleted_at is not None:
            continue
        key = r.type.value
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(ResourceResponse.model_validate(r))
    topic_data.resources_by_type = grouped
    return topic_data


@router.get("/{topic_id}/resources", response_model=list[ResourceResponse])
def get_topic_resources(
    topic_id: int,
    type: ResourceType | None = Query(None),
    db: Session = Depends(get_db),
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    query = db.query(Resource).filter(Resource.topic_id == topic_id, Resource.deleted_at.is_(None))
    if type is not None:
        query = query.filter(Resource.type == type)
    return query.all()
