from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceResponse

router = APIRouter(prefix="/api/faculty", tags=["faculty"])


@router.post("/resources", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(
        topic_id=resource.topic_id,
        type=resource.type,
        title=resource.title,
        url=resource.url,
        content=resource.content,
        metadata_=resource.metadata_,
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource
