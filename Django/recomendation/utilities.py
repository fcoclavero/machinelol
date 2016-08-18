import requests, json, random

import pandas as pd

import recomendation.constants as constants

from django.core.management.base import BaseCommand, CommandError
from recomendation.models import LasUser
from recomendation._getChampionsDataFromIdArray import main as getChampionsDataFromIdArray
from recomendation._recomendationSystem import recomenderSystem
from recomendation._champIdToName import idToName as itn
from recomendation._newDataParser import DataParser
from recomendation._snnClass import SNN

# Estas son las caracteriticas que se incluiran en la base de datos. El resto de las caracteristicas quedan con NULL en sus valores.

characteristics = constants.characteristics
regions = constants.regions
dataDirectory = constants.dataDirectory
keys = constants.keys

def getId(summonerName, region):
    data = requests.get("https://las.api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + keys[0])

    try:
        id = data.json()[summonerName]['id']
    except:
        id = False

    return id

def getChampionData(region, id):
    data = requests.get("https://las.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + str(id) + "?api_key=" + keys[1])
    return data.json()

def getRecomendation(playerId, playerRegion, dataSize = 10):
    populateDb(playerId, playerRegion, dataSize)

    return recomendation(playerId)

def populateDb(playerId, playerRegion, dataSize):
    # Create a new DataParser Object
    dataParser = DataParser(characteristics, regions, dataDirectory, dataSize, playerId, playerRegion)

    # #######################################################
    # #                 Player Summary                  #
    # #######################################################

    # Obtain numpy array with the parsed summary information.
    playersArray = dataParser.parseSummary(log='j2d')

    # For each player an 'User Model' is created and saved in db
    for charDict in playersArray:
        # Depending of the region
        if charDict['region'] == 'las':
            p = LasUser(id=charDict['id'])

        else:
            raise KeyError
            raise CommandError("No existe modelo de user para esta region")

        for key in charDict:
            value = charDict[key]
            if key == 'id':
                pass

            elif key == 'region':
                pass
            # p.region = value

            elif key == 'wins':
                p.wins = value

            elif key == 'losses':
                p.losses = value

            elif key == 'totalChampionKills':
                p.totalChampionKills = value

            elif key == 'totalTurretsKilled':
                p.totalTurretsKilled = value

            elif key == 'totalMinionKills':
                p.totalMinionKills = value

            elif key == 'totalNeutralMinionsKilled':
                p.totalNeutralMinionsKilled = value

            elif key == 'totalAssists':
                p.totalAssists = value

            else:
                raise KeyError

        try:
            # print("save")
            p.save()
        except:
            # print("skip")
            continue

def recomendation(id, dataSize = 500):
    playerArray = []
    try:
        playerArray.append(LasUser.objects.filter(id=id).values('id', 'wins', 'totalChampionKills')[0])
    except IndexError:
        raise CommandError("Id entregada no esta en la BD.")

    # Get k players randomly from the db
    lenInstanceList = LasUser.objects.count()
    l = lenInstanceList * 1.0 / dataSize
    if l < 1:
        raise CommandError("No hay suficientes datos en la base de datos.")
    for i in range(dataSize):
        rand = random.randint(1, int(l))
        playerArray.append(LasUser.objects.all().values('id', 'wins', 'totalChampionKills')[int((l * i + rand) - 1)])

    ## Make a dataframe with the list of players
    data = pd.DataFrame.from_records(playerArray)

    # Parameters for clustering
    k = 20
    eps = 15
    snn = SNN(data, k, eps)

    # Create statistics
    print("Number of clusters: " + str(snn.nClusters))
    print("User " + str(id) + "'s cluser:")
    print(snn.getCluster(id))

    # this func exports players (cluster) champion data to resultDict
    resultDict = getChampionsDataFromIdArray(snn.getCluster(id))
    # pass the dict to the recomender system to make recomendations
    rsys = recomenderSystem(resultDict)

    # Get the rankings from the recomenderSystem
    (cpRanking, kdaRanking, wrRanking, hRanking) = rsys.NaiveRecomenderSystem()
    cfRanking = rsys.collaborativeFiltering(id)

    idToName = itn(dataDirectory)

    return {'mastery': cpRanking, 'kda': kdaRanking, 'winrate': wrRanking, 'heuristic': hRanking, 'colaborative': cfRanking}
