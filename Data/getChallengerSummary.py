import requests
import json

# ==================== CHALLENGER DATA ====================================

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]

for region in regions:
    print("Current region: " + region)

    # Obtain region challengers
    with open("Challenger2016/"+region+"/"+region+"_players.json", "r") as readfile:
        data = json.load(readfile)

    # Get summary data por all players
    i = 1
    for entry in data['entries']:
        playerId = entry["playerOrTeamId"]

        summary = requests.get("https://las.api.pvp.net/api/lol/" + region + "/v1.3/stats/by-summoner/" + playerId + "/summary?season=SEASON2016&")

    print("----------------------------------------")
