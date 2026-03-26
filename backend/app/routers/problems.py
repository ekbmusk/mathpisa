from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database.database import get_db
from app.models.problem import Problem
from app.models.user import User
from app.schemas.problem import ProblemOut, AnswerCheck, AnswerResult
from app.services.progress_service import update_streak

router = APIRouter()

# Seed problems if DB is empty
SEED_PROBLEMS = [
    {
        "topic": "quantity",
        "question": "Дүкенде тауар бағасы 20%-ға арзандады. Бастапқы бағасы 5000 теңге болса, жаңа бағасын табыңыз.",
        "formula": "P_{жаңа} = P \\cdot (1 - \\frac{d}{100})",
        "correct_answer": "4000",
        "solution": "Жеңілдік: 5000 × 20/100 = 1000 теңге. Жаңа баға: 5000 - 1000 = 4000 теңге.",
        "difficulty": "1",
        "tags": ["пайыз", "бағалау"],
    },
    {
        "topic": "quantity",
        "question": "Рецептте 4 адамға 600 г ұн керек. 6 адамға қанша ұн керек?",
        "formula": "\\frac{a}{b} = \\frac{c}{d}",
        "correct_answer": "900",
        "solution": "Пропорция: 600/4 = x/6. x = 600 × 6/4 = 900 г.",
        "difficulty": "1",
        "tags": ["пропорция"],
    },
    {
        "topic": "quantity",
        "question": "$\\frac{3}{4} + \\frac{2}{3}$ неге тең?",
        "formula": "\\frac{a}{b} + \\frac{c}{d} = \\frac{ad+bc}{bd}",
        "correct_answer": "1.4167",
        "solution": "Ортақ бөлім 12: 9/12 + 8/12 = 17/12 ≈ 1.4167",
        "difficulty": "2",
        "tags": ["бөлшек", "қосу"],
    },
    {
        "topic": "change_and_relationships",
        "question": "Теңдеуді шешіңіз: $2x + 6 = 20$. $x$ неге тең?",
        "formula": "ax + b = c \\Rightarrow x = \\frac{c - b}{a}",
        "correct_answer": "7",
        "solution": "2x = 20 - 6 = 14. x = 14/2 = 7.",
        "difficulty": "1",
        "tags": ["сызықтық теңдеу"],
    },
    {
        "topic": "change_and_relationships",
        "question": "$x^2 - 5x + 6 = 0$ теңдеуінің түбірлерінің қосындысын табыңыз.",
        "formula": "x_1 + x_2 = -\\frac{b}{a}",
        "correct_answer": "5",
        "solution": "Виет теоремасы бойынша: x₁ + x₂ = -(-5)/1 = 5. Тексеру: D = 25-24 = 1, x = 2 және x = 3, қосындысы 5.",
        "difficulty": "3",
        "tags": ["квадрат теңдеу", "Виет теоремасы"],
    },
    {
        "topic": "change_and_relationships",
        "question": "Арифметикалық прогрессияда $a_1 = 3$, $d = 4$. $a_{10}$ табыңыз.",
        "formula": "a_n = a_1 + (n-1)d",
        "correct_answer": "39",
        "solution": "a₁₀ = 3 + (10-1)×4 = 3 + 36 = 39.",
        "difficulty": "2",
        "tags": ["прогрессия", "заңдылық"],
    },
    {
        "topic": "space_and_shape",
        "question": "Радиусы 7 см шеңбердің ауданын табыңыз. ($\\pi \\approx 3.14$)",
        "formula": "S = \\pi r^2",
        "correct_answer": "153.86",
        "solution": "S = 3.14 × 7² = 3.14 × 49 = 153.86 см².",
        "difficulty": "2",
        "tags": ["аудан", "шеңбер"],
    },
    {
        "topic": "space_and_shape",
        "question": "Тікбұрышты үшбұрыштың катеттері 3 см және 4 см. Гипотенузасын табыңыз.",
        "formula": "c = \\sqrt{a^2 + b^2}",
        "correct_answer": "5",
        "solution": "c = √(3² + 4²) = √(9 + 16) = √25 = 5 см.",
        "difficulty": "2",
        "tags": ["Пифагор теоремасы", "үшбұрыш"],
    },
    {
        "topic": "space_and_shape",
        "question": "Тікбұрышты параллелепипедтің қырлары 3, 4, 5 см. Көлемін табыңыз.",
        "formula": "V = a \\cdot b \\cdot c",
        "correct_answer": "60",
        "solution": "V = 3 × 4 × 5 = 60 см³.",
        "difficulty": "1",
        "tags": ["көлем", "параллелепипед"],
    },
    {
        "topic": "uncertainty_and_data",
        "question": "5 оқушының бойы: 155, 160, 158, 162, 165 см. Орташа бойды табыңыз.",
        "formula": "\\bar{x} = \\frac{\\sum x_i}{n}",
        "correct_answer": "160",
        "solution": "Орташа = (155 + 160 + 158 + 162 + 165) / 5 = 800 / 5 = 160 см.",
        "difficulty": "1",
        "tags": ["орташа мән", "статистика"],
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Қапта 3 қызыл, 5 көк, 2 жасыл шар бар. Кездейсоқ көк шар алу ықтималдығын табыңыз.",
        "formula": "P(A) = \\frac{m}{n}",
        "correct_answer": "0.5",
        "solution": "Барлығы: 3 + 5 + 2 = 10 шар. P(көк) = 5/10 = 0.5.",
        "difficulty": "2",
        "tags": ["ықтималдық"],
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Деректер жинағы: 2, 3, 3, 5, 7, 8, 8, 8, 10. Моданы табыңыз.",
        "formula": "",
        "correct_answer": "8",
        "solution": "Мода — ең жиі кездесетін мән. 8 саны 3 рет кездеседі — ол мода.",
        "difficulty": "1",
        "tags": ["мода", "статистика"],
    },
    {
        "topic": "change_and_relationships",
        "question": "$f(x) = 3x - 2$ функциясы үшін $f(5)$ мәнін табыңыз.",
        "formula": "f(x) = kx + b",
        "correct_answer": "13",
        "solution": "f(5) = 3 × 5 - 2 = 15 - 2 = 13.",
        "difficulty": "1",
        "tags": ["функция", "мән табу"],
    },
    {
        "topic": "space_and_shape",
        "question": "$A(1, 2)$ және $B(4, 6)$ нүктелері арасындағы қашықтықты табыңыз.",
        "formula": "d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}",
        "correct_answer": "5",
        "solution": "d = √((4-1)² + (6-2)²) = √(9 + 16) = √25 = 5.",
        "difficulty": "3",
        "tags": ["координаталық геометрия", "қашықтық"],
    },
    {
        "topic": "quantity",
        "question": "Банкке 100 000 теңге 10% жылдық пайызбен салынды. 2 жылдан кейін қанша ақша болады? (күрделі пайыз)",
        "formula": "A = P(1 + r)^t",
        "correct_answer": "121000",
        "solution": "A = 100000 × (1 + 0.1)² = 100000 × 1.21 = 121000 теңге.",
        "difficulty": "4",
        "tags": ["күрделі пайыз", "қаржылық математика"],
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Екі сүйекті бір мезгілде лақтырғанда, қосындысы 7 болу ықтималдығы қандай?",
        "formula": "P = \\frac{m}{n}",
        "correct_answer": "0.1667",
        "solution": "Барлық жағдай: 6×6 = 36. Қосындысы 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6 жағдай. P = 6/36 = 1/6 ≈ 0.1667.",
        "difficulty": "4",
        "tags": ["ықтималдық", "комбинаторика"],
    },
]


