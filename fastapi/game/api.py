from os import stat_result
from datetime import date as d
import httpx

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings, Field

app = FastAPI()

@app.get("/")
def index():
    return "in game"

@app.post("/game/new")
def newGame(username):
    stats_url = 'http://localhost:9999/api/stats/username/' + username
    res = httpx.get(stats_url)
    user_id = res.json()["user_id"]
    print(user_id)
    
    
    # This is our calculation for today's wordle number and game_id.
    # Ideally this would be in a module of its own and included at the top
    default_start_date = d(2022, 5, 5)
    today = d.today()
    date_idx = (today - default_start_date).days
    
    newgame_url = 'http://localhost:9999/api/game-state/game-state/newgame'
    params = {"user_id": user_id, "game_id": date_idx}
    gamestate_res = httpx.post(newgame_url, params=params)
    print(params)
    # Users have not started the game today
    if (gamestate_res.status_code == 200):
        res = {"status:": "welcome"}
        res.update(params)
        return res
    
    # Populate guess if the users already existsed
    elif (gamestate_res.status_code == 409):
        res = {"status:": "playing"}
        
        game_status_url = "http://localhost:9999/api/game-state/game-state/" + str(user_id) + "/" + str(date_idx)
        t = httpx.get(game_status_url)
        res.update(params)
        res.update({"remain: " : t.json()["remaining"]})
        
        guesses = []
        if (len(t.json()) > 1):
            for i in range(1, len(t.json())):
                guesses.append(t.json()[str(i)])
        # Add to the response
        res.update({"guesses": guesses})

        # To match professor's requirements, need to create this letters {correct, present} thing
        # Basically, if there are guesses, check the accuracy of the most recent(last) guess.
        # that is a list of 5 values of either 0 (incorrect), 1 (present), or 2 (correct).
        # For each letter in the word, append it to the appropriate list or none if incorrect
        letters = {"correct": [], "present": []}
        if (guesses):
            lastguess = guesses[-1]
            check_answerurl = 'http://localhost:9999/api/answer-checking/answer/check/reach' + lastguess
            u = httpx.get(check_answerurl)
            print(u.json())
            for i in range(0, 5):
                letterscore = u.json()["accuracy"][i]
                if (letterscore == 1):
                    letters["present"].append(lastguess[i])
                if (letterscore == 2):
                    letters["correct"].append(lastguess[i])
        #toss it on the response object
        res.update({"letters": letters})
        #done
        return res
    
    # return NOW only for testing
    return "passed"

@app.post("/game/{game_id}")
def newGuess(game_id: int, guess: str, user_id: str):
    word_validateurl = 'http://127.0.0.1:9999/api/word-validation/word/isvalid/' + guess

    #make sure that the word is in the word dict
    v = httpx.get(word_validateurl)
    isValid = v.json()['valid'] == 'true'

    #check the number of remaining guess
    url = "http://localhost:9999/api/game-state/game-state/" + str(user_id) + "/" + str(game_id)
    g = httpx.get(url)
    guesses = g.json()

    #Record the guess and update the number of guesses
    if int(guesses['remaining']) > 0 and isValid:
        updated_guesses = int(guesses['remaining']) - 1
        url = 'http://127.0.0.1:9999/api/game-state/game-state/newguess'
        params = {"user_id": user_id, "game_id": game_id, "guess": guess}
        r = httpx.post(url, params=params)
        res = {"remaining": updated_guesses}
        #If the guess is correct
        if (r.status_code == httpx.codes.OK):
            check_answerurl = 'http://127.0.0.1:9999/api/answer-checking/answer/check/' + guess
            u = httpx.get(check_answerurl)
            letters = {"correct": [], "present": []}
            for i in range(0, 5):
                letterscore = u.json()["accuracy"][i]
                if (letterscore == 1):
                    letters["present"].append(guess[i])
                if (letterscore == 2):
                    letters["correct"].append(guess[i])
            # User got all 5 letters
            if len(letters['correct']) == 5:
                win_url = 'http://127.0.0.1:9999/api/stats/stats/' 
                guesses = 6 - updated_guesses 
                params = {"user_id": user_id, "game_id": game_id, "finished": d.today(), "guesses": guesses, "won": True} 
                s = httpx.post(win_url, params=params) 
                res.update({"status": "win", "remaining": updated_guesses}) 
                # Get their xcore
                scoreurl = 'http://localhost:9999/api/stats/stats/user/' + user_id 
                scores = httpx.get(scoreurl) 
                res.update(scores.json()) 
                return res 
            #Out of guesses
            elif len(letters['correct']) < 5 and updated_guesses == 0:
                return "wrong"
            else:
                res.update({"status": "incorrect", "letters": letters})
                return res
    return "You are out of guesses"
