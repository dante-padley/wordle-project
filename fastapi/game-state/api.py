from typing import List
import uuid
import redis

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

class Settings(BaseSettings):
    GAME_STATE_KEYSTORE: int

    class Config:
        env_file = "./.env"


settings = Settings()
app = FastAPI()

@app.get("/")
async def root():
    return{"message":"What in the world?"}

@app.post("/newgame")
def newGame(user_id: uuid.UUID, game_id: int):

    r = redis.Redis(port=settings.GAME_STATE_KEYSTORE)

    game_key = "user:" + str(user_id) + ":game:" + str(game_id)

    if (r.exists(game_key) == 0):
        r.hset(game_key, "remaining", "6")
        return
    else:
        raise HTTPException(status_code=409, detail="Item already exists")


#Updating the state of a game. When a user makes a new guess for a game,
#record the guess and update the number of guesses remaining. If a user 
#tries to guess more than six times, they should receive an error
#Note: you do not need to check whether the guess is valid, if the guess 
#is correct, or report on the placement of the letters in the answer.
#This functionality was completed in project 2


@app.post("/newguess")
def newGuess(user_id: uuid.UUID, game_id: int, guess: str):
    r = redis.Redis(port=settings.GAME_STATE_KEYSTORE)
    game_key = "user:" + str(user_id) + ":game:" + str(game_id)
    if (int(r.hget(game_key, "remaining")) > 0):
        guess_number = 7 - int(r.hget(game_key, "remaining"))
        r.hset(game_key, guess_number, guess)
        r.hincrby(game_key, "remaining", -1)
        return
    else:
        raise HTTPException(status_code=400, detail="Game is finished")

#Restoring the state of a game. Upon request, the user should be able to 
#retrieve an object containing the current state of a game, including words
#guessed so far and the number of guesses remaining.
@app.get("/{user_id}/{game_id}")
def getGameState(user_id: uuid.UUID, game_id: int):
    r = redis.Redis(port = settings.GAME_STATE_KEYSTORE)
    game_key = "user:" + str(user_id) + ":game:" + str(game_id)
    if (r.exists(game_key)):
        x = r.hgetall(game_key)
        return x