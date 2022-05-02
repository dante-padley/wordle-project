# wordle-project
## Nathan Eduvala, Marcellus Jones, Hoang Long Nguyen, Dante Padley

# Project 3 Responsibilites
1. Creating Initial service with single db
- Dante Padley
2. Sharding and service modifications
- Nathan Eduvala
- Hoang Long Nguyen
- Dante Padley
3. Load balancing
- Marcellus

### PROJECT 3 INITIALIZATION






1. Initialization
To get the list of wordle answers, run the following:

`curl --silent https://www.nytimes.com/games/wordle/main.bfba912f.js |
sed -e 's/^.*var Ma=//' -e 's/,Oa=.*$//' -e 1q > ./fastapi/answer-checking/answers.json`

To initialize the answers db, navigate to the /fastapi/answer-checking and run the following:
`mkdir db
cd db
sqlite3 answers.db
CREATE TABLE answers(id INTEGER PRIMARY KEY, word TEXT)
.quit`

To initialize the answers db, navigate to the /fastapi/word-validation and run the following:

`mkdir db
cd db
sqlite3 words.db
CREATE TABLE words(word TEXT)
.quit
`

To populate the answers db, run the /fastapi/answer-checking/
populatedb.py script:

`python3 ./fastapi/answer-checking/populatedb.py`

To get the dictionary from linux and trim it down to only valid words for wordle, run the command:
source 

`./fastapi/word-validation/script.sh`

To populate the words db, run the 

`/fastapi/word-validation/populatewords.py`

script:

`python3 ./fastapi/word-validation/populatewords.py`



2. Execution
To start the services, run the following foreman command in the fastapi directory:

`foreman start --formation all=1,stats=3`