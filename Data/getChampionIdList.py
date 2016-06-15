import json

def getChampionIds():
    array = []
    dir = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data/ChampionData"
    with open("las.json") as readfile:
        try:
            data = json.load(readfile)['data']
        except IOError:
            print("Error loading json")

    for key in data:
        array.append(data[key]['id'])

    array.sort()
    return array