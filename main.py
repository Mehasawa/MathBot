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

# Состояния бота
WAITING_FOR_ANSWER = 0
SENDING_NEXT_QUESTION = 1

# Словарь для хранения состояния и данных для каждого пользователя
user_data = {}
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
    problem = f'{num1} * {num2} = '
    answer = num1*num2
    return problem,answer


def send_next_question(chat_id, user_id):
    """Отправляет следующий вопрос пользователю."""
    user_data[user_id]["current_question"] += 1
    if user_data[user_id]["current_question"] > 20:
        end_time = time.time()
        total_time = end_time - user_data[user_id]["start_time"]
        if user_data[user_id]['score']==user_data[user_id]["current_question"]:
            bot.send_message(chat_id,
                      f"Поздравляем, вы прошли без ошибок.\nВремя прохождения: {total_time:.2f} секунд.")
        else:
            bot.send_message(chat_id,
                             f"Поздравляем, у вас {user_data[user_id]["current_question"]-user_data[user_id]["score"]}ошибок. Время не засчитано.")
        del user_data[user_id]
        return

    problem, answer = primer(1)
    user_data[user_id]["problem"] = problem
    user_data[user_id]["answer"] = answer
    bot.send_message(chat_id, problem)

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Привет! Это MathBot, выберите режим:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "👍 Тренировка")
def button1_handler(message):
    bot.send_message(message.chat.id, "Режим тренировки 👍!", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == "🚀 Соревнование")
def button2_handler(message):
    user_id = message.from_user.id
    # сессия для каждого пользователя
    user_data[user_id] = {
        "state": WAITING_FOR_ANSWER,
        "current_question": 0,
        "score": 0,
        "problem": None,
        "answer": None,
        "start_time": time.time(),
    }


    bot.send_message(message.chat.id, "Соревновательный режим 🚀!",reply_markup=telebot.types.ReplyKeyboardRemove())
    for i in range(3):
        time.sleep(1)
        bot.send_message(message.chat.id,spisokemo[i])
    user_data['start_time']=time.time()
    send_next_question(message.chat.id, user_id)
    # for i in range(10):
    #     print(primer(1))
    # for i in range(5):
    #     print(primer(2))
    # for i in range(5):
    #     print(primer(3))


# Запуск бота
bot.polling(none_stop=True)