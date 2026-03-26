import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.admin_test import AdminTestQuestion
from app.models.progress import Progress as ProgressModel
from app.models.user import User
from app.services.analytics_service import update_topic_mastery
from app.services.progress_service import update_streak

TOPIC_NAMES = {
    "quantity": "Сан және шама",
    "change_and_relationships": "Өзгерістер мен тәуелділіктер",
    "space_and_shape": "Кеңістік пен пішін",
    "uncertainty_and_data": "Анықсыздық пен деректер",
}

router = APIRouter()


# --- Quiz schemas ---

class QuizAnswerItem(BaseModel):
    question_id: int
    answer: int  # 0-3 index


class QuizSubmit(BaseModel):
    telegram_id: int
    topic_id: str
    answers: list[QuizAnswerItem]
    check_only: bool = False  # If True, only check answers without awarding XP

TOPICS = [
    {
        "id": "quantity",
        "label": "Сан және шама",
        "icon": "🔢",
        "subtopics": [
            {
                "title": "Пропорциялар мен пайыздар",
                "description": "Сандар арасындағы пропорциялар, пайыздық есептеулер және олардың күнделікті өмірдегі қолданысы.",
                "formulas": [
                    {"name": "Пропорция", "latex": "\\frac{a}{b} = \\frac{c}{d}", "description": "Тура пропорция: a·d = b·c"},
                    {"name": "Пайыз табу", "latex": "P = \\frac{A}{B} \\times 100\\%", "description": "A — бөлік, B — бүтін сан"},
                    {"name": "Пайыздық өзгеріс", "latex": "\\Delta\\% = \\frac{V_{жаңа} - V_{ескі}}{V_{ескі}} \\times 100\\%", "description": "Мәннің пайыздық өзгерісі"},
                ],
            },
            {
                "title": "Сандық амалдар",
                "description": "Натурал сандар, бөлшектер, ондық бөлшектер және теріс сандармен амалдар.",
                "formulas": [
                    {"name": "Бөлшектерді қосу", "latex": "\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}", "description": "Ортақ бөлім арқылы қосу"},
                    {"name": "Дәреже", "latex": "a^m \\cdot a^n = a^{m+n}", "description": "Бірдей негізді дәрежелерді көбейту"},
                    {"name": "Түбір", "latex": "\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}", "description": "Көбейтіндінің түбірі"},
                ],
            },
            {
                "title": "Бағалау және дөңгелектеу",
                "description": "Сандарды бағалау, дөңгелектеу және шамамен есептеу дағдылары.",
                "formulas": [
                    {"name": "Дөңгелектеу", "latex": "|x - a| \\leq \\frac{1}{2} \\cdot 10^{-n}", "description": "n-ші разрядқа дейін дөңгелектеу қателігі"},
                    {"name": "Абсолют қателік", "latex": "\\Delta x = |x_{нақты} - x_{шамамен}|", "description": "Бағалау қателігі"},
                ],
            },
        ],
    },
    {
        "id": "change_and_relationships",
        "label": "Өзгерістер мен тәуелділіктер",
        "icon": "📈",
        "subtopics": [
            {
                "title": "Сызықтық теңдеулер мен функциялар",
                "description": "Сызықтық теңдеулерді шешу, функцияларды графикпен бейнелеу.",
                "formulas": [
                    {"name": "Сызықтық функция", "latex": "y = kx + b", "description": "k — бұрыштық коэффициент, b — бос мүше"},
                    {"name": "Сызықтық теңдеу", "latex": "ax + b = 0 \\Rightarrow x = -\\frac{b}{a}", "description": "Бір белгісізді теңдеу"},
                    {"name": "Теңдеулер жүйесі", "latex": "\\begin{cases} a_1x + b_1y = c_1 \\\\ a_2x + b_2y = c_2 \\end{cases}", "description": "Екі белгісізді теңдеулер жүйесі"},
                ],
            },
            {
                "title": "Квадрат теңдеулер мен функциялар",
                "description": "Квадрат теңдеулер, парабола графигі және оның қасиеттері.",
                "formulas": [
                    {"name": "Квадрат теңдеу", "latex": "ax^2 + bx + c = 0", "description": "a, b, c — коэффициенттер"},
                    {"name": "Дискриминант", "latex": "D = b^2 - 4ac", "description": "D > 0: екі түбір, D = 0: бір түбір, D < 0: түбір жоқ"},
                    {"name": "Түбірлер формуласы", "latex": "x = \\frac{-b \\pm \\sqrt{D}}{2a}", "description": "Квадрат теңдеудің түбірлері"},
                ],
            },
            {
                "title": "Заңдылықтар мен тізбектер",
                "description": "Сандық заңдылықтар, арифметикалық және геометриялық прогрессиялар.",
                "formulas": [
                    {"name": "Арифметикалық прогрессия", "latex": "a_n = a_1 + (n-1)d", "description": "d — ортақ айырма"},
                    {"name": "Геометриялық прогрессия", "latex": "b_n = b_1 \\cdot q^{n-1}", "description": "q — ортақ бөлім"},
                    {"name": "АП қосындысы", "latex": "S_n = \\frac{n(a_1 + a_n)}{2}", "description": "Алғашқы n мүшенің қосындысы"},
                ],
            },
        ],
    },
    {
        "id": "space_and_shape",
        "label": "Кеңістік пен пішін",
        "icon": "📐",
        "subtopics": [
            {
                "title": "Ауданы мен периметрі",
                "description": "Жазық фигуралардың ауданы мен периметрін есептеу.",
                "formulas": [
                    {"name": "Тіктөртбұрыш ауданы", "latex": "S = a \\cdot b", "description": "a, b — қабырғалары"},
                    {"name": "Үшбұрыш ауданы", "latex": "S = \\frac{1}{2} a \\cdot h", "description": "a — табаны, h — биіктігі"},
                    {"name": "Шеңбер ауданы", "latex": "S = \\pi r^2", "description": "r — радиус"},
                    {"name": "Шеңбер ұзындығы", "latex": "C = 2\\pi r", "description": "r — радиус"},
                ],
            },
            {
                "title": "Көлемі мен беті",
                "description": "Кеңістіктік денелердің көлемі мен бет ауданы.",
                "formulas": [
                    {"name": "Тікбұрышты параллелепипед", "latex": "V = a \\cdot b \\cdot c", "description": "a, b, c — қырлары"},
                    {"name": "Цилиндр көлемі", "latex": "V = \\pi r^2 h", "description": "r — радиус, h — биіктік"},
                    {"name": "Шар көлемі", "latex": "V = \\frac{4}{3}\\pi r^3", "description": "r — радиус"},
                    {"name": "Конус көлемі", "latex": "V = \\frac{1}{3}\\pi r^2 h", "description": "r — радиус, h — биіктік"},
                ],
            },
            {
                "title": "Координаталық геометрия және түрлендірулер",
                "description": "Координаталар жазықтығы, нүктелер арасындағы қашықтық, симметрия және жылжыту.",
                "formulas": [
                    {"name": "Нүктелер арасы", "latex": "d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}", "description": "Координат жазықтығында қашықтық"},
                    {"name": "Орта нүкте", "latex": "M = \\left(\\frac{x_1+x_2}{2},\\; \\frac{y_1+y_2}{2}\\right)", "description": "Кесіндінің ортасы"},
                    {"name": "Пифагор теоремасы", "latex": "a^2 + b^2 = c^2", "description": "Тікбұрышты үшбұрыш қабырғалары"},
                ],
            },
        ],
    },
    {
        "id": "uncertainty_and_data",
        "label": "Анықсыздық пен деректер",
        "icon": "📊",
        "subtopics": [
            {
                "title": "Орташа мәндер",
                "description": "Деректер жинағының орташа мәні, медианасы, модасы және ауқымы.",
                "formulas": [
                    {"name": "Арифметикалық орта", "latex": "\\bar{x} = \\frac{\\sum_{i=1}^{n} x_i}{n}", "description": "Барлық мәндердің қосындысын санына бөлу"},
                    {"name": "Медиана", "latex": "Me = x_{\\frac{n+1}{2}}", "description": "Реттелген қатардың ортаңғы мәні"},
                    {"name": "Ауқым", "latex": "R = x_{max} - x_{min}", "description": "Ең үлкен мен ең кіші мәннің айырмасы"},
                ],
            },
            {
                "title": "Ықтималдық",
                "description": "Кездейсоқ оқиғалардың ықтималдығын есептеу, тәуелді және тәуелсіз оқиғалар.",
                "formulas": [
                    {"name": "Классикалық ықтималдық", "latex": "P(A) = \\frac{m}{n}", "description": "m — қолайлы жағдайлар, n — барлық жағдайлар"},
                    {"name": "Қосу ережесі", "latex": "P(A \\cup B) = P(A) + P(B) - P(A \\cap B)", "description": "Екі оқиғаның біріккен ықтималдығы"},
                    {"name": "Көбейту ережесі", "latex": "P(A \\cap B) = P(A) \\cdot P(B)", "description": "Тәуелсіз оқиғалар үшін"},
                ],
            },
            {
                "title": "Деректерді талдау",
                "description": "Диаграммалар, кестелер, графиктер арқылы деректерді оқу және түсіндіру.",
                "formulas": [
                    {"name": "Жиілік", "latex": "f_i = \\frac{n_i}{N}", "description": "Салыстырмалы жиілік: n_i — оқиға саны, N — жалпы саны"},
                    {"name": "Дисперсия", "latex": "D = \\frac{\\sum(x_i - \\bar{x})^2}{n}", "description": "Мәндердің орташадан ауытқу шамасы"},
                    {"name": "Стандарт ауытқу", "latex": "\\sigma = \\sqrt{D}", "description": "Дисперсияның квадрат түбірі"},
                ],
            },
        ],
    },
]


