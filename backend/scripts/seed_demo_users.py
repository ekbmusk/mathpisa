"""Seed 30 demo users with Kazakh names, completed tests, AI chat history, and progress.

Usage (from backend/):
    python -m scripts.seed_demo_users
"""
from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
# Load .env from project root (same path as backend/main.py uses)
load_dotenv(BACKEND_DIR.parent / ".env")
# Allow `python scripts/seed_demo_users.py` from backend/
sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal, create_tables  # noqa: E402
from app.models.admin_test import AdminTestQuestion  # noqa: E402
from app.models.chat_history import ChatHistory  # noqa: E402
from app.models.progress import Progress  # noqa: E402
from app.models.test_result import TestResult  # noqa: E402
from app.models.topic_mastery import TopicMastery  # noqa: E402
from app.models.user import User  # noqa: E402


KZ_FIRST_NAMES = [
    "Айбек", "Айдана", "Айгерім", "Алишер", "Аружан", "Асылжан", "Әсем", "Әлихан",
    "Бекзат", "Балауса", "Дамир", "Диана", "Дінмұхаммед", "Ерасыл", "Еркежан",
    "Жанибек", "Жасмин", "Әділ", "Аян", "Камила", "Қуаныш", "Мадина", "Мерей",
    "Нұрсұлтан", "Нұрай", "Олжас", "Райымбек", "Сабина", "Сұлтан", "Тимур",
    "Томирис", "Ұлан", "Ілияс", "Айзере", "Әсел", "Бауыржан", "Гүлназ",
]

KZ_LAST_NAMES = [
    "Ермеков", "Серікқызы", "Темірбекова", "Қасымов", "Жұмабай", "Сатыбалды",
    "Нұрланқызы", "Бекетов", "Ахметова", "Ілиясов", "Сейтжанов", "Дәулетова",
    "Қанатов", "Болатов", "Ескендір", "Ержанов", "Тұрсынбек", "Қайратқызы",
    "Балабекова", "Молдабай", "Сапарғали", "Темірлан", "Жарасов", "Әбілқас",
    "Ораз", "Хамитова", "Әлмұхамед", "Бақытжанов", "Дәурен", "Қожахмет",
]

