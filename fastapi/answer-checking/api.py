from fastapi import FastAPI
app = FastAPI()

import fileinput
word_dictionary = []
for line in fileinput.input():
    word_dictionary.append(line)
print(word_dictionary)

@app.get("/")
async def root():
    return {"message": "Goodbye World"}

@app.post("/answer/check/{word}")
def validateWord(word):
    return {"word": word}