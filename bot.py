from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import random

TOKEN = '7739867818:AAHEgUd_Ct8UdJm-9W40XsFnolqeq-3wHQM'
ADMIN_ID = 6900365422

user_states = {}
user_balances = {}

tasks = [
{"title": "🌊 Daryoga sakrash", "price": "20 000", "desc": "Daryo yoki kanalga sakrayotganingni videoga ol!"},
{"title": "🪜 2-qavatdan sakrash (yostiqqa)", "price": "25 000", "desc": "Xavfsiz joyga, masalan, yostiq ustiga sakraganingni video qil."},
{"title": "🪧 Ko‘chada banner ko‘tarib yurish", "price": "15 000", "desc": "'Bugun men aqlli bo‘ldim' deb yozilgan banner bilan ko‘chada yur."},
{"title": "🛒 Savatchada yurish", "price": "10 000", "desc": "Do‘kon savatchasiga o‘tirib, do‘sting itarib video oladi."},
{"title": "📢 Ko‘chada baland ovozda she’r o‘qish", "price": "12 000", "desc": "Jamoat joyida she’r o‘qib, odamlarning reaksiyasini ol."},
{"title": "🥶 Muzdek suv bilan dush olish", "price": "10 000", "desc": "Ertalab sovuq suvda dush olib, uni videoga ol."},
{"title": "👻 Tunda qabriston yonidan o‘tish", "price": "30 000", "desc": "Do‘stlaring bilan kechasi qabriston oldidan yurib o‘ting."},
{"title": "🛵 Elektr skuterda aylanish", "price": "7 000", "desc": "Bir qo‘l bilan minib, videoga ol (xavfsizlikni unutmang!)."},
{"title": "🧼 Tuxum bilan boshni yuvish", "price": "10 000", "desc": "Tuxumni boshingga sindirib, uni yuvib tashlaganingni yozib ol."},
{"title": "🍕 Tasodifiy odamga pitsa ulash", "price": "15 000", "desc": "Yangi odamga pitsa olib ber va suratga tush."},
{"title": "🧃 10ta ichimlik aralashtirib ichish", "price": "12 000", "desc": "10 xil ichimlikni aralashtirib ichib, reaksiya qil."},
{"title": "🧊 Muz qutisiga oyoq tiqish", "price": "8 000", "desc": "Muz to‘ldirilgan suvga oyoq tiqib 2 daqiqa kut."},
{"title": "🗣️ Do‘kondan 1 so‘m so‘rash", "price": "7 000", "desc": "Sodda do‘konga kirib, '1 so‘m kerak' deb so‘rab video ol."},
{"title": "🎤 Jamoat joyida mikrofon bilan qo‘shiq aytish", "price": "30 000", "desc": "Savdo markazida mikrofon bilan kuylang."},
{"title": "🥒 Achchiq bodring yeyish", "price": "6 000", "desc": "Birdaniga achchiq bodring yoki qalampir yeyish."},
{"title": "🎭 3 ta odamni qo‘rqitish", "price": "18 000", "desc": "Yaxshi niyatli prank: do‘stlar bilan kichik qo‘rqitish sahnalari."},
{"title": "🏀 Ko‘z bog‘lab to‘p urish", "price": "9 000", "desc": "Ko‘z bog‘lab basket to‘pi ur va videoga ol."},
{"title": "🦆 It, mushuk yoki qushni suratga olish", "price": "3 000", "desc": "Begona hayvonni suratga tushirib, unga ovqat ber."},
{"title": "🧦 5 xil rangda paypoq kiyish", "price": "5 000", "desc": "Har bir oyog‘ingda boshqa paypoq bo‘lishi kerak."},
{"title": "📷 5 ta notanish bilan selfi olish", "price": "10 000", "desc": "Jamoat joyida notanish 5 kishi bilan selfi tush."},
{"title": "🚲 Aksincha yurish (velosiped)", "price": "8 000", "desc": "Velosipedni orqaga tortib minib ko‘r."},
{"title": "🪙 Yerdan pul topib olib qaytarish", "price": "6 000", "desc": "Yerdan 1000 so‘m topib, egasini izlab top."},
{"title": "🧁 Begona bolaga shirinlik berish", "price": "10 000", "desc": "Ruxsat bilan, bolaga sovg‘a ber va reaksiyasini yoz."},
{"title": "🥚 Xom tuxum yutish", "price": "12 000", "desc": "1 ta xom tuxumni yutib, videoga ol."},
{"title": "🥶 Muzdek yerda 30 soniya o‘tirish", "price": "8 000", "desc": "Beton yoki yerda sovuqda o‘tirib ko‘r."},
{"title": "🧻 Tualet qog‘ozdan kiyim tayyorlash", "price": "7 000", "desc": "Tualet qog‘ozdan libos yasab kiying va suratga tush."},
{"title": "🛏️ Do‘konda yotib ko‘rish", "price": "14 000", "desc": "Mebel do‘konida yotoqda yotgandek suratga tush."},
{"title": "🎮 3 soat tanaffussiz o‘yin o‘ynash", "price": "9 000", "desc": "Ortiqcha harakatsiz 3 soat o‘yin o‘yna va isbotla."},
{"title": "📞 Qariyb unutgan tanishga qo‘ng‘iroq qilish", "price": "6 000", "desc": "Eski tanishdan hol-ahvol so‘rash."},
{"title": "🍔 4 xil fastfood yeyish", "price": "13 000", "desc": "4 xil brenddan oziq-ovqat olib, ularni taqqoslab ko‘r."},
{"title": "🪞 Oynaga qarab o‘zingni maqtash", "price": "5 000", "desc": "Oynaga qarab 1 daqiqa o‘zingga motivatsiya ber."},
{"title": "👖 Bog‘lab yurgan oyoq bilan yurish", "price": "7 000", "desc": "2 oyog‘ingni bog‘lab 20 metr yurgin."},
{"title": "🎬 Kino qahramonini parodiya qilish", "price": "12 000", "desc": "Bir mashhur kino sahnasini qayta ijro et."},
{"title": "🍉 Katta tarvuzni 1 daqiqada yemoq", "price": "10 000", "desc": "Tezlik bilan tarvuzni yeyish challenge."},
{"title": "🚪 Notanish joyga kirib 'men adashdim' deb chiqish", "price": "9 000", "desc": "Xavfsiz tarzda qiziqarli prank."},
{"title": "🎒 20kg yuk bilan yugurish", "price": "15 000", "desc": "Og‘ir sumka bilan 100 metr yugur."},
{"title": "🧃 Limon sharbatini ichish", "price": "5 000", "desc": "Toza limon sharbatini ichish va yuz ifodasini ko‘rsatish."},
{"title": "🌪️ Chang bosgan joyni artib suratga tush", "price": "4 000", "desc": "Tozalanayotgan changli joydan 'oldin va keyin' surat."},
{"title": "👽 G‘alati libosda jamoat joyida yurish", "price": "20 000", "desc": "Kino obrazida jamoat joyiga chiqib, odamlar reaksiya."},
{"title": "🎲 Ko‘r-ko‘rona ovqat tanlab yeyish", "price": "8 000", "desc": "Ko‘z bog‘liq holatda 5 ovqatdan 1 tasini tanlab ye."},
{"title": "🎒 Begona maktabga 'tashrif' qilish", "price": "30 000", "desc": "Do‘st maktabiga 'mehmon bo‘lish' va selfi."},
{"title": "🗯️ 'Men yulduzman' deb yurish", "price": "11 000", "desc": "Ko‘chada odamlarga o‘zingni 'mashhurman' deb ayt."},
{"title": "🐸 Qurbaqa tovushi qilib odamlarni chalg‘itish", "price": "7 000", "desc": "Jamoat joyida hayvon ovozlari chiqarish va reaksiyani olish."},
{"title": "🥴 G‘alati yuzi bilan suratga tushish", "price": "4 000", "desc": "Eng g‘alati yuz ifodasi bilan selfie."},
{"title": "🥛 2 litr suvni 1 daqiqada ichish", "price": "9 000", "desc": "Sog‘lig‘ingni tekshirib, 2 litr suv ichishga urinish."},
{"title": "🧑‍🚀 Kosmonavtdek kiyinib yurish", "price": "15 000", "desc": "Kosmonavtga o‘xshash libosda savdo markazida yurish."},
{"title": "👶 Bolalarcha gapirish", "price": "6 000", "desc": "1 daqiqa davomida faqat bolalarcha gapiring va yozib oling."}
]


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Vazifa topish", callback_data='find_tasks')],
        [InlineKeyboardButton("💳 Kabinet", callback_data='open_cabinet')]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_balances.setdefault(user.id, 0)
    await update.message.reply_text(
        "💣 *ACRIDES* ga hush kelibsiz!\n\n🔻 Quyidagi bo‘limlardan birini tanlang:",
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

async def open_cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "🔹 *Kabinet* bo‘limiga xush kelibsiz!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💸 Balansni tekshirish", callback_data='check_balance')],
            [InlineKeyboardButton("💰 Pul yechish", callback_data='withdraw_money')],
            [InlineKeyboardButton("✋ Admin bilan bog'lanish", callback_data='contact_admin')],
            [InlineKeyboardButton("🔙 Asosiy menyuga qaytish", callback_data='back_to_menu')]
        ]),
        parse_mode='Markdown'
    )

