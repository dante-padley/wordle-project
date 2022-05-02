import sqlite3
import uuid

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

db = sqlite3.connect("./games1.db")
stmt = db.execute("""
    SELECT * FROM games;
""")
rows = stmt.fetchall()

for game in rows:
    myuuid = uuid.UUID(bytes_le=game[0])
    myuuidint = myuuid.int
    myuuidshard = myuuid.int % 3
    if myuuidshard != 0:
        print(str(myuuidshard))

db = sqlite3.connect("./games2.db")
stmt = db.execute("""
    SELECT * FROM games;
""")
rows = stmt.fetchall()

for game in rows:
    myuuid = uuid.UUID(bytes_le=game[0])
    myuuidint = myuuid.int
    myuuidshard = myuuid.int % 3
    if myuuidshard != 1:
        print(str(myuuidshard))

db = sqlite3.connect("./games3.db")
stmt = db.execute("""
    SELECT * FROM games;
""")
rows = stmt.fetchall()

for game in rows:
    myuuid = uuid.UUID(bytes_le=game[0])
    myuuidint = myuuid.int
    myuuidshard = myuuid.int % 3
    if myuuidshard != 2:
        print(str(myuuidshard))

