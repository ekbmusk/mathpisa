from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, date
import random

from app.database.database import get_db
from app.models.user import User
from app.models.test_result import TestResult
from app.models.progress import Progress as ProgressModel
from app.models.admin_test import AdminTestQuestion
from app.schemas.test_result import TestSet, TestQuestion, TestSubmit, TestResultOut
from app.services.analytics_service import update_topic_mastery
from app.services.achievement_service import check_and_award
from app.services.progress_service import update_streak

router = APIRouter()

TOPIC_META = {
    "quantity": "Сан және шама",
    "change_and_relationships": "Өзгерістер мен тәуелділіктер",
    "space_and_shape": "Кеңістік пен пішін",
    "uncertainty_and_data": "Анықсыздық пен деректер",
}

OPTION_TO_IDX = {"A": 0, "B": 1, "C": 2, "D": 3}

# Keep TEST_BANK only for initial seed (used by database.py seeder)
TEST_BANK = [
    {"id": 1, "topic": "quantity", "question": "250-нің 12%-ы неге тең?", "options": ["25", "30", "28", "32"], "correct_answer": 1, "explanation": "250 × 12/100 = 30."},
    {"id": 2, "topic": "quantity", "question": "Егер $\\frac{3}{5} = \\frac{x}{20}$ болса, $x$ нешеге тең?", "options": ["10", "15", "12", "18"], "correct_answer": 2, "explanation": "Айқас көбейту: 3 × 20 = 5x → x = 60/5 = 12."},
    {"id": 3, "topic": "change_and_relationships", "question": "$3x - 7 = 14$ теңдеуін шешіңіз.", "options": ["5", "7", "3", "21"], "correct_answer": 1, "explanation": "3x = 14 + 7 = 21, x = 21/3 = 7."},
    {"id": 4, "topic": "change_and_relationships", "question": "$y = 2x + 1$ функциясының графигі қай нүктеден өтеді?", "options": ["(0, 1)", "(1, 0)", "(0, 2)", "(2, 0)"], "correct_answer": 0, "explanation": "x = 0 болғанда y = 2(0) + 1 = 1, сондықтан (0, 1) нүктесі."},
    {"id": 5, "topic": "space_and_shape", "question": "Қабырғасы 6 см квадраттың ауданы нешеге тең?", "options": ["24 см²", "36 см²", "12 см²", "48 см²"], "correct_answer": 1, "explanation": "S = a² = 6² = 36 см²."},
    {"id": 6, "topic": "space_and_shape", "question": "Пифагор теоремасы бойынша, катеттері 5 және 12 болса, гипотенуза нешеге тең?", "options": ["17", "13", "15", "14"], "correct_answer": 1, "explanation": "c = √(5² + 12²) = √(25 + 144) = √169 = 13."},
    {"id": 7, "topic": "uncertainty_and_data", "question": "Деректер: 4, 7, 7, 9, 13. Медиана неге тең?", "options": ["7", "8", "9", "4"], "correct_answer": 0, "explanation": "Реттелген қатарда ортаңғы мән 7."},
    {"id": 8, "topic": "uncertainty_and_data", "question": "Монетаны 2 рет лақтырғанда екеуі де елтаңба болу ықтималдығы?", "options": ["1/2", "1/4", "1/3", "1/8"], "correct_answer": 1, "explanation": "P = 1/2 × 1/2 = 1/4."},
    {"id": 9, "topic": "change_and_relationships", "question": "$x^2 - 9 = 0$ теңдеуінің шешімдері қандай?", "options": ["3 және -3", "9 және -9", "3 және 0", "0 және -3"], "correct_answer": 0, "explanation": "x² = 9, x = ±3."},
    {"id": 10, "topic": "quantity", "question": "$2^5$ неге тең?", "options": ["10", "25", "32", "64"], "correct_answer": 2, "explanation": "2⁵ = 2×2×2×2×2 = 32."},
    {"id": 11, "topic": "space_and_shape", "question": "Радиусы 10 см шеңбердің ұзындығы нешеге тең? ($\\pi \\approx 3.14$)", "options": ["31.4 см", "62.8 см", "314 см", "20 см"], "correct_answer": 1, "explanation": "C = 2πr = 2 × 3.14 × 10 = 62.8 см."},
    {"id": 12, "topic": "uncertainty_and_data", "question": "Кәсіпорынның 5 жылдағы пайдасы (млн тг): 10, 15, 12, 18, 20. Орташа жылдық пайда?", "options": ["12", "15", "18", "20"], "correct_answer": 1, "explanation": "Орташа = (10+15+12+18+20)/5 = 75/5 = 15 млн тг."},
]


