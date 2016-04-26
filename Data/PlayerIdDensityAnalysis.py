
import json
import matplotlib.pyplot as plt
import numpy as np


# ==================== CHALLENGER DATA ====================================

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]

ids = []

i = 0
for region in regions:
    print("Current region: " + region)

    # Obtain region challengers
    with open("Challenger2016/"+region+"_players.json", "r") as readfile:
        data = json.load(readfile)

    # Get summary data por all players
    for entry in data['entries']:
        i += 1
        playerId = entry["playerOrTeamId"]

        ids.append(int(playerId))

print ("ids contains every player id")
print (str(i))
arr = np.asarray(ids)

plt.hist(arr, bins = 50)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
print("done")


