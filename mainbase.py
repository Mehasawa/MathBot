
import sqlite3
def get_all_surnames():
  conn = sqlite3.connect('names.db')
  cursor = conn.cursor()
  cursor.execute("SELECT surname, hiscore FROM students")
  surnames = cursor.fetchall()
  conn.close()
  return surnames

def find_surname(search_surname):
   conn = sqlite3.connect('names.db')
   cursor = conn.cursor()
   cursor.execute("SELECT surname, hiscore FROM students WHERE surname = ?", (search_surname,))
   surname = cursor.fetchone()
   conn.close()
   return surname

def update_hiscore(surname, new_score):
  conn = sqlite3.connect('names.db')
  cursor = conn.cursor()
  cursor.execute("UPDATE students SET hiscore = ? WHERE surname = ?", (new_score, surname))
  conn.commit()
  conn.close()

def showscore(name):
    print("Список всех фамилий с рекордами:")
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute('SELECT surname, hiscore FROM students ORDER BY hiscore ASC')
    results = cursor.fetchall()
    # surnames_list = get_all_surnames()
    for surname, hiscore in results:
        print(f"Фамилия: {surname}, Рекорд: {hiscore}")
    conn.commit()
    conn.close()

def newscore(name,score):
    score=round(score,2)
    if find_surname(name):
        update_hiscore(name,score)
    else:
        conn = sqlite3.connect('names.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (surname,hiscore) VALUES (?,?) ", (name, score))
        conn.commit()
        conn.close()
    showscore(name)
    pass
# Пример использования
#     surnames_list = get_all_surnames()
#     print("Список всех фамилий с рекордами:")
#     for surname, hiscore in surnames_list:
#         print(f"Фамилия: {surname}, Рекорд: {hiscore}")



#
# searched_surname = "Петров"
# result = find_surname(searched_surname)
# if result:
#     surname, hiscore = result
#     print(f"Найдена фамилия {surname}, рекорд: {hiscore}")
# else:
#    print(f"Фамилия {searched_surname} не найдена")
#
# new_hiscore = 15
# update_hiscore(searched_surname, new_hiscore)
# print(f"Рекорд пользователя {searched_surname} изменен на {new_hiscore}")
#
# result = find_surname(searched_surname)
# if result:
#     surname, hiscore = result
#     print(f"Проверка: Найдена фамилия {surname}, рекорд: {hiscore}")
# else:
#    print(f"Фамилия {searched_surname} не найдена")
#
#
# searched_surname = "Кротов"
# result = find_surname(searched_surname)
# if result:
#     surname, hiscore = result
#     print(f"Найдена фамилия {surname}, рекорд: {hiscore}")
# else:
#    print(f"Фамилия {searched_surname} не найдена")


