from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Общий список
default_checklist = [
    "Паспорт / ID", "Страховка", "Трекинговые ботинки", "Термобельё", "Флиска",
    "Ветровка", "Очки / кепка / шапка", "Бутылка воды", "Перекус",
    "Трекинговые палки", "Дрон", "Бинокль", "Зарядка / пауэрбанк",
    "Аптечка", "Солнцезащитный крем", "Оффлайн-карты"
]

# Персональные данные пользователей
user_data = {}

def get_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "marked": set(),
            "custom": []
        }
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-чеклист для Доломитов 🏔️\n\n"
        "Команды:\n"
        "/checklist — общий список\n"
        "/mylist — твой персональный список\n"
        "/mark [номер] — отметить пункт\n"
        "/unmark [номер] — снять отметку\n"
        "/add [текст] — добавить свою вещь\n"
        "/remove [номер] — удалить свою вещь\n"
        "/reset — сбросить список"
    )

async def checklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📋 Общий чек-лист:\n\n"
    for i, item in enumerate(default_checklist, start=1):
        msg += f"{i}. {item}\n"
    await update.message.reply_text(msg)

async def mylist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    data = get_user_data(uid)
    full_list = default_checklist + data["custom"]

    msg = "🧳 Твой чек-лист:\n\n"
    if not full_list:
        msg += "— пока пусто"
    else:
        for i, item in enumerate(full_list, start=1):
            mark = "✅" if i in data["marked"] else "🔲"
            msg += f"{mark} {i}. {item}\n"
    await update.message.reply_text(msg)

async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    data = get_user_data(uid)
    full_list = default_checklist + data["custom"]
    try:
        num = int(context.args[0])
        if 1 <= num <= len(full_list):
            data["marked"].add(num)
            await update.message.reply_text(f"✅ Отметил: {full_list[num-1]}")
        else:
            await update.message.reply_text("❗ Неверный номер.")
    except:
        await update.message.reply_text("❗ Используй: /mark [номер]")

async def unmark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    data = get_user_data(uid)
    try:
        num = int(context.args[0])
        data["marked"].discard(num)
        await update.message.reply_text("❎ Снял отметку.")
    except:
        await update.message.reply_text("❗ Используй: /unmark [номер]")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    data = get_user_data(uid)
    text = ' '.join(context.args)
    if text:
        data["custom"].append(text)
        await update.message.reply_text(f"➕ Добавлено в твой список: {text}")
    else:
        await update.message.reply_text("❗ Используй: /add [текст]")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    data = get_user_data(uid)
    try:
        num = int(context.args[0])
        index = num - len(default_checklist) - 1
        if 0 <= index < len(data["custom"]):
            removed = data["custom"].pop(index)
            data["marked"].discard(num)
            await update.message.reply_text(f"➖ Удалено: {removed}")
        else:
            await update.message.reply_text("❗ Можно удалить только свои пункты.")
    except:
        await update.message.reply_text("❗ Используй: /remove [номер]")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_data[uid] = {"marked": set(), "custom": []}
    await update.message.reply_text("🔁 Твой список сброшен.")

# 🔑 ЗАМЕНИ ТОКЕН НИЖЕ НА ТОТ, ЧТО ДАЛ BotFather
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("checklist", checklist))
app.add_handler(CommandHandler("mylist", mylist))
app.add_handler(CommandHandler("mark", mark))
app.add_handler(CommandHandler("unmark", unmark))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("reset", reset))

app.run_polling()
