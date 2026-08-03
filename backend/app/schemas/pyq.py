from pydantic import BaseModel
from typing import Optional


class PYQBase(BaseModel):
    session: str
    year: int
    paper_code: str = ""
    paper_title: str = ""
    question_id: str = ""
    question_text: str
    question_type: str = ""
    marks: str = ""
    subject_id: Optional[int] = None
    unit_id: Optional[int] = None
    topic_id: Optional[int] = None


class PYQCreate(PYQBase):
    pass


class PYQResponse(PYQBase):
    id: int

    model_config = {"from_attributes": True}


class PYQListResponse(BaseModel):
    id: int
    session: str
    year: int
    paper_code: str = ""
    paper_title: str = ""
    question_id: str = ""
    question_text: str
    question_type: str = ""
    marks: str = ""
    unit_name: Optional[str] = None
    topic_name: Optional[str] = None


class PYQSessionResponse(BaseModel):
    session: str
    year: int
    paper_code: str = ""
    paper_title: str = ""
    question_count: int
