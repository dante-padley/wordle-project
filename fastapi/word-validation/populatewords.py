import sqlite3
import json

f = open("./dictionary.txt")
y = f.read()
z = y.splitlines()
#print(z)

db = sqlite3.connect("./db/words.db")

for x in z:
    db.execute('INSERT INTO words(word) VALUES(?)', [x])

db.commit()

db.close()