import requests
import json

'''
Things you can do with the request object:
r.status_code               # 200
r.headers['content-type']   # 'application/json; charset=utf8'
r.encoding                  # 'utf-8'
r.text                      # returns request text
r.json()                    # returns request json
print(json.dumps(r.json())) # json.dumps() returns a string with the json contents
'''

# ==================== CHALLENGER DATA ====================================

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]

for region in regions:
    print("Current region: " + region)

    # Obtain request object for region challengers
    data = requests.get("https://" + region + ".api.pvp.net/api/lol/" + region
    + "/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=" + keys[0])

    # Write data to .json file
    with open("Data/Challenger2016/" + region + "/" + region + "_players.json", "w") as outfile:
        json.dump(data.json(), outfile)

    # Get data por all players
    i = 1
    for entry in data.json()['entries']:
        playerId = entry["playerOrTeamId"]

        print(str(i) + ". " + playerId)
        i += 1

        with open("Data/Challenger2016/" + region + "/" + playerId + ".json", "w") as outfile:
            playerData = requests.get("https://" + region + ".api.pvp.net/api/lol/" + region
            + "/v1.3/stats/by-summoner/" + playerId + "/ranked?season=SEASON2016&api_key=" + keys[0])

            json.dump(playerData.json(), outfile)

    print("----------------------------------------")
