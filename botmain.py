import time
import random
import mainbase
import telebot
import fromGenerate
from telebot import types
import sqlite3

#t.me/AlabugaMathtest_bot.
from tokenpy import token
bot = telebot.TeleBot(token)


# Состояния бота
WAITING_FOR_ANSWER = 0
SENDING_NEXT_QUESTION = 1
FIRST_CHOICE = 1
SECOND_CHOICE = 2
THIRD_CHOICE = 3

# Словарь для хранения состояния и данных для каждого пользователя
user_data = {}
QLEN=4

# Создание клавиатуры с кнопками и эмодзи
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = telebot.types.KeyboardButton("👍 Тренировка")  # Эмодзи 👍
button2 = telebot.types.KeyboardButton("🚀 Соревнование")  # Эмодзи 🚀
keyboard1.add(button1, button2)

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [telebot.types.KeyboardButton(f"👍 Уровень {i}") for i in range(1, 7)]
keyboard2.add(*buttons)

keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# button1 = telebot.types.KeyboardButton("👍 Тема1")  # Эмодзи 👍
# button2 = telebot.types.KeyboardButton("👍 Тема2")  # Эмодзи 👍
# button3 = telebot.types.KeyboardButton("👍 Тема3")  # Эмодзи 👍
# keyboard3.add(button1, button2, button3)
#ПОКАЗАТЬ КЛАВИАТУРЫ
def show_first_choice_keyboard(message):
    bot.send_message(message.chat.id, "Выберите режим:", reply_markup=keyboard1)

def show_second_choice_keyboard(message):
    bot.send_message(message.chat.id, "Выберите уровень:", reply_markup=keyboard2)

def show_third_choice_keyboard(message,k):
    spisokTem =[['0 уровень'],
             ['Арифметика','Задачи','Фигуры','Информация'],
             ['Арифметика','Задачи','Фигуры','Периметр'],
             ['Площадь','Задачи','Фигуры','Информация'],
             ['Величины','Арифметика','Задачи на движение','Задачи на работу','Задачи купли-продажи',
              'Уравнения','Порядок действий'],
             ['Вычисления','Преобразования','Сравнения','Признаки делимости','Округление',
              'Задачи','Величины','Геометрия','Координатный луч'],
             ['Вычисления','НОД и НОК','Сравнения','Задачи','Координатная прямая','Задачи 6.3','Геометрия']]
    k=int(k[-1])
    print(k)
    buttons = [telebot.types.KeyboardButton(f"👍 Тема {i}") for i in spisokTem[k]]
    keyboard3.add(*buttons)
    bot.send_message(message.chat.id, "Выберите тему:", reply_markup=keyboard3)


def generate_error_message(error_count):
    print(error_count)
    if error_count == 1:
        return "ка"
    elif 2 <= error_count <= 4:
        return "ки"
    else:
        return "ок"

"""Отправляет следующий вопрос пользователю."""
def send_next_question(chat_id, user_id,message):
    print('next')####################
    user_data[user_id]["current_question"] += 1
    print(user_data[user_id]["current_question"], user_data[user_id]["score"],)########################
    if user_data[user_id]["current_question"] > QLEN:
        end_time = time.time()#конец времени
        total_time = end_time - user_data[user_id]["start_time"]
        if user_data[user_id]['score']==user_data[user_id]["current_question"]-1:
            bot.send_message(chat_id,
                      f"Поздравляем, вы прошли без ошибок.\nВремя прохождения: {total_time:.2f} секунд.")
            mainbase.newscore(user_data[user_id]['studentname'],total_time)
            # start(message)
        else:
            bot.send_message(chat_id,
                             f"Поздравляем, у вас {user_data[user_id]['current_question']-user_data[user_id]['score']-1} "
                             f"ошиб{generate_error_message(user_data[user_id]['current_question']-user_data[user_id]['score']-1)}. Время не засчитано.")
            print('#########################')
            print(user_data[user_id]["state"])
            print(user_data[user_id])
            #
        del user_data[user_id]#удалить сессию
        start(message)#начать новую сессию
        return

    print(user_data)

    problem,answer = fromGenerate.taskcount(message,user_data)
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
    user_id = message.from_user.id
    # сессия для каждого пользователя
    user_data[user_id] = {
        "state": WAITING_FOR_ANSWER,
        "state_choice": FIRST_CHOICE,
        "first_choice": None,
        "second_choice": None,
        "third_choice": None,
        "current_question": 0,
        "score": 0,
        "problem": None,
        "answer": None,
        "start_time": time.time(),
        'list': [],
        'studentname': studentname,
        'start':0
    }
    bot.send_message(message.chat.id, f"Привет! {studentname} Это MathBot, выберите режим:", reply_markup=keyboard1)

