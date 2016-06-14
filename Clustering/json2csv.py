import matplotlib.pyplot as plt
import numpy as np

from DataParser import *

# Parameters

# characteristics = ["wins", "losses", "totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]
characteristics = ["wins", "totalChampionKills"]
# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["lan", "las"]
dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"
dataSize = 100

# Create a new DataParser Object
dataParser = DataParser(characteristics, regions, dataDirectory, dataSize)

# #######################################################
# #                 Challenger Summary                  #
# #######################################################

# Obtain numpy array with the parsed summary information.
array = dataParser.parseSummary()

np.savetxt(dataDirectory + "/csv/Summary/Challenger.csv", array, delimiter=",")
