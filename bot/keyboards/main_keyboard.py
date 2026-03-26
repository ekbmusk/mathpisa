from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from config import MINI_APP_URL


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Main reply keyboard with Mini App button and quick actions."""
    buttons = []

    # Mini App button (only if URL is configured)
    if MINI_APP_URL:
        buttons.append([
            KeyboardButton(
                text="📐 Mini App ашу",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        ])

    buttons.extend([
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="🔥 Streak"),
        ],
        [
            KeyboardButton(text="🏆 Рейтинг"),
            KeyboardButton(text="❓ Көмек"),
        ],
    ])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
    )
