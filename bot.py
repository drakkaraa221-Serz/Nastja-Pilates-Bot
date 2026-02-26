import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# =========================
TOKEN = "7227595822:AAGs-eSy0FGEFMK3UU68Ab9I6846bBCdj3s"
ADMIN_CHAT_ID = -1003833370596  # ВСТАВЬ ID АДМИН-ЧАТА
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ========= СОСТОЯНИЯ =========

class Booking(StatesGroup):
    age = State()
    first_time = State()
    pain = State()
    goal = State()
    time = State()
    format = State()

class Question(StatesGroup):
    waiting = State()

class Consultation(StatesGroup):
    situation = State()
    restrictions = State()

# ========= КЛАВИАТУРЫ =========

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌿 О занятиях")],
        [KeyboardButton(text="🧘 Форматы")],
        [KeyboardButton(text="✨ Подойдёт ли мне")],
        [KeyboardButton(text="🏡 О студии")],
        [KeyboardButton(text="📅 Записаться")],
        [KeyboardButton(text="❓ Вопрос")]
    ],
    resize_keyboard=True
)

yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, впервые")],
        [KeyboardButton(text="Уже занималась")]
    ],
    resize_keyboard=True
)

pain_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спина")],
        [KeyboardButton(text="Шея")],
        [KeyboardButton(text="Поясница")],
        [KeyboardButton(text="Колени")],
        [KeyboardButton(text="После родов")],
        [KeyboardButton(text="Нет выраженной боли")],
        [KeyboardButton(text="Опишу сама")]
    ],
    resize_keyboard=True
)

goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Восстановление после родов")],
        [KeyboardButton(text="Улучшить осанку")],
        [KeyboardButton(text="Убрать напряжение")],
        [KeyboardButton(text="Мягко укрепить тело")],
        [KeyboardButton(text="Повысить мобильность")],
        [KeyboardButton(text="Хочу заниматься для себя")],
        [KeyboardButton(text="Напишу сама")]
    ],
    resize_keyboard=True
)

time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Утро")],
        [KeyboardButton(text="День")],
        [KeyboardButton(text="Вечер")]
    ],
    resize_keyboard=True
)

format_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Индивидуально")],
        [KeyboardButton(text="Мини-группа")],
        [KeyboardButton(text="Консультация")]
    ],
    resize_keyboard=True
)

# ========= START =========

@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "Здравствуйте 🌿\n\n"
        "Меня зовут Настя.\n\n"
        "Я работаю с женщинами, помогая восстановить тело через мягкое, "
        "осознанное движение и физиотерапевтический подход.\n\n"
        "Выберите, что для вас сейчас важно 🤍"
    )
    await message.answer(text, reply_markup=main_menu)

# ========= О ЗАНЯТИЯХ =========

@dp.message(F.text == "🌿 О занятиях")
async def about_handler(message: Message):
    text = (
        "Мой путь начался с медицинского образования "
        "и дальнейшего обучения в сфере физиотерапии.\n\n"
        "На занятиях мы:\n"
        "— укрепляем глубокие мышцы\n"
        "— улучшаем осанку\n"
        "— восстанавливаем подвижность\n"
        "— работаем с дыханием\n\n"
        "Это не интенсив. Это осознанная работа с телом."
    )
    await message.answer(text, reply_markup=main_menu)

# ========= ФОРМАТЫ =========

@dp.message(F.text == "🧘 Форматы")
async def formats_handler(message: Message):
    text = (
        "▪ Индивидуальные занятия — персональный разбор вашей ситуации.\n\n"
        "▪ Мини-группы — камерный формат только для женщин.\n\n"
        "При необходимости можно начать с консультации."
    )
    await message.answer(text, reply_markup=main_menu)

# ========= ПОДОЙДЁТ ЛИ =========

@dp.message(F.text == "✨ Подойдёт ли мне")
async def fit_handler(message: Message):
    text = (
        "Занятия подойдут вам, если:\n\n"
        "— есть напряжение в спине или шее\n"
        "— хотите мягкую, но эффективную нагрузку\n"
        "— восстанавливаетесь после родов\n"
        "— цените спокойную атмосферу\n\n"
        "Формат не подойдёт тем, кто ищет интенсивные тренировки."
    )
    await message.answer(text, reply_markup=main_menu)

# ========= О СТУДИИ =========

@dp.message(F.text == "🏡 О студии")
async def studio_handler(message: Message):
    text = (
        "Занятия проходят в уютной студии в Риге.\n\n"
        "• Светлое пространство\n"
        "• Бесплатная парковка\n"
        "• Камерная атмосфера — только для женщин\n\n"
        "Я сознательно выбрала небольшой формат, "
        "чтобы сохранить качество и комфорт."
    )
    await message.answer(text, reply_markup=main_menu)

# ========= ЗАПИСЬ =========

@dp.message(F.text == "📅 Записаться")
async def booking_start(message: Message, state: FSMContext):
    await message.answer(
        "Благодарю за доверие 🌿\n\n"
        "Пожалуйста, укажите ваш возраст:"
    )
    await state.set_state(Booking.age)

@dp.message(Booking.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        "Возраст помогает мне подобрать корректную нагрузку 🤍\n\n"
        "Это ваше первое занятие со мной?",
        reply_markup=yes_no_keyboard
    )
    await state.set_state(Booking.first_time)

@dp.message(Booking.first_time)
async def get_first_time(message: Message, state: FSMContext):
    await state.update_data(first_time=message.text)
    await message.answer(
        "Есть ли сейчас дискомфорт или ограничения?",
        reply_markup=pain_keyboard
    )
    await state.set_state(Booking.pain)

@dp.message(Booking.pain)
async def get_pain(message: Message, state: FSMContext):
    await state.update_data(pain=message.text)
    await message.answer(
        "Что сейчас для вас наиболее важно?",
        reply_markup=goal_keyboard
    )
    await state.set_state(Booking.goal)

@dp.message(Booking.goal)
async def get_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer(
        "В какое время вам удобнее заниматься?",
        reply_markup=time_keyboard
    )
    await state.set_state(Booking.time)

@dp.message(Booking.time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(
        "Выберите формат занятий:",
        reply_markup=format_keyboard
    )
    await state.set_state(Booking.format)

@dp.message(Booking.format)
async def get_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    data = await state.get_data()

    admin_text = (
        "🌿 Новая заявка\n\n"
        f"Имя: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username}\n"
        f"Возраст: {data['age']}\n"
        f"Первое занятие: {data['first_time']}\n"
        f"Дискомфорт: {data['pain']}\n"
        f"Цель: {data['goal']}\n"
        f"Время: {data['time']}\n"
        f"Формат: {data['format']}"
    )

    await bot.send_message(ADMIN_CHAT_ID, admin_text)

    await message.answer(
        "Благодарю вас 🌿\n\n"
        "Я получила вашу информацию и свяжусь с вами лично.",
        reply_markup=main_menu
    )

    await state.clear()

# ========= ВОПРОС =========

@dp.message(F.text == "❓ Вопрос")
async def question_start(message: Message, state: FSMContext):
    await message.answer("Напишите ваш вопрос. Я отвечаю лично.")
    await state.set_state(Question.waiting)

@dp.message(Question.waiting)
async def forward_question(message: Message, state: FSMContext):
    admin_text = (
        "❓ Новый вопрос\n\n"
        f"От: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username}\n\n"
        f"{message.text}"
    )

    await bot.send_message(ADMIN_CHAT_ID, admin_text)

    await message.answer("Благодарю 🌿 Я отвечу вам лично.", reply_markup=main_menu)
    await state.clear()

# ========= ЗАПУСК =========

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
