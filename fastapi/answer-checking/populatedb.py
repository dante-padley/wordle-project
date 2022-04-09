import json;
import sqlite3

conn = sqlite3.connect("./db/answers.db")
f = open("./answers.json", "r")
y = json.loads(f.read())
f.close();
#print(y)

for x in y:
    conn.execute('INSERT INTO answers(word) VALUES(?)', [x])

conn.commit()

conn.close()