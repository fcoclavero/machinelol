import numpy as np
import json
import os

class DataParser:

    def __init__(self, characteristics, regions, dataDirectory, dataSize, playerId):
        self.characteristics = characteristics
        self.regions = regions
        self.dataDirectory = dataDirectory
        self.dataSize = dataSize - 1
        self.playerId = playerId

    def parseSummary(self):
        array = []

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerSummary/" + region + "/"    # region's directory

            i = 0
            for fileDir in os.listdir(dir):
                print(fileDir)

                if (i > self.dataSize): break

                # for every file in the directory
                with open(dir + fileDir, "r") as readfile:
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
                # Player id as first element in each row
                aux = [os.path.splitext(fileDir)[0]]

                try:
                    for char in self.characteristics:
                        if(char == 'wins'):
                            aux.append(data[normalIndex]['wins'] + data[rankedIndex]['wins'])
                        elif(char == 'losses'):
                            aux.append(data[rankedIndex]['losses'])
                        else:
                            aux.append(data[normalIndex]["aggregatedStats"][char] + data[rankedIndex]["aggregatedStats"][char])
                except:
                    continue

                array.append(aux)
                i += 1

        return(array)

    def typeIndex(self, data, type):
        for i in range(len(data)):
            if data[i]["playerStatSummaryType"] == type:
                return i