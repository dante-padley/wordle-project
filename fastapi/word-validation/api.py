import re
import sqlite3

from fastapi import FastAPI
from string import ascii_lowercase, punctuation

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/word/isvalid/{word}")
def validateWord(word):
    pattern = re.compile("^[\x61-\x7A]{5}$")
    if (pattern.match(word)):
        # at this point, we know the word contains 5 lowercase letters
        return{"word": word, "valid": "true"}
    return {"word": word, "valid": "false"}