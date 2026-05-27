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
    main_menu,
    gender_keyboard,
    water_keyboard
)

from services.calories import (
    calculate_calories
)

from database.database import (
    save_user,
    get_user,
    save_water,
    get_water
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

    await state.update_data(
        age=20,
        height=170,
        weight=70
    )

    await callback.message.edit_text(
        "👤 Выберите пол:",
        reply_markup=gender_keyboard
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

@router.callback_query(lambda c: c.data == "water")
async def water_menu(callback: CallbackQuery):

    user = get_user(
        callback.from_user.id
    )

    if not user:

        await callback.message.edit_text(
            "❌ Сначала рассчитайте калории",
            reply_markup=main_menu
        )

        await callback.answer()

        return

    age, height, weight, calories = user

    water_goal = weight * 35

    water_data = get_water(
        callback.from_user.id
    )

    if water_data:

        current_water, _ = water_data

    else:

        current_water = 0

        save_water(
            callback.from_user.id,
            current_water,
            water_goal
        )

    percent = int(
        (current_water / water_goal) * 100
    )

    bars = int(percent / 10)

    progress = (
        "█" * bars +
        "░" * (10 - bars)
    )

    await callback.message.edit_text(
        f"💧 Вода за сегодня\n\n"

        f"{progress} {percent}%\n\n"

        f"🥤 {current_water} / {water_goal} мл\n\n"

        f"🔥 Осталось:\n"
        f"{water_goal - current_water} мл",

        reply_markup=water_keyboard
    )

    await callback.answer()


@router.callback_query()
async def callbacks(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    if not data and callback.data not in [
        "water_add",
        "water_refresh",
        "back_menu"
    ]:
        await callback.answer(
            "Введите /start"
        )

        return

    age = data.get("age", 20)
    height = data.get("height", 170)
    weight = data.get("weight", 70)

    # GENDER

    if callback.data == "male":

        await state.update_data(
            gender="male"
        )

        await state.set_state(
            UserForm.age
        )

        await callback.message.edit_text(
            f"📅 Возраст: {age}",
            reply_markup=number_keyboard("age")
        )

    elif callback.data == "female":

        await state.update_data(
            gender="female"
        )

        await state.set_state(
            UserForm.age
        )

        await callback.message.edit_text(
            f"📅 Возраст: {age}",
            reply_markup=number_keyboard("age")
        )

    # AGE

    elif callback.data == "age_plus":

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

        gender = data.get("gender")
        if not gender:
            await callback.message.edit_text(
                "❌ Ошибка.\n\nНачните заново: /start"
            )

            await state.clear()

            await callback.answer()

            return

        calories = calculate_calories(
            gender,
            weight,
            height,
            age,
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
    # WATER

    elif callback.data == "water_add":

        water_data = get_water(
            callback.from_user.id
        )

        if not water_data:

            await callback.answer()

            return

        current_water, water_goal = water_data

        current_water += 250

        if current_water > water_goal:
            current_water = water_goal

        save_water(
            callback.from_user.id,
            current_water,
            water_goal
        )

        percent = int(
            (current_water / water_goal) * 100
        )

        bars = int(percent / 10)

        progress = (
            "█" * bars +
            "░" * (10 - bars)
        )

        await callback.message.edit_text(
            f"💧 Вода за сегодня\n\n"

            f"{progress} {percent}%\n\n"

            f"🥤 {current_water} / {water_goal} мл\n\n"

            f"🔥 Осталось:\n"
            f"{water_goal - current_water} мл",

            reply_markup=water_keyboard
        )

    elif callback.data == "water_refresh":

        water_data = get_water(
            callback.from_user.id
        )

        if not water_data:

            await callback.answer()

            return

        current_water, water_goal = water_data

        percent = int(
            (current_water / water_goal) * 100
        )

        bars = int(percent / 10)

        progress = (
            "█" * bars +
            "░" * (10 - bars)
        )

        await callback.message.edit_text(
            f"💧 Вода за сегодня\n\n"

            f"{progress} {percent}%\n\n"

            f"🥤 {current_water} / {water_goal} мл\n\n"

            f"🔥 Осталось:\n"
            f"{water_goal - current_water} мл",

            reply_markup=water_keyboard
        )

    elif callback.data == "back_menu":

        await callback.message.edit_text(
            "🔥 Главное меню",
            reply_markup=main_menu
        )
    await callback.answer()