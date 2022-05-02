import contextlib
import datetime
import random
import sqlite3
import uuid

import faker

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

#if you are reading this, this is incomplete!!
#if you are reading this, this is incomplete!!
#if you are reading this, this is incomplete!!

GAME_DB_1 = './games1.db'
GAME_DB_2 = './games2.db'
GAME_DB_3 = './games3.db'
USER_DB = './users.db'
GAME_SCHEMA = './game_schema.sql'
USER_SCHEMA = './user_schema.sql'


NUM_STATS = 1_000
NUM_USERS = 100_000
YEAR = 2022

random.seed(YEAR)
fake = faker.Faker()
fake.seed(YEAR)
allUsers = None

with contextlib.closing(sqlite3.connect(GAME_DB_1, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    with open(GAME_SCHEMA) as f:
        db.executescript(f.read())
        db.commit()
with contextlib.closing(sqlite3.connect(GAME_DB_2, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    with open(GAME_SCHEMA) as f:
        db.executescript(f.read())
        db.commit()
with contextlib.closing(sqlite3.connect(GAME_DB_3, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    with open(GAME_SCHEMA) as f:
        db.executescript(f.read())
        db.commit()

with contextlib.closing(sqlite3.connect(USER_DB, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    allUsers = db.execute("""
        SELECT user_id FROM users;
    """).fetchall()

def addGame(user_id, game_id, finished, guesses, won):
    whichShard = user_id.int % 3
    db = None
    if whichShard == 0:
        db = sqlite3.connect(GAME_DB_1, detect_types=sqlite3.PARSE_DECLTYPES)
    elif whichShard == 1:
        db = sqlite3.connect(GAME_DB_2, detect_types=sqlite3.PARSE_DECLTYPES)
    elif whichShard == 2:
        db = sqlite3.connect(GAME_DB_3, detect_types=sqlite3.PARSE_DECLTYPES)
    
    db.execute(
                """
                INSERT INTO games(user_id, game_id, finished, guesses, won)
                VALUES(?, ?, ?, ?, ?)
                """,
                [user_id, game_id, finished, guesses, won]
            )
    db.commit()



jan_1 = datetime.date(YEAR, 1, 1)
today = datetime.date.today()
num_days = (today - jan_1).days
i = 0
for user in allUsers:
    while True:
        try:
            user_id = user[0]
            for i in range(1,10):
                game_id = random.randint(1, num_days)
                finished = jan_1 + datetime.timedelta(random.randint(0, num_days))
                # N.B. real game scores aren't uniformly distributed...
                guesses = random.randint(1, 6)
                # ... and people mostly play to win
                won = random.choice([False, True, True, True])
                addGame(user_id, game_id, finished, guesses, won)
        except sqlite3.IntegrityError:
            continue
        i += 1
        break


    