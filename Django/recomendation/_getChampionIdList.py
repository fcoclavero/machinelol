import json

def getChampionIds():
    array = []
    dir = "C:/Users/fcocl_000/Documents/Data/ChampionData"
    with open(dir + "/las.json") as readfile:
        try:
            data = json.load(readfile)['data']
        except IOError:
            print("Error loading json")

    for key in data:
        array.append(data[key]['id'])

    array.sort()
    return array
