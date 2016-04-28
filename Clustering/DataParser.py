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
        array = np.zeros(shape=(len(self.characteristics) + 3, self.dataSize))

        i = 0                                                         # user index
        for region in self.regions:
            dir = self.dataDirectory + "/PlayerSummary/" + region + "/"    # region's directory
            for fileDir in os.listdir(dir):                           # for every file in the directory
                with open(dir + fileDir, "r") as readfile:            # open file
                    # load data onto dict
                    try:
                        data = json.load(readfile)['playerStatSummaries']
                    except:
                        continue


                normalIndex = self.typeIndex(data, "Unranked")
                rankedIndex = self.typeIndex(data, "RankedSolo5x5")
                if normalIndex is None or rankedIndex is None:
                    continue

                # Transfer data from dict to np array
                array[1][i] = data[normalIndex]['wins'] + data[rankedIndex]['wins']
                array[2][i] = data[rankedIndex]['losses']
                array[0][i] = array[1][i] + array[2][i] # total ranked and unranked games

                for j in range(2, len(self.characteristics)):
                    array[j][i] = data[normalIndex]["aggregatedStats"][self.characteristics[j]] + data[rankedIndex]["aggregatedStats"][self.characteristics[j]]

                i += 1

        return(array)

    def typeIndex(self, data, type):
        for i in range(len(data)):
            if data[i]["playerStatSummaryType"] == type:
                return i
