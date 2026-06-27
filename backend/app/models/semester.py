from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False, unique=True)

    subjects = relationship("Subject", back_populates="semester", cascade="all, delete-orphan")
