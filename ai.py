men ga shu ozim yozgan from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import random
import os

# ✅ Bot token va admin ID

TOKEN = '7739867818\:AAHEgUd\_Ct8UdJm-9W40XsFnolqeq-3wHQM'
ADMIN_ID = 6900365422  # admin Telegram ID

# Vazifalar ro'yxati

tasks = \[
{
"title": "📸 suratga tushush",
"price": "5 000",
"desc": "🧑‍💻 IT-ishnik bola bilan birga suratga tushdik 📸💻."
},
{
"title": "🎨 logo chizing",
"price": "10 000",
"desc": "🎨 Devorga Acrides logosi chizildi! 🧱🔥."
},
{
"title": "🎨 logo chizing",
"price": "10 000",
"desc": "🎨 Devorga Acrides logosi chizildi! 🧱🔥."
},
{
"title": "begona odamga yordam berish",
"price": "10 000",
"desc": "Begona odamga yordam berish  📸💻."
},
{
"title": "🎨 logo chizing",
"price": "10 000",
"desc": "🎨 Devorga Acrides logosi chizildi! 🧱🔥."
},
{
"title": "🍔 burger ye",
"price": "3 000",
"desc": "🍔 Do‘sting bilan burger yeb, suratga ol 📷😋."
},
{
"title": "🚲 velosiped minib video ol",
"price": "4 000",
"desc": "🚲 1 daqiqalik video: velosiped minayotganingni tushur 📹."
},
{
"title": "📚 kitob o‘qiyotgan holatingni suratga ol",
"price": "3 500",
"desc": "📖 Sevimli kitobingni o‘qiyotgan holatingni suratga tushir 📸📘."
},
{
"title": "☕ kofe tayyorlab video yubor",
"price": "4 500",
"desc": "☕ Uyda kofe yoki choy tayyorlab, 30 soniyalik video qil 📹🍵."
},
{
"title": "💻 VS Code ochilgan ekran",
"price": "2 500",
"desc": "💻 Kompyuteringda VS Code ochib, ekran rasmini yubor 🖥️📷."
},
{
"title": "🎧 musiqa eshitayotgan holat",
"price": "3 000",
"desc": "🎧 Sevimli musiqangni qo‘yib, eshitayotgan holatingni suratga ol 🎶📸."
},
{
"title": "🧹 xona tozalayotgan video",
"price": "6 000",
"desc": "🧼 1 daqiqalik video: xona tozalayotgan holatingni ko‘rsat 📽️✨."
},
{
"title": "10k istagram akount topish",
"price": "50 000",
"desc": "📸 10k dan ortiq istagram akount topish. login va parol"
},
{
"title": "10k istagram akount topish",
"price": "50 000",
"desc": "📸 10k dan ortiq istagram akount topish. login va parol"
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "Telfon qilib gaplashish",
"price": "150 000",
"desc": " +998 91 496 88 50 shu  raqamga telfon qilib 30 secunt gaplashish nima deyish kerak acriides botidan sizga salom deb 30 soniya gaplashib turish kerak agar shartni toliq bajarilsa video tarzida botga tashang adminga yoqsa bonus sifatida 100 000 ming otkazib beriladi jami suma 350 000 ming boladi video tarzida botga tashang "
},
{
"title": "10k istagram akount topish",
"price": "50 000",
"desc": "📸 10k dan ortiq istagram akount topish. login va parol"
},
{
"title": "instagramda video qoyish",
"price": "15 000",
"desc": "📸 bot haqida video qoyish atm qilib"
}

]

# Foydalanuvchi holati

user\_states = {}

# /start buyrug'i

async def start(update: Update, context: ContextTypes.DEFAULT\_TYPE):
user = update.effective\_user
await context.bot.send\_message(
chat\_id=user.id,
text=f"💣 *ACRIDES* ga hush kelibsiz!\n\n🔻 Quyidagi tugmani bosing:",
reply\_markup=InlineKeyboardMarkup(\[
\[InlineKeyboardButton("📝 Vazifa topish", callback\_data='find\_tasks')]
]),
parse\_mode='Markdown'
)

# ✅ Har safar 3 ta random vazifa va "Boshqa vazifalar" tugmasi chiqadi

async def find\_tasks(update: Update, context: ContextTypes.DEFAULT\_TYPE):
query = update.callback\_query
await query.answer()

```
selected_tasks = random.sample(tasks, 3)
image_path = os.path.join(os.path.dirname(__file__), "acrides.jpg")

for task in selected_tasks:
    if os.path.exists(image_path):
        with open(image_path, 'rb') as photo_file:
            await context.bot.send_photo(
                chat_id=query.from_user.id,
                photo=photo_file
            )

    await context.bot.send_message(
        chat_id=query.from_user.id,
        text=(
            f"📝 *Vazifa:* {task['title']}\n"
            f"💰 *To‘lov:* {task['price']}\n\n"
            f"📌 {task['desc']}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Qabul qilish", callback_data=f"accept_{tasks.index(task)}")]
        ]),
        parse_mode='Markdown'
    )

await context.bot.send_message(
    chat_id=query.from_user.id,
    text="🔁 Yana boshqa vazifalarni ko‘rish uchun tugmani bosing:",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Boshqa vazifalar", callback_data='find_tasks')]
    ])
)
```

