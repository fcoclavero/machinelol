from math import sqrt,log
import json
from _getChampionIdList import getChampionIds

''' caracteristicas tomadas en cuenta:
    ChampionMasteries: 'championPoints'
    RankedStats:  "totalAssists", "totalDeathsPerSession", "totalSessionsWon",
        "totalChampionKills", "totalSessionsLost"
    '''
    
class recomenderSystem:
    """ recibe un json con el formato {playerId: {champId: {characteristic: , ...}, ...}, ...} correspondiente a un cluser de usuarios y una id de usuario.
		permite generar distintos tipos de recomendaciones"""
    def __init__(self, sourceDict):
        # Source file created by getChampionsDataFromIdArray.py
        self.sourceDict = sourceDict
        self.championIdList = getChampionIds()

        # Metadata
        self.metadataDict = {}

        # Create output mean dictionary
        self.meanDict = {}

        # create output total dictionary
        self.totalDict = {}
        #
        # # Open source file
        # try:
        #     with open(self.sourceFile) as readfile:
        #         try:
        #             self.data = json.load(readfile)
        #         except IOError:
        #             print("Error loading json")
        #
        # except IOError:
        #     print("Error in source file.")


        self.data = sourceDict

        # Init output dicts, also count the number of masteries and ranked stats per champion (saved in metadataDict)
        for champId in self.championIdList:
            # Initialize dicts for output and metadata
            self.meanDict[champId] = {}
            self.totalDict[champId] = {}
            self.metadataDict[champId] = {}

            # Count the total quantity of effective data for mastery and ranked stats (For each champion).
            masteryEntryNumber = 0
            rankedEntryNumber = 0
            for playerId in self.data:
                try:
                    self.data[playerId][champId]['championPoints']
                    masteryEntryNumber += 1
                except KeyError:
                    pass

                try:
                    self.data[playerId][champId]['totalSessionsWon']
                    rankedEntryNumber += 1
                except KeyError:
                    try:
                        # If totalSessionWon isn't found try to found totalSessionLost, if it's found it'd be strange.
                        self.data[playerId][champId]['totalSessionsLost']
                        print ("Something strange happened")
                        rankedEntryNumber += 1
                        pass
                    except KeyError:
                        pass

            self.metadataDict[champId]['numberOfMasteryEntries'] = masteryEntryNumber
            self.metadataDict[champId]['numberOfRankedEntries'] = rankedEntryNumber


    def getMeanAndTotalChampionStats(self):
        ''' recibe un json con el formato {playerId: {champId: {characteristic: , ...}, ...}, ...}
            y genera un dict de la forma {champId: {characteristic: , ...}, ...} con las caracteristicas
            promedio y totales sobre todos los jugadores del json input (cluster). '''

        playersTotalNumber = len(self.data)

        # Calculate the championPoints mean. Players with no championPoints = 0 championPoints.
        # Also the total champion points for the total dict.
        for champId in self.championIdList:
            champTotalChampionPoints = 0

            ## Iterate over every player in the source file
            for playerId in self.data:
                try:
                    champTotalChampionPoints += self.data[playerId][champId]['championPoints']
                except KeyError:
                    continue
            self.totalDict[champId]['championPoints'] = champTotalChampionPoints
            self.meanDict[champId]['championPoints'] = (champTotalChampionPoints / playersTotalNumber) if playersTotalNumber!=0 else 0

        # Calculate the totalAssist, totalDeathsPerSession, totalChampionKills,
        # totalSessionsWon, totalSessionsLost mean over the players that have ranked games with those
        # champs
        for champId in self.championIdList:
            champTotalAssists = 0
            champTotalDeaths = 0
            champTotalKills = 0
            champTotalSessionsWon = 0
            champTotalSessionsLost = 0

            ## Iterate over every player in the source file
            for playerId in self.data:
                try:
                    champTotalAssists += self.data[playerId][champId]['totalAssists']
                except KeyError:
                    pass
                try:
                    champTotalDeaths += self.data[playerId][champId]['totalDeathsPerSession']
                except KeyError:
                    pass
                try:
                    champTotalKills += self.data[playerId][champId]['totalChampionKills']
                except KeyError:
                    pass
                try:
                    champTotalSessionsWon += self.data[playerId][champId]['totalSessionsWon']
                except KeyError:
                    pass
                try:
                    champTotalSessionsLost += self.data[playerId][champId]['totalSessionsLost']
                except KeyError:
                    pass

            self.totalDict[champId]['totalAssists'] = champTotalAssists
            self.totalDict[champId]['totalDeathsPerSession'] = champTotalDeaths
            self.totalDict[champId]['totalChampionKills'] = champTotalKills
            self.totalDict[champId]['totalSessionsWon'] = champTotalSessionsWon
            self.totalDict[champId]['totalSessionsLost'] = champTotalSessionsLost

            numberOfRankedEntries = self.metadataDict[champId]['numberOfRankedEntries']
            self.meanDict[champId]['totalAssists'] = (champTotalAssists / numberOfRankedEntries) if numberOfRankedEntries != 0 else 0
            self.meanDict[champId]['totalDeathsPerSession'] = (champTotalDeaths / numberOfRankedEntries) if numberOfRankedEntries != 0 else 0
            self.meanDict[champId]['totalChampionKills'] = (champTotalKills / numberOfRankedEntries) if numberOfRankedEntries != 0 else 0
            self.meanDict[champId]['totalSessionsWon'] = (champTotalSessionsWon / numberOfRankedEntries) if numberOfRankedEntries != 0 else 0
            self.meanDict[champId]['totalSessionsLost'] = (champTotalSessionsLost / numberOfRankedEntries) if numberOfRankedEntries != 0 else 0

    def NaiveRecomenderSystem(self):
        ''' El sistema retorna 4 'rankings':
            1. Ranking descendente de championPoints
            2. Rankind descendente de KDA = (Kills+Assists)/Deaths
            3. Ranking descendente de winRate = (Wins/Loses)
            4. Ranking descendente de funcion heuristica

            En base a un diccionario fuente de la forma {champid: {caracteristica: , ...}, ...}'''

        # Fills the meanDict and totalDict with the data from the source json.
        self.getMeanAndTotalChampionStats()

        # Chose the source dict: Can be meanDict or totalDict
        sourceDict = self.totalDict

        # # Champion Points ranking creation
        # First leave the source dict with only championPoints as value and championId as key.
        auxDict = {}
        for champId in sourceDict:
            auxDict[champId] = sourceDict[champId]['championPoints']
        # Now sort the dict by championPoints (dict value)
        cpRanking = sorted(auxDict, key=auxDict.__getitem__, reverse=True)

        # # KDA ranking creation
        # First leave the source dict with only kda as value and championId as key (Need to do some calculus)
        auxDict = {}
        for champId in sourceDict:
            kills = sourceDict[champId]['totalChampionKills']
            assists = sourceDict[champId]['totalAssists']
            deaths = sourceDict[champId]['totalDeathsPerSession']
            auxDict[champId] = ((kills + assists)*1.0) / deaths if deaths != 0 else ((kills + assists)*1.0)/0.1
        # Now sort the dict by kda (dict value)
        kdaRanking = sorted(auxDict, key=auxDict.__getitem__, reverse=True)

        # # winRate ranking creation
        # First leave the source dict with only winrate as value and championId as key (Need to do some calculus)
        auxDict = {}
        for champId in sourceDict:
            wins = sourceDict[champId]['totalSessionsWon']
            loses = sourceDict[champId]['totalSessionsLost']
            auxDict[champId] = (wins*1.0) / loses if loses != 0 else (wins*1.0)/0.1   # Now sort the dict by kda (dict value)
        wrRanking = sorted(auxDict, key=auxDict.__getitem__, reverse=True)

        # # Heuristic ranking creation
        # First leave the source dict with one value (result of heuristic function) and
        # championId as key (Need to do some calculus)
        def hfunc(sourceDict, champId, alpha1=2, alpha2=1, alpha3=10):
            cp = sourceDict[champId]['championPoints']
            wins = sourceDict[champId]['totalSessionsWon']
            loses = sourceDict[champId]['totalSessionsLost']
            kills = sourceDict[champId]['totalChampionKills']
            assists = sourceDict[champId]['totalAssists']
            deaths = sourceDict[champId]['totalDeathsPerSession']

            winrate = (wins*1.0) / loses if loses != 0 else (wins*1.0)/0.1
            kda = ((kills + assists)*1.0) / deaths if deaths != 0 else ((kills + assists)*1.0)/0.1

            return (alpha1 * log(cp)) + (alpha2 * kda) + (alpha3 * winrate) if cp!=0 else (alpha2 * kda) + (alpha3 * winrate)

        auxDict = {}
        for champId in sourceDict:

            auxDict[champId] =  hfunc(sourceDict, champId)
        # Now sort the dict by kda (dict value)
        hRanking = sorted(auxDict, key=auxDict.__getitem__, reverse=True)

        return (cpRanking, kdaRanking, wrRanking, hRanking)

    ## Given a playerid, returns a list of recomended champions that he'd like based on championPoints (Expierence).
    def collaborativeFiltering(self, player):
        # player = unicode(player)

        # Correlation function returns value between -1 to 1. Value of 1 means
        # same taste (Taste is measured by similar championPoints)
        def pearson_correlation(data, player1, player2):
            # To get both played champions
            # A champion is played if user have 1000+ championpoints
            both_played = {}
            for champion in data[int(player1)]:
                try:
                    if data[player1][champion]['championPoints'] > 1000:
                        if champion in data[player2]:
                            try:
                                if data[player2][champion]['championPoints'] > 1000:
                                    both_played[champion] = 1
                            except KeyError:
                                # here if data[player2][champion][u'championPoints'] doesn't exist
                                pass
                except KeyError:
                    # here if data[player1][champion][u'championPoints'] doesn't exist
                    pass

            number_of_played_champs = len(both_played)

            # Checking for number of played in common
            if number_of_played_champs == 0:
                return 0

            # Add up all the preferences of each player
            player1_preferences_sum = sum([data[player1][champion]['championPoints'] for champion in both_played])
            player2_preferences_sum = sum([data[player2][champion]['championPoints'] for champion in both_played])

            # Sum up the squares of preferences of each user
            player1_square_preferences_sum = sum([pow(data[player1][champion]['championPoints'], 2) for champion in both_played])
            player2_square_preferences_sum = sum([pow(data[player2][champion]['championPoints'], 2) for champion in both_played])

            # Sum up the product value of both preferences for each champion
            product_sum_of_both_players = sum([data[player1][champion]['championPoints'] *
                                               data[player2][champion]['championPoints'] for champion in both_played])

            # Calculate the pearson score
            numerator_value = product_sum_of_both_players - (
                player1_preferences_sum * player2_preferences_sum / number_of_played_champs)
            denominator_value = sqrt(
                (player1_square_preferences_sum - pow(player1_preferences_sum, 2) / number_of_played_champs) * (
                    player2_square_preferences_sum - pow(player2_preferences_sum, 2) / number_of_played_champs))
            if denominator_value == 0:
                return 0
            else:
                r = numerator_value / denominator_value
                return r

        # returns the number_of_players (similar players) for a given specific player.
        def most_similar_players(player, number_of_players, data):
            scores = [(pearson_correlation(player, other_player), other_player) for other_player in data if
                      other_player != player]

            # Sort the similar persons so that highest scores player will appear at the first
            scores.sort()
            scores.reverse()
            return scores[0:number_of_players]

        # Gets recommendations for a player by using a weighted average of every other players's played champions
        totals = {}
        simSums = {}
        rankings_list = []

        for other_player in self.data:
            # don't compare me to myself
            if other_player == player:
                continue
            sim = pearson_correlation(self.data, player, other_player)

            # ignore scores of zero or lower
            if sim <= 0:
                continue

            for champion in self.data[other_player]:
                try:
                    # This shoud pass
                    self.data[other_player][champion]['championPoints']
                    # only score champions i doesn't play a lot (6000+ is lvl 3 with the champion)
                    try:
                        if self.data[player][champion]['championPoints'] < 6000:
                            # Similrity * score
                            totals.setdefault(champion, 0)
                            totals[champion] += self.data[other_player][champion]['championPoints'] * sim
                            # sum of similarities
                            simSums.setdefault(champion, 0)
                            simSums[champion] += sim
                    # If key [u'championPoints'] not exist, then this
                    except KeyError:
                        # Similrity * score
                        totals.setdefault(champion, 0)
                        totals[champion] += self.data[other_player][champion]['championPoints'] * sim
                        # sum of similarities
                        simSums.setdefault(champion, 0)
                        simSums[champion] += sim
                except KeyError:
                    pass


        # Create the normalized list
        rankings = [(total / simSums[champion], champion) for champion, total in totals.items()]
        rankings.sort()
        rankings.reverse()
        # returns the recommended items
        recommendation_list = [int(recomend_champion) for score, recomend_champion in rankings]
        return recommendation_list
