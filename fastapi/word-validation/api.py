import re
import sqlite3
import json

from fastapi import FastAPI, Depends, Response, HTTPException, status
from string import ascii_lowercase, punctuation

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/word/isvalid/{word}")
def validateWord(word):
    
    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./word-validation/db/words.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM words WHERE word = ?", [word])
        
        print(cur.arraysize)
        dbWords = cur.fetchall()
        print(dbWords)
        if len(dbWords) == 0:
            return{"word": word, "valid": "false"}
        
        return{"word": word, "valid": "true"}

@app.post("/word/add/")
def addWord(word: str):

    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./word-validation/db/words.db')
        cur = db.cursor()
        cur.execute("INSERT INTO words(word) VALUES(?)", [word])
        db.commit()
        return 

@app.delete("/word/delete/")
def deleteWord(word:str):
    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./word-validation/db/words.db')
        cur = db.cursor()
        cur.execute("DELETE FROM words WHERE word = ?", [word])
        db.commit()
        return 