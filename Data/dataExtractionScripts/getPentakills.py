import json

playerId = str(1097326)
region = "kr"

with open("Challenger2016/" + region + "/" + playerId + ".json", "r") as readfile:
    data = json.load(readfile)

pentakills = 0
for champion in data["champions"]:
    pentakills += champion["stats"]["totalPentaKills"]

print(pentakills)
