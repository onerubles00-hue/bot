import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

TOKEN = os.getenv("BOT_TOKEN")            # токен из переменных окружения
USER_ID = int(os.getenv("TARGET_USER_ID"))  # ID пользователя

# Сообщение, которое будет отправляться каждый день
DAILY_TEXT = "Привет! Это твое ежедневное сообщение 😊"


# ---- Функция ежедневной отправки ----
async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=USER_ID,
        text=DAILY_TEXT
    )


# ---- Команда /start ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и расписание работает!")


def main():
    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Планировщик задач
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Kiev"))
    scheduler.add_job(
        send_daily,
        trigger="cron",
        hour=12,      # <-- ТУТ ставь время
        minute=0
    )
    scheduler.start()

    # Команда /start
    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    app.run_polling()


if __name__ == "__main__":
    main()
