import json

import recomendation.constants as constants

def getChampionIds():
    array = []
    dir = constants.dataDirectory
    with open(dir + "/ChampionData/las.json") as readfile:
        try:
            data = json.load(readfile)['data']
        except IOError:
            print("Error loading json")

    for key in data:
        array.append(data[key]['id'])

    array.sort()
    return array
