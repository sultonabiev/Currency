import sqlite3

connection = sqlite3.connect('Currency.db', check_same_thread=False)
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS customer(id INTEGER, name TEXT, phone_number TEXT, loc TEXT);')

def register(id, name, phone_number, loc):
    sql.execute('INSERT INTO customer VALUES(?,?,?,?);', (id, name, phone_number, loc))
    connection.commit()

def checker(id):
    check = sql.execute('SELECT id FROM customer WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False


