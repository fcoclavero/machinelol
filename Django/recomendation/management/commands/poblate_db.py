from django.core.management.base import BaseCommand, CommandError
from recomendation.models import LasUser
from _newDataParser import DataParser



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('player_id', type=int)
        parser.add_argument('ndata', type=int)

    def handle(self, *args, **options):

        # characteristics = ["wins", "losses", "totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]
        # Estas son las caracteriticas que se incluiran en la base de datos. El resto de las caracteristicas quedan con NULL en sus valores.
        characteristics = ["wins", "totalChampionKills"]
        # regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
        regions = ["las"]
        dataDirectory = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data"
        dataSize = options['ndata']

        playerid, playerregion = (options['player_id'], "las")
        print(dataSize)
        print(playerid)
        # Create a new DataParser Object
        dataParser = DataParser(characteristics, regions, dataDirectory, dataSize, playerid, playerregion)

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
            p.save()
