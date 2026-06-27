from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    description = Column(Text, default="")
    tags = Column(JSON, default=list)
    importance_score = Column(Float, default=0.0)

    unit = relationship("Unit", back_populates="topics")
    resources = relationship("Resource", back_populates="topic", cascade="all, delete-orphan")