@router.get("/topics")
async def get_topics():
    return [{"id": t["id"], "label": t["label"], "icon": t["icon"]} for t in TOPICS]


@router.get("/topics/{topic_id}")
async def get_topic_detail(topic_id: str):
    topic = next((t for t in TOPICS if t["id"] == topic_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail="Тақырып табылмады")
    return topic


OPTION_TO_IDX = {"A": 0, "B": 1, "C": 2, "D": 3}


@router.get("/topics/{topic_id}/quiz")
async def get_topic_quiz(topic_id: str, count: int = 5, db: Session = Depends(get_db)):
    """Get 3-5 MCQ questions for a theory topic mini-test."""
    if not any(t["id"] == topic_id for t in TOPICS):
        raise HTTPException(status_code=404, detail="Тақырып табылмады")

    questions = db.query(AdminTestQuestion).filter(AdminTestQuestion.topic == topic_id).all()

    # Fallback: if not enough topic-specific questions, include from other topics
    if len(questions) < 3:
        other = db.query(AdminTestQuestion).filter(
            AdminTestQuestion.topic != topic_id
        ).all()
        questions.extend(other)

    if not questions:
        return {"questions": [], "topic_id": topic_id}

    selected = random.sample(questions, min(count, len(questions)))
    return {
        "topic_id": topic_id,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "options": [q.option_a, q.option_b, q.option_c, q.option_d],
                "explanation": q.explanation,
                "image_url": q.image_url,
                "table_data": q.table_data,
            }
            for q in selected
        ],
    }


