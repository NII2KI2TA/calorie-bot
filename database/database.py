import sqlite3


connection = sqlite3.connect(
    "calories.db"
)

cursor = connection.cursor()


cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    telegram_id INTEGER,
    age INTEGER,
    height INTEGER,
    weight INTEGER,
    calories INTEGER

)

""")

connection.commit()


def save_user(
    telegram_id,
    age,
    height,
    weight,
    calories
):

    cursor.execute("""

    INSERT INTO users (
        telegram_id,
        age,
        height,
        weight,
        calories
    )

    VALUES (?, ?, ?, ?, ?)

    """, (
        telegram_id,
        age,
        height,
        weight,
        calories
    ))

    connection.commit()


def get_user(telegram_id):

    cursor.execute("""

    SELECT age, height, weight, calories

    FROM users

    WHERE telegram_id = ?

    ORDER BY id DESC

    LIMIT 1

    """, (telegram_id,))

    return cursor.fetchone()