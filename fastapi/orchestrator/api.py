from fastapi import FastAPI, Response, HTTPException, status
import httpx

app = FastAPI()

@app.post("/game/new")
def newGame(username: str):
    # TODO: call game api to create new game
    # Find User ID for username
    # Choose a new game ID for the user to play and return
    return status.HTTP_200_OK

@app.post("/game/{game_id}")
def guessWord(guess: str):
    # TODO: bulk of work likely here
    # 1. verify guess with word validation service
    # 2. check that user has guesses remaining (get game state)
    # if 1 and 2 are true
    # 3. Record the guess and update number of guesses remaining
    # 4. Check to see if guess correct

    # if guess correct
        # record the win
        # return the user's score
    
    # if guess is incorrect and no guesses remain
        # record the loss
        # return the user's score
    
    # if guess is incorrect and additional guesses remain
        # return which letters are included in the word
        # and which are correctly placed

    return status.HTTP_200_OK