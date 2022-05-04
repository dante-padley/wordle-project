#!/bin/bash -f

CWD=$(pwd)
echo "*/10 * * * * cd ${CWD}; python3 ./stats/db/populate_leaderboards.py" >> cronjob
crontab cronjob
rm cronjob
