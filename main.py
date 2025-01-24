import time
import random

import telebot
import sqlite3

#t.me/AlabugaMathtest_bot.
#7463754915:AAG0fnfEqlVaRg_hv6WB6-Qt3jISJK9R5gc
token='7605231410:AAE3xxUPIyz8FLdGvdWPOqqryWmUribS_ic'
# Замените "YOUR_BOT_TOKEN" на токен вашего бота, полученный от BotFather
bot = telebot.TeleBot(token)
spisokemo= ['3️⃣','2️⃣','1️⃣']
# Создание клавиатуры с кнопками и эмодзи

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = telebot.types.KeyboardButton("👍 Тренировка")  # Эмодзи 👍
button2 = telebot.types.KeyboardButton("🚀 Соревнование")  # Эмодзи 🚀
keyboard.add(button1, button2)

def primer(a=1):#генерирует примеры на умножение
    if a==1:
        num1=random.randint(2,9)
        num2=random.randint(2,9)
    elif a==2:
        num1=10
        while num1%10==0:
            num1 = random.randint(12, 99)
            num2 = random.randint(2, 9)
    elif a==3:
        num1 = 10
        num2 = 10
        while num1 % 10 == 0 and num2 % 10 == 0:
            num1 = random.randint(12, 99)
            num2 = random.randint(12, 99)
    return f'{num1} * {num2}'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это MathBot, выберите режим:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "👍 Тренировка")
def button1_handler(message):
    bot.send_message(message.chat.id, "Режим тренировки 👍!", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == "🚀 Соревнование")
def button2_handler(message):
    bot.send_message(message.chat.id, "Соревновательный режим 🚀!",reply_markup=telebot.types.ReplyKeyboardRemove())
    for i in range(3):
        time.sleep(1)
        bot.send_message(message.chat.id,spisokemo[i])
    for i in range(10):
        print(primer(1))
    for i in range(5):
        print(primer(2))
    for i in range(5):
        print(primer(3))


# Запуск бота
bot.polling(none_stop=True)