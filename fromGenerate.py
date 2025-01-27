import random

def task_level():
    pass

def taskcount(message,user_data):
    user_id = message.from_user.id
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
    return problem,answer

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