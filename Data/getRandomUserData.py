import requests
import json
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

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["lan", "las"]
year = "2016"

#Tries to load the log to continue where it stopped
try:
    log = open("log_getRandomUserData.txt", "r+")
    currentLine = int(log.read())

except ValueError:
    print ("The log is corrupt.")
    print ("Creating log...")
    log = open("log_getRandomUserData.txt", "w+")
    currentLine = 0

except IOError:
    print ("Creating log...")
    log = open("log_getRandomUserData.txt", "w+")
    currentLine = 0

currentLine = 8250

#Load spanish word dictionary
dictFile = open("dict.txt", "r+")
dict = dictFile.readlines()
dictLen = len(dict)
print("dictLen" + str(dictLen))


for region in regions:
    print("Current region: " + region)

    # The dictionary is proccesed
    while dictLen >= currentLine:

        # Each query allows up to 40 usernames at once.
        usernames = ""
        for i in range(0,40):
            if i == 39:
                usernames += dict[currentLine + i].rstrip("\n")
            else:
                usernames += dict[currentLine + i] + ","
        currentLine += 40

        print ("Users selected. Making request")

        # Obtain request object for region usernames
        data = requests.get("https://" + region + ".api.pvp.net/api/lol/" + region
        + "/v1.4/summoner/by-name/" + usernames + "?api_key=" + keys[0])
        print ("Request recieved")

        # Formats the interval of words checked
        ran = "[" + str(currentLine-40) +"," + str(currentLine) + "]"
        print(ran)

        # Write data to .json file
        with open("RandomUsers/" + region + "_" + ran + "players.json", "w+") as outfile:
            json.dump(data.json(), outfile)

        # The log is overwritten
        log = open("log_getRandomUserData.txt", "w")
        log.write(str(currentLine))
