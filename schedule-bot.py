import telebot
import schedule
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import threading

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


if not TOKEN or not CHAT_ID:
    print("ОШИБКА: Не найдены BOT_TOKEN или CHAT_ID в .env файле")
    print("Убедись, что файл .env лежит в папке D:\\daily_bot")
    exit(1)

print("✅ Бот запускается...")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Бот работает! wake up в 06:30, go sleep в 22:00")

def send_wake_up():
    bot.send_message(CHAT_ID, "wake up")
    print(f"[{datetime.now()}] Отправлено: wake up")

def send_go_sleep():
    bot.send_message(CHAT_ID, "go sleep")
    print(f"[{datetime.now()}] Отправлено: go sleep")

schedule.every().day.at("06:30").do(send_wake_up)
schedule.every().day.at("22:00").do(send_go_sleep)

print("⏰ Расписание:")
print("   06:30 → wake up")
print("   22:00 → go sleep")

threading.Thread(target=bot.infinity_polling, daemon=True).start()

while True:
    schedule.run_pending()
    time.sleep(30)