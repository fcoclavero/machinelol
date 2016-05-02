import os
import sys
import time
import jsonrequest as jr
import logsystem as logsys

# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Things you can do with the request object:
r.status_code               # 200
r.headers['content-type']   # 'application/json; charset=utf8'
r.encoding                  # 'utf-8'
r.text                      # returns request text
r.json()                    # returns request json
print(json.dumps(r.json())) # json.dumps() returns a string with the json contents

Access parent directory (python 3.4+):

from pathlib import Path
Path('C:\Program Files').parent
'''

# ==================== NAIVE ID BOMBING ====================================
''' This data-suction attack uses an iterative id to get valid user Summaries'''

keys = ["0b808dbd-c044-43db-88a0-829dbd390aa7", "9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d"]
regions = ["lan", "las"]

id_inicial = 0

# Parse the command line input parameters
##First parameter is the key
if len(sys.argv) < 3:
    region = regions[0]
    key = keys[0]
##
else:
    if sys.argv[1] == 'c':
        key = keys[1]
    else:
        key = keys[0]

    ##
    if sys.argv[2] == "lan":
        region = "lan"
    else:
        region = "las"
print("Key selected: " + key)
print("Current region: " + region)

########################


try:  #For unexpected errors, except clause saves the playerID in the log.

    #
    logPath = "log_getNaiveID" + region + ".txt"
    log = logsys.Log(logPath)

    # If the log was correctly loaded extract the content of the log.
    if log.loaded:
        playerId = int(log.read())
        print("Loaded " + str(playerId))

    else:
        playerId = id_inicial

    # The ids are proceeded
    while playerId <= 10000000:

        ## The time is saved for syncronizing with the API rate-limit.
        t0 = time.time()

        print (str(playerId) + "  ID. Making request...")

        # Checks if the saving directory exists and creates it if needed.
        dirPath = os.getcwd() + "/" + "playerSummary" + "/" + region + "/"
        if not os.path.exists(dirPath):
            print ("Creating folder: " + dirPath)
            os.makedirs(dirPath)

        address = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.3/stats/by-summoner/" + str(
            playerId) + "/summary?season=SEASON2016&api_key="

        outfile = dirPath + str(playerId) + ".json"

        req = jr.Request(address, outfile, key)

        # If the request answer is: Internal server error, Service unavailable or Rate limit exceded
        if req.status in (429, 500, 503):
            # Re-try same playerId
            pass
        # Any other responce just pass to the next playerId (Successful or data not found)
        else:
            playerId += 1

        # Synchronization module to prevent rate-limit exceeded response
        tf = time.time()
        dt = tf - t0
        if dt < 1200:
            ##hold until 1.2 secs; argument is in seconds, dt is in ms.
            time.sleep(1.2 - dt / 1000)

        # After each request the player id is saved in the log
        log.write(str(playerId))

except Exception:
    print ("Error detected: " + type(Exception).__name__)
    print(" Saving ID in log: " + str(playerId))
    log.write(str(playerId))

print ("Finished the region")
