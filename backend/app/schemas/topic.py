from pydantic import BaseModel
from app.schemas.resource import ResourceResponse


class TopicBase(BaseModel):
    name: str
    unit_id: int
    subject_id: int | None = None
    description: str = ""
    tags: list[str] = []
    importance_score: float = 0.0


class TopicCreate(TopicBase):
    pass


class TopicDetailResponse(TopicBase):
    id: int
    resources_by_type: dict[str, list[ResourceResponse]] = {}

    model_config = {"from_attributes": True}
