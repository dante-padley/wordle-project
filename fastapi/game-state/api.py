from typing import List
import uuid

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

class Settings(BaseSettings):
    DATABASE: str

    class Config:
        env_file = "./game-state/.env"

#Need to write this GameState object once we design the database
class GameState(BaseModel):
    guesses: list

settings = Settings()
app = FastAPI()

#Starting a new game. The client should supply a user ID and game ID
#when a game starts. If the user has already played the game, they should receive an error
#Starting a game sounds like POST to me. They want to add something new to the db
@app.post("/game-state/newgame")
def newGame(user_id: uuid.UUID, game_id: int):
    return []

#Updating the state of a game. When a user makes a new guess for a game,
#record the guess and update the number of guesses remaining. If a user 
#tries to guess more than six times, they should receive an error
#Note: you do not need to check whether the guess is valid, if the guess 
#is correct, or report on the placement of the letters in the answer.
#This functionality was completed in project 2
@app.post("/game-state/newguess")
def newGuess(user_id: uuid.UUID, game_id: int, guess: str):
    return []

#Restoring the state of a game. Upon request, the user should be able to 
#retrieve an object containing the current state of a game, including words
#guessed so far and the number of guesses remaining.
@app.get("/game-state/{user_id}/{game_id}")
def getGameState(user_id: uuid.UUID, game_id: int):
    return []