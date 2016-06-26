import matplotlib.pyplot as plt
import numpy as np

from DataParser import *

# Parameters

# characteristics = ["wins", "losses", "totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]
characteristics = ["wins", "totalChampionKills"]
# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["las"]
dataDirectory = "C:\Users\Vichoko\Documents\GitHub\machinelol\machinelol\Data"
dataSize = 1000

# Create a new DataParser Object
dataParser = DataParser(characteristics, regions, dataDirectory, dataSize)

# #######################################################
# #                 Challenger Summary                  #
# #######################################################

# Obtain numpy array with the parsed summary information.
array = dataParser.parseSummary()

# Open write file
f = open(dataDirectory + "/csv/Summary/las.csv", 'w')

# Save headers
f.write("id;")
for i in range(len(characteristics)):
    f.write(characteristics[i])
    if i != (len(characteristics) - 1): f.write(";")
f.write("\n")

# Save characteristics array
for i in range(len(array)):
    for j in range(len(array[i])):
        f.write(str(array[i][j]))
        if j != (len(array[i]) - 1): f.write(";")
    f.write("\n")
import matplotlib.pyplot as plt
import numpy as np

from DataParser import *

# Parameters

# characteristics = ["wins", "losses", "totalChampionKills", "totalTurretsKilled", "totalMinionKills", "totalNeutralMinionsKilled", "totalAssists"]
characteristics = ["wins", "totalChampionKills"]
# regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
regions = ["las"]
dataDirectory = "C:\Users\Vichoko\Documents\GitHub\machinelol\machinelol\Data"
dataSize = 1000

# Create a new DataParser Object
dataParser = DataParser(characteristics, regions, dataDirectory, dataSize)

# #######################################################
# #                 Challenger Summary                  #
# #######################################################

# Obtain numpy array with the parsed summary information.
array = dataParser.parseSummary()

# Open write file
f = open(dataDirectory + "/csv/Summary/las.csv", 'w')

# Save headers
f.write("id;")
for i in range(len(characteristics)):
    f.write(characteristics[i])
    if i != (len(characteristics) - 1): f.write(";")
f.write("\n")

# Save characteristics array
for i in range(len(array)):
    for j in range(len(array[i])):
        f.write(str(array[i][j]))
        if j != (len(array[i]) - 1): f.write(";")
    f.write("\n")
