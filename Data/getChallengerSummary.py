import requests
import json
import os

# ==================== CHALLENGER DATA ====================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["las", "na", "oce", "ru", "tr"]

for region in regions:

    # Obtain region challengers
    with open("Challenger2016/"+region+"_players.json", "r") as readfile:
        data = json.load(readfile)

    # Get summary data por all players
    i = 1

    for entry in data['entries']:
        playerId = entry["playerOrTeamId"]

        print(str(i) + ". " + playerId)
        i += 1

        # Checks if the directory exists and creates it if needed.
        path = os.getcwd() + "/" + "PlayerSummary" + "/" + region
        if not os.path.exists(path):
            print ("Creating folder: PlayerSummary" + "/" + region)
            os.makedirs(path)

        with open("PlayerSummary" + "/" + region + "/" + playerId + ".json", "w+") as outfile:
            summary = requests.get("https://las.api.pvp.net/api/lol/" + region + "/v1.3/stats/by-summoner/" + playerId + "/summary?season=SEASON2016&api_key=" + keys[0])

            json.dump(summary.json(), outfile)

    print("----------------------------------------")



