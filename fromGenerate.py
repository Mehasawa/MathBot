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


def taskcount(message,user_data):#цикл задач
    user_id = message.from_user.id
    tema,lvl,rezhim = task_level(message,user_data)#############
    problem, answer='empty','empty'
    # if 'Тренировка' in rezhim:
    #     COUNT = START1
    # else:
    #     COUNT = START2
    # if user_data[user_id]["current_question"] <= COUNT:
    if 'Арифмет' in tema or 'Вычисл' in tema:
            problem, answer = primer(lvl)
            #проверка на то что пример уже попадался
            while problem in user_data[user_id]['list']:
                problem, answer = primer(lvl)
    if 'Сравн' in tema:
            problem, answer = sravn(lvl)
            # проверка на то что пример уже попадался
            while problem in user_data[user_id]['list']:
                problem, answer = sravn(lvl)

    return problem,answer

diff = {'lvl':[],'act':[]}
#СРАВНЕНИЯ
def preobrRes(n1,n2,act):
    if act=='+':
        return n1+n2
    elif act=='-':
        return n1-n2
    elif act=='*':
        return n1*n2
    else:
        return n1/n2

def sravnRes(n1,n2):
    if n1<n2:
        return '<'
    elif n1>n2:
        return '>'
    else:
        return '='

def rand0(n1,n2):
    n=0
    while n==0:
        n=random.randint(-99,99)
    return n

def makeDelenie(*args):
    n1 = args[0]*args[1]
    n2 = args[0]
    if count_decimal_places(n1)>4:
        n1=round(n1,4)
    if len(args)>2:
        n3 = args[2]*args[3]
        n4 = args[2]
        if count_decimal_places(n3) > 4:
            n3 = round(n3, 4)
        return n1,n2,n3,n4
    else:
        return n1,n2

def minusSkobki(*args):
    if len(args)>3:
        num1=args[0]
        num2=args[1]
        num3=args[2]
        num4=args[3]
        act1=args[-1]
        if num2 < 0 and num4 < 0:
            problem = f'{num1} {act1} ({num2})_?_{num3} {act1} ({num4})'
        elif num2 < 0:
            problem = f'{num1} {act1} ({num2})_?_{num3} {act1} {num4}'
        elif num4 < 0:
            problem = f'{num1} {act1} {num2}_?_{num3} {act1} ({num4})'
        else:
            problem = f'{num1} {act1} {num2}_?_{num3} {act1} {num4}'
        return problem
    else:
        num1 = args[0]
        num2 = args[1]
        act1 = args[-1]
        if num2 < 0:
            problem = f'{num1} {act1} ({num2})'
        else:
            problem = f'{num1} {act1} {num2}'
        return problem


