# Run this to setup the bot

import sqlite3

conn = sqlite3.connect("main.db")
cur = conn.cursor()

cur.execute("CREATE TABLE Tensors (user_id INTEGER, context BLOB)")
conn.commit()

token = input("Enter your discord token: ")
with open(".env", "w") as f:
    f.write(f"TOKEN = {token}")