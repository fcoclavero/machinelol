import requests, json

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]

def getId(summonerName, region):
    data = requests.get("https://las.api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + keys[0])

    # TODO: manage name not found
    return data.json()[summonerName]['id']
