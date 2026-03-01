import telebot
import schedule
import time
from datetime import datetime

TOKEN = env.TOKEN
CHAT_ID = env.CHAT_ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Бот работает! Буду писать в 06:30 и 22:00")
    print(f"[{datetime.now()}] Получена команда /start")

def send_wake_up():
    bot.send_message(CHAT_ID, "wake up")
    print(f"[{datetime.now()}] Отправлено: wake up")

def send_go_sleep():
    bot.send_message(CHAT_ID, "go sleep")
    print(f"[{datetime.now()}] Отправлено: go sleep")

schedule.every().day.at("06:30").do(send_wake_up)
schedule.every().day.at("22:00").do(send_go_sleep)

print("Бот запущен! Расписание: 06:30 и 22:00")

import threading
def bot_polling():
    bot.infinity_polling()
    
threading.Thread(target=bot_polling, daemon=True).start()

while True:
    schedule.run_pending()
    time.sleep(30)