def sravn(lvl=1):
    proverka = False
    problem,answer='none','none'
    while not proverka:
        if lvl == 2:
            num1 = random.randint(11, 99)
            num2 = random.randint(11, 99)
            problem = f'{num1}_?_{num2}'
            answer = sravnRes(num1,num2)
            proverka = True
        elif lvl==3:
            act1 = random.choice(['+', '-'])
            act2 = random.choice(['+', '-'])
            while not proverka:###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!test
                num1 = random.randint(2, 99)
                num2 = random.randint(2, 99)
                num3 = random.randint(2, 99)
                num4 = random.randint(2, 99)
                problem = f'{num1} {act1} {num2}_?_{num3} {act1} {num4}'
                answer = sravnRes(preobrRes(num1,num2,act1),preobrRes(num3,num4,act1))
                if num1>num2 and num3>num4:
                    proverka = True
        elif lvl==4:
            act1 = random.choice(['+', '-','*','/'])
            act2 = random.choice(['+', '-','*','/'])
            while not proverka:  ###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!test
                num1 = random.randint(12, 990)
                num2 = random.randint(12, 990)
                num3 = random.randint(12, 990)
                num4 = random.randint(12, 990)
                problem = f'{num1} {act1} {num2}_?_{num3} {act1} {num4}'
                answer = sravnRes(preobrRes(num1, num2, act1), preobrRes(num3, num4, act1))
                if act1=='+':
                    proverka=True
                elif act1=='-' and num1 > num2 and num3 > num4:
                    proverka = True
                elif act1=='*':
                    proverka = True
                elif act1=='/':
                    n1,n2,n3,n4 = makeDelenie(num1,num2,num3,num4)
                    n1, n2, n3, n4 = int(n1),int(n2),int(n3),int(n4)
                    problem = f'{n1} {act1} {n2}_?_{n3} {act1} {n4}'
                    answer = sravnRes(preobrRes(n1, n2, act1), preobrRes(n3, n4, act1))
                    proverka = True

        elif lvl==5:
            act1 = random.choice(['+', '-', '*', '/'])
            act2 = random.choice(['+', '-', '*', '/'])
            while not proverka:  ###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!test
                num1 = round(random.uniform(12, 99),2)
                num2 = round(random.uniform(12, 99),2)
                num3 = round(random.uniform(12, 99),2)
                num4 = round(random.uniform(12, 99),2)
                print(num1, num2, num3, num4)
                problem = f'{num1} {act1} {num2}_?_{num3} {act1} {num4}'
                answer = sravnRes(preobrRes(num1, num2, act1), preobrRes(num3, num4, act1))
                if act1=='+':
                    proverka=True
                elif act1=='-' and num1 > num2 and num3 > num4:
                    proverka = True
                elif act1=='*':
                    proverka = True
                elif act1=='/':
                    n1,n2,n3,n4 = makeDelenie(num1,num2,num3,num4)
                    res1 = n1 / n2
                    res2 = n3 / n4
                    if count_decimal_places(res1)<=2 and count_decimal_places(res2)<=2:
                        proverka = True
                    else:
                        proverka = False
                    # n1, n2, n3, n4 = int(n1),int(n2),int(n3),int(n4)
                    problem = f'{n1} {act1} {n2}_?_{n3} {act1} {n4}'
                    answer = sravnRes(preobrRes(n1, n2, act1), preobrRes(n3, n4, act1))

        elif lvl==6:
            act1 = random.choice(['+', '-', '*', '/'])
            act2 = random.choice(['+', '-', '*', '/'])
            while not proverka:  ###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!test
                num1 = rand0(-99, 99)
                num2 = rand0(-99, 99)
                num3 = rand0(-99, 99)
                num4 = rand0(-99, 99)
                print(num1,num2,num3,num4, act1)
                problem = minusSkobki(num1,num2,num3,num4,act1)
                answer = sravnRes(preobrRes(num1, num2, act1), preobrRes(num3, num4, act1))
                if act1 == '/' and num2!=0 and num4!=0 and num1!=0 and num3!=0:
                    n1, n2, n3, n4 = makeDelenie(num1, num2, num3, num4)
                    res1 = n1 / n2
                    res2 = n3 / n4
                    if count_decimal_places(res1) <= 4 and count_decimal_places(res2) <= 4:
                        problem = minusSkobki(n1,n2,n3,n4,act1)
                        answer = sravnRes(preobrRes(n1, n2, act1), preobrRes(n3, n4, act1))
                        proverka = True
                    else:
                        proverka = False
                else:
                    proverka = True
    print(problem, answer) #####################
    return problem, answer
#ВЕЛИЧИНЫ
#ОКРУГЛЕНИЯ
#УРАВНЕНИЯ
#ВЫЧИСЛЕНИЯ
def proverkaPrimer(*args):
    num1=args[0]
    num2=args[1]
    act=args[2]
    lvl=args[3]
    problem,answer='none','none'
    proverka=False
    if lvl<5:
        if act=='-' and num1>num2:
            problem = f'{num1} - {num2} = '
            answer = num1 - num2
            proverka = True
        elif act == '/' and num2 != 0:
            n1, n2 = makeDelenie(num1, num2)
            problem = f'{n1} {act} {n2}'
            answer = int(n1/n2)
            proverka = True
        elif act=='+':
            problem = f'{num1} {act} {num2}'
            answer = num1+num2
            proverka = True
        elif act=='*':
            problem = f'{num1} {act} {num2}'
            answer = num1 * num2
            proverka = True
    elif lvl==5:
        if act=='-' and num1>num2:
            problem = f'{num1} - {num2} = '
            answer = num1 - num2
            if count_decimal_places(answer) > 4:
                answer = round(answer, 4)
            proverka = True
        elif act == '/' and num2!=0 and num1!=0:
            n1, n2 = makeDelenie(num1, num2)
            problem = f'{n1} {act} {n2}'
            res1 = n1 / n2
            answer = n1/n2
            if count_decimal_places(res1) <= 4:
                proverka = True
        elif act == '+':
                problem = f'{num1} {act} {num2}'
                answer = num1 + num2
                if count_decimal_places(answer) > 4:
                    answer = round(answer, 4)
                proverka = True
        elif act=='*':
                problem = f'{num1} {act} {num2}'
                answer = num1 * num2
                if count_decimal_places(answer) > 4:
                    answer = round(answer, 4)
                proverka = True
    elif lvl==6:
        if act == '/' and num2!=0 and num1!=0:
            n1, n2 = makeDelenie(num1, num2)
            problem = minusSkobki(num1,num2,act)
            res1 = n1 / n2
            answer = n1 / n2
            if count_decimal_places(res1) <= 4:
                proverka = True
        elif act=='-':
            problem = minusSkobki(num1,num2,act)
            answer = num1 - num2
            if count_decimal_places(answer) > 4:
                answer = round(answer, 4)
            proverka = True
        elif act == '+':
                problem = minusSkobki(num1,num2,act)
                answer = num1 + num2
                if count_decimal_places(answer) > 4:
                    answer = round(answer, 4)
                proverka = True
        elif act=='*':
                problem = minusSkobki(num1,num2,act)
                answer = num1 * num2
                if count_decimal_places(answer) > 4:
                    answer = round(answer, 4)
                proverka = True

    return problem,answer,proverka

