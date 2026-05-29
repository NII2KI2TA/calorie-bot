from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def number_keyboard(prefix):

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=f"{prefix}_minus"
                ),

                InlineKeyboardButton(
                    text="➕",
                    callback_data=f"{prefix}_plus"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data=f"{prefix}_done"
                )
            ]
        ]
    )


activity_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🪑 Низкая",
                callback_data="activity_1.2"
            )
        ],

        [
            InlineKeyboardButton(
                text="🚶 Средняя",
                callback_data="activity_1.55"
            )
        ],

        [
            InlineKeyboardButton(
                text="🏃 Высокая",
                callback_data="activity_1.725"
            )
        ]
    ]
)


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🔥 Рассчитать",
                callback_data="calculate"
            )
        ],

        [
            InlineKeyboardButton(
                text="👤 Профиль",
                callback_data="profile"
            )
        ],

        [
            InlineKeyboardButton(
                text="💧 Вода",
                callback_data="water"
            )
        ]
    ]
)
gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="👨 Мужчина",
                callback_data="male"
            )
        ],

        [
            InlineKeyboardButton(
                text="👩 Женщина",
                callback_data="female"
            )
        ]
    ]
)
water_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🥤 +250 мл",
                callback_data="water_add"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_menu"
            )
        ]
    ]
)