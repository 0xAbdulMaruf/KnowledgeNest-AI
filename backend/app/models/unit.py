from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    description = Column(Text, default="")

    subject = relationship("Subject", back_populates="units")
    topics = relationship("Topic", back_populates="unit", cascade="all, delete-orphan")
