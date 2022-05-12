import uuid
import httpx

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

app = FastAPI()

@app.post("/game/new")
def newGame():
    return []

@app.post("/game/{game_id}")
def newGuess():
    return []