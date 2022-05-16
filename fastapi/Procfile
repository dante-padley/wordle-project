word-validation: uvicorn --port $PORT api:app --app-dir=./word-validation/  --reload --reload-dir ./word-validation --root-path /api/word-validation
answer-checking: uvicorn --port $PORT api:app --app-dir=./answer-checking/ --reload --reload-dir ./answer-checking --root-path /api/answer-checking
stats: uvicorn --port $PORT api:app --app-dir=./stats/ --reload --reload-dir ./stats --root-path /api/stats
game-state: uvicorn --port $PORT api:app --app-dir=./game-state/ --reload --reload-dir ./game-state --root-path /api/game-state
game: uvicorn --port $PORT api:app --app-dir=./game/ --reload --reload-dir ./game --root-path /api/game
redis-state: redis-server --port 6380 --dir ./game-state/db --dbfilename redis-state-dump.rdb --save 60 1
redis-leaderboard: redis-server --port 6381 --dir ./game-state/db --dbfilename redis-leaderboard.rdb --save 60 1
load-balancer: ./traefik --configFile=traefik.toml