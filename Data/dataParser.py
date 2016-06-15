import numpy as np
import json
import os


class DataParser:

    def __init__(self, characteristics, regions, dataDirectory, dataSize):
        self.regions = regions
        self.dataDirectory = dataDirectory
        self.dataSize = dataSize
        self.characteristics = characteristics

    def parseSummary(self):
        array = []

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerSummary/" + region + "/"    # region's directory

            i = 0
            for fileDir in os.listdir(dir):
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
                aux = []

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

    def parseChampionMasteryByIdArray(self, idArray):
        playersDict = {}

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerMasteries/" + region + "/"  # region's directory

            i = 0
            for id in idArray:
                if (i > self.dataSize):
                    break

                try:
                    with open(dir + str(id) + ".json") as readfile:
                        try:
                            data = json.load(readfile)
                        except IOError:
                            print("Error loading json for ID: " + str(id))
                            continue
                except IOError:
                    print("Player Mastery for ID: " + str(id) + " doesn't exist.")
                    continue

                ''' The champion mastery data for each player is stored as a dict:
                {'champID1': {'char1' = value1, 'char2' = ...}, 'champID2': ...} '''

                playerChampionStats = {}

                # Each entry in data is a champion with its mastery data
                for entry in data:
                    # Create the key championID in the output dict
                    playerChampionStats[entry['championId']] = {}

                    for char in self.characteristics:
                        try:
                            playerChampionStats[entry['championId']][char] = entry[char]
                        except KeyError:
                            print ("Error getting the characteristic: " + char)
                            continue

                playersDict[id] = playerChampionStats
                i += 1
        return playersDict

    def parseChampionRankedStatsByIdArray(self, idArray, year=2015):
        playersDict = {}

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerRankedStats/" + region + "/" + str(year) + "/"  # region's directory

            i = 0
            for id in idArray:
                if (i > self.dataSize):
                    break

                try:
                    with open(dir + str(id) + ".json") as readfile:
                        try:
                            data = json.load(readfile)['champions']
                        except IOError:
                            print("Error loading json for ID: " + str(id))
                            continue
                except IOError:
                    print("Player Ranked Stats for ID: " + str(id) + " doesn't exist.")
                    print(dir + str(id) + ".json")
                    continue

                ''' The champion ranked data for each player is stored as a dict:
                {'champID1': {'char1' = value1, 'char2' = ...}, 'champID2': ...} '''
                playerChampionStats = {}


                # Each entry in data is a champion dict with its ranked data under 'stats' key
                for entry in data:
                    # Create the key championID in the output dict
                    playerChampionStats[entry['id']] = {}

                    for char in self.characteristics:
                        try:
                            playerChampionStats[entry['id']][char] = entry['stats'][char]
                        except KeyError:
                            print ("Error getting the characteristic: " + char)
                            continue

                playersDict[id] = playerChampionStats
                i += 1
        return playersDict

