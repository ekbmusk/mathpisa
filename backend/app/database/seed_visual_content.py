"""
Seed script: adds test questions and problems with images and tables.
Run from backend/: python -m app.database.seed_visual_content
"""

from app.database.database import SessionLocal
from app.models.admin_test import AdminTestQuestion
from app.models.problem import Problem

# ─────────────────────────────────────────────
# TEST QUESTIONS WITH TABLES (~12)
# ─────────────────────────────────────────────
TABLE_TEST_QUESTIONS = [
    # ── uncertainty_and_data (4) ──
    {
        "topic": "uncertainty_and_data",
        "question": "Кестеде сынып оқушыларының математикадан алған бағалары берілген. Оқушылардың орташа бағасы нешеге тең?",
        "option_a": "3,6",
        "option_b": "4,0",
        "option_c": "3,8",
        "option_d": "4,2",
        "correct_option": "B",
        "difficulty": "2",
        "explanation": "Орташа = (3+5+4+4+2+5+4+3+5+5)/10 = 40/10 = 4,0.",
        "table_data": {
            "headers": ["Оқушы", "Баға"],
            "rows": [
                ["Айгүл", "3"], ["Болат", "5"], ["Сара", "4"], ["Дамир", "4"], ["Ерлан", "2"],
                ["Жанна", "5"], ["Қайрат", "4"], ["Ләззат", "3"], ["Мадина", "5"], ["Нұрлан", "5"]
            ],
            "caption": "Математика бағалары"
        },
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Кестеде дүкендегі сатылымдар көрсетілген. Қай күні ең көп сатылым болған?",
        "option_a": "Дүйсенбі",
        "option_b": "Сәрсенбі",
        "option_c": "Жұма",
        "option_d": "Сенбі",
        "correct_option": "D",
        "difficulty": "1",
        "explanation": "Сенбіде 87 бірлік сатылған — бұл ең жоғары көрсеткіш.",
        "table_data": {
            "headers": ["Күн", "Сатылым (бірлік)"],
            "rows": [
                ["Дүйсенбі", "45"], ["Сейсенбі", "52"], ["Сәрсенбі", "61"],
                ["Бейсенбі", "58"], ["Жұма", "73"], ["Сенбі", "87"], ["Жексенбі", "65"]
            ],
            "caption": "Апталық сатылым"
        },
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Кестеде оқушылардың бойлары берілген (см). Медианасын табыңыз.",
        "option_a": "162",
        "option_b": "165",
        "option_c": "164",
        "option_d": "168",
        "correct_option": "C",
        "difficulty": "3",
        "explanation": "Реттелген қатар: 155, 158, 162, 164, 165, 170, 175. Ортаңғы мән = 164.",
        "table_data": {
            "headers": ["Оқушы", "Бой (см)"],
            "rows": [
                ["Асыл", "170"], ["Бақыт", "155"], ["Гүлнар", "162"],
                ["Дана", "175"], ["Елдос", "158"], ["Жасмин", "165"], ["Қанат", "164"]
            ],
            "caption": "Оқушылардың бойлары"
        },
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Кестеде спорт секциясындағы оқушылар саны берілген. Барлық оқушылардың неше пайызы футбол ойнайды?",
        "option_a": "25%",
        "option_b": "30%",
        "option_c": "35%",
        "option_d": "40%",
        "correct_option": "B",
        "difficulty": "3",
        "explanation": "Барлығы: 30+20+25+15+10 = 100. Футбол: 30. Пайызы: 30/100 × 100% = 30%.",
        "table_data": {
            "headers": ["Спорт түрі", "Оқушы саны"],
            "rows": [
                ["Футбол", "30"], ["Волейбол", "20"], ["Баскетбол", "25"],
                ["Жүзу", "15"], ["Теннис", "10"]
            ],
            "caption": "Спорт секциялары"
        },
    },
    # ── quantity (3) ──
    {
        "topic": "quantity",
        "question": "Кестеде жемістердің бағалары берілген. 3 кг алма мен 2 кг банан сатып алсаңыз, қанша төлейсіз?",
        "option_a": "2800 тг",
        "option_b": "3100 тг",
        "option_c": "2950 тг",
        "option_d": "3250 тг",
        "correct_option": "A",
        "difficulty": "2",
        "explanation": "3 × 600 + 2 × 500 = 1800 + 1000 = 2800 тг.",
        "table_data": {
            "headers": ["Жеміс", "Бағасы (1 кг)"],
            "rows": [["Алма", "600 тг"], ["Банан", "500 тг"], ["Апельсин", "750 тг"], ["Жүзім", "900 тг"]],
            "caption": "Жемістер бағасы"
        },
    },
    {
        "topic": "quantity",
        "question": "Кестеде 4 қаланың халық саны берілген. Барлық қалалардың жалпы халық саны қанша?",
        "option_a": "3 200 000",
        "option_b": "3 450 000",
        "option_c": "3 500 000",
        "option_d": "3 650 000",
        "correct_option": "C",
        "difficulty": "1",
        "explanation": "1 200 000 + 900 000 + 800 000 + 600 000 = 3 500 000.",
        "table_data": {
            "headers": ["Қала", "Халық саны"],
            "rows": [
                ["Алматы", "1 200 000"], ["Астана", "900 000"],
                ["Шымкент", "800 000"], ["Ақтобе", "600 000"]
            ],
            "caption": "Қалалар халқы"
        },
    },
    {
        "topic": "quantity",
        "question": "Кестеде тауарлардың бағасы мен жеңілдігі берілген. Жеңілдіктен кейін кроссовка қанша тұрады?",
        "option_a": "13 500 тг",
        "option_b": "12 000 тг",
        "option_c": "14 250 тг",
        "option_d": "11 250 тг",
        "correct_option": "A",
        "difficulty": "3",
        "explanation": "Кроссовка: 18 000 тг, жеңілдік 25%. 18 000 × 0.25 = 4 500. 18 000 − 4 500 = 13 500 тг.",
        "table_data": {
            "headers": ["Тауар", "Бағасы", "Жеңілдік"],
            "rows": [
                ["Футболка", "5 000 тг", "10%"],
                ["Кроссовка", "18 000 тг", "25%"],
                ["Джинсы", "12 000 тг", "15%"],
                ["Куртка", "25 000 тг", "20%"]
            ],
            "caption": "Жеңілдіктер"
        },
    },
    # ── change_and_relationships (3) ──
    {
        "topic": "change_and_relationships",
        "question": "Кестеде $x$ пен $y$ мәндері берілген. $y = kx + b$ сызықтық функциясында $k$ коэффициентін табыңыз.",
        "option_a": "2",
        "option_b": "3",
        "option_c": "4",
        "option_d": "5",
        "correct_option": "B",
        "difficulty": "3",
        "explanation": "$k = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{8 - 5}{2 - 1} = 3$.",
        "table_data": {
            "headers": ["x", "y"],
            "rows": [["0", "2"], ["1", "5"], ["2", "8"], ["3", "11"], ["4", "14"]],
            "caption": "Функция мәндері"
        },
    },
    {
        "topic": "change_and_relationships",
        "question": "Кестеде автомобильдің жүрген уақыты мен жолы берілген. 6 сағатта қанша км жол жүреді?",
        "option_a": "420 км",
        "option_b": "480 км",
        "option_c": "360 км",
        "option_d": "540 км",
        "correct_option": "A",
        "difficulty": "2",
        "explanation": "Жылдамдық = 140/2 = 70 км/сағ. 6 сағатта: 70 × 6 = 420 км.",
        "table_data": {
            "headers": ["Уақыт (сағ)", "Жол (км)"],
            "rows": [["1", "70"], ["2", "140"], ["3", "210"], ["4", "280"]],
            "caption": "Автомобиль қозғалысы"
        },
    },
    {
        "topic": "change_and_relationships",
        "question": "Кестеде тізбектің мүшелері берілген. 7-ші мүше нешеге тең?",
        "option_a": "128",
        "option_b": "96",
        "option_c": "112",
        "option_d": "64",
        "correct_option": "A",
        "difficulty": "4",
        "explanation": "Геометриялық тізбек: $a_n = 2^n$. $a_7 = 2^7 = 128$.",
        "table_data": {
            "headers": ["n", "$a_n$"],
            "rows": [["1", "2"], ["2", "4"], ["3", "8"], ["4", "16"], ["5", "32"]],
            "caption": "Тізбек мүшелері"
        },
    },
    # ── space_and_shape (2) ──
    {
        "topic": "space_and_shape",
        "question": "Кестеде фигуралардың өлшемдері берілген. Тіктөртбұрыштың ауданы мен шеңбердің ауданы арасындағы айырмашылық қанша? ($\\pi \\approx 3.14$)",
        "option_a": "$21.5$ см²",
        "option_b": "$19.74$ см²",
        "option_c": "$22.86$ см²",
        "option_d": "$18.44$ см²",
        "correct_option": "C",
        "difficulty": "4",
        "explanation": "Тіктөртбұрыш: $S = 8 \\times 6 = 48$ см². Шеңбер: $S = \\pi r^2 = 3.14 \\times 2.83^2 \\approx 25.14$ см². Айырма: $48 - 25.14 = 22.86$ см².",
        "table_data": {
            "headers": ["Фигура", "Өлшемі"],
            "rows": [
                ["Тіктөртбұрыш", "8 см × 6 см"],
                ["Шеңбер", "r = 2.83 см"],
                ["Үшбұрыш", "табаны 10 см, биіктігі 7 см"]
            ],
            "caption": "Фигуралар өлшемдері"
        },
    },
    {
        "topic": "space_and_shape",
        "question": "Кестеде 3 бөлменің өлшемдері берілген. Барлық бөлмелердің жалпы ауданы нешеге тең?",
        "option_a": "42 м²",
        "option_b": "45 м²",
        "option_c": "48 м²",
        "option_d": "50 м²",
        "correct_option": "C",
        "difficulty": "2",
        "explanation": "Зал: 5×4 = 20 м². Жатын бөлме: 4×4 = 16 м². Ас бөлме: 4×3 = 12 м². Барлығы: 20+16+12 = 48 м².",
        "table_data": {
            "headers": ["Бөлме", "Ұзындығы", "Ені"],
            "rows": [["Зал", "5 м", "4 м"], ["Жатын бөлме", "4 м", "4 м"], ["Ас бөлме", "4 м", "3 м"]],
            "caption": "Үй жоспары"
        },
    },
]

