from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class PYQ(Base):
    __tablename__ = "pyqs"

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    paper_code = Column(String, default="")
    paper_title = Column(String, default="")
    question_id = Column(String, default="")
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="")
    marks = Column(String, default="")
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