def _db_to_question(q: AdminTestQuestion) -> TestQuestion:
    return TestQuestion(
        id=q.id,
        question=q.question,
        options=[q.option_a, q.option_b, q.option_c, q.option_d],
        correct_answer=OPTION_TO_IDX.get(q.correct_option, 0),
        explanation=q.explanation,
        image_url=q.image_url,
        table_data=q.table_data,
    )


@router.get("/topics")
def get_topics(db: Session = Depends(get_db)):
    rows = db.query(AdminTestQuestion.topic).distinct().all()
    topics = []
    for (topic_id,) in rows:
        count = db.query(AdminTestQuestion).filter(AdminTestQuestion.topic == topic_id).count()
        topics.append({
            "id": topic_id,
            "name": TOPIC_META.get(topic_id, topic_id),
            "count": count,
        })
    return topics


@router.get("/daily", response_model=TestSet)
def get_daily_test(db: Session = Depends(get_db)):
    seed = int(date.today().strftime("%Y%m%d"))
    all_qs = db.query(AdminTestQuestion).all()
    if not all_qs:
        return TestSet(questions=[])
    rng = random.Random(seed)
    selected = rng.sample(all_qs, min(10, len(all_qs)))
    return TestSet(questions=[_db_to_question(q) for q in selected])


@router.get("/daily/status/{telegram_id}")
def get_daily_status(telegram_id: int, db: Session = Depends(get_db)):
    today = date.today().isoformat()
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    completed = bool(user and user.last_daily_date == today)
    return {"completed": completed, "bonus_xp": 50}


@router.get("/random", response_model=TestSet)
def get_random_test(count: int = 10, topic: str = None, db: Session = Depends(get_db)):
    query = db.query(AdminTestQuestion)
    if topic:
        query = query.filter(AdminTestQuestion.topic == topic)
    all_qs = query.all()
    if not all_qs:
        return TestSet(questions=[])
    selected = random.sample(all_qs, min(count, len(all_qs)))
    return TestSet(questions=[_db_to_question(q) for q in selected])


