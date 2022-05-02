#!/usr/bin/env python3

import contextlib
import sqlite3
import uuid
from xml.dom.minidom import TypeInfo


sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

OLD_DB = './stats.db'
USER_DB = './users.db'
GAME_DB1 = './games1.db'
GAME_DB2 = './games2.db'
GAME_DB3 = './games3.db'
USER_SCHEMA = './user_schema.sql'
GAME_SCHEMA = './game_schema.sql'

xferlist_users = []
xferlist_games1 = []
xferlist_games2 = []
xferlist_games3 = []

# open a connection to a brand new db for users and three for games
with contextlib.closing(sqlite3.connect(USER_DB, detect_types=sqlite3.PARSE_DECLTYPES)) as db:
    # open and execute the schema file onto the new db
    with open(USER_SCHEMA) as f:
        db.executescript(f.read())
    # ...
    with contextlib.closing(sqlite3.connect(GAME_DB1, detect_types=sqlite3.PARSE_DECLTYPES)) as dbg1:
        with open(GAME_SCHEMA) as g:
            dbg1.executescript(g.read())
        
        with contextlib.closing(sqlite3.connect(GAME_DB2, detect_types=sqlite3.PARSE_DECLTYPES)) as dbg2:
            with open(GAME_SCHEMA) as h:
                dbg2.executescript(h.read())

            with contextlib.closing(sqlite3.connect(GAME_DB3, detect_types=sqlite3.PARSE_DECLTYPES)) as dbg3:
                with open(GAME_SCHEMA) as j:
                    dbg3.executescript(j.read())

                #connect to the un-sharded db and just run a select on the whole users table
                with contextlib.closing(sqlite3.connect(OLD_DB)) as olddb:
                    selectstmt = olddb.execute("""
                        SELECT * FROM users;
                    """)
                    #in the loop below, this will hold 1000 records at a time from the select statement
                    rowcur = None
                    #for testing purposes
                    i = 1
                    #if you run fetchmany(size=x) and there are no results left, it returns [], so that will be our exit condition
                    while rowcur != []:
                        #grab a batch of users
                        rowcur = selectstmt.fetchmany(size=1000)
                        print("Fetch " + str(i))
                        #iterate through the batch
                        for row in rowcur:
                            
                            
                            #construct the dict we want to insert later and append it to our list
                            rowdata = {"user_id": uuid.uuid4(), "username": row[1]}
                            #need to use the old user id to find the user's games
                            old_user_id = row[0]
                            #select the user's games 
                            rowgamestmt = olddb.execute("""
                                SELECT * FROM games WHERE user_id = ?;
                            """, [old_user_id])
                            rowgames = rowgamestmt.fetchall()
                            #aggregate for our game dicts
                            gamedatalist = []

                            #assemble our list of games for this user
                            for game in rowgames:
                                gamedata = {"user_id": rowdata['user_id'], "game_id": game[1], "finished": game[2], "guesses": game[3], "won": game[4]}
                                gamedatalist.append(gamedata)
                            
                            #decide the shard list the games go in
                            #then add the list of games to the insert list
                            if (rowdata['user_id'].int % 3) == 0:
                                xferlist_games1.extend(gamedatalist)
                            elif (rowdata['user_id'].int % 3) == 1:
                                xferlist_games2.extend(gamedatalist)
                            elif (rowdata['user_id'].int % 3) == 2:
                                xferlist_games3.extend(gamedatalist)

                            #add the user to the users insert list
                            xferlist_users.append(rowdata)

                            

                            i += 1
                        #this will fire once every 1000 user records. not sure what the optimal number is, but this works fine
                        db.executemany("""
                            INSERT INTO users(user_id, username) VALUES(:user_id, :username)
                        """, xferlist_users)
                        dbg1.executemany("""
                            INSERT INTO games(user_id, game_id, finished, guesses, won) VALUES(:user_id, :game_id, :finished, :guesses, :won)
                        """, xferlist_games1)
                        dbg2.executemany("""
                            INSERT INTO games(user_id, game_id, finished, guesses, won) VALUES(:user_id, :game_id, :finished, :guesses, :won)
                        """, xferlist_games2)
                        dbg3.executemany("""
                            INSERT INTO games(user_id, game_id, finished, guesses, won) VALUES(:user_id, :game_id, :finished, :guesses, :won)
                        """, xferlist_games3)
                        #be sure to clear the lists!!!
                        xferlist_users.clear()
                        xferlist_games1.clear()
                        xferlist_games2.clear()
                        xferlist_games3.clear()
                        
                #commit after all is said and done
                db.commit()
                dbg1.commit()
                dbg2.commit()
                dbg3.commit()
