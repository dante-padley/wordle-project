from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/word/isvalid/{word}")
def validateWord(word):
    return {"word": word}