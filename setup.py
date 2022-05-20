import sqlite3

conn = sqlite3.connect("main.db")
cur = conn.cursor()

cur.execute("CREATE TABLE Tensors (user_id INTEGER, context BLOB)")
conn.commit()