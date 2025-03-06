import time
import mainbase
import telebot
import fromGenerate
import fromBaseZadachi
from telebot import types

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
QUESTIONLEN=2

# Создание клавиатуры с кнопками и эмодзи
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = telebot.types.KeyboardButton("👍 Тренировка")  # Эмодзи 👍
button2 = telebot.types.KeyboardButton("🚀 Соревнование")  # Эмодзи 🚀
keyboard1.add(button1, button2)

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [telebot.types.KeyboardButton(f"👍 Уровень {i}") for i in range(1, 7)]
keyboard2.add(*buttons)

keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboardSRAVN = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = telebot.types.KeyboardButton("<")  #
button2 = telebot.types.KeyboardButton(">")  #
button3 = telebot.types.KeyboardButton("=")  #
keyboardSRAVN.add(button1, button2, button3)
'''
 Эмодзи 👍😐😀👆🚀🔥
'''
#ПОКАЗАТЬ КЛАВИАТУРЫ
def show_first_choice_keyboard(message):
    print('клава1')
    bot.send_message(message.chat.id, "Выберите режим:", reply_markup=keyboard1)

def show_second_choice_keyboard(message):
    print('клава2')
    bot.send_message(message.chat.id, "Выберите уровень:", reply_markup=keyboard2)

def show_third_choice_keyboardCOMP(message,k):
    print('клава3')
    spisokTem =[['0 уровень'],
             ['🔥Арифметика'],
             ['🔥Арифметика','🚀Сравнения'],
             ['🔥Вычисления','🚀Сравнения','👆Округление'],#3
             ['🔥Арифметика','😀Величины','🚀Сравнения'],
             ['🔥Вычисления','😀Величины','🚀Сравнения','👆Округление'],#5
             ['🔥Вычисления','😀Величины','🚀Сравнения']]
    k=int(k[-1])
    # print(k)
    keyboard3.keyboard=[]
    buttons = [telebot.types.KeyboardButton(f"{i}") for i in spisokTem[k]]
    # print(buttons)
    keyboard3.add(*buttons)
    bot.send_message(message.chat.id, "Выберите тему:", reply_markup=keyboard3)

def show_third_choice_keyboardTREN(message,k):
    print('клава3')
    spisokTem =[['0 уровень'],
             ['🔥Арифметика','Задачи','Фигуры','Информация'],
             ['🔥Арифметика','Задачи','Фигуры','Периметр','🚀Сравнения'],
             ['🔥Вычисления','Площадь','Задачи','Фигуры','Информация','🚀Сравнения'],
             ['😀Величины','🔥Арифметика','😐Задачи на движение','😐Задачи на работу','Задачи купли-продажи','Уравнения','🚀Сравнения'],#'Порядок действий'
             ['🔥Вычисления','😀Величины','🚀Сравнения','👆Округление','Задачи','😐Геометрия','😐Преобразование дробей'],#'Признаки делимости'
             ['🔥Вычисления','🚀Сравнения','Задачи','Координатная прямая','😀Величины','😐Геометрия']]#'НОД и НОК'
    k=int(k[-1])
    # print(k)
    keyboard3.keyboard=[]
    buttons = [telebot.types.KeyboardButton(f"{i}") for i in spisokTem[k]]
    # print(buttons)
    keyboard3.add(*buttons)
    bot.send_message(message.chat.id, "Выберите тему:", reply_markup=keyboard3)

def generate_error_message(error_count):
    # print(error_count)
    if error_count == 1:
        return "ка"
    elif 2 <= error_count <= 4:
        return "ки"
    else:
        return "ок"

