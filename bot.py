import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

from data import tasks, get_random_tasks

from decouple import config

TOKEN = config('TOKEN')
ADMIN_ID = config('ADMIN_ID')

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
    await message.answer(
        "💣 *ACRIDES ga xush kelibsiz!*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ================= MENU ================= #

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text("🔙 Asosiy menyu", reply_markup=main_menu())

@dp.callback_query(F.data == "cabinet")
async def cabinet(callback: CallbackQuery):
    await callback.message.edit_text("💳 Kabinet", reply_markup=cabinet_menu())

# ================= BALANCE ================= #

@dp.callback_query(F.data == "balance")
async def balance(callback: CallbackQuery):
    bal = user_balances.get(callback.from_user.id, 0)
    await callback.message.answer(f"💰 Balans: ${bal}")

# ================= WITHDRAW ================= #

@dp.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery, state: FSMContext):
    bal = user_balances.get(callback.from_user.id, 0)
    if bal < 100:
        await callback.message.answer("❌ Minimal pul yechish 100$")
        return
    await callback.message.answer(
        "💸 Pul yechish uchun admin bilan bog‘laning."
    )
    await state.set_state(UserState.contacting_admin)

# ================= ADMIN ================= #

@dp.callback_query(F.data == "admin")
async def admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ Admin uchun xabar yozing:")
    await state.set_state(UserState.contacting_admin)

@dp.message(UserState.contacting_admin)
async def admin_msg(message: Message, state: FSMContext):
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

    if message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
    else:
        await bot.send_video(ADMIN_ID, message.video.file_id, caption=caption)

    await message.answer("Admin tekshirib pulni qo‘shadi")

    
    if task["price"] > 0:
        await message.answer(f"💰 {task['price']}$ qo‘shildi!")
        user_balances[message.from_user.id] += task["price"]
    await message.answer("✅ Qabul qilindi. Karta yuboring.")
    await state.set_state(UserState.sending_card)

# ================= CARD ================= #

@dp.message(UserState.sending_card)
async def card(message: Message, state: FSMContext):
    await bot.send_message(
        ADMIN_ID,
        f"💳 {message.from_user.full_name} karta:\n{message.text}"
    )

    await message.answer("✅ So‘rov qabul qilindi!")
    await state.clear()

# ================= RUN ================= #

async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