@router.post("/submit", response_model=TestResultOut)
async def submit_test(body: TestSubmit, db: Session = Depends(get_db)):
    question_ids = [a.question_id for a in body.answers]
    db_questions = db.query(AdminTestQuestion).filter(AdminTestQuestion.id.in_(question_ids)).all()
    question_map = {q.id: q for q in db_questions}

    correct = 0
    total = len(body.answers)
    detailed_answers = []
    topic_correct: dict[str, int] = {}
    topic_total: dict[str, int] = {}

    for answer_item in body.answers:
        q = question_map.get(answer_item.question_id)
        if not q:
            continue
        correct_idx = OPTION_TO_IDX.get(q.correct_option, 0)
        is_correct = answer_item.answer == correct_idx
        if is_correct:
            correct += 1
        detailed_answers.append({
            "question_id": answer_item.question_id,
            "answer": answer_item.answer,
            "correct": is_correct,
        })
        topic_total[q.topic] = topic_total.get(q.topic, 0) + 1
        if is_correct:
            topic_correct[q.topic] = topic_correct.get(q.topic, 0) + 1

    percentage = round((correct / total * 100) if total > 0 else 0, 1)
    actual_bonus_xp = 0
    new_achievements = []
    result = None

    if body.telegram_id:
        user = db.query(User).filter(User.telegram_id == body.telegram_id).first()
        if not user:
            user = User(telegram_id=body.telegram_id)
            db.add(user)
            db.flush()
        elif user.is_banned:
            raise HTTPException(status_code=403, detail="Сіздің аккаунт бұғатталған")

        base_xp = int(percentage)
        bonus_xp = 0
        today_str = date.today().isoformat()

        if body.is_daily and user.last_daily_date != today_str:
            user.last_daily_date = today_str
            db.flush()  # Prevent race condition on concurrent submissions
            actual_bonus_xp = 50

        user.score = (user.score or 0) + base_xp + actual_bonus_xp
        update_streak(db, user)

        result = TestResult(
            user_id=user.id,
            total_questions=total,
            correct_answers=correct,
            percentage=percentage,
            answers=detailed_answers,
        )
        db.add(result)

        now = datetime.now(timezone.utc)
        for topic_id, t_total in topic_total.items():
            t_score = round((topic_correct.get(topic_id, 0) / t_total) * 100, 1)
            rec = (
                db.query(ProgressModel)
                .filter(ProgressModel.user_id == user.id, ProgressModel.topic_id == topic_id)
                .first()
            )
            if rec:
                rec.completion_percent = min(100.0, max(rec.completion_percent, t_score))
                rec.problems_solved += 1
                rec.last_updated = now
            else:
                db.add(ProgressModel(
                    user_id=user.id,
                    topic_id=topic_id,
                    topic_name=TOPIC_META.get(topic_id, topic_id),
                    completion_percent=t_score,
                    problems_solved=1,
                    last_updated=now,
                ))

        # Update topic mastery with per-question results
        mastery_results: dict[str, list[bool]] = {}
        for answer_item in body.answers:
            q = question_map.get(answer_item.question_id)
            if not q:
                continue
            correct_idx = OPTION_TO_IDX.get(q.correct_option, 0)
            is_correct_item = answer_item.answer == correct_idx
            mastery_results.setdefault(q.topic, []).append(is_correct_item)
        if mastery_results:
            update_topic_mastery(db, user.id, mastery_results)

        new_achievements = check_and_award(db, user)
        db.commit()

    result_id = result.id if body.telegram_id and result else None
    return TestResultOut(
        result_id=result_id,
        correct=correct,
        total=total,
        percentage=percentage,
        passed=percentage >= 70,
        xp_earned=int(percentage) if body.telegram_id else 0,
        bonus_xp=actual_bonus_xp,
        new_achievements=new_achievements if body.telegram_id else [],
    )


@router.get("/history/{telegram_id}")
async def get_test_history(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return []
    if user.is_banned:
        raise HTTPException(status_code=403, detail="Сіздің аккаунт бұғатталған")
    results = (
        db.query(TestResult)
        .filter(TestResult.user_id == user.id)
        .order_by(TestResult.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": r.id,
            "correct": r.correct_answers,
            "total": r.total_questions,
            "percentage": r.percentage,
            "date": r.created_at.strftime("%d.%m.%Y"),
        }
        for r in results
    ]


@router.get("/review/{result_id}")
async def review_test(result_id: int, db: Session = Depends(get_db)):
    """Return full question details for reviewing a completed test."""
    test_result = db.query(TestResult).filter(TestResult.id == result_id).first()
    if not test_result:
        raise HTTPException(status_code=404, detail="Тест нәтижесі табылмады")

    answers_data = test_result.answers or []
    question_ids = [a.get("question_id") for a in answers_data if a.get("question_id")]
    db_questions = db.query(AdminTestQuestion).filter(AdminTestQuestion.id.in_(question_ids)).all()
    q_map = {q.id: q for q in db_questions}

    questions = []
    for a in answers_data:
        q = q_map.get(a.get("question_id"))
        if not q:
            continue
        correct_idx = OPTION_TO_IDX.get(q.correct_option, 0)
        questions.append({
            "question": q.question,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "your_answer": a.get("answer"),
            "correct_answer": correct_idx,
            "correct": a.get("correct", False),
            "explanation": q.explanation,
            "topic": TOPIC_META.get(q.topic, q.topic),
            "image_url": q.image_url,
            "table_data": q.table_data,
        })

    return {
        "percentage": test_result.percentage,
        "correct": test_result.correct_answers,
        "total": test_result.total_questions,
        "questions": questions,
    }
