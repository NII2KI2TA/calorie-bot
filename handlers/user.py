from aiogram import Router

from aiogram.types import (
    Message,
    CallbackQuery
)

from aiogram.filters import Command

from aiogram.fsm.context import FSMContext

from states.states import UserForm

from keyboards.keyboards import (
    number_keyboard,
    activity_keyboard,
    main_menu
)

from services.calories import (
    calculate_calories
)

from database.database import (
    save_user,
    get_user
)


router = Router()


@router.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "🔥 CalorieBot\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )


@router.callback_query(lambda c: c.data == "calculate")
async def calculate_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(UserForm.age)

    await state.update_data(
        age=20,
        height=170,
        weight=70
    )

    await callback.message.edit_text(
        "📅 Возраст: 20",
        reply_markup=number_keyboard("age")
    )

    await callback.answer()


@router.callback_query(lambda c: c.data == "profile")
async def profile(callback: CallbackQuery):

    user = get_user(
        callback.from_user.id
    )

    if not user:

        await callback.message.edit_text(
            "❌ Профиль пуст"
        )

        await callback.answer()

        return

    age, height, weight, calories = user

    await callback.message.edit_text(
        f"👤 Ваш профиль\n\n"

        f"📅 Возраст: {age}\n"
        f"📏 Рост: {height} см\n"
        f"⚖ Вес: {weight} кг\n\n"

        f"🔥 Норма: {calories} ккал",

        reply_markup=main_menu
    )

    await callback.answer()


@router.callback_query()
async def callbacks(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    if not data:

        await callback.answer(
            "Введите /start"
        )

        return

    age = data.get("age", 20)
    height = data.get("height", 170)
    weight = data.get("weight", 70)

    # AGE

    if callback.data == "age_plus":

        age += 1

        await state.update_data(age=age)

        await callback.message.edit_text(
            f"📅 Возраст: {age}",
            reply_markup=number_keyboard("age")
        )

    elif callback.data == "age_minus":

        if age > 1:
            age -= 1

        await state.update_data(age=age)

        await callback.message.edit_text(
            f"📅 Возраст: {age}",
            reply_markup=number_keyboard("age")
        )

    elif callback.data == "age_done":

        await state.set_state(
            UserForm.height
        )

        await callback.message.edit_text(
            f"📏 Рост: {height} см",
            reply_markup=number_keyboard("height")
        )

    # HEIGHT

    elif callback.data == "height_plus":

        height += 1

        await state.update_data(
            height=height
        )

        await callback.message.edit_text(
            f"📏 Рост: {height} см",
            reply_markup=number_keyboard("height")
        )

    elif callback.data == "height_minus":

        if height > 50:
            height -= 1

        await state.update_data(
            height=height
        )

        await callback.message.edit_text(
            f"📏 Рост: {height} см",
            reply_markup=number_keyboard("height")
        )

    elif callback.data == "height_done":

        await state.set_state(
            UserForm.weight
        )

        await callback.message.edit_text(
            f"⚖ Вес: {weight} кг",
            reply_markup=number_keyboard("weight")
        )

    # WEIGHT

    elif callback.data == "weight_plus":

        weight += 1

        await state.update_data(
            weight=weight
        )

        await callback.message.edit_text(
            f"⚖ Вес: {weight} кг",
            reply_markup=number_keyboard("weight")
        )

    elif callback.data == "weight_minus":

        if weight > 20:
            weight -= 1

        await state.update_data(
            weight=weight
        )

        await callback.message.edit_text(
            f"⚖ Вес: {weight} кг",
            reply_markup=number_keyboard("weight")
        )

    elif callback.data == "weight_done":

        await state.set_state(
            UserForm.activity
        )

        await callback.message.edit_text(
            "🏃 Выберите активность:",
            reply_markup=activity_keyboard
        )

    # ACTIVITY

    elif callback.data.startswith(
        "activity_"
    ):

        activity = float(
            callback.data.split("_")[1]
        )

        calories = calculate_calories(
            age,
            height,
            weight,
            activity
        )

        save_user(
            callback.from_user.id,
            age,
            height,
            weight,
            calories
        )

        await callback.message.edit_text(
            f"🔥 Ваша норма:\n\n"

            f"⚖ Поддержание — {calories}\n"
            f"📉 Похудение — {calories - 300}\n"
            f"💪 Масса — {calories + 300}",

            reply_markup=main_menu
        )

        await state.clear()

    await callback.answer()