import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from keep_alive import keep_alive

keep_alive()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Общий чек-лист
default_checklist = [
    "Паспорт / ID", "Страховка", "Трекинговые ботинки", "Термобельё", "Флиска",
    "Ветровка", "Очки / кепка / шапка", "Бутылка воды", "Перекус",
    "Трекинговые палки", "Дрон", "Бинокль", "Зарядка / пауэрбанк",
    "Аптечка", "Солнцезащитный крем", "Оффлайн-карты"
]

# Храним данные по пользователям
user_data = {}

def get_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "marked": set()
        }
    return user_data[user_id]

def generate_checklist_markup(user_id):
    data = get_user_data(user_id)
    buttons = []

    for i, item in enumerate(default_checklist, start=1):
        checked = "✅" if i in data["marked"] else "🔲"
        buttons.append([
            InlineKeyboardButton(f"{checked} {item}", callback_data=str(i))
        ])

    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-чеклист для Доломитов 🏔️\n\n"
        "Нажми /menu чтобы открыть интерактивный список."
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    markup = generate_checklist_markup(uid)
    await update.message.reply_text("🧳 Твой интерактивный чек-лист:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = get_user_data(uid)
    item_num = int(query.data)

    if item_num in data["marked"]:
        data["marked"].remove(item_num)
    else:
        data["marked"].add(item_num)

    new_markup = generate_checklist_markup(uid)
    await query.edit_message_reply_markup(reply_markup=new_markup)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
