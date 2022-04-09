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
        #db.execute("CREATE TABLE IF NOT EXISTS words (id INT PRIMARY KEY, word TEXT NOT NULL)")
        cur = db.cursor()
        cur.execute("SELECT * FROM words WHERE word = ?", [word])
        # f = open("./word-validation/dictionary.txt", "r")
        # y = f.read().split("\n")
        # f.close()
        # for x in y:
        #     db.execute('INSERT INTO words(word) VALUES(?)', [x])
        
        print(cur.arraysize)
        dbWords = cur.fetchall()
        print(dbWords)
        if len(dbWords) == 0:
            return{"word": word, "valid": "false"}
        
        return{"word": word, "valid": "true"}

    #     f = open("./word-validation/dictionary.txt", "r")
    #     words = []
    #     words = f.read().split("\n")
    #     if word in words:
    #     # at this point, we know the word contains 5 lowercase letters
    #         return {"word": word, "valid": "true"}
    # return {"word": word, "valid": "false"}

@app.post("/word/add/")
def addWord(word: str):

    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./word-validation/db/words.db')
        #db.execute("CREATE TABLE IF NOT EXISTS words (id INT PRIMARY KEY, word TEXT NOT NULL)")
        cur = db.cursor()
        cur.execute("INSERT INTO words(word) VALUES(?)", [word])
        db.commit()
        return 

@app.delete("/word/delete/")
def deleteWord(word:str):
    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./word-validation/db/words.db')
        #db.execute("CREATE TABLE IF NOT EXISTS words (id INT PRIMARY KEY, word TEXT NOT NULL)")
        cur = db.cursor()
        cur.execute("DELETE FROM words WHERE word = ?", [word])
        db.commit()
        return 

# import os
# @app.get("/word2/isvalid/{word}")
# def validateWord2(word):
    
#     pattern = re.compile("^[\x61-\x7A]{5}$")
#     if (pattern.match(word)):
#         db = sqlite3.Connection("./word-validation/db/words.db")
#         db.execute("CREATE TABLE IF NOT EXISTS words2 (id INT PRIMARY KEY, word TEXT NOT NULL)")
#         stream = os.popen("cat /usr/share/dict/words | grep -P  '^[\x61-\x7A]{5}$'")
#         print("king king")
#         print(stream)
        
#     return True