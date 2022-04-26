import re
import sqlite3
import contextlib

#import datetime
#from datetime import date, datetime

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings

class Settings(BaseSettings):
    database: str
    
    class Config:
        env_file = ".env"

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
    return {}

@app.get("/stats/user/{user}")
def getUserStats():
    return {}

@app.get("/stats/leaderboard/wins")
def getLeaderWins():
    return {}

@app.get("/stats/leaderboard/streaks")
def getLeaderStreaks():
    return {}
