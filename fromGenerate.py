import random

START1 = 5
START2 = 10
END = 20

def count_decimal_places(number):
    number_str = str(number)
    if "." not in number_str:
        return 0  # Если нет десятичной части, возвращаем 0
    decimal_part = number_str.split(".")[1]
    return len(decimal_part)

def task_level(message, user_data):#собирает инфу
    user_id=message.from_user.id
    tema = user_data[user_id]['third_choice']
    lvl =  int(user_data[user_id]['second_choice'][-1])
    rezhim = user_data[user_id]['first_choice']
    return tema,lvl,rezhim
    pass

def taskcount(message,user_data):#цикл задач
    user_id = message.from_user.id
    tema,lvl,rezhim = task_level(message,user_data)############################################################
    # print(lvl,rezhim)
    # print(len(lvl))
    if 'Тренировка' in rezhim:
        COUNT = START1
    else:
        COUNT = START2
    if user_data[user_id]["current_question"] <= COUNT:
        if 'Арифметика' in tema or 'Вычисления' in tema:
            print('111')
            problem, answer = primer(lvl)
        #проверка на то что пример уже попадался
        while problem in user_data[user_id]['list']:
            problem, answer = primer(lvl)

    return problem,answer
#СРАВНЕНИЯ
#ВЕЛИЧИНЫ
#ОКРУГЛЕНИЯ
#УРАВНЕНИЯ
#ВЫЧИСЛЕНИЯ
def primer(lvl=1):#генерирует примеры в одно действие
    proverka=False
    while not proverka:
        if lvl==1:
            act = random.choice(['+','-'])
            num1=random.randint(2,9)
            num2=random.randint(2,9)
        elif lvl==2:
            act = random.choice(['+', '-','*'])
            if act=='*':
                print('*')
                num1 = random.randint(2, 9)
                num2 = random.randint(2, 9)
            else:
                print('not')
                num1 = random.randint(12, 99)
                num2 = random.randint(2, 9)
        elif lvl==3:
            act = random.choice(['+', '-', '*','/'])
            num1 = random.randint(12, 99)
            num2 = random.randint(12, 99)
        elif lvl==4:
            act = random.choice(['+', '-', '*','/'])
            num1 = random.randint(12, 1990)
            num2 = random.randint(12, 99)
        elif lvl==5:
                act = random.choice(['+', '-', '*','/'])
            # monetka = random.choice(['dec','ob'])
            # if monetka=='ob':
            #     ch1 = random.randint(1, 10)
            #     ch2 = random.randint(1, 10)
            #     z1 = random.randint(2, 20)
            #     num1 = ch1/z1
            #     num2 = ch2/z1
            #     if z1>ch1:
            #         proverka=True
            # else:
                if act=='*' or act=='/':
                    okr1 = random.randint(0,2)
                    okr2 = random.randint(0,2)
                else:
                    okr1 = random.randint(1, 4)
                    okr2 = random.randint(1, 4)
                num1 = round(random.uniform(2, 99),okr1)
                num2 = round(random.uniform(2, 99),okr2)
        elif lvl==6:
                act = random.choice(['+', '-', '*','/'])
            # monetka = random.choice(['dec','ob'])
            # if monetka=='ob':
            #     ch1 = random.randint(1, 10)
            #     ch2 = random.randint(1, 10)
            #     z1 = random.randint(2, 20)
            #     num1 = ch1/z1
            #     num2 = ch2/z1
            #
            # else:
                okr1 = random.randint(1,4)
                okr2 = random.randint(1,4)
                num1 = round(random.uniform(-99, 99),okr1)
                num2 = round(random.uniform(-99, 99),okr2)
        print(act)
        if act=='*':
            problem = f'{num1} * {num2} = '
            answer = num1*num2
            if lvl<5:
                proverka=True
            elif count_decimal_places(answer)<=max(okr1,okr2):
                proverka=True
        if act=='+':
            problem = f'{num1} + {num2} = '
            answer = num1+num2
            if lvl < 5:
                proverka = True
            elif count_decimal_places(answer) <= max(okr1, okr2):
                proverka = True
        if act=='-':
            problem = f'{num1} - {num2} = '
            answer = num1-num2
            if num1>num2 and lvl<5:
                proverka = True
            elif lvl==5 and num1>num2 and count_decimal_places(answer) <= max(okr1,okr2):
                proverka = True
            elif lvl==6 and count_decimal_places(answer) <= max(okr1,okr2):
                proverka = True
        if act=='/':
            problem = f'{num1} : {num2} = '
            answer = num1/num2

            # if lvl==5 or lvl==6:
            #     answer=round(answer,max(okr1,okr2))
            if answer.is_integer() and num2!=0 and num1>num2 and lvl<6:
                proverka = True
            if lvl==6 and num2!=0:
                if answer.is_integer() or count_decimal_places(answer)<=2:
                    proverka=True
    print(problem,answer)#####################
    return problem,answer