async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    balance = user_balances.get(query.from_user.id, )
    await query.message.reply_text(f"💰 Sizning balansingiz: *${balance}*", parse_mode='Markdown')

async def withdraw_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("💳 Pul yechish uchun admin bergan shartni bajarish lozim. Shartni esa admin bilan bog‘lanish orqali olasiz.")
    user_states[query.from_user.id] = {"awaiting_payment": True}

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✍️ Savolingizni yozing. Admin sizga javob beradi.")
    user_states[query.from_user.id] = {"contacting_admin": True}

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🔙 Asosiy menyu:", reply_markup=main_menu())

async def find_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = random.sample(tasks, 3)

    for task in selected:
        with open("acrides.jpg", "rb") as img:
            await context.bot.send_photo(
                chat_id=query.from_user.id,
                photo=img,
                caption=f"📝 *Vazifa:* {task['title']}\n💰 *To‘lov:* {task['price']}\n\n📌 {task['desc']}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Qabul qilish", callback_data=f"accept_{tasks.index(task)}")]
                ]),
                parse_mode='Markdown'
            )

    await context.bot.send_message(
        chat_id=query.from_user.id,
        text="🔁 Yana boshqa vazifalarni ko‘rish yoki kabinetga kirish uchun:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Boshqa vazifalar", callback_data='find_tasks')],
            [InlineKeyboardButton("💳 Kabinet", callback_data='open_cabinet')]
        ])
    )

