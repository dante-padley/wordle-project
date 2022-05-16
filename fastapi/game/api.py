import uuid
import httpx

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

app = FastAPI()

@app.post("/new")
def newGame(username: str):
    # Okay so there are 2 basic scenarios for this
    # The user has not started today's game
    # The user has started today's game
    # If the user has not started, we need to create a new game in /game-state/newgame
    # so we would need to POST user_id and game_id to that endpoint.
    # Then we respond with today's game_id
    # {
    # "status": "new",
    # "user_id": "866e0602-23b1-4c8d-a0e9-205b0884247f",
    # "game_id": 20220424
    # }
    #
    # If the user has started, we respond with their game status
    # which is (for now) just the output from /game-state/{user_id}/{game_id}
    # We might include the "status" line for consistency and just base it off 
    # of the remaining guesses number
    url = 'http://127.0.0.1:9999/api/stats/username/' + username
    r = httpx.get(url)
    user_id = r.json()["user_id"]

    
    return []

@app.post("/{game_id}")
def newGuess():
    return []