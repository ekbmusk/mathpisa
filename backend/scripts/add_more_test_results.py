"""Add 10-20 extra TestResult records for each demo user (language_code = 'kk').

Usage (from backend/):
    python scripts/add_more_test_results.py
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
    rng = random.Random(20260526)
    now = datetime.now(timezone.utc)

    with SessionLocal() as db:
        questions = db.query(AdminTestQuestion).all()
        if not questions:
            print("Нет admin_test_questions.")
            return

        # Demo users: kk language + non-admin + not the 'do not disturb' tester
        demo_users = (
            db.query(User)
            .filter(User.language_code == "kk")
            .filter(User.is_admin == False)  # noqa: E712
            .all()
        )

        if not demo_users:
            print("Демо-юзеров не найдено.")
            return

        added_tests = 0
        progress_cache: dict[tuple[int, str], Progress] = {}
        for p in db.query(Progress).filter(Progress.user_id.in_([u.id for u in demo_users])).all():
            progress_cache[(p.user_id, p.topic_id)] = p

        for user in demo_users:
            n_extra = rng.randint(10, 20)
            created_at = user.created_at or (now - timedelta(days=30))
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            days_span = max(1, (now - created_at).days)

            topic_correct: dict[str, int] = {}
            topic_total: dict[str, int] = {}
            user_xp_gain = 0

            for _ in range(n_extra):
                qs = rng.sample(questions, min(rng.randint(5, 10), len(questions)))
                answers = []
                correct_count = 0
                accuracy_target = rng.uniform(0.55, 0.95)
                for q in qs:
                    correct_idx = OPT_TO_IDX.get(q.correct_option, 0)
                    if rng.random() < accuracy_target:
                        answer = correct_idx
                        is_correct = True
                        correct_count += 1
                    else:
                        answer = rng.choice([j for j in range(4) if j != correct_idx])
                        is_correct = False
                    answers.append({
                        "question_id": q.id,
                        "answer": answer,
                        "correct": is_correct,
                    })
                    topic_total[q.topic] = topic_total.get(q.topic, 0) + 1
                    if is_correct:
                        topic_correct[q.topic] = topic_correct.get(q.topic, 0) + 1

                pct = round(correct_count / len(qs) * 100, 1)
                user_xp_gain += int(pct)

                tr_created = created_at + timedelta(
                    days=rng.randint(0, days_span),
                    hours=rng.randint(0, 23),
                    minutes=rng.randint(0, 59),
                )
                db.add(TestResult(
                    user_id=user.id,
                    total_questions=len(qs),
                    correct_answers=correct_count,
                    percentage=pct,
                    answers=answers,
                    created_at=tr_created,
                ))
                added_tests += 1

            # Bump score so leaderboards stay coherent
            user.score = (user.score or 0) + user_xp_gain

            # Update / create Progress per topic
            for topic_id, total in topic_total.items():
                acc = round(topic_correct.get(topic_id, 0) / total * 100, 1)
                key = (user.id, topic_id)
                rec = progress_cache.get(key)
                if rec:
                    rec.completion_percent = min(100.0, max(rec.completion_percent or 0, acc))
                    rec.problems_solved = (rec.problems_solved or 0) + total
                    rec.last_updated = now
                else:
                    new_rec = Progress(
                        user_id=user.id,
                        topic_id=topic_id,
                        topic_name=TOPIC_NAMES_KK.get(topic_id, topic_id),
                        completion_percent=acc,
                        problems_solved=total,
                        last_updated=now,
                    )
                    db.add(new_rec)
                    progress_cache[key] = new_rec

        db.commit()

        print(f"✓ Демо-юзеров обработано: {len(demo_users)}")
        print(f"✓ Добавлено test_results: {added_tests}")
        print(f"✓ Всего test_results в БД: {db.query(TestResult).count()}")


if __name__ == "__main__":
    run()
