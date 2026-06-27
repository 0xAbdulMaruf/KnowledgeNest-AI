from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    description = Column(Text, default="")
    tags = Column(JSON, default=list)

    semester = relationship("Semester", back_populates="subjects")
    units = relationship("Unit", back_populates="subject", cascade="all, delete-orphan")
