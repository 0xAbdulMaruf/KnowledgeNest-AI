import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class ResourceType(str, enum.Enum):
    college_notes = "college_notes"
    external_notes = "external_notes"
    pdf = "pdf"
    video = "video"
    pyq = "pyq"
    important_questions = "important_questions"
    practice_questions = "practice_questions"
    coding_problems = "coding_problems"
    assignment = "assignment"
    book = "book"
    documentation = "documentation"
    image = "image"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, default="")
    content = Column(Text, default="")
    metadata_ = Column("metadata", JSON, default=dict)

    topic = relationship("Topic", back_populates="resources")