"""Отправляет следующий вопрос пользователю."""
def send_next_question(chat_id, user_id,message):
    problem,answer = 'пусто','пусто'
    keyb=keyboard1
    print('next')####################
    user_data[user_id]["current_question"] += 1
    print(user_data[user_id]["current_question"], user_data[user_id]["score"],)########################
    if user_data[user_id]["current_question"] > QUESTIONLEN:
        end_time = time.time()#конец времени
        total_time = end_time - user_data[user_id]["start_time"]
        if 'Соревн' in user_data[user_id]['first_choice']:
            if user_data[user_id]['score']==user_data[user_id]["current_question"]-1:
                print('прошел без ошибок')
                bot.send_message(chat_id,
                          f"Поздравляем, вы прошли без ошибок.\nВремя прохождения: {total_time:.2f} секунд.")
                mainbase.newscore(user_data[user_id]['studentname'],total_time)
                # start(message)
            else:
                print('прошел с ошибками')
                bot.send_message(chat_id,
                                 f"Поздравляем, у вас {user_data[user_id]['current_question']-user_data[user_id]['score']-1} "
                                 f"ошиб{generate_error_message(user_data[user_id]['current_question']-user_data[user_id]['score']-1)}. Время не засчитано.")
                print('#########################')
            # print(user_data[user_id]["state"])
            print(user_data[user_id])
            #
        else:
            bot.send_message(chat_id,
                             f"Поздравляем, у вас {user_data[user_id]['current_question'] - user_data[user_id]['score'] - 1} "
                             f"ошиб{generate_error_message(user_data[user_id]['current_question'] - user_data[user_id]['score'] - 1)}.")

        del user_data[user_id]#удалить сессию
        start(message)#начать новую сессию
        return

    # print(user_data)
    if user_data[user_id]["start"]==1:
        print('включился старт')
        if user_data[user_id]["type_question"]=='srav':
            print('сравнения')
            ########################################################################################
            keyb=keyboardSRAVN
            # keyb = types.ReplyKeyboardRemove()
            problem, answer = fromGenerate.taskcount(message, user_data)  # вопрос из генерации
        elif user_data[user_id]["type_question"] == 'base':
            print('из базы')
            problem, answer, image = fromBaseZadachi.taskcount(message, user_data)  # вопрос из базы
            answer = str(answer).strip()
            answer = answer.replace(' ','_')
            if image!='none':
                user_data[user_id]["image"] = image
                try:
                    with open(image, 'rb') as photo:
                        bot.send_photo(chat_id, photo)#отправляет картинку
                except FileNotFoundError:
                    bot.send_message(chat_id, "Файл не найден.")
                except Exception as e:
                    bot.send_message(chat_id, f"Произошла ошибка: {e}")
                # bot.send_photo(chat_id, image)
            keyb=types.ReplyKeyboardRemove()
                #
        elif user_data[user_id]["type_question"] == 'number':
            print('арифметика',user_data[user_id]["sub_type"])
            keyb=types.ReplyKeyboardRemove()
            # keyb = keyboardSRAVN
            problem,answer = fromGenerate.taskcount(message,user_data)#вопрос из генерации
        user_data[user_id]['list'].append(problem) #в список примеров
        print('добавил пример в лист')
        user_data[user_id]["problem"] = problem
        user_data[user_id]["answer"] = answer

        bot.send_message(chat_id, problem ,reply_markup=keyb)

def whatname(message):
    print('узнает имя')
    if message.from_user.first_name and message.from_user.last_name:
        studentname = f'{message.from_user.first_name} {message.from_user.last_name}'
    elif message.from_user.first_name:
        studentname = message.from_user.first_name
    else:
        studentname = message.from_user.username
    return studentname

def temaDef(m):
    print('выбор темы')
    m=m.text.lower()
    if 'сравн' in m:
        return 'srav',''
    elif 'округл' in m:
        return 'number','round'
    elif 'арифм' in m or 'вычисл' in m:
        return 'number',''
    elif 'велич' in m:
        return 'number', 'preob'
    elif 'дроб' in m:
        return 'base','drob'
    else:
        return 'base',''

#СТАРТОВОЕ СООБЩЕНИЕ:
@bot.message_handler(commands=['start'])
def start(message):
    print('первое сообщение')
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
        "type_question":'number',
        "sub_type":'',
        "score": 0,
        "problem": None,
        "answer": None,
        "image":None,
        "start_time": time.time(),
        'list': [],
        'studentname': studentname,
        'start':0
    }
    bot.send_message(message.chat.id, f"Привет! {studentname} Это MathBot, выберите режим:", reply_markup=keyboard1)

def choicerezhim(message):
    print('выбор режима')
    user_id = message.from_user.id
    global QUESTIONLEN
    if 'Тренировка' in user_data[user_id]['first_choice']:
        QUESTIONLEN = 5
        training(message,user_data[user_id]['second_choice'],user_data[user_id]['third_choice'])
    else:
        QUESTIONLEN = 10
        competitive(message, user_data[user_id]['second_choice'], user_data[user_id]['third_choice'])
    pass

#РЕЖИМ ТЕРНИРОВКИ
def training(message,l,t):
    bot.send_message(message.chat.id, "Режим тренировки 👍!", reply_markup=telebot.types.ReplyKeyboardRemove())
    user_id = message.from_user.id
    send_next_question(message.chat.id, user_id, message)

