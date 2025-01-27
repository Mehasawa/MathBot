import  sqlite3

conn = sqlite3.connect('zadachi.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS zadachi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level INTEGER,
        tema TEXT,
        task TEXT,
        taskimg BLOB
    )
''')

# Добавление начальных фамилий

for i in range(1,9):
    cursor.execute("INSERT INTO zadachi (level,tema, task,taskimg)"
                   " VALUES (?,?,?,?) ", (i,'тема','задача','NULL'))


# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
print("База данных и таблица созданы.")