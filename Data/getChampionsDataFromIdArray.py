import matplotlib.pyplot as plt
import numpy as np

from dataParser import *
from getChampionIdList import getChampionIds

# Parameters
# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["las"]
dataDirectory = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data"
dataSize = 100

''' Extracts user information from a userId array referent to champions '''
def main(idArray):
    ''' First extracts player championMastery stats '''
    # Relevant characteristics for masteries
    masteryCharacteristics = ["championPoints"]
    rankedCharacteristics = ['totalChampionKills', 'totalAssists', 'totalDeathsPerSession',
                                  'totalSessionsWon', 'totalSessionsLost']

    # Create a new DataParser Object
    dataParser = DataParser(masteryCharacteristics, regions, dataDirectory, dataSize)

    # Get a list of dicts {'champ': data} for each user; where data is a dict of characteristics.
    playerMasteryDict = dataParser.parseChampionMasteryByIdArray(idArray)

    ''' Second extracts player champion ranked stats '''
    # Relevant characteristics for ranked champion stats
    dataParser.characteristics = rankedCharacteristics

    # Get a list of dicts {'champ': data} for each user; where data is a dict of characteristics.
    playerRankedStatsDict = dataParser.parseChampionRankedStatsByIdArray(idArray, 2015)

    championIdList = getChampionIds()

    # Join both dicts of dicts in one with both characteristics set (Ranked and Mastery).
    playerDict = {}
    for userId in idArray:
        characteristicsCounter = 0

        playerDict[userId] = {}
        # Iterates over the champions that exist
        for champId in championIdList:
            # For each ranked characteristic is added to the output dict.
            playerDict[userId][champId] = {}
            for rankedChar in rankedCharacteristics:
                try:
                    rankedStat = playerRankedStatsDict[userId][champId][rankedChar]
                    characteristicsCounter += 1
                except KeyError:
                    continue
                playerDict[userId][champId][rankedChar] = rankedStat

            for masteryChar in masteryCharacteristics:
                try:
                    masteryStat = playerMasteryDict[userId][champId][masteryChar]
                    characteristicsCounter += 1
                except KeyError:
                    continue
                playerDict[userId][champId][masteryChar] = masteryStat

        # Check if the user have information, i.e. if it has any charasteristic in any champion.
        if characteristicsCounter == 0:
            del playerDict[userId]

    jstr = json.dumps(playerDict, indent=4)
    with open('result.json', 'w') as fp:
        print >> fp, jstr
        fp.close()

userId = range(33000, 33640)
main(userId)