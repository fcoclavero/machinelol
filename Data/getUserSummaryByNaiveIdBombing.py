import requests
import json
import os
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

# ==================== RANDOM USER DATA ====================================
''' This data-suction attack uses a Spanish Dictonary to get valid userIds'''

keys = ["0b808dbd-c044-43db-88a0-829dbd390aa7", "9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d"]
regions = ["lan", "las"]
year = "2016"

id_inicial = 0

for region in regions:
    try:##For unexpected errors, saves the playerID in the log.
        print("Current region: " + region)

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
                keys[1])

            ## The next if's check different status codes of the request.
            if request.status_code == 200:
                print("pass")
                with open("IdBombingSummary" + "/" + region + "/" + str(playerId) + ".json", "w+") as outfile:
                        json.dump(request.json(), outfile)

            elif request.status_code == 429:
                print ("Rate Limit exceded")
                break
            elif request.status_code == 500:
                print ("Internal server error")
                break
            elif request.status_code == 503:
                print ("Service Unavailable")
                break
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
        log = open("log_getNaiveID.txt", "w")
        log.write(str(playerId))
        break

    except Exception:
        print ("Error detected: " + type(Exception).__name__)
        print(" Saving ID in log: " + str(playerId))
        log = open("log_getNaiveID" + region + ".txt", "w")
        log.write(str(playerId))

    print ("Finished all regions")