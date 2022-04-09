import re
import sqlite3
import datetime
from datetime import date, datetime
from fastapi import FastAPI


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Goodbye World"}


@app.get("/answer/check/{word}")
def checkAnswer(word):
    db = sqlite3.Connection('./answer-checking/db/answers.db')

    wordleStartDate = date(2021, 6, 19)
    today = date.today()
    diff = today - wordleStartDate
    diffDays = diff.days


    cur = db.execute("SELECT * FROM answers WHERE id = ?", [diffDays])
    todaysWord = cur.fetchall()
    #print(todaysWord)
    word_array = []
    answer = todaysWord[0][1]
    print(answer)
    print(word)
    count = 0
    for x in word:
        z=0
        counter = 0
        for y in answer:
            if x == y and count == counter:
                z = 2
                break
            if x == y and count != counter:
                z = 1 
            counter += 1
        word_array.append(z)
        count += 1
    guess = {"word": word, "accuracy": word_array}
    return guess
        
@app.put("/answer/")
def updateAnswer(id: int, word: str):

    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        db = sqlite3.Connection('./answer-checking/db/answers.db')
        db.execute("UPDATE answers SET word = ? WHERE id = ?", (word, id))
        db.commit()
        return