#РЕЖИМ СОРЕВНОВАНИЯ
def competitive(message,l,t):
    spisokemo = ['3️⃣', '2️⃣', '1️⃣']
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Соревновательный режим 🚀!",reply_markup=telebot.types.ReplyKeyboardRemove())
    for i in range(3):#обратный отсчет
        time.sleep(1)
        bot.send_message(message.chat.id,spisokemo[i])

    user_data[user_id]['start_time']=time.time()#старт времени
    print('старт времени')
    user_data[user_id]['studentname']=whatname(message)
    send_next_question(message.chat.id, user_id,message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print('любое сообщение')
    user_id = message.from_user.id
    # print(user_id)#################################
    if user_id not in user_data:
        print('нет пользователя')
        bot.send_message(message.chat.id, "Напишите команду /start")
        return
    # if user_data[user_id]['problem']=='пусто':
    #     print('нет задачи')
    #     bot.send_message(message.chat.id, "Напишите команду /start")
    #     return

    state_choice = user_data[user_id]["state_choice"]
    print('начало выборов')
    if user_data[user_id]['start']==0:
        print('не старт')
        if state_choice  == FIRST_CHOICE:
            print('выбор1')
            if message.text in ["👍 Тренировка","🚀 Соревнование"]:
                user_data[user_id]["first_choice"] = message.text
                user_data[user_id]["state_choice"] = SECOND_CHOICE
                show_second_choice_keyboard(message)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")

        elif state_choice == SECOND_CHOICE:
            print('выбор2')
            if  'Уровень' in message.text:
                user_data[user_id]["second_choice"] = message.text
                user_data[user_id]["state_choice"] = THIRD_CHOICE
                if 'Тренир' in user_data[user_id]["first_choice"]:
                    show_third_choice_keyboardTREN(message,message.text)
                else:
                    show_third_choice_keyboardCOMP(message,message.text)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")

        elif state_choice == THIRD_CHOICE:
                print('выбор3')
                user_data[user_id]['type_question'],user_data[user_id]['sub_type']=temaDef(message)
                user_data[user_id]["third_choice"] = message.text
                user_data[user_id]['start']=1
                print('включил старт')
                bot.send_message(message.chat.id, "Выбор записан.", reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, f"#-{user_data[user_id]['first_choice']}"
                                                  f"#-{user_data[user_id]['second_choice']}"
                                                  f"#-{user_data[user_id]['third_choice']}")
                choicerezhim(message)
            # else:
            #     bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов")


    if user_data[user_id]["state"] == WAITING_FOR_ANSWER and user_data[user_id]["start"]:
            print('начало проверки ответа')
            if user_data[user_id]['problem'] == 'пусто':
                print('нет задачи')
                bot.send_message(message.chat.id, "Напишите команду /start")
                return
            user_answer ='none'
            if user_data[user_id]["type_question"]=='number':
                    print('ответ число')
                    try:
                        user_answer = float(message.text)###########!!!!!!!!!!!!!
                    except ValueError:
                        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
            elif user_data[user_id]["type_question"]=='srav':
                print('ответ знак сравнения')
                if message.text in ['<','>','=']:
                    user_answer = message.text####
                else:
                    bot.send_message(message.chat.id, "Пожалуйста, введите правильный знак.")
            elif user_data[user_id]["type_question"]=='base' and user_data[user_id]['sub_type']=='':
                print('из  базы число')
                try:
                    user_answer = float(message.text)####
                except:
                    bot.send_message(message.chat.id, "Пожалуйста, введите ответ к задаче в виде числа.")
            elif user_data[user_id]["type_question"]=='base' and user_data[user_id]['sub_type']=='drob':
                print('из  базы дробь')
                print(message.text)
                if message.text!=user_data[user_id]["third_choice"]:
                    user_answer = message.text####
                else:
                    bot.send_message(message.chat.id,
                                     "Введите дробь в формате: числитель/знаменатель, например 1/3")
                    bot.send_message(message.chat.id,
                                     "А если дробь смешанная, то после целой части ставим нижнее подчеркивание 1_1/3")
            correct_answer = user_data[user_id]["answer"]

            # print(user_data)
            if user_answer!='none':
                print('проверка ответа')
                print(user_answer,type(user_answer))
                try:
                    if user_answer == correct_answer or float(user_answer)==float(correct_answer):
                        user_data[user_id]["score"] += 1
                        bot.send_message(message.chat.id, "Правильно!")
                    else:
                        bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")
                except:
                    if user_answer == correct_answer:
                        user_data[user_id]["score"] += 1
                        bot.send_message(message.chat.id, "Правильно!")
                    else:
                        bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")
                user_data[user_id]["state"] = SENDING_NEXT_QUESTION
                print('след вопрос')
                send_next_question(message.chat.id, user_id,message)
            print(user_data)
    if user_id in user_data:
        print('переключение на waiting')
        user_data[user_id]["state"] = WAITING_FOR_ANSWER

# Запуск бота
bot.polling(none_stop=True)