AI_QA_PAIRS = [
    (
        "Квадрат теңдеуді қалай шешеді?",
        "Квадрат теңдеу $ax^2 + bx + c = 0$ түрінде болады. Дискриминант формуласын қолданамыз: "
        "$D = b^2 - 4ac$. Егер $D > 0$ болса, екі түбір бар: $x = \\frac{-b \\pm \\sqrt{D}}{2a}$. "
        "Мысал: $x^2 - 5x + 6 = 0$ үшін $D = 25 - 24 = 1$, $x_1 = 3$, $x_2 = 2$.",
    ),
    (
        "Пифагор теоремасын түсіндіріңізші.",
        "Пифагор теоремасы тікбұрышты үшбұрышта қолданылады: $a^2 + b^2 = c^2$, мұндағы $c$ — "
        "гипотенуза, $a$ және $b$ — катеттер. Мысалы, катеттері 3 және 4 болса, "
        "гипотенуза $\\sqrt{9 + 16} = 5$ болады.",
    ),
    (
        "Пайыз қалай есептеледі?",
        "Пайыз деген — жүзден алынған үлес. Санның $p$%-ын табу үшін: $\\text{нәтиже} = "
        "\\frac{\\text{сан} \\times p}{100}$. Мысалы, 250-нің 12%-ы: $\\frac{250 \\times 12}{100} = 30$.",
    ),
    (
        "Шеңбердің ұзындығы қалай табылады?",
        "Шеңбердің ұзындығы $C = 2\\pi r$ формуласымен табылады, мұндағы $r$ — радиус. "
        "Мысалы, радиусы 10 см шеңбердің ұзындығы $2 \\times 3.14 \\times 10 = 62.8$ см.",
    ),
    (
        "Орташа мән мен медиана айырмашылығы неде?",
        "Орташа мән — барлық сандардың қосындысын олардың санына бөлу: "
        "$\\bar{x} = \\frac{\\sum x_i}{n}$. Медиана — реттелген қатардың дәл ортасындағы сан. "
        "Деректер: 4, 7, 7, 9, 13 → орташа = 8, медиана = 7.",
    ),
    (
        "Ықтималдықты қалай есептейді?",
        "Ықтималдық $P = \\frac{\\text{қолайлы оқиғалар саны}}{\\text{барлық мүмкін оқиғалар саны}}$. "
        "Мысалы, монетаны екі рет лақтырғанда екеуі де елтаңба болу ықтималдығы $\\frac{1}{2} \\times \\frac{1}{2} = \\frac{1}{4}$.",
    ),
    (
        "Сызықтық функцияның графигі қалай салынады?",
        "$y = kx + b$ функциясының графигі — түзу. Екі нүкте табу жеткілікті: мысалы, "
        "$x=0$ кезінде $y=b$, $x=1$ кезінде $y=k+b$. Осы екі нүктені қосамыз.",
    ),
    (
        "Квадраттың ауданын қалай табады?",
        "Квадраттың ауданы $S = a^2$ формуласымен есептеледі, мұндағы $a$ — қабырғасының ұзындығы. "
        "Мысалы, $a = 6$ см болса, $S = 36$ см².",
    ),
    (
        "Бөлшекті ондық бөлшекке қалай айналдырамын?",
        "Алымын бөліміне бөлесіз. Мысалы, $\\frac{3}{4} = 3 \\div 4 = 0.75$. "
        "$\\frac{1}{3} = 0.333...$ — периодты ондық бөлшек.",
    ),
    (
        "Дәреже дегеніміз не?",
        "Дәреже — санды өзіне бірнеше рет көбейту: $a^n = a \\cdot a \\cdots a$ ($n$ рет). "
        "Мысалы, $2^5 = 2 \\times 2 \\times 2 \\times 2 \\times 2 = 32$.",
    ),
    (
        "Үшбұрыштың ауданы қалай табылады?",
        "Үшбұрыштың ауданы $S = \\frac{1}{2} a h$ формуласымен есептеледі, мұндағы $a$ — табан, "
        "$h$ — биіктік. Тікбұрышты үшбұрыш үшін катеттер арқылы: $S = \\frac{1}{2} a b$.",
    ),
    (
        "Пропорция дегеніміз не?",
        "Пропорция — екі қатынастың теңдігі: $\\frac{a}{b} = \\frac{c}{d}$. Айқас көбейту арқылы "
        "белгісізді табамыз. Мысалы, $\\frac{3}{5} = \\frac{x}{20}$ → $5x = 60$ → $x = 12$.",
    ),
]


TOPIC_NAMES_KK = {
    "quantity": "Сан және шама",
    "change_and_relationships": "Өзгерістер мен тәуелділіктер",
    "space_and_shape": "Кеңістік пен пішін",
    "uncertainty_and_data": "Анықсыздық пен деректер",
    "Жалпы физика": "Жалпы физика",
}

OPT_TO_IDX = {"A": 0, "B": 1, "C": 2, "D": 3}


def random_telegram_id(rng: random.Random) -> int:
    return rng.randint(900_000_000, 9_999_999_999)


def make_username(first: str, last: str, idx: int) -> str:
    base = (first[:3] + last[:3]).lower()
    # Replace non-ascii with simple translit-ish letters; fallback to user index
    safe = "".join(c if c.isalnum() else "" for c in base)
    return f"{safe or 'user'}{idx:02d}"