async def accept_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    task_index = int(query.data.split('_')[1])
    user_states[query.from_user.id] = {
        "task_index": task_index,
        "awaiting_media": True,
        "awaiting_card": False
    }
    task = tasks[task_index]
    await query.message.reply_text(
    f"📝 *Vazifa:* {task['title']}\n💰 *To‘lov:* {task['price']}\n\n📌 {task['desc']}\n\n"
    "📤 Iltimos, vazifani bajarganingizni tasdiqlovchi (foto/video) yuboring.",
    parse_mode='Markdown'
)

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    state = user_states.get(user.id, {})
    if not state.get("awaiting_media"):
        await update.message.reply_text("⚠️ Avval vazifani tanlang.")
        return

    task_index = state["task_index"]
    task = tasks[task_index]
    caption = f"✅ {user.full_name} (@{user.username})\nID: {user.id}\nVazifa: {task['title']}\nTo‘lov: {task['price']}"

    if update.message.photo:
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption)
    elif update.message.video:
        await context.bot.send_video(chat_id=ADMIN_ID, video=update.message.video.file_id, caption=caption)
    else:
        await update.message.reply_text("⚠️ Faqat foto yoki video yuboring.")
        return

    await update.message.reply_text(
        "✅ Isbot adminga yuborildi. 24 soat ichida ko‘rib chiqiladi.\n\n"
        "📥 Endi karta yoki telefon raqamingizni yuboring."
    )

    user_states[user.id] = {"awaiting_card": True}

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    state = user_states.get(user.id, {})

    if state.get("contacting_admin"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Xabar {user.full_name} (@{user.username}) dan:\n{update.message.text}"
        )
        await update.message.reply_text("✅ Xabaringiz yuborildi. Javobni kuting.")
        del user_states[user.id]
        return

    if state.get("awaiting_card"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💳 {user.full_name} (@{user.username}) karta/raqam yubordi:\n{update.message.text}"
        )
        await update.message.reply_text(
            "✅ Ma’lumot qabul qilindi.\n📌 Isbot tasdiqlangandan so‘ng sizga to‘lov amalga oshiriladi.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔁 Yana boshlash", callback_data='back_to_menu')],
                [InlineKeyboardButton("💳 Kabinet", callback_data='open_cabinet')]
            ])
        )
        del user_states[user.id]
    else:
        await update.message.reply_text("⚠️ Avval vazifa bajaring yoki menyudan tanlang.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(find_tasks, pattern="^find_tasks$"))
    app.add_handler(CallbackQueryHandler(open_cabinet, pattern="^open_cabinet$"))
    app.add_handler(CallbackQueryHandler(check_balance, pattern="^check_balance$"))
    app.add_handler(CallbackQueryHandler(withdraw_money, pattern="^withdraw_money$"))
    app.add_handler(CallbackQueryHandler(contact_admin, pattern="^contact_admin$"))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))
    app.add_handler(CallbackQueryHandler(accept_task, pattern="^accept_"))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()















