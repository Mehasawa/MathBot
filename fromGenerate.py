import random

START1 = 5
START2 = 10
END = 20

def task_level(message, user_data):#собирает инфу
    user_id=message.from_user.id
    tema = user_data[user_id]['third_choice']
    lvl =  user_data[user_id]['second_choice']
    rezhim = user_data[user_id]['first_choice']

    pass

def taskcount(message,user_data,tema,lvl):#цикл задач
    user_id = message.from_user.id
    task_level(message,user_data)############################################################
    if user_data[user_id]["current_question"] <= START1:
        problem, answer = primer(1)
        #проверка на то что пример уже попадался
        while problem in user_data[user_id]['list']:
            problem, answer = primer(1)
    elif user_data[user_id]["current_question"] <= START2:
        problem, answer = primer(2)
        # проверка на то что пример уже попадался
        while problem in user_data[user_id]['list']:
            problem, answer = primer(2)
    elif user_data[user_id]["current_question"] <= END:
        problem, answer = primer(3)
        # проверка на то что пример уже попадался
        while problem in user_data[user_id]['list']:
            problem, answer = primer(3)
    return problem,answer

def primer(lvl=1,act='*'):#генерирует примеры в одно действие
    proverka=False
    while not proverka:
        if lvl==1:
            num1=random.randint(2,9)
            num2=random.randint(2,9)
        elif lvl==2:
            num1=10
            while num1%10==0:
                num1 = random.randint(12, 99)
                num2 = random.randint(2, 9)
        elif lvl==3:
            num1 = 10
            num2 = 10
            while num1 % 10 == 0 and num2 % 10 == 0:
                num1 = random.randint(12, 99)
                num2 = random.randint(12, 99)
        if act=='*':
            problem = f'{num1} * {num2} = '
            answer = num1*num2
            proverka=True
        if act=='+':
            problem = f'{num1} + {num2} = '
            answer = num1+num2
            proverka = True
        if act=='-':
            problem = f'{num1} - {num2} = '
            answer = num1-num2
            if num1>num2:
                proverka = True
        if act=='/':
            problem = f'{num1} : {num2} = '
            answer = num1/num2
            if num2!=0 and num1>num2:
                proverka = True
        print(problem,answer)#####################
    return problem,answer