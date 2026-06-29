from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.database import Base


class FacultyActivity(Base):
    __tablename__ = "faculty_activities"

    id = Column(Integer, primary_key=True, index=True)
    teacher_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)