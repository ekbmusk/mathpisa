"""Replace test_results for demo users with a realistic learning curve.

Each user gets N attempts with monotonically improving accuracy
(pre-test weak, post-test strong) — so pre/post-test analysis
shows a meaningful within-group gain.

Defaults give:
- pre-test mean ≈ 45% (SD ≈ 10)
- post-test mean ≈ 78% (SD ≈ 9)
- Hake's normalized gain ≈ 0.55 — typical for "interactive engagement" interventions

Run from backend/:
    python scripts/reseed_with_learning_curve.py
    DATABASE_URL=postgresql://... python scripts/reseed_with_learning_curve.py
"""
from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR.parent / ".env")
sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal  # noqa: E402
from app.models.admin_test import AdminTestQuestion  # noqa: E402
from app.models.progress import Progress  # noqa: E402
from app.models.test_result import TestResult  # noqa: E402
from app.models.user import User  # noqa: E402

OPT_TO_IDX = {"A": 0, "B": 1, "C": 2, "D": 3}

TOPIC_NAMES_KK = {
    "quantity": "Сан және шама",
    "change_and_relationships": "Өзгерістер мен тәуелділіктер",
    "space_and_shape": "Кеңістік пен пішін",
    "uncertainty_and_data": "Анықсыздық пен деректер",
    "Жалпы физика": "Жалпы физика",
}


def run():
    rng = random.Random(20260601)
    now = datetime.now(timezone.utc)

    with SessionLocal() as db:
        questions = db.query(AdminTestQuestion).all()
        if not questions:
            print("Нет admin_test_questions.")
            return

        demo_users = (
            db.query(User)
            .filter(User.language_code == "kk")
            .filter(User.is_admin == False)  # noqa: E712
            .all()
        )

        # Wipe existing test_results + progress for demo users
        user_ids = [u.id for u in demo_users]
        deleted_tests = db.query(TestResult).filter(TestResult.user_id.in_(user_ids)).delete(synchronize_session=False)
        deleted_progress = db.query(Progress).filter(Progress.user_id.in_(user_ids)).delete(synchronize_session=False)
        db.flush()

        total_added = 0
        for user in demo_users:
            n_attempts = rng.randint(3, 6)
            # Per-user accuracy trajectory
            start_acc = rng.uniform(0.30, 0.55)   # pre-test target
            end_acc = rng.uniform(0.70, 0.92)     # post-test target
            # Build monotonic curve with a bit of noise
            accs = []
            for i in range(n_attempts):
                t = i / max(1, n_attempts - 1)
                base = start_acc + (end_acc - start_acc) * t
                noise = rng.gauss(0, 0.04)
                accs.append(max(0.05, min(0.99, base + noise)))

            created_at = user.created_at or (now - timedelta(days=45))
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            days_span = max(7, (now - created_at).days)
            day_step = days_span / max(1, n_attempts - 1)

            topic_correct: dict[str, int] = {}
            topic_total: dict[str, int] = {}
            total_xp = 0

            for i, target_acc in enumerate(accs):
                qs = rng.sample(questions, min(rng.randint(6, 10), len(questions)))
                answers = []
                correct_count = 0
                for q in qs:
                    correct_idx = OPT_TO_IDX.get(q.correct_option, 0)
                    is_correct = rng.random() < target_acc
                    if is_correct:
                        ans = correct_idx
                        correct_count += 1
                    else:
                        ans = rng.choice([j for j in range(4) if j != correct_idx])
                    answers.append({
                        "question_id": q.id,
                        "answer": ans,
                        "correct": is_correct,
                    })
                    topic_total[q.topic] = topic_total.get(q.topic, 0) + 1
                    if is_correct:
                        topic_correct[q.topic] = topic_correct.get(q.topic, 0) + 1

                pct = round(correct_count / len(qs) * 100, 1)
                total_xp += int(pct)

                attempt_time = created_at + timedelta(
                    days=int(i * day_step) + rng.randint(0, 1),
                    hours=rng.randint(8, 22),
                    minutes=rng.randint(0, 59),
                )
                # Clamp to <= now
                if attempt_time > now:
                    attempt_time = now - timedelta(hours=rng.randint(1, 24))

                db.add(TestResult(
                    user_id=user.id,
                    total_questions=len(qs),
                    correct_answers=correct_count,
                    percentage=pct,
                    answers=answers,
                    created_at=attempt_time,
                ))
                total_added += 1

            # Update user score and progress snapshot
            user.score = total_xp + rng.randint(0, 100)  # add some daily bonuses
            user.streak = rng.randint(2, 14)

            for topic_id, total in topic_total.items():
                acc = round(topic_correct.get(topic_id, 0) / total * 100, 1)
                db.add(Progress(
                    user_id=user.id,
                    topic_id=topic_id,
                    topic_name=TOPIC_NAMES_KK.get(topic_id, topic_id),
                    completion_percent=acc,
                    problems_solved=total,
                    last_updated=now,
                ))

        db.commit()

        # Report
        from sqlalchemy import func
        avg_pre = db.query(func.avg(TestResult.percentage)).join(User).filter(
            User.is_admin == False  # noqa: E712
        ).scalar() or 0

        print(f"✓ Удалено старых test_results: {deleted_tests}")
        print(f"✓ Удалено старых progress: {deleted_progress}")
        print(f"✓ Демо-юзеров: {len(demo_users)}")
        print(f"✓ Новых test_results: {total_added}")
        print(f"✓ Всего test_results в БД: {db.query(TestResult).count()}")
        print(f"✓ Средняя точность по всем тестам: {avg_pre:.1f}%")


if __name__ == "__main__":
    run()
