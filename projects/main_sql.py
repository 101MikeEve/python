import sqlite3

con = sqlite3.connect("test.db")

names = ['John', 'Mike', 'Jane', 'Bella']
grades = [90, 95, 92, 98]

# Создаем курсор
cur = con.cursor()

# Создаем таблицу с именем transcript
cur.execute("CREATE TABLE transcript (name text, grade integer);")

# Вставляем записи
cur.executemany("INSERT into transcript values (?, ?)", zip(names, grades))

# Выполняем все транзакции
con.commit()