from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

HELP_TEXT = (
    "📐 <b>Математика PISA Боты — Нұсқаулық</b>\n"
    "━━━━━━━━━━━━━━━━━\n\n"
    "<b>📱 Командалар:</b>\n"
    "/start   — Басты бетті ашу\n"
    "/app     — Mini App ашу\n"
    "/profile — Профильді көру\n"
    "/rating  — Рейтинг TOP-10\n"
    "/streak  — Streak статистикасы\n"
    "/help    — Осы нұсқаулық\n\n"
    "<b>📘 PISA домендері:</b>\n"
    "🔢 Сан және шама\n"
    "📈 Өзгерістер мен тәуелділіктер\n"
    "📐 Кеңістік пен пішін\n"
    "📊 Анықсыздық пен деректер\n\n"
    "<b>🎮 Мүмкіндіктер:</b>\n"
    "• Теория — 4 PISA домені\n"
    "• Есептер — 6 деңгей (PISA 1-6)\n"
    "• Тесттер — 10 сұрақ, 20 сек таймер\n"
    "• AI репетитор — қазақша жауап\n"
    "• Рейтинг — апта/ай/жалпы\n"
    "• Streak — күнделікті оқу жолағы\n\n"
    "<b>📩 Байланыс:</b> @callmebekaa"
)


@router.message(Command("help"))
@router.message(F.text == "❓ Көмек")
async def show_help(message: Message):
    await message.answer(HELP_TEXT, parse_mode="HTML")
