import sqlite3
import uuid

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

db = sqlite3.connect("./users.db")
stmt = db.execute("""
    SELECT * FROM users LIMIT 1;
""")
user = stmt.fetchone()
print(uuid.UUID(bytes_le= user[0]))