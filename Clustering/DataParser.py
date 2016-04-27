import numpy as np
import json
import os

class DataParser:

    # regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
    regions = ["las", "na", "oce", "ru", "tr"]
    dataRoot = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"
    dataSize = 10 * 200
    characteristics = ["totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]

    def parseSummary(self):
        array = np.zeros(shape=(len(self.characteristics), self.dataSize))

        i = 0                                                         # user index
        for region in self.regions:
            dir = self.dataRoot + "/PlayerSummary/" + region + "/"    # region's directory
            for fileDir in os.listdir(dir):                           # for every file in the directory
                with open(dir + fileDir, "r") as readfile:            # open file
                    # load data onto dict
                    try:
                        data = json.load(readfile)['playerStatSummaries']
                    except:
                        continue


                normalIndex = self.typeIndex(data, "Unranked")
                rankedIndex = self.typeIndex(data, "RankedSolo5x5")
                if normalIndex == None or rankedIndex == None:
                    continue

                # Transfer data from dict to np array
                array[0][i] = data[normalIndex]['wins'] + data[rankedIndex]['wins']
                array[1][i] = 1313
                for j in range(2,len(self.characteristics)):
                    array[j][i] = data[normalIndex]["aggregatedStats"][self.characteristics[j]] + data[rankedIndex]["aggregatedStats"][self.characteristics[j]]

                i += 1

        return(array)

    def typeIndex(self, data, type):
        for i in range(len(data)):
            if data[i]["playerStatSummaryType"] == type:
                return(i)
