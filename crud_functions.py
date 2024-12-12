import sqlite3

connection = sqlite3.connect('initiate.db')
cursor = connection.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Products(
#     id INTEGER PRIMARY KEY,
#     title TEXT NOT NULL,
#     description TEXT,
#     price INTEGER NOT NULL
#     )
#     ''')
#
# cursor.execute('''DELETE FROM Products''')
# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)',
#                    (f'Product{i}', f'title{i}', '{i * 100}'))
connection.commit()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()

# cursor.execute('DELETE FROM Products')
# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)',
#                    (f'Продукт{i}', f'Описание{i}', i * 100))
# connection.commit()

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()


#cursor.execute(''' DELETE FROM Users''')

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, 1000)',
                   (username, email, age))
    connection.commit()

def is_included(username):
    cursor.execute('SELECT * FROM Users')
    all_users = cursor.fetchall()
    for user in all_users:
        if username == user[1]:
            return True
    return False