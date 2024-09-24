import sqlite3


conn = sqlite3.connect('newsdb.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY,
                    title TEXT UNIQUE NOT NULL,
                    text TEXT NOT NULL
                )''')

conn.commit()
conn.close()