import sqlite3
import uuid

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

db = sqlite3.connect("./games1.db")
stmt = db.execute("""
    SELECT * FROM games LIMIT 1;
""")
row = stmt.fetchone()
myuuid = uuid.UUID(bytes_le=row[0])
myuuidint = myuuid.int
print(myuuid)