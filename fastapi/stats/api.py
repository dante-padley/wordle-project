import re
import sqlite3
import contextlib
from typing import Dict

#import datetime
#from datetime import date, datetime

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

class Settings(BaseSettings):
    database: str
    
    class Config:
        env_file = "./stats/.env"

class Scores(BaseModel):
    one: int = Field(alias="1", default=0)
    two: int = Field(alias="2", default=0)
    three: int = Field(alias="3", default=0)
    four: int = Field(alias="4", default=0)
    five: int = Field(alias="5", default=0)
    six: int = Field(alias="6", default=0)
    fail: int = 0

class Stats(BaseModel):
    currentStreak: int = 0
    maxStreak: int = 0
    guesses: Scores = Scores()
    winPercentage: float = 0
    gamesPlayed: int = 0
    gamesWon: int = 0
    averageGuesses: float = 0
    
def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db

settings = Settings()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "What a world!"}

@app.post("/stats/{game}")
def postGame():
    #NEEDS:
    #a model for a "game" submission with a proper date type exactly like whats in DB
    #a simple db execute and commit line that nicely places the game object members
    #    into the DB
    return {}

@app.get("/stats/user/{user_id}", response_model=Stats)
def getUserStats(user_id, db: sqlite3.Connection = Depends(get_db)):
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

    return testStats

@app.get("/stats/leaderboards/wins")
def getLeaderWins(db: sqlite3.Connection = Depends(get_db)):
    #Select the top 10 winners according to wins in the wins view
    selectWinners = db.execute("SELECT * FROM wins ORDER BY wins DESC LIMIT 10")
    
    #Throw them all in a list
    topWins = selectWinners.fetchall()
    #To assemble the leaderboard, here's a list
    leaderboard = []

    #iterate through the top winners and grab their usernames
    for winner in topWins:
        #select current user's username
        selectUser = db.execute("SELECT username FROM users WHERE user_id = :user_id", [winner[0]])
        userRow = selectUser.fetchall()
        #assemble the object
        user = {"username": userRow[0][0], "wins": winner[1]}
        #toss it in the leaderboard
        leaderboard.append(user)

    return {"Top10Winners": leaderboard}

@app.get("/stats/leaderboards/streaks")
def getLeaderStreaks(db: sqlite3.Connection = Depends(get_db)):
    #Select the top 10 winners according to wins in the wins view
    selectStreaks = db.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10")
    
    #Throw the all in a list
    topStreaks = selectStreaks.fetchall()
    #To assemble the leaderboard, here's a list
    leaderboard = []

    #iterate through the top winners and grab their usernames
    for streak in topStreaks:
        #select current user's username
        selectUser = db.execute("SELECT username FROM users WHERE user_id = :user_id", [streak[0]])
        userRow = selectUser.fetchall()
        #assemble the object
        user = {"username": userRow[0][0], "streak": streak[1]}
        #toss it in the leaderboard
        leaderboard.append(user)
        
    return {"Top10Winners": leaderboard}
