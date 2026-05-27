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

cursor.execute("""

CREATE TABLE IF NOT EXISTS water (

    telegram_id INTEGER PRIMARY KEY,

    current_water INTEGER,
    water_goal INTEGER

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
def save_water(
    telegram_id,
    current,
    goal
):

    cursor.execute("""

    INSERT OR REPLACE INTO water (
        telegram_id,
        current_water,
        water_goal
    )

    VALUES (?, ?, ?)

    """, (
        telegram_id,
        current,
        goal
    ))

    connection.commit()


def get_water(telegram_id):

    cursor.execute("""

    SELECT current_water, water_goal

    FROM water

    WHERE telegram_id = ?

    """, (telegram_id,))

    return cursor.fetchone()