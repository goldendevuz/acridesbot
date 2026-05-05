import asyncio
import uvloop

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

from loguru import logger
from decouple import config

from app.data import tasks, get_random_tasks

# ================= PERFORMANCE ================= #

uvloop.install()

# ================= CONFIG ================= #

TOKEN = config('TOKEN')
ADMIN_ID = int(config('ADMIN_ID'))

# ================= LOGGER ================= #

logger.add(
    "logs/bot.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

logger.info("🚀 Bot starting...")

# ================= INIT ================= #

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================= STATES ================= #

class UserState(StatesGroup):
    choosing_task = State()
    sending_proof = State()
    sending_card = State()
    contacting_admin = State()

# ================= STORAGE ================= #

user_balances = {}

# ================= KEYBOARDS ================= #

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Vazifa topish", callback_data="tasks")],
        [InlineKeyboardButton(text="💳 Kabinet", callback_data="cabinet")]
    ])

def cabinet_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Balans", callback_data="balance")],
        [InlineKeyboardButton(text="💸 Pul yechish", callback_data="withdraw")],
        [InlineKeyboardButton(text="✉️ Admin", callback_data="admin")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])

# ================= START ================= #

@dp.message(Command("start"))
async def start(message: Message):
    user_balances.setdefault(message.from_user.id, 0)

    logger.info(f"User started bot: {message.from_user.id}")

    await message.answer(
        "💣 *ACRIDES ga xush kelibsiz!*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ================= MENU ================= #

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    logger.info(f"Back pressed by {callback.from_user.id}")
    await callback.message.edit_text("🔙 Asosiy menyu", reply_markup=main_menu())

@dp.callback_query(F.data == "cabinet")
async def cabinet(callback: CallbackQuery):
    logger.info(f"Cabinet opened by {callback.from_user.id}")
    await callback.message.edit_text("💳 Kabinet", reply_markup=cabinet_menu())

# ================= BALANCE ================= #

@dp.callback_query(F.data == "balance")
async def balance(callback: CallbackQuery):
    bal = user_balances.get(callback.from_user.id, 0)
    logger.info(f"Balance check: {callback.from_user.id} = {bal}")
    await callback.message.answer(f"💰 Balans: ${bal}")

# ================= WITHDRAW ================= #

@dp.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery, state: FSMContext):
    bal = user_balances.get(callback.from_user.id, 0)

    if bal < 100:
        logger.warning(f"Withdraw denied (low balance): {callback.from_user.id}")
        await callback.message.answer("❌ Minimal pul yechish 100$")
        return

    logger.info(f"Withdraw requested: {callback.from_user.id}")

    await callback.message.answer(
        "💸 Pul yechish uchun admin bilan bog‘laning."
    )
    await state.set_state(UserState.contacting_admin)

# ================= ADMIN ================= #

@dp.callback_query(F.data == "admin")
async def admin(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User contacting admin: {callback.from_user.id}")
    await callback.message.answer("✍️ Admin uchun xabar yozing:")
    await state.set_state(UserState.contacting_admin)

@dp.message(UserState.contacting_admin)
async def admin_msg(message: Message, state: FSMContext):
    logger.info(f"Message to admin from {message.from_user.id}")

    await bot.send_message(
        ADMIN_ID,
        f"📩 {message.from_user.full_name}:\n{message.text}"
    )

    await message.answer("✅ Yuborildi!")
    await state.clear()

# ================= TASKS ================= #

@dp.callback_query(F.data == "tasks")
async def tasks_handler(callback: CallbackQuery, state: FSMContext):
    selected = get_random_tasks(2)

    logger.info(f"Tasks requested by {callback.from_user.id}")

    for task in selected:
        idx = tasks.index(task)

        await callback.message.answer(
            f"📝 {task['title']}\n💰 {task['price']}\n\n{task['desc']}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"accept_{idx}"
                )]
            ])
        )

    await state.set_state(UserState.choosing_task)

# ================= ACCEPT ================= #

@dp.callback_query(F.data.startswith("accept_"))
async def accept(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split("_")[1])
    task = tasks[idx]

    logger.info(f"Task accepted by {callback.from_user.id}: {task['title']}")

    await state.update_data(task=task)

    await callback.message.answer(
        f"📌 {task['title']}\n\n📤 Isbot yuboring (foto/video)"
    )

    await state.set_state(UserState.sending_proof)

# ================= MEDIA ================= #

@dp.message(UserState.sending_proof, F.photo | F.video)
async def proof(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data["task"]

    caption = f"{message.from_user.full_name}\n{task['title']}"

    logger.info(f"Proof received from {message.from_user.id}")

    if message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
    else:
        await bot.send_video(ADMIN_ID, message.video.file_id, caption=caption)

    await message.answer("Admin tekshirib pulni qo‘shadi")

    logger.info(f"Proof sent to admin: {message.from_user.id}")

    await message.answer("✅ Qabul qilindi. Karta yuboring.")
    await state.set_state(UserState.sending_card)

# ================= CARD ================= #

@dp.message(UserState.sending_card)
async def card(message: Message, state: FSMContext):
    logger.info(f"Card received from {message.from_user.id}")

    await bot.send_message(
        ADMIN_ID,
        f"💳 {message.from_user.full_name} karta:\n{message.text}"
    )

    await message.answer("✅ So‘rov qabul qilindi!")
    await state.clear()

# ================= ERROR HANDLER ================= #

@dp.errors()
async def errors_handler(event):
    logger.exception(f"Error occurred: {event.exception}")

# ================= RUN ================= #

async def main():
    logger.info("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