def start_reg(message):
    user_id = message.from_user.id
    if 'Тренировка' in user_data[user_id]['first_choice']:
        training(message,user_data[user_id]['second_choice'],user_data[user_id]['third_choice'])
    else:
        competitive(message, user_data[user_id]['second_choice'], user_data[user_id]['third_choice'])
    pass

#РЕЖИМ ТЕРНИРОВКИ

def training(message,l,t):
    bot.send_message(message.chat.id, "Режим тренировки 👍!", reply_markup=telebot.types.ReplyKeyboardRemove())

#РЕЖИМ СОРЕВНОВАНИЯ

def competitive(message,l,t):
    spisokemo = ['3️⃣', '2️⃣', '1️⃣']
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Соревновательный режим 🚀!",reply_markup=telebot.types.ReplyKeyboardRemove())
    for i in range(3):#обратный отсчет
        time.sleep(1)
        bot.send_message(message.chat.id,spisokemo[i])

    user_data[user_id]['start_time']=time.time()#старт времени
    user_data[user_id]['studentname']=whatname(message)
    send_next_question(message.chat.id, user_id,message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    # print(user_id)#################################
    if user_id not in user_data:
        return
    state_choice = user_data[user_id]["state_choice"]
    if user_data[user_id]['start']==0:
        if state_choice  == FIRST_CHOICE:
            if message.text in ["👍 Тренировка","🚀 Соревнование"]:
                user_data[user_id]["first_choice"] = message.text
                user_data[user_id]["state_choice"] = SECOND_CHOICE
                show_second_choice_keyboard(message)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")

        elif state_choice == SECOND_CHOICE:
            if  'Уровень' in message.text:
                user_data[user_id]["second_choice"] = message.text
                user_data[user_id]["state_choice"] = THIRD_CHOICE
                show_third_choice_keyboard(message,message.text)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")

        elif state_choice == THIRD_CHOICE:
            # print(message.text)
            if 'Тема' in message.text:

                user_data[user_id]["third_choice"] = message.text
                user_data[user_id]['start']=1
                bot.send_message(message.chat.id, "Ваши выборы записаны!", reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, f"#-{user_data[user_id]['first_choice']}"
                                                  f"#-{user_data[user_id]['second_choice']}"
                                                  f"#-{user_data[user_id]['third_choice']}")
                start_reg(message)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")

    if user_data[user_id]["state"] == WAITING_FOR_ANSWER and user_data[user_id]["start"]:
        try:
            user_answer = int(message.text)
            correct_answer = user_data[user_id]["answer"]
            # print(user_data)
            if user_answer == correct_answer:
                user_data[user_id]["score"] += 1
                bot.send_message(message.chat.id, "Правильно!")
            else:
                bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")

            user_data[user_id]["state"] = SENDING_NEXT_QUESTION
            send_next_question(message.chat.id, user_id,message)
            print(user_data)
            if user_id in user_data:
                    user_data[user_id]["state"] = WAITING_FOR_ANSWER

        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите число.")

# Запуск бота
bot.polling(none_stop=True)