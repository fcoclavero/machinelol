from django.core.management.base import BaseCommand, CommandError
from recomendation.models import LasUser


from _getChampionsDataFromIdArray import main as getChampionsDataFromIdArray
from _recomendationSystem import recomenderSystem
from _champIdToName import idToName as itn
from _snnClass import SNN

import pandas as pd
import random


dataDirectory = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data"

# Caracteristicas sobre las cual se hara el clustering. Fijarse que esten incluidas en poblate_db.py Line 12 i.e. en la BD
# Realmente
# characteristics = ["wins", "totalChampionKills"]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('player_id', type=int)

    def handle(self, *args, **options):
        k = 1000
        id = options['player_id']
        playerArray = []
        try:
            playerArray.append(LasUser.objects.filter(id=id).values('id', 'wins', 'totalChampionKills')[0])
        except IndexError:
            raise CommandError("Id entregada no esta en la BD.")

        # Get k players randomly from the db
        lenInstanceList = LasUser.objects.count()
        l = lenInstanceList * 1.0 / k
        if l < 1:
            raise CommandError("No hay suficientes datos en la base de datos.")
        for i in range(k):
            rand = random.randint(1, int(l))
            playerArray.append(LasUser.objects.all().values('id', 'wins', 'totalChampionKills')[int((l * i + rand) - 1)])
            #[)
        ## Make a dataframe with the list of players
        data = pd.DataFrame.from_records(playerArray)

        # Parameters for clustering
        # k = 25
        # eps = 20
        aux = k
        k = 20
        eps = 15
        snn = SNN(data, k, eps)
        snn.plot2D()

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
        print("Champion points ranking: ")
        print(idToName.convert(cpRanking))
        print(" kda ranking: ")
        print(idToName.convert(kdaRanking))
        print(" winrate ranking: ")
        print(idToName.convert(wrRanking))
        print(" heuristic ranking: ")
        print(idToName.convert(hRanking))
        print("Colaborative filtering ranking: ")
        print(idToName.convert(cfRanking))

        #return {'Champion Mastery Ranking': cpRanking, 'KDA Ranking': kdaRanking, 'Winrate Ranking': wrRanking,
        #     'Heuristic ranking': hRanking, 'Colaborative Filtering Ranking': cfRanking}