def seed_problems(db: Session):
    count = db.query(Problem).count()
    if count == 0:
        for p in SEED_PROBLEMS:
            db.add(Problem(**p))
        db.commit()


@router.get("", response_model=List[ProblemOut])
async def get_problems(
    difficulty: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    seed_problems(db)
    query = db.query(Problem)
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    if topic:
        query = query.filter(Problem.topic == topic)
    return query.all()


@router.get("/{problem_id}", response_model=ProblemOut)
async def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Есеп табылмады")
    return problem


@router.post("/{problem_id}/check", response_model=AnswerResult)
async def check_answer(problem_id: int, body: AnswerCheck, request: Request, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Есеп табылмады")

    # Normalize answer for comparison
    user_ans = body.answer.strip().replace(",", ".").lower()
    correct = problem.correct_answer.strip().replace(",", ".").lower()

    is_correct = user_ans == correct
    # Fallback: numeric comparison with tolerance
    if not is_correct:
        try:
            is_correct = abs(float(user_ans) - float(correct)) < 0.01
        except (ValueError, TypeError):
            pass

    # Update streak on correct answer
    if is_correct:
        try:
            init_data = request.headers.get("x-telegram-init-data", "")
            if "user" in init_data:
                import json, urllib.parse
                params = dict(urllib.parse.parse_qsl(init_data))
                user_data = json.loads(params.get("user", "{}"))
                telegram_id = user_data.get("id")
                if telegram_id:
                    user = db.query(User).filter(User.telegram_id == telegram_id).first()
                    if user:
                        update_streak(db, user)
                        db.commit()
        except Exception:
            pass

    return AnswerResult(
        correct=is_correct,
        message="Дұрыс жауап!" if is_correct else f"Қате. Дұрыс жауап: {problem.correct_answer}",
        solution=problem.solution if not is_correct else None,
    )
