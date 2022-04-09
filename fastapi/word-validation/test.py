import sqlite3
import os

db = sqlite3.Connection("./word-validation/db/words.db")
db.execute("CREATE TABLE IF NOT EXISTS words2 (id INT PRIMARY KEY, word TEXT NOT NULL)")
# stream = os.popen("cat /usr/share/dict/words | grep -P  '^[\x61-\x7A]{5}$'")