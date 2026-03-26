from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from app.database.database import Base


class AdminTestQuestion(Base):
    __tablename__ = "admin_test_questions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True, nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String, nullable=False)
    difficulty = Column(String, default="3")
    explanation = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    table_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