# ─────────────────────────────────────────────
# TEST QUESTIONS WITH IMAGES (~8)
# ─────────────────────────────────────────────
IMAGE_TEST_QUESTIONS = [
    # ── space_and_shape (4) ──
    {
        "topic": "space_and_shape",
        "question": "Суреттегі тең қабырғалы үшбұрыштың қабырғасы 10 см. Периметрін табыңыз.",
        "option_a": "20 см",
        "option_b": "30 см",
        "option_c": "40 см",
        "option_d": "25 см",
        "correct_option": "B",
        "difficulty": "1",
        "explanation": "Тең қабырғалы үшбұрыштың периметрі: P = 3a = 3 × 10 = 30 см.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Triangle.Equilateral.svg/320px-Triangle.Equilateral.svg.png",
    },
    {
        "topic": "space_and_shape",
        "question": "Суреттегі параллелограмның табаны 12 см, биіктігі 5 см. Ауданын табыңыз.",
        "option_a": "60 см²",
        "option_b": "48 см²",
        "option_c": "72 см²",
        "option_d": "34 см²",
        "correct_option": "A",
        "difficulty": "2",
        "explanation": "$S = a \\times h = 12 \\times 5 = 60$ см².",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Parallelogram_area.svg/320px-Parallelogram_area.svg.png",
    },
    {
        "topic": "space_and_shape",
        "question": "Суреттегі трапецияның параллель қабырғалары 8 см және 14 см, биіктігі 6 см. Ауданын табыңыз.",
        "option_a": "56 см²",
        "option_b": "66 см²",
        "option_c": "72 см²",
        "option_d": "84 см²",
        "correct_option": "B",
        "difficulty": "3",
        "explanation": "$S = \\frac{(a+b)}{2} \\times h = \\frac{(8+14)}{2} \\times 6 = \\frac{22}{2} \\times 6 = 66$ см².",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Trapezoid.svg/320px-Trapezoid.svg.png",
    },
    {
        "topic": "space_and_shape",
        "question": "Суреттегі цилиндрдің радиусы 3 см, биіктігі 10 см. Көлемін табыңыз. ($\\pi \\approx 3.14$)",
        "option_a": "282.6 см³",
        "option_b": "188.4 см³",
        "option_c": "314 см³",
        "option_d": "94.2 см³",
        "correct_option": "A",
        "difficulty": "4",
        "explanation": "$V = \\pi r^2 h = 3.14 \\times 9 \\times 10 = 282.6$ см³.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Cylinder_geometry.svg/220px-Cylinder_geometry.svg.png",
    },
    # ── uncertainty_and_data (2) ──
    {
        "topic": "uncertainty_and_data",
        "question": "Суреттегі дөңгелек диаграммада оқушылардың сүйікті пәндері көрсетілген. Математиканы 90 оқушы таңдаған. Барлық оқушылар саны нешеге тең, егер математика үлесі 30% болса?",
        "option_a": "250",
        "option_b": "300",
        "option_c": "270",
        "option_d": "350",
        "correct_option": "B",
        "difficulty": "3",
        "explanation": "30% = 90 оқушы. 100% = 90 / 0.3 = 300 оқушы.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pie_chart_EP_election_2004.svg/320px-Pie_chart_EP_election_2004.svg.png",
    },
    {
        "topic": "uncertainty_and_data",
        "question": "Суреттегі бағаналы диаграммада 5 айдың жауын-шашын мөлшері көрсетілген. Ең аз жауын-шашын қай айда болған?",
        "option_a": "Қаңтар",
        "option_b": "Наурыз",
        "option_c": "Шілде",
        "option_d": "Қыркүйек",
        "correct_option": "C",
        "difficulty": "1",
        "explanation": "Диаграмма бойынша шілде айында жауын-шашын ең аз.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Bar_chart_of_the_population_of_countries_bordering_Austria.svg/400px-Bar_chart_of_the_population_of_countries_bordering_Austria.svg.png",
    },
    # ── change_and_relationships (2) ──
    {
        "topic": "change_and_relationships",
        "question": "Суреттегі координата жазықтығында $y = x + 2$ сызығы берілген. Бұл сызық $y$ осін қай нүктеде қиады?",
        "option_a": "(0, 1)",
        "option_b": "(0, 2)",
        "option_c": "(2, 0)",
        "option_d": "(0, -2)",
        "correct_option": "B",
        "difficulty": "2",
        "explanation": "$x = 0$ болғанда $y = 0 + 2 = 2$. Сондықтан $(0, 2)$ нүктесінде.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Cartesian-coordinate-system.svg/354px-Cartesian-coordinate-system.svg.png",
    },
    {
        "topic": "change_and_relationships",
        "question": "Суреттегі парабола $y = x^2$ функциясының графигі. $x = -3$ болғанда $y$ нешеге тең?",
        "option_a": "6",
        "option_b": "-9",
        "option_c": "9",
        "option_d": "-6",
        "correct_option": "C",
        "difficulty": "3",
        "explanation": "$y = (-3)^2 = 9$.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Quadratic_function_graph_%28y%3Dx%5E2%29.svg/320px-Quadratic_function_graph_%28y%3Dx%5E2%29.svg.png",
    },
]

