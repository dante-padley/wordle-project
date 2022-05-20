import uuid
import httpx

from datetime import date
from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

class Settings(BaseSettings):
    STARTDATE: str

    class Config:
        env_file = "./.env"

settings = Settings()
app = FastAPI()

@app.post("/new")
def newGame(username: str):
    # Okay so there are 2 basic scenarios for this
    # The user has not started today's game
    # The user has started today's game
    # If the user has not started, we need to create a new game in /game-state/newgame
    # so we would need to POST user_id and game_id to that endpoint.
    # Then we respond with today's game_id
    # {
    # "status": "new",
    # "user_id": "866e0602-23b1-4c8d-a0e9-205b0884247f",
    # "game_id": 20220424
    # }
    #
    # If the user has started, we respond with their game status
    # which is (for now) just the output from /game-state/{user_id}/{game_id}
    # We might include the "status" line for consistency and just base it off
    # of the remaining guesses number

    # Start off by getting the user's id
    url = 'http://127.0.0.1:9999/api/stats/username/' + username
    r = httpx.get(url)
    user_id = r.json()["user_id"]

    # This is our calculation for today's wordle number and game_id.
    # Ideally this would be in a module of its own and included at the top
    wordleStartDate = date.fromisoformat(settings.STARTDATE)
    today = date.today()
    diff = today - wordleStartDate
    game_id = diff.days

    # Try to create a new game
    newgameurl = 'http://127.0.0.1:9999/api/game-state/newgame'
    params = {"user_id": user_id, "game_id": game_id}
    s = httpx.post(newgameurl, params=params)

    # If successful, return the basic status and the user/game id
    if (s.status_code == httpx.codes.OK):
        responseObj = {"status": "new"}
        responseObj.update(params)
        return responseObj
    # If the game already exists, need to return an object that communicates game state
    # Following the professor's examples in the project requirements doc for structure of the response
    elif (s.status_code == 409):
        # First need to get the game state. Also initializing the response object here
        responseObj = {"status": "in-progress"}
        gamestatusurl = 'http://127.0.0.1:9999/api/game-state/' + str(user_id) + '/' + str(game_id)
        t = httpx.get(gamestatusurl)

        # Add the user_id, game_id, and remaining guesses count to response
        responseObj.update(params)
        responseObj.update({"remaining": t.json()["remaining"]})

        # Populate the guesses object with the guesses from game state.
        # The game state will only have 1 member if no guesses have been made.
        # So we check if it is longer than 1
        guesses = []
        if (len(t.json()) > 1):
            for i in range(1, len(t.json())):
                guesses.append(t.json()[str(i)])
        # Add to the response
        responseObj.update({"guesses": guesses})

        # To match professor's requirements, need to create this letters {correct, present} thing
        # Basically, if there are guesses, check the accuracy of the most recent(last) guess.
        # that is a list of 5 values of either 0 (incorrect), 1 (present), or 2 (correct).
        # For each letter in the word, append it to the appropriate list or none if incorrect
        letters = {"correct": [], "present": []}
        if (guesses):
            lastguess = guesses[-1]
            checkanswerurl = 'http://127.0.0.1:9999/api/answer-checking/answer/check/' + lastguess
            u = httpx.get(checkanswerurl)
            print(u.json())
            for i in range(0, 5):
                letterscore = u.json()["accuracy"][i]
                if (letterscore == 1):
                    letters["present"].append(lastguess[i])
                if (letterscore == 2):
                    letters["correct"].append(lastguess[i])
        #toss it on the response object
        responseObj.update({"letters": letters})
        #done
        return responseObj

@app.post("/{game_id}")
async def newGuess(game_id: int, guess: str, user_id: str):
    wordvalidateurl = 'http://127.0.0.1:9999/api/word-validation/word/isvalid/' + guess

    #validate word
    u = httpx.get(wordvalidateurl)
    isValid = u.json()['valid'] == 'true'


    #get how many guesses remains in games
    url = 'http://127.0.0.1:9999/api/game-state/' + str(user_id) + '/' + str(game_id)
    r = httpx.get(url)
    guesses = r.json()

    #Record the guess and update the number of guesses remaining
    if int(guesses['remaining']) > 0 and isValid:
        updatedGuesses = int(guesses['remaining']) - 1
        url = 'http://127.0.0.1:9999/api/game-state/newguess'
        params = {"user_id": user_id, "game_id": game_id, "guess": guess}
        r = httpx.post(url, params=params)

        responseObj = {"remaining": updatedGuesses}

        #Check to see if the guess is correct
        if (r.status_code == httpx.codes.OK):
            checkanswerurl = 'http://127.0.0.1:9999/api/answer-checking/answer/check/' + guess
            u = httpx.get(checkanswerurl)
            letters = {"correct": [], "present": []}

            for i in range(0, 5):
                letterscore = u.json()["accuracy"][i]
                if (letterscore == 1):
                    letters["present"].append(guess[i])
                if (letterscore == 2):
                    letters["correct"].append(guess[i])

            #Record the win
            #Return the user’s score
            if len(letters['correct']) == 5:
                 #Record the win 

                recordwinurl = 'http://127.0.0.1:9999/api/stats/' 

                guesses = 6 - updatedGuesses 

                params = {"user_id": user_id, "game_id": game_id, "finished": str(date.today()), "guesses": guesses, "won": "true"} 

                async with httpx.AsyncClient() as client:
                    s = await client.post(recordwinurl, json=params) 
                    print(s.text)

                responseObj.update({"status": "win", "remaining": updatedGuesses}) 

                #Return users score 

                scoreurl = 'http://127.0.0.1:9999/api/stats/user/' + user_id 

                scores = httpx.get(scoreurl) 

                responseObj.update(scores.json()) 

                return responseObj 
                #return "correct"

            #If the guess is incorrect and no guesses remain…
            elif len(letters['correct']) < 5 and updatedGuesses == 0:
                recordlossurl = 'http://127.0.0.1:9999/api/stats/'
                guesses = updatedGuesses
                params = {"user_id": user_id, "game_id": game_id, "finished": str(date.today()), "guesses": guesses, "won": "false"}

                async with httpx.AsyncClient() as client:
                    s = await client.post(recordlossurl, json=params) 

                responseObj.update({"status": "loss", "remaining": updatedGuesses})  

                #Return users score
                scoreurl = 'http://127.0.0.1:9999/api/stats/user/' + user_id

                scores = httpx.get(scoreurl)

                responseObj.update(scores.json())

                return responseObj

            #If the guess is incorrect and additional guesses remain
            else:
                responseObj.update({"status": "incorrect", "letters": letters})
                return responseObj

    return "Sorry you reached the max number of guesses"
