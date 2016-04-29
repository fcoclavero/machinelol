import requests
import json
import os

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

# ==================== CHALLENGER DATA ====================================

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
# Year is now a variable
year = "2015"

for region in regions:
    print("Current region: " + region)

    # Obtain request object for region challengers
    data = requests.get("https://" + region + ".api.pvp.net/api/lol/" + region
    + "/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=" + keys[0])

    # Write data to .json file
    with open("Challenger2016/" + region + "_players.json", "w+") as outfile:
        json.dump(data.json(), outfile)

    # Get ranked data for each player in the Challenger tier in the corresponding year.
    i = 1
    print("Exporting year: " + year)
    for entry in data.json()['entries']:
        playerId = entry["playerOrTeamId"]

        print(str(i) + ". " + playerId)
        i += 1

        # Checks if the directory exists and creates it if needed.
        path = os.getcwd() + "/" + "ChallengerRanked" + year + "/" + region
        if not os.path.exists(path):
            print ("Creating folder: ChallengerRanked" + year + "/" + region)
            os.makedirs(path)

        with open("ChallengerRanked" + year + "/" + region + "/" + playerId + ".json", "w+") as outfile:
            playerData = requests.get("https://" + region + ".api.pvp.net/api/lol/" + region
            + "/v1.3/stats/by-summoner/" + playerId + "/ranked?season=SEASON" + year + "&api_key=" + keys[0])

            json.dump(playerData.json(), outfile)

    print("----------------------------------------")
