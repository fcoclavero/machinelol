import json
import requests

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
platforms = {"br" : "BR1", "eune" : "EUN1", "euw" : "EUW1", "kr" : "KR", "lan" : "LA1",
            "las" : "LA2", "na" : "NA1", "oce" : "OC1", "ru" : "RU", "tr" : "TR1"}

for region in regions:

    with open("Challenger2016/"+region+"/"+region+"_players.json", "r") as readfile:
        data = json.load(readfile)

    for entry in data['entries']:

        playerId = entry["playerOrTeamId"]
        print(playerId)

        masteries = requests.get("https://" + region + ".api.pvp.net/championmastery/location/" + platforms[region]
        + "/player/" + playerId + "/champions?api_key=" + keys[0])

        with open("Data/ChallengerMasteries2016/" + region + "/" + playerId + ".json", "w") as outfile:
            json.dump(masteries.json(), outfile)
