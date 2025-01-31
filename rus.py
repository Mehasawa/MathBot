def ask_question(n1: int, n2: int):
    m1 = max(n1, n2)
    m2 = min(n1, n2)
    if m2>2:
        print(f"Сколько будет {' + '.join([str(m1)] * m2)}?")
        user_sum_answer = int(input("Введите ваш ответ: "))
        correct_sum = m1 * m2

        if user_sum_answer == correct_sum:
            print(f"Верно! Теперь сколько будет {m1} * {m2}?")

        else:
            ask_question(m1, m2-1)  # Возвращаемся к предыдущему вопросу
    else:
        ask = int(input(f"сколько будет {m1} * {m2}?"))
        if ask == m1*m2:
            ask_question(m1,m2+1)

ask_question(7,4)