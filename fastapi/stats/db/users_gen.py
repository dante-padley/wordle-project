#!/usr/bin/env python3

import contextlib
import datetime
import random
import sqlite3
import uuid

import faker

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


GAME_DB_1 = './games1.db'
GAME_DB_2 = './games2.db'
GAME_DB_3 = './games3.db'
USER_DB = './users.db'
GAME_SCHEMA = './game_schema.sql'
USER_SCHEMA = './user_schema.sql'

NUM_STATS = 1_000_000
NUM_USERS = 100_000
YEAR = 2022

random.seed(YEAR)
fake = faker.Faker()
fake.seed(YEAR)

with contextlib.closing(sqlite3.connect(USER_DB, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    with open(USER_SCHEMA) as f:
        db.executescript(f.read())
    for _ in range(NUM_USERS):
        while True:
            try:
                profile = fake.simple_profile()
                profile["user_id"] = uuid.uuid4()
                db.execute('INSERT INTO users(user_id, username) VALUES(:user_id, :username)', profile)

            except sqlite3.IntegrityError:
                continue
            break
    db.commit()
    # jan_1 = datetime.date(YEAR, 1, 1)
    # today = datetime.date.today()
    # num_days = (today - jan_1).days
    # i = 0
    # while i < NUM_STATS:
    #     while True:
    #         try:
    #             user_id = random.randint(1, NUM_USERS)
    #             game_id = random.randint(1, num_days)
    #             finished = jan_1 + datetime.timedelta(random.randint(0, num_days))
    #             # N.B. real game scores aren't uniformly distributed...
    #             guesses = random.randint(1, 6)
    #             # ... and people mostly play to win
    #             won = random.choice([False, True, True, True])
    #             db.execute(
    #                 """
    #                 INSERT INTO games(user_id, game_id, finished, guesses, won)
    #                 VALUES(?, ?, ?, ?, ?)
    #                 """,
    #                 [user_id, game_id, finished, guesses, won]
    #             )
    #         except sqlite3.IntegrityError:
    #             continue
    #         i += 1
    #         break
    # db.commit()