def seed():
    rng = random.Random(20260525)

    # Make sure tables exist
    create_tables()

    with SessionLocal() as db:
        questions = db.query(AdminTestQuestion).all()
        if not questions:
            print("Нет admin_test_questions — нечего отвечать. Запусти backend хоть раз, чтобы seed прошёл.")
            return

        used_telegram_ids: set[int] = set(
            tid for (tid,) in db.query(User.telegram_id).all()
        )

        created_users: list[User] = []
        names = list(zip(KZ_FIRST_NAMES, KZ_LAST_NAMES))
        rng.shuffle(names)

        now = datetime.now(timezone.utc)

        for i in range(30):
            first, last = names[i % len(names)]
            while True:
                tid = random_telegram_id(rng)
                if tid not in used_telegram_ids:
                    used_telegram_ids.add(tid)
                    break

            score = rng.randint(80, 900)
            streak = rng.randint(0, 14)
            created_at = now - timedelta(days=rng.randint(3, 60))
            last_activity = now - timedelta(hours=rng.randint(0, 72))

            user = User(
                telegram_id=tid,
                username=make_username(first, last, i + 1),
                first_name=first,
                last_name=last,
                language_code="kk",
                is_active=True,
                score=score,
                streak=streak,
                level=str(rng.randint(2, 5)),
                created_at=created_at,
                last_activity=last_activity,
                last_daily_date=(now - timedelta(days=rng.randint(0, 3))).date().isoformat(),
                notifications_enabled=True,
            )
            db.add(user)
            db.flush()  # need user.id
            created_users.append(user)

            # --- Test results (1-5 tests per user) ---
            n_tests = rng.randint(2, 5)
            topic_correct: dict[str, int] = {}
            topic_total: dict[str, int] = {}

            for t in range(n_tests):
                qs = rng.sample(questions, min(rng.randint(5, 10), len(questions)))
                answers = []
                correct_count = 0
                for q in qs:
                    correct_idx = OPT_TO_IDX.get(q.correct_option, 0)
                    # 65-90% chance of right answer
                    if rng.random() < rng.uniform(0.65, 0.9):
                        answer = correct_idx
                        is_correct = True
                        correct_count += 1
                    else:
                        wrong_choices = [j for j in range(4) if j != correct_idx]
                        answer = rng.choice(wrong_choices)
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
                tr_created = created_at + timedelta(days=rng.randint(0, max(1, (now - created_at).days)))
                db.add(TestResult(
                    user_id=user.id,
                    total_questions=len(qs),
                    correct_answers=correct_count,
                    percentage=pct,
                    answers=answers,
                    created_at=tr_created,
                ))

            # --- Progress per topic ---
            for topic_id, total in topic_total.items():
                accuracy = round(topic_correct.get(topic_id, 0) / total * 100, 1)
                db.add(Progress(
                    user_id=user.id,
                    topic_id=topic_id,
                    topic_name=TOPIC_NAMES_KK.get(topic_id, topic_id),
                    completion_percent=accuracy,
                    problems_solved=total,
                    last_updated=now,
                ))

            # --- Topic mastery records (best-effort) ---
            for topic_id, total in topic_total.items():
                correct = topic_correct.get(topic_id, 0)
                acc = round(correct / total * 100, 1)
                last5 = [rng.random() < (correct / total) for _ in range(min(5, total))]
                try:
                    db.add(TopicMastery(
                        user_id=user.id,
                        topic_id=topic_id,
                        total_attempts=total,
                        correct_attempts=correct,
                        current_accuracy=acc,
                        last_5_results=__import__("json").dumps(last5),
                        estimated_level=rng.randint(2, 5),
                        last_attempted=now,
                    ))
                except Exception:
                    pass

            # --- AI chat history (3-7 Q/A pairs) ---
            n_chats = rng.randint(3, 7)
            chat_pairs = rng.sample(AI_QA_PAIRS, min(n_chats, len(AI_QA_PAIRS)))
            chat_time = created_at + timedelta(hours=1)
            for q_text, a_text in chat_pairs:
                db.add(ChatHistory(
                    telegram_id=tid,
                    role="user",
                    content=q_text,
                    created_at=chat_time,
                ))
                chat_time += timedelta(seconds=rng.randint(5, 30))
                db.add(ChatHistory(
                    telegram_id=tid,
                    role="assistant",
                    content=a_text,
                    created_at=chat_time,
                ))
                chat_time += timedelta(minutes=rng.randint(1, 60))

        db.commit()

        print(f"✓ Создано юзеров: {len(created_users)}")
        print(f"✓ Test results: {db.query(TestResult).count()}")
        print(f"✓ Chat history записей: {db.query(ChatHistory).count()}")
        print(f"✓ Progress записей: {db.query(Progress).count()}")


if __name__ == "__main__":
    seed()
