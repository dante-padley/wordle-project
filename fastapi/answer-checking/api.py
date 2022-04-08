from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Goodbye World"}

@app.post("/answer/check/{word}")
def validateWord(word):
    return {"word": word}