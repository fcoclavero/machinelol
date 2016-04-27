import requests
import json
import os
import sys
import time
#!/usr/bin/env python
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

#Parse the command line input parameters
##First parameter is the key
if len(sys.argv) < 3:
    region = regions[0]
    key = keys[0]
##
if sys.argv[1]=='c':
    key = keys[1]
else:
    key = keys[0]
print("Key selected: " + key)
##
if sys.argv[2]=="lan":
    region = "lan"
else:
    region = "las"
print("Current region: " + region)

########################


try:##For unexpected errors, saves the playerID in the log.
    try: # Tries to load the log to continue where it stopped before
        print("Loading log...")
        log = open("log_getNaiveID" + region + ".txt", "r")
        playerId = int(log.read())
        print(str(playerId))

    except ValueError:
        print ("The log is corrupt.")
        playerId = id_inicial

    except IOError:
        print ("Creating log...")
        playerId = id_inicial


    # The ids are proccesed
    while playerId <= 10000000:

        ## The time is saved for syncronizing with the API rate-limit.
        t0 = time.time()

        playerId += 1

        print (str(playerId) + "  ID. Making request...")

        # Checks if the saving directory exists and creates it if needed.
        path = os.getcwd() + "/" + "IdBombingSummary" + "/" + region
        if not os.path.exists(path):
            print ("Creating folder: IdBombingSummary" + "/" + region)
            os.makedirs(path)

        # Request is made.
        request = requests.get(
            "https://las.api.pvp.net/api/lol/" + region + "/v1.3/stats/by-summoner/" + str(
                playerId) + "/summary?season=SEASON2016&api_key=" +
            key)

        ## The next if's check different status codes of the request.
        if request.status_code == 200:
            print("pass")
            with open("IdBombingSummary" + "/" + region + "/" + str(playerId) + ".json", "w+") as outfile:
                    json.dump(request.json(), outfile)

        elif request.status_code == 429:
            print ("Rate Limit exceded")
            playerId -= 1
            time.sleep(60)
        elif request.status_code == 500:
            print ("Internal server error")
            playerId -= 1
        elif request.status_code == 503:
            print ("Service Unavailable")
            playerId -= 1
        elif request.status_code == 404:
            print ("Stat data not found")
        else:
            print (request.status_code)

        tf = time.time()
        dt = tf - t0
        if dt < 1200:
            ##hold until 1.2 secs; argument is in seconds, dt is in ms.
            time.sleep(1.2 - dt/1000)

    ##Here if all ids were procesed.
    print(" Saving ID in log: " + str(playerId))
    log = open("log_getNaiveID" + region + ".txt", "w")
    log.write(str(playerId))

except Exception:
    print ("Error detected: " + type(Exception).__name__)
    print(" Saving ID in log: " + str(playerId))
    log = open("log_getNaiveID" + region + ".txt", "w")
    log.write(str(playerId))

print ("Finished the region")
