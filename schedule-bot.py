import telebot
import schedule
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import threading
import random

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("ОШИБКА: Не найдены BOT_TOKEN или CHAT_ID в .env файле")
    print("Убедись, что файл .env лежит в папке D:\\daily_bot")
    exit(1)

print("✅ Бот запускается...")

bot = telebot.TeleBot(TOKEN)

# ============= КОМАНДЫ =============

@bot.message_handler(commands=['start'])
def start_command(message):
    text = ("Привет! Я твой личный будильник 🤖\n\n"
            "Расписание:\n"
            "🌅 06:30 — wake up\n"
            "🌙 22:00 — go sleep\n\n"
            "Доступные команды:\n"
            "/help — помощь\n"
            "/time — текущее время\n"
            "/joke — шутка\n"
            "/status — статус\n"
            "/hui — проверка")
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help_command(message):
    text = ("📚 Доступные команды:\n\n"
            "/start — запуск и информация\n"
            "/help — это сообщение\n"
            "/time — показать текущее время\n"
            "/joke — случайная шутка\n"
            "/status — статус бота и расписания\n"
            "/hui — проверка связи")
    bot.reply_to(message, text)

@bot.message_handler(commands=['time'])
def time_command(message):
    now = datetime.now().strftime("%H:%M:%S")
    today = datetime.now().strftime("%d.%m.%Y")
    bot.reply_to(message, f"🕐 Сегодня {today}\n⏰ Точное время: {now}")

@bot.message_handler(commands=['joke'])
def joke_command(message):
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 = Dec 25!",
        "Что говорит один бот другому? Привет, я тоже бот!",
        "Вставать в 6:30 — это подвиг. Ты герой!",
        "Лучший будильник — это голодный кот.",
        "Как называется бот, который не шутит? Скучный бот.",
        "Идёт медведь по лесу, видит: машина горит. Сел в неё и сгорел.",
        "Колобок повесился.",
        "А что это за шутки? Это же бот!"
    ]
    bot.reply_to(message, "😄 " + random.choice(jokes))

@bot.message_handler(commands=['status'])
def status_command(message):
    text = ("🤖 Статус бота:\n"
            "✅ Активен\n\n"
            "⏰ Текущее расписание:\n"
            "   🌅 06:30 — wake up\n"
            "   🌙 22:00 — go sleep\n"
            "   🔧 15:40 — test\n\n"
            "📊 Версия: 2.0")
    bot.reply_to(message, text)

@bot.message_handler(commands=['hui'])
def hui_command(message):
    bot.reply_to(message, "hui")

# ============= ФУНКЦИИ РАСПИСАНИЯ =============

def send_wake_up():
    bot.send_message(CHAT_ID, "🌅 wake up")
    print(f"[{datetime.now()}] Отправлено: wake up")

def send_go_sleep():
    bot.send_message(CHAT_ID, "🌙 go sleep")
    print(f"[{datetime.now()}] Отправлено: go sleep")

def test():
    bot.send_message(CHAT_ID, "🔧 test")
    print(f"[{datetime.now()}] Отправлено: test")

# ============= НАСТРОЙКА РАСПИСАНИЯ =============
schedule.every().day.at("06:30").do(send_wake_up)
schedule.every().day.at("22:00").do(send_go_sleep)
schedule.every().day.at("15:40").do(test)  # это для проверки, потом можешь убрать

print("\n⏰ Расписание установлено:")
print("   06:30 → wake up")
print("   22:00 → go sleep")
print("   15:40 → test (проверка)\n")

# ============= ЗАПУСК =============
print("🚀 Бот запущен и слушает команды...")
print("📋 Доступные команды: /start, /help, /time, /joke, /status, /hui")

# Запускаем polling в отдельном потоке
threading.Thread(target=bot.infinity_polling, daemon=True).start()

# Главный цикл для расписания
while True:
    schedule.run_pending()
    time.sleep(30)
