import matplotlib.pyplot as plt
import numpy as np

from DataParser import *

# Parameters

# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["las", "na", "oce", "ru", "tr"]
dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"
dataSize = 10 * 200

# Create a new DataParser Object
dataParser = DataParser(regions, dataDirectory, dataSize)

# #######################################################
# #                 Challenger Summary                  #
# #######################################################

# Obtain numpy array with the parsed summary information.
array = dataParser.parseSummary()

np.savetxt(dataDirectory + "/csv/Summary/Challenger.csv", array, delimiter=",")