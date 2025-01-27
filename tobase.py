import  sqlite3

conn = sqlite3.connect('names.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT,
        hiscore INTEGER
    )
''')

# Добавление начальных фамилий
surnames = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
for surname in surnames:
    cursor.execute("INSERT INTO students (surname,hiscore) VALUES (?,?) ", (surname,0))


# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
print("База данных и таблица созданы.")