import time
import random
import main
import telebot
import sqlite3

#t.me/AlabugaMathtest_bot.
#7463754915:AAG0fnfEqlVaRg_hv6WB6-Qt3jISJK9R5gc
token='7605231410:AAFT8E36Eaod_9kDAXk1ey6Jbz8eYv8wNmk'

bot = telebot.TeleBot(token)


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
    print(problem,answer)#####################
    return problem,answer

def generate_error_message(error_count):
    print(error_count)
    if error_count == 1:
        return "ка"
    elif 2 <= error_count <= 4:
        return "ки"
    else:
        return "ок"

"""Отправляет следующий вопрос пользователю."""
def send_next_question(chat_id, user_id):
    print('next')####################
    user_data[user_id]["current_question"] += 1
    print(user_data[user_id]["current_question"], user_data[user_id]["score"],)########################
    if user_data[user_id]["current_question"] > 4:
        end_time = time.time()#конец времени
        total_time = end_time - user_data[user_id]["start_time"]
        if user_data[user_id]['score']==user_data[user_id]["current_question"]-1:
            bot.send_message(chat_id,
                      f"Поздравляем, вы прошли без ошибок.\nВремя прохождения: {total_time:.2f} секунд.",
                             reply_markup=keyboard)
            main.newscore(user_data[user_id]['studentname'],total_time)
        else:

            bot.send_message(chat_id,
                             f"Поздравляем, у вас {user_data[user_id]["current_question"]-user_data[user_id]["score"]-1} "
                             f"ошиб{generate_error_message(user_data[user_id]["current_question"]-user_data[user_id]["score"]-1)}. Время не засчитано.",
                             reply_markup=keyboard)
        del user_data[user_id]
        return

    print(user_data)

    if user_data[user_id]["current_question"] <8:
            problem, answer = primer(1)
            #проверка на то что пример уже попадался
            while problem in user_data[user_id]['list']:
                problem, answer = primer(1)
    elif user_data[user_id]["current_question"] < 11:
            problem, answer = primer(2)
            # проверка на то что пример уже попадался
            while problem in user_data[user_id]['list']:
                problem, answer = primer(2)
    elif user_data[user_id]["current_question"] < 21:
            problem, answer = primer(3)
            # проверка на то что пример уже попадался
            while problem in user_data[user_id]['list']:
                problem, answer = primer(3)

    user_data[user_id]['list'].append(problem) #в список примеров
    user_data[user_id]["problem"] = problem
    user_data[user_id]["answer"] = answer

    bot.send_message(chat_id, problem)
def whatname(message):
    if message.from_user.first_name and message.from_user.last_name:
        studentname = f'{message.from_user.first_name} {message.from_user.last_name}'
    elif message.from_user.first_name:
        studentname = message.from_user.first_name
    else:
        studentname = message.from_user.username
    return studentname

#СТАРТОВОЕ СООБЩЕНИЕ:
@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    studentname=whatname(message)
    bot.send_message(message.chat.id, f"Привет! {studentname} Это MathBot, выберите режим:", reply_markup=keyboard)

#РЕЖИМ ТЕРНИРОВКИ
@bot.message_handler(func=lambda message: message.text == "👍 Тренировка")
def button1_handler(message):
    bot.send_message(message.chat.id, "Режим тренировки 👍!", reply_markup=telebot.types.ReplyKeyboardRemove())

#РЕЖИМ СОРЕВНОВАНИЯ
@bot.message_handler(func=lambda message: message.text == "🚀 Соревнование")
def button2_handler(message):
    spisokemo = ['3️⃣', '2️⃣', '1️⃣']
    user_id = message.from_user.id
    # сессия для каждого пользователя
    user_data[user_id] = {
        "state": WAITING_FOR_ANSWER,
        "current_question": 0,
        "score": 0,
        "problem": None,
        "answer": None,
        "start_time": time.time(),
        'list':[],
        'studentname':''
    }
    bot.send_message(message.chat.id, "Соревновательный режим 🚀!",reply_markup=telebot.types.ReplyKeyboardRemove())
    for i in range(3):#обратный отсчет
        time.sleep(1)
        bot.send_message(message.chat.id,spisokemo[i])
    user_data[user_id]['start_time']=time.time()#старт времени
    user_data[user_id]['studentname']=whatname(message)
    send_next_question(message.chat.id, user_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    print(user_id)#################################
    if user_id not in user_data:
        return

    if user_data[user_id]["state"] == WAITING_FOR_ANSWER:
        try:
            user_answer = int(message.text)
            correct_answer = user_data[user_id]["answer"]
            print(user_data)
            if user_answer == correct_answer:
                user_data[user_id]["score"] += 1
                bot.send_message(message.chat.id, "Правильно!")
            else:
                bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")

            user_data[user_id]["state"] = SENDING_NEXT_QUESTION
            send_next_question(message.chat.id, user_id)
            print(user_data)
            if user_id in user_data:
                    user_data[user_id]["state"] = WAITING_FOR_ANSWER

        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        # print(user_data[user_id]["current_question"], user_data[user_id]["score"], )  #####
# Запуск бота
bot.polling(none_stop=True)