# ─────────────────────────────────────────────
# PROBLEMS WITH IMAGES AND TABLES (~5)
# ─────────────────────────────────────────────
NEW_PROBLEMS = [
    # ── change_and_relationships with table (2) ──
    {
        "topic": "change_and_relationships",
        "question": "Кестеде температураның уақытқа байланысты өзгерісі берілген. 10 сағатта температура қанша болады, егер өзгеріс сызықтық болса?",
        "correct_answer": "25",
        "difficulty": "3",
        "formula": "$T = 2t + 5$",
        "solution": "Кестеден заңдылық: T = 2t + 5. t = 10 болғанда: T = 2(10) + 5 = 25°C.",
        "table_data": {
            "headers": ["Уақыт (сағ)", "Температура (°C)"],
            "rows": [["0", "5"], ["1", "7"], ["2", "9"], ["3", "11"], ["5", "15"]],
            "caption": "Температура өзгерісі"
        },
    },
    {
        "topic": "change_and_relationships",
        "question": "Кестеде тауардың бағасы жыл бойынша көрсетілген. 2025 жылы бағасы қанша болады, егер жыл сайынғы өсім тұрақты болса?",
        "correct_answer": "3500",
        "difficulty": "4",
        "formula": None,
        "solution": "Жылдық өсім: 500 тг. 2024 жылы: 3000 тг. 2025 жылы: 3000 + 500 = 3500 тг.",
        "table_data": {
            "headers": ["Жыл", "Баға (тг)"],
            "rows": [["2020", "1000"], ["2021", "1500"], ["2022", "2000"], ["2023", "2500"], ["2024", "3000"]],
            "caption": "Тауар бағасының өзгерісі"
        },
    },
    # ── change_and_relationships with image (1) ──
    {
        "topic": "change_and_relationships",
        "question": "Суреттегі координата жазықтығында сызықтық функция $y = 3x - 1$ берілген. $y = 8$ болғанда $x$ нешеге тең?",
        "correct_answer": "3",
        "difficulty": "2",
        "formula": "$y = 3x - 1$",
        "solution": "$8 = 3x - 1$, $3x = 9$, $x = 3$.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Cartesian-coordinate-system.svg/354px-Cartesian-coordinate-system.svg.png",
    },
    # ── space_and_shape with image (2) ──
    {
        "topic": "space_and_shape",
        "question": "Суреттегі ромбтың диагональдары 10 см және 24 см. Ромбтың ауданын табыңыз.",
        "correct_answer": "120",
        "difficulty": "3",
        "formula": "$S = \\frac{d_1 \\cdot d_2}{2}$",
        "solution": "$S = \\frac{10 \\times 24}{2} = \\frac{240}{2} = 120$ см².",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Rhombus2.svg/280px-Rhombus2.svg.png",
    },
    {
        "topic": "space_and_shape",
        "question": "Суреттегі призманың табаны тең қабырғалы үшбұрыш, қабырғасы 6 см, биіктігі 10 см. Призманың көлемін табыңыз.",
        "correct_answer": "155.88",
        "difficulty": "5",
        "formula": "$V = S_{\\text{tab}} \\times h = \\frac{a^2\\sqrt{3}}{4} \\times h$",
        "solution": "$S_{\\text{табан}} = \\frac{6^2 \\sqrt{3}}{4} = \\frac{36 \\times 1.732}{4} \\approx 15.588$ см². $V = 15.588 \\times 10 = 155.88$ см³.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Triangular_prism.png/220px-Triangular_prism.png",
    },
]


def seed_visual_content():
    with SessionLocal() as db:
        existing_questions = {
            q.question for q in db.query(AdminTestQuestion.question).all()
        }
        existing_problems = {
            p.question for p in db.query(Problem.question).all()
        }

        added_tests = 0
        for item in TABLE_TEST_QUESTIONS + IMAGE_TEST_QUESTIONS:
            if item["question"] in existing_questions:
                continue
            db.add(AdminTestQuestion(**item))
            existing_questions.add(item["question"])
            added_tests += 1

        added_problems = 0
        for item in NEW_PROBLEMS:
            if item["question"] in existing_problems:
                continue
            db.add(Problem(**item))
            existing_problems.add(item["question"])
            added_problems += 1

        db.commit()
        print(f"Added {added_tests} test questions, {added_problems} problems.")


if __name__ == "__main__":
    seed_visual_content()
