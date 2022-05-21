import re
import sqlite3
import contextlib
import uuid
import redis

from datetime import date
from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


#!!! IMPORTANT !!!
#.env file in this directory contains environment variables.
#We can use that to refer to the locations of the database(s)
#without needing to rewrite a ton of stuff.
#If you want to add env variables to that file, make sure
#to represent them here.
class Settings(BaseSettings):
    GAME_DATABASE1: str
    GAME_DATABASE2: str
    GAME_DATABASE3: str
    USER_DATABASE: str
    LEADERBOARD_KEYSTORE: int
    
    class Config:
        env_file = "./.env"
        


#Game class to elegantly accept game submissions to the postGame path
#Can be used in future operations
class Game(BaseModel):
    user_id: uuid.UUID
    game_id: int
    finished: date
    guesses: int
    won: bool


#Scores object: this is only implemented within the Stats object
#and uses aliases to match Wordle's stats model.
#When referring to a score in a Stats object, you will use the concrete names
#like this: [nameOfObject].guesses.four
class Scores(BaseModel):
    one: int = Field(alias="1", default=0)
    two: int = Field(alias="2", default=0)
    three: int = Field(alias="3", default=0)
    four: int = Field(alias="4", default=0)
    five: int = Field(alias="5", default=0)
    six: int = Field(alias="6", default=0)
    fail: int = 0


#Stats object: use this to assemble a user's stats and return
#it to them in a standard format.
class Stats(BaseModel):
    currentStreak: int = 0
    maxStreak: int = 0
    guesses: Scores = Scores()
    winPercentage: float = 0
    gamesPlayed: int = 0
    gamesWon: int = 0
    averageGuesses: float = 0


