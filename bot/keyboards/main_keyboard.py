from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Main reply keyboard with quick actions."""
    buttons = [
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="🔥 Streak"),
        ],
        [
            KeyboardButton(text="🏆 Рейтинг"),
            KeyboardButton(text="❓ Көмек"),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
    )
