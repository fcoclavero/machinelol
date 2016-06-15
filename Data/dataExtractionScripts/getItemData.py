import json
import os
import requests

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]

for region in regions:

    items = requests.get("https://global.api.pvp.net/api/lol/static-data/"
    + region + "/v1.2/item?locale=en_US&itemListData=all&api_key="
    + keys[0])

    directory = "Items2016/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + region + ".json", "w") as outfile:
        json.dump(items.json(), outfile)
