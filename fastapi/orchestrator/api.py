from fastapi import FastAPI, Response, HTTPException, status
import httpx

app = FastAPI()

@app.post("/game/new")
def newGame(username: str):
    # TODO: call game api to create new game
    # likely require username as input
    return status.HTTP_200_OK

@app.post("/game/{game_id}")
def guessWord(guess: str):
    # TODO: bulk of work likely here
    # need to fetch game state
    # check guess against answer service
    # potentially update stats?
    return status.HTTP_200_OK