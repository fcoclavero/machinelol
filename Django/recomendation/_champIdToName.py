import json

''' ChampionData json contains {data: {champname1: {id: xx, ...}, ...}}'''
class idToName:
    def __init__(self, dataDirectory, region = "las"):
        dir = dataDirectory + "/ChampionData/"  # region's directory
        fileDir = region + ".json"

        with open(dir + fileDir, "r") as readfile:
            self.champData = json.load(readfile)['data']

        self.idDict = {}
        for key in self.champData:
            id = self.champData[key]['id']
            self.idDict[id] = key

    def convert(self, element):
        if isinstance(element, list):
            outList = []
            for atom in element:
                if isinstance(atom, int):
                    outList.append(self.idDict[atom])
                else:
                    raise ValueError
            return outList

        elif isinstance(element, int):
            return self.idDict[element]

        else:
            print (type(element))
            raise ValueError