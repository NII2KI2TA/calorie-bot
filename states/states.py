from aiogram.fsm.state import (
    State,
    StatesGroup
)


class UserForm(StatesGroup):

    age = State()
    height = State()
    weight = State()
    activity = State()