def primer(lvl=1):#генерирует примеры в одно действие
    proverka=False
    problem,answer='none','none'
    num1,num2,act=0,0,'%'
    while not proverka:
        if lvl==1:
            act = random.choice(['+','-'])
            while not proverka:
                num1=random.randint(2,9)
                num2=random.randint(2,9)
                problem, answer, proverka = proverkaPrimer(num1,num2,act,lvl)
        elif lvl==2:
            act = random.choice(['+', '-','*'])
            while not proverka:
                num1=random.randint(12,99)
                num2=random.randint(2,9)
                if act=='*':
                    num1=random.randint(2,9)
                problem, answer, proverka = proverkaPrimer(num1, num2, act, lvl)
        elif lvl==3:
            act = random.choice(['+', '-', '*','/'])
            while not proverka:
                num1 = random.randint(12, 99)
                num2 = random.randint(12, 99)
                problem, answer, proverka = proverkaPrimer(num1, num2, act, lvl)
        elif lvl==4:
            act = random.choice(['+', '-', '*','/'])
            while not proverka:
                num1 = random.randint(12, 1990)
                num2 = random.randint(12, 99)
                problem, answer, proverka = proverkaPrimer(num1, num2, act, lvl)
        elif lvl==5:
                act = random.choice(['+', '-', '*','/'])
                while not proverka:
                    if act=='*' or act=='/':
                        okr1 = random.randint(0,2)
                        okr2 = random.randint(0,2)
                    else:
                        okr1 = random.randint(1, 4)
                        okr2 = random.randint(1, 4)
                    num1 = round(random.uniform(2, 99),okr1)
                    num2 = round(random.uniform(2, 99),okr2)
                    problem, answer, proverka = proverkaPrimer(num1, num2, act, lvl)
        elif lvl==6:
                act = random.choice(['+', '-', '*','/'])
                while not proverka:
                    okr1 = random.randint(1,4)
                    okr2 = random.randint(1,4)
                    num1 = round(random.uniform(-99, 99),okr1)
                    num2 = round(random.uniform(-99, 99),okr2)
                    problem, answer, proverka = proverkaPrimer(num1, num2, act, lvl)
        print(num1,num2,act)
        # if act=='*':
        #     if num2 < 0:
        #         problem = f'{num1} * ({num2}) = '
        #     else:
        #         problem = f'{num1} * {num2} = '
        #     answer = num1*num2
        #     if lvl<5:
        #         proverka=True
        #     elif count_decimal_places(answer)<=4:
        #         proverka=True
        # if act=='+':
        #     if num2 < 0:
        #         problem = f'{num1} + ({num2}) = '
        #     else:
        #         problem = f'{num1} + {num2} = '
        #     answer = num1+num2
        #     if lvl < 5:
        #         proverka = True
        #     elif count_decimal_places(answer) <= 4:
        #         proverka = True
        # if act=='-':
        #     if num2<0:
        #         problem = f'{num1} - ({num2}) = '
        #     else:
        #         problem = f'{num1} - {num2} = '
        #     answer = num1-num2
        #     if num1>num2 and lvl<5:
        #         proverka = True
        #     elif lvl==5 and num1>num2 and count_decimal_places(answer) <= 4:
        #         proverka = True
        #     elif lvl==6 and count_decimal_places(answer) <= 4:
        #         proverka = True
        # if act=='/':
        #     if num2 < 0:
        #         problem = f'{num1} : ({num2}) = '
        #     else:
        #         problem = f'{num1} : {num2} = '
        #     answer = num1/num2
        #     if answer.is_integer() and num2!=0 and num1>num2 and lvl<6:
        #         proverka = True
        #     if lvl==6 and num2!=0:
        #         if answer.is_integer() or count_decimal_places(answer)<=4:
        #             proverka=True
    print(problem,answer)#####################
    return problem,answer   