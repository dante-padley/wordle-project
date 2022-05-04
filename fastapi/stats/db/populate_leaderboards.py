#!/usr/bin/env python3
import sqlite3
import uuid
import redis

from pydantic import BaseSettings

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

class Settings(BaseSettings):
    GAME_DATABASE1: str
    GAME_DATABASE2: str
    GAME_DATABASE3: str
    USER_DATABASE: str
    class Config:
        env_file = "./stats/.env"

settings = Settings()

db1 = sqlite3.connect(settings.GAME_DATABASE1, detect_types=sqlite3.PARSE_DECLTYPES)
db2 = sqlite3.connect(settings.GAME_DATABASE2, detect_types=sqlite3.PARSE_DECLTYPES)
db3 = sqlite3.connect(settings.GAME_DATABASE3, detect_types=sqlite3.PARSE_DECLTYPES)
db4 = sqlite3.connect(settings.USER_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)

r = redis.Redis(port=6381)

selectWinners1 = db1.execute("SELECT * FROM wins ORDER BY wins DESC LIMIT 10").fetchall()
selectWinners2 = db2.execute("SELECT * FROM wins ORDER BY wins DESC LIMIT 10").fetchall()
selectWinners3 = db3.execute("SELECT * FROM wins ORDER BY wins DESC LIMIT 10").fetchall()

topWins = selectWinners1
topWins.extend(selectWinners2)
topWins.extend(selectWinners3)

winnerLeaderboard = {}

for winner in topWins:
    #select current user's username
    selectUser = db4.execute("SELECT username FROM users WHERE user_id = :user_id", [winner[0]])
    userRow = selectUser.fetchall()
    #toss it in the leaderboard
    winnerLeaderboard[userRow[0][0]] = int(winner[1])



selectStreaks1 = db1.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()
selectStreaks2 = db2.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()
selectStreaks3 = db3.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()

#Throw them all in a list
topStreaks = selectStreaks1
topStreaks.extend(selectStreaks2)
topStreaks.extend(selectStreaks3)

streakLeaderboard = {}

for streak in topStreaks:
    #select current user's username
    selectUser = db4.execute("SELECT username FROM users WHERE user_id = :user_id", [streak[0]])
    userRow = selectUser.fetchall()
    #toss it in the leaderboard
    streakLeaderboard[userRow[0][0]] = int(streak[1])


r.zadd("WinnerLeaderboard", winnerLeaderboard)
r.zadd("StreakLeaderboard", streakLeaderboard)
