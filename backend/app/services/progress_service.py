from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.models.user import User
from app.models.test_result import TestResult
from app.models.progress import Progress

# Kazakhstan timezone (UTC+5) for day boundary comparison
KZ_TZ = timezone(timedelta(hours=5))


def get_or_create_user(db: Session, telegram_id: int, **kwargs) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, **kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def update_streak(db: Session, user: User):
    """Update user streak based on Kazakhstan local dates.
    Does NOT commit — caller is responsible for committing."""
    now = datetime.now(timezone.utc)
    last = user.last_activity

    if last:
        last_aware = last.replace(tzinfo=timezone.utc) if last.tzinfo is None else last
        now_kz = now.astimezone(KZ_TZ).date()
        last_kz = last_aware.astimezone(KZ_TZ).date()
        diff_days = (now_kz - last_kz).days

        if diff_days == 1:
            user.streak = (user.streak or 0) + 1
        elif diff_days == 0:
            pass  # Already active today
        else:
            user.streak = 1
    else:
        user.streak = 1

    user.last_activity = now


def calculate_user_score(db: Session, user_id: int) -> int:
    results = db.query(TestResult).filter(TestResult.user_id == user_id).all()
    return sum(int(r.percentage) for r in results)


def get_user_stats(db: Session, user: User) -> dict:
    tests = db.query(TestResult).filter(TestResult.user_id == user.id).all()
    tests_taken = len(tests)
    avg_score = round(sum(t.percentage for t in tests) / tests_taken, 1) if tests_taken else 0

    progress = db.query(Progress).filter(Progress.user_id == user.id).all()
    problems_solved = sum(p.problems_solved for p in progress)

    return {
        "tests_taken": tests_taken,
        "avg_score": avg_score,
        "problems_solved": problems_solved,
        "streak": user.streak or 0,
        "total_score": user.score or 0,
    }