@router.post("/quiz/submit")
async def submit_quiz(body: QuizSubmit, db: Session = Depends(get_db)):
    """Submit mini-test answers, update mastery, award XP."""
    user = db.query(User).filter(User.telegram_id == body.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пайдаланушы табылмады")

    question_ids = [a.question_id for a in body.answers]
    db_questions = db.query(AdminTestQuestion).filter(AdminTestQuestion.id.in_(question_ids)).all()
    question_map = {q.id: q for q in db_questions}

    correct = 0
    total = len(body.answers)
    results = []
    topic_results: dict[str, list[bool]] = {}

    for item in body.answers:
        q = question_map.get(item.question_id)
        if not q:
            continue
        correct_idx = OPTION_TO_IDX.get(q.correct_option, 0)
        is_correct = item.answer == correct_idx
        if is_correct:
            correct += 1

        results.append({
            "question_id": item.question_id,
            "correct": is_correct,
            "correct_answer": correct_idx,
            "explanation": q.explanation,
        })

        topic_key = q.topic if q.topic in [t["id"] for t in TOPICS] else body.topic_id
        topic_results.setdefault(topic_key, []).append(is_correct)

    percentage = round((correct / total * 100) if total > 0 else 0, 1)

    quiz_xp = 0
    if not body.check_only:
        # Award XP (15 per mini-quiz)
        quiz_xp = 15
        user.score = (user.score or 0) + quiz_xp

        update_streak(db, user)

        # Update topic mastery
        if topic_results:
            update_topic_mastery(db, user.id, topic_results)

        # Update Progress table so progress page reflects mini-test results
        progress_rec = (
            db.query(ProgressModel)
            .filter(ProgressModel.user_id == user.id, ProgressModel.topic_id == body.topic_id)
            .first()
        )
        if progress_rec:
            progress_rec.completion_percent = min(100.0, max(progress_rec.completion_percent, percentage))
            progress_rec.problems_solved += total
            progress_rec.last_updated = now
        else:
            db.add(ProgressModel(
                user_id=user.id,
                topic_id=body.topic_id,
                topic_name=TOPIC_NAMES.get(body.topic_id, body.topic_id),
                completion_percent=percentage,
                problems_solved=total,
            ))

        db.commit()

    return {
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "xp_earned": quiz_xp,
        "results": results,
    }
