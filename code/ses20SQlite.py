import sqlite3
conn = sqlite3.connect('towns.db')
conn.execute('''CREATE TABLE IF NOT EXISTS towns
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)''')
conn.execute("INSERT INTO towns (name) VALUES ('Wellesley')")
conn.commit()

for row in conn.execute("SELECT * FROM towns"):
    print(row)