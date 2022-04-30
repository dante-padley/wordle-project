#!/usr/bin/env python3

import contextlib
import datetime
import random
import sqlite3
import uuid


# import faker

DATABASE_GAME1 = 'fastapi/shards/db/gameShard1.db'
DATABASE_GAME2 = 'fastapi/shards/db/gameShard2.db'
DATABASE_GAME3 = 'fastapi/shards/db/gameShard3.db'
DATABASE_USER = 'fastapi/shards/db/users.db'

GAME_SCHEMA = 'fastapi/shards/game_schema.sql'
USER_SCHEMA = 'fastapi/shards/user_schema.sql'

# POPULATED_GAME = 'fastapi/shards/game_schema_populated.sql'
# POPULATED_USER = 'fastapi/shards/user_schema_populated.sql'

NUM_STATS = 1_000_000
NUM_USERS = 100_000
YEAR = 2022

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

# conn1 = sqlite3.connect(DATABASE_GAME1, detect_types=sqlite3.PARSE_DECLTYPES)
# conn2 = sqlite3.connect(DATABASE_GAME2, detect_types=sqlite3.PARSE_DECLTYPES)
# conn3 = sqlite3.connect(DATABASE_GAME3, detect_types=sqlite3.PARSE_DECLTYPES)
# conn4 = sqlite3.connect(DATABASE_USER, detect_types=sqlite3.PARSE_DECLTYPES)

with contextlib.closing(sqlite3.connect(DATABASE_USER), detect_types=sqlite3.PARSE_DECLTYPES) as db:
    with open(USER_SCHEMA) as f:
        # print(f)
        db.executescript(f.read())
    db.commit()

with contextlib.closing(sqlite3.connect(DATABASE_GAME1, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    with open(GAME_SCHEMA) as f:
        # print(f)
        db.executescript(f.read())
    db.commit()

with contextlib.closing(sqlite3.connect(DATABASE_GAME2), detect_types=sqlite3.PARSE_DECLTYPES) as db:
    with open(GAME_SCHEMA) as f:
        # print(f)
        db.executescript(f.read())
    db.commit()

with contextlib.closing(sqlite3.connect(DATABASE_GAME3), detect_types=sqlite3.PARSE_DECLTYPES) as db:
    with open(GAME_SCHEMA) as f:
        # print(f)
        db.executescript(f.read())
    db.commit()


# for i in range(0,3):
#     with contextlib.closing(sqlite3.connect(f"DATABASE_GAME{i+1}")) as db:
#         with open(GAME_SCHEMA) as f:
#             # print(f)
#             db.executescript(f.read())
#         db.commit()


# random.seed(YEAR)
# fake = faker.Faker()
# fake.seed(YEAR)
# with contextlib.closing(sqlite3.connect(DATABASE)) as db:
#     with open(SCHEMA) as f:
#         db.executescript(f.read())
#     for _ in range(NUM_USERS):
#         while True:
#             try:
#                 profile = fake.simple_profile()
#                 db.execute('INSERT INTO users(username) VALUES(:username)', profile)

#             except sqlite3.IntegrityError:
#                 continue
#             break
#     db.commit()
#     jan_1 = datetime.date(YEAR, 1, 1)
#     today = datetime.date.today()
#     num_days = (today - jan_1).days
#     i = 0
#     while i < NUM_STATS:
#         while True:
#             try:
#                 user_id = random.randint(1, NUM_USERS)
#                 game_id = random.randint(1, num_days)
#                 finished = jan_1 + datetime.timedelta(random.randint(0, num_days))
#                 # N.B. real game scores aren't uniformly distributed...
#                 guesses = random.randint(1, 6)
#                 # ... and people mostly play to win
#                 won = random.choice([False, True, True, True])
#                 db.execute(
#                     """
#                     INSERT INTO games(user_id, game_id, finished, guesses, won)
#                     VALUES(?, ?, ?, ?, ?)
#                     """,
#                     [user_id, game_id, finished, guesses, won]
#                 )
#             except sqlite3.IntegrityError:
#                 continue
#             i += 1
#             break
#     db.commit()