import numpy as np
import json
import os

class DataParser:

    def __init__(self, regions, dataDirectory, dataSize):
        self.regions = regions
        self.dataDirectory = dataDirectory
        self.dataSize = dataSize

    characteristics = ["totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]

    def parseSummary(self):
        array = []

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerSummary/" + region + "/"    # region's directory

            i = 0
            for fileDir in os.listdir(dir):
                if (i > self.dataSize): break

                # for every file in the directory
                with open(dir + fileDir, "r") as readfile:            # open file
                    # load data onto dict
                    try:
                        data = json.load(readfile)['playerStatSummaries']
                    except:
                        continue


                # Check if file contains match data
                normalIndex = self.typeIndex(data, "Unranked")
                rankedIndex = self.typeIndex(data, "RankedSolo5x5")
                if normalIndex is None or rankedIndex is None:
                    continue

                # Transfer data from dict to np array
                aux = []

                try:
                    aux.append(data[normalIndex]['wins'] + data[rankedIndex]['wins'])
                    #aux.append(data[rankedIndex]['losses'])

                    aux.append(data[normalIndex]["aggregatedStats"][self.characteristics[2]] + data[rankedIndex]["aggregatedStats"][self.characteristics[2]])

                    for j in range(2, len(self.characteristics)):
                        aux.append(data[normalIndex]["aggregatedStats"][self.characteristics[j]] + data[rankedIndex]["aggregatedStats"][self.characteristics[j]])
                except:
                    continue

                array.append(aux)
                i += 1

        return(array)

    def typeIndex(self, data, type):
        for i in range(len(data)):
            if data[i]["playerStatSummaryType"] == type:
                return i
