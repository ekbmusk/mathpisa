from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TopicProgress(BaseModel):
    topic_id: str
    name: str
    icon: str
    percent: float
    problems_solved: int


class RecentTest(BaseModel):
    id: int
    date: str
    score: float
    correct: int = 0
    total: int = 0


class ProgressOut(BaseModel):
    tests_taken: int
    avg_score: float
    problems_solved: int
    streak: int
    total_score: int
    topics: List[TopicProgress]
    recent_tests: List[RecentTest]


class ProgressUpdate(BaseModel):
    telegram_id: int
    topic_id: str
    score: float