# Vazifani qabul qilish

async def accept\_task(update: Update, context: ContextTypes.DEFAULT\_TYPE):
query = update.callback\_query
await query.answer()
task\_index = int(query.data.split('\_')\[1])
user\_states\[query.from\_user.id] = {"task\_index": task\_index}

```
task = tasks[task_index]

image_path = os.path.join(os.path.dirname(__file__), "acrides.jpg")
if os.path.exists(image_path):
    with open(image_path, 'rb') as photo_file:
        await context.bot.send_photo(
            chat_id=query.from_user.id,
            photo=photo_file
        )

await query.message.reply_text(
    f"📝 *Vazifa:* {task['title']}\n"
    f"💰 *To‘lov:* {task['price']}\n\n"
    f"📌 {task['desc']}\n\n"
    "✅ Shartni bajarganingizdan so‘ng, isbot sifatida rasm, video yoki ovoz yuboring.",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 Shart bajarildi (Isbot yuborish)", callback_data='send_proof')]
    ]),
    parse_mode='Markdown'
)
```

# Isbot yuborish bosilganda

async def send\_proof\_instruction(update: Update, context: ContextTypes.DEFAULT\_TYPE):
query = update.callback\_query
await query.answer()
await query.message.reply\_text("📄 Iltimos, isbot sifatida rasm, video yoki ovoz yuboring.")

# Media qabul qilish

async def handle\_media(update: Update, context: ContextTypes.DEFAULT\_TYPE):
user = update.message.from\_user
if user.id not in user\_states:
await update.message.reply\_text("Iltimos, avval vazifa tanlang.")
return

```
task_index = user_states[user.id]["task_index"]
task = tasks[task_index]

# Rasm yuborilgan bo‘lsa, uni adminga forward qilamiz
if update.message.photo:
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"✅ {user.full_name} (@{user.username})\nID: {user.id}\nVazifa: {task['title']}\nTo‘lov: {task['price']}"
    )
elif update.message.video:
    await context.bot.send_video(
        chat_id=ADMIN_ID,
        video=update.message.video.file_id,
        caption=f"✅ {user.full_name} (@{user.username})\nID: {user.id}\nVazifa: {task['title']}\nTo‘lov: {task['price']}"
    )
elif update.message.voice:
    await context.bot.send_voice(
        chat_id=ADMIN_ID,
        voice=update.message.voice.file_id,
        caption=f"✅ {user.full_name} (@{user.username})\nID: {user.id}\nVazifa: {task['title']}\nTo‘lov: {task['price']}"
    )

await update.message.reply_text("✅ Isbot admin tominida tekshirilmoqda!  Endi karta yoki telefon raqamingizni yuboring.")
user_states[user.id]["awaiting_payment"] = True
```

# Matnli habar (karta yoki raqam)

async def handle\_text(update: Update, context: ContextTypes.DEFAULT\_TYPE):
user = update.message.from\_user
if user.id in user\_states and user\_states\[user.id].get("awaiting\_payment"):
await context.bot.send\_message(
chat\_id=ADMIN\_ID,
text=f"💳 {user.full\_name} (@{user.username}) karta/raqami:\n{update.message.text}"
)
await update.message.reply\_text(
"✅ Ma'lumot qabul qilindi ! 24 soat ichida sizga to‘lov o‘tkaziladi.\n\n"
"🔄 Qayta boshlash uchun:",
reply\_markup=InlineKeyboardMarkup(\[
\[InlineKeyboardButton("🔄 Qayta boshlash", callback\_data='start\_over')]
])
)
del user\_states\[user.id]
else:
await update.message.reply\_text("Iltimos, avval vazifani tanlang yoki tugmani bosing.")

# Qayta boshlash

async def start\_over(update: Update, context: ContextTypes.DEFAULT\_TYPE):
query = update.callback\_query
await query.answer()
await start(update, context)

# Botni ishga tushurish

if **name** == '**main**':
app = ApplicationBuilder().token(TOKEN).build()

```
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(find_tasks, pattern="^find_tasks$"))
app.add_handler(CallbackQueryHandler(accept_task, pattern="^accept_"))
app.add_handler(CallbackQueryHandler(send_proof_instruction, pattern="^send_proof$"))
app.add_handler(CallbackQueryHandler(start_over, pattern="^start_over"))

app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.VOICE, handle_media))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("🤖 Bot ishga tushdi...")
app.run_polling()  kotimga qoshimcha kiritmoqchiman bu telgram bor bunga sen menga balan va pul yechi va admin bilan aloqa qilib berasan har bir foydalanuvchida 100$ dan balan boslihis kerka uni yechi uchun esa admin shartni bajarish kerak boladi shuni qilib ber 
```