#This is a fastapi Depends function that we can use to basically
#plug in our db connection and DRY up our code quite a bit.
#See it used in any of the API paths here
def get_db1():
    with contextlib.closing(sqlite3.connect(settings.GAME_DATABASE1, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db

def get_db2():
    with contextlib.closing(sqlite3.connect(settings.GAME_DATABASE2, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db
def get_db3():
    with contextlib.closing(sqlite3.connect(settings.GAME_DATABASE3, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db
def get_db4():
    with contextlib.closing(sqlite3.connect(settings.USER_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db
 

#IMPORTANT!!!
#Can use the settings object to refer to environment variables 
#like database paths, loggers, etc.
#Can see an example of usage in the get_db() function just above this
#Look to just below the imports at the top for more on settings.
settings = Settings()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "What a world!"}

@app.get("/username/{user_name}")
async def getUserID(user_name: str, db: sqlite3.Connection = Depends(get_db4)):
    selectedUser = db.execute(f"Select [user_id] FROM users WHERE users.username = '{user_name}'")
    user_id = selectedUser.fetchone()[0]
    data = {"user_name": user_name, "user_id": user_id}
    return data

@app.post("/stats/", status_code=status.HTTP_201_CREATED)
def postGame(game: Game, db1: sqlite3.Connection = Depends(get_db1), db2: sqlite3.Connection = Depends(get_db2), db3: sqlite3.Connection = Depends(get_db3)):
    #FYI: This function is almost entirely based off of Prof Avery's create_book function
    #We set the Game object to a dict now to make the db.execute line a bit cleaner
    g = dict(game)
    db = None

    shard_id = g['user_id'].int % 3
    if shard_id == 0:
        db = db1
    elif shard_id == 1:
        db = db2
    elif shard_id == 2:
        db = db3

    #We use try so we can catch errors writing to the db
    try:
        stmt = db.execute(
            """
            INSERT INTO games(user_id, game_id, finished, guesses, won)
            VALUES(:user_id, :game_id, :finished, :guesses, :won)
            """,
            g,
        )
        db.commit()
    #handle sqlite integrity errors
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    
    return g


@app.get("/stats/user/{user_id}", response_model=Stats)
def getUserStats(user_id: uuid.UUID, db1: sqlite3.Connection = Depends(get_db1), db2: sqlite3.Connection = Depends(get_db2), db3: sqlite3.Connection = Depends(get_db3)):

    #establishes proper database connection to the proper database shard
    db = None
    shard_id = user_id.int % 3
    if shard_id == 0:
        db = db1
    elif shard_id == 1:
        db = db2
    else:
        db = db3

   #Lets start by getting the games data for the user
    
    selectUser = db.execute("Select * FROM games WHERE user_id = :user_id", [user_id])
    userGames = selectUser.fetchall()

    #Create a Stats object to return to the user
    testStats = Stats()

    #This variable will be used in the userGames for loop to find the most recent game
    latestGame = userGames[0][2]

    #Want to iterate over each row and come up with the stats
    for row in userGames:
        #Start with the easy stuff
        testStats.gamesPlayed += 1
        testStats.gamesWon += row[4]
        testStats.winPercentage = testStats.gamesWon / testStats.gamesPlayed

        #Check if it is a more recent game
        if row[2] > latestGame:
            latestGame = row[2]

        #Conditions for enumerating guesses
        #If the game was actually a loss, add 1 to fail
        if row[4] == 0:
            testStats.guesses.fail += 1
        #Otherwise, figure out how many guesses they got
        else:
            guesses = row[3]
            #Depending on number of guesses, add 1 to appropriate variable
            if guesses == 1:
                testStats.guesses.one += 1
            if guesses == 2:
                testStats.guesses.two += 1
            if guesses == 3:
                testStats.guesses.three += 1
            if guesses == 4:
                testStats.guesses.four += 1
            if guesses == 5:
                testStats.guesses.five += 1
            if guesses == 6:
                testStats.guesses.six += 1
    #After the for loop is finished, we can calculate the average guesses per game
    testStats.averageGuesses = ((testStats.guesses.one * 1) + (testStats.guesses.two * 2) + (testStats.guesses.three * 3) + (testStats.guesses.four * 4) + (testStats.guesses.five * 5) + (testStats.guesses.six * 6) + (testStats.guesses.fail * 6)) / testStats.gamesPlayed

    #Now all we need is streaks data
    selectStreaks = db.execute("SELECT * FROM streaks WHERE user_id = :user_id", [user_id])
    userStreaks = selectStreaks.fetchall()

    #Check through all the user's streaks
    for streak in userStreaks:
        #Find the largest streak (max streak)
        if streak[1] > testStats.maxStreak:
            testStats.maxStreak = streak[1]

        # We are going to say that the "current streak" will be determined
        # by whether or not the most recent game was played on the same date as 
        # the "end" of the most recent streak. If they are the same day,
        # we use that streak value. If there is a more recent game, then the 
        # streak is 1. Otherwise, it is 0 by default   
        if latestGame == streak[3]:
            testStats.currentStreak = streak[1]
        elif latestGame > streak[3]:
            testStats.currentStreak = 1
    
        # Unsure if we should set currentStreak to 0 if it is older than "Yesterday"
        # We can implement later if needed.

    # We return the testStats Stats object (which is not a dict) because we set the
    # response_model in the path declaration to expect a Stats object.
    # This is just a different way to do what we did in postGame()
    return testStats


@app.get("/stats/leaderboards/wins")
def getLeaderWins():
    
    r = redis.Redis(port=settings.LEADERBOARD_KEYSTORE)

    #grab the full leaderboard 
    winnerLeaders = r.zrevrangebyscore("WinnerLeaderboard", min='-inf', max='+inf', withscores=True)
    #cut it to top 10
    winnerLeaders = winnerLeaders[:10]
    #A little bit of processing. Data needs to be decoded from bytes and arranged in a list of dicts
    leaderboard = []
    for item in winnerLeaders:
        item = list(item)
        item[0] = item[0].decode("utf-8")
        leaderboard.append({"username": item[0], "wins": int(item[1])})


    return {"Top10Winners": leaderboard}


@app.get("/stats/leaderboards/streaks")
def getLeaderStreaks():
    
    r = redis.Redis(port=settings.LEADERBOARD_KEYSTORE)

    #grab the full leaderboard 
    streakLeaders = r.zrevrangebyscore("StreakLeaderboard", min='-inf', max='+inf', withscores=True)
    #cut it to top 10
    streakLeaders = streakLeaders[:10]
    #A little bit of processing. Data needs to be decoded from bytes and arranged in a list of dicts
    leaderboard = []
    for item in streakLeaders:
        item = list(item)
        item[0] = item[0].decode("utf-8")
        leaderboard.append({"username": item[0], "wins": int(item[1])})

    return {"Top10Streaks": leaderboard}