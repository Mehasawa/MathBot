
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



