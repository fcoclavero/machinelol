import os
import json
import _logsystem as logsys

class DataParser:

    def __init__(self, characteristics, regions, dataDirectory, dataSize, playerId=0, playerRegion='las'):
        self.regions = regions
        self.dataDirectory = dataDirectory
        self.dataSize = dataSize - 1
        self.characteristics = characteristics
        self.subjectId = playerId
        self.subjectRegion = playerRegion

    def parseSummary(self, log ='0'):
        array = []

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerSummary/" + region + "/"  # region's directory
            i = 0

            # Log system for recovering
            logPath = "log_" + log + region + ".txt"
            log = logsys.Log(logPath, enable=False if log == '0' else True)

            # If the log was correctly loaded extract the content of the log.
            if log.loaded:
                playerId = int(log.read())
                print("Loaded " + str(playerId))

            else:
                playerId = 0


            for fileDir in os.listdir(dir):
                pid = os.path.splitext(fileDir)[0]
                if i > self.dataSize:
                    break
                if int(pid) < playerId:
                    continue

                # for every file in the directory
                # If the subject is from this region, force add his stats to the db
                if i == 0 and self.subjectRegion == region:
                    print("Procesing user " + str(self.subjectId))
                    pid = self.subjectId
                    ''' This if adds the subject to the parsed data'''
                    fileDir = str(self.subjectId) + ".json"
                    with open(dir + fileDir, "r") as readfile:
                        print (dir + fileDir)
                        # load data onto dict
                        try:
                            data = json.load(readfile)['playerStatSummaries']
                        except:
                            raise KeyError("No se encontro sujeto de recomendacion en summary.")

                else:
                    with open(dir + fileDir, "r") as readfile:
                        # load data onto dict
                        data = json.load(readfile)['playerStatSummaries']
                        log.write(pid)


                # Check if file contains match data
                normalIndex = self.typeIndex(data, "Unranked")
                rankedIndex = self.typeIndex(data, "RankedSolo5x5")
                if normalIndex is None or rankedIndex is None:
                    continue

                # Transfer data from dict to compact dict
                aux = {}
                aux['id'] = pid
                aux['region'] = region

                #try:
                for char in self.characteristics:
                    if char == 'wins':
                        aux[char] = (data[normalIndex][u'wins'] + data[rankedIndex][u'wins'])
                    elif char == 'losses':
                        aux[char] = (data[rankedIndex][u'losses'])
                    else:
                        try:
                            aux[char] = (
                                data[normalIndex][u"aggregatedStats"][unicode(char)] + data[rankedIndex][u"aggregatedStats"][unicode(char)])
                        except:
                            try:
                                aux[char] = (
                                    data[normalIndex][u"aggregatedStats"][unicode(char)])
                            except:
                                aux[char] = (data[rankedIndex][u"aggregatedStats"][unicode(char)])
                #except:
                #    continue

                array.append(aux)
                i += 1

        return array

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

    def parseChampionRankedStatsByIdArray(self, idArray, year=2016):
        playersDict = {}

        for region in self.regions:
            dir = self.dataDirectory + "/PlayerRanked/" + region + "/" + str(year) + "/"  # region's directory

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

