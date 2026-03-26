import json
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class TopicMastery(Base):
    __tablename__ = "topic_mastery"
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(String, nullable=False, index=True)
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    current_accuracy = Column(Float, default=0.0)
    last_5_results = Column(String, default="[]")  # JSON array of booleans
    estimated_level = Column(Integer, default=3)
    last_attempted = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="topic_mastery_records")

    def get_last_5(self) -> list[bool]:
        try:
            return json.loads(self.last_5_results or "[]")
        except (json.JSONDecodeError, TypeError):
            return []

    def set_last_5(self, results: list[bool]):
        self.last_5_results = json.dumps(results[-5:])

    @property
    def last_5_accuracy(self) -> float:
        results = self.get_last_5()
        if not results:
            return 0.0
        return sum(results) / len(results) * 100
