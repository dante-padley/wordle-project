# wordle-project
## Dante Padley, Jay Patel, Robin Khiv, Rohan Patwardhan

### API browser endpoints

The project serves to 127.0.0.1:9999

All services live in the 127.0.0.1:9999/api path

The entire list of services:
- /answer-checking
- /word-validation
- /stats
- /game-state
- /game

**To test the apis in the browser, go to the desired endpoint and add /docs (i.e. 127.0.0.1:9999/api/game/docs)**

### PROJECT 5

No setup needed for this project. The newest service is /game.

Refer to Project 4 Execution for execution instructions.

### PROJECT 4 INITIALIZATION

Cron job setup (only do this after following the project 3 initialization):

Navigate to the fastapi director

`cd ./fastapi`

Run the cronjob setup script

`sh ./cron-scheduler.sh`

### PROJECT 4 EXECUTION

Navigate to the fastapi directory

`cd ./fastapi`

Run foreman exactly like this:

`foreman start --formation all=1,stats=3`

### PROJECT 3 INITIALIZATION

Database setup:

Navigate to the stats service db directory

`cd ./fastapi/stats/db/`

Create the base db

`python3 stats.py`

Shard the db

`python3 sharding_script.py`



### PROJECT 2 INITIALIZATION

Initialization
To get the list of wordle answers, run the following:

`curl --silent https://www.nytimes.com/games/wordle/main.bfba912f.js |
sed -e 's/^.*var Ma=//' -e 's/,Oa=.*$//' -e 1q > ./fastapi/answer-checking/answers.json`

To initialize the answers db, navigate to the /fastapi/answer-checking and run the following:
```
mkdir db
cd db
sqlite3 answers.db
CREATE TABLE answers(id INTEGER PRIMARY KEY, word TEXT)
.quit
```

To initialize the answers db, navigate to the /fastapi/word-validation and run the following:

```
mkdir db
cd db
sqlite3 words.db
CREATE TABLE words(word TEXT)
.quit
```

To populate the answers db, navigate to /fastapi/answer-checking and run the populatedb.py script:

`python3 ./populatedb.py`


To get the dictionary from linux and trim it down to only valid words for wordle, navigate to ./fastapi/word-validation and run the command:
source 

`sh ./script.sh`

To populate the words db, run the script:

`python3 ./populatewords.py`




