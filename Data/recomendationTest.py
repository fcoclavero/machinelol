import pandas as pd
from snnClass import SNN
from getChampionsDataFromIdArray import main as getChampionsDataFromIdArray
from recomendationSystem import recomenderSystem
from champIdToName import idToName

# Test constants
k = 25
eps = 20
min_pts = 10

dataDirectory = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data"

# Test user
requested = 100016

# Execute test
data = pd.read_csv(dataDirectory + "/csv/Summary/las.csv", sep = ";")

snn = SNN(data, k, eps, min_pts)
# snn.plot2D()

# Create statistics
print("Number of clusters: " + str(snn.nClusters))

print("User " + str(requested) + "'s cluser:")
# for user in snn.getCluster(requested):
#    print(user)
print(snn.getCluster(requested))
# this func exports players champion data to result.json
getChampionsDataFromIdArray(snn.getCluster(requested))

 # Load the result kson to the recomender system
rsys = recomenderSystem("C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data/workspace/result.json")
(cpRanking, kdaRanking, wrRanking, hRanking) = rsys.NaiveRecomenderSystem()
cfRanking = rsys.collaborativeFiltering(requested)

idToName = idToName(dataDirectory)
print ("Champion points ranking: ")
print (idToName.convert(cpRanking))
print (" kda ranking: ")
print (idToName.convert(kdaRanking))
print (" winrate ranking: ")
print (idToName.convert(wrRanking))
print (" heuristic ranking: ")
print (idToName.convert(hRanking))
print ("Colaborative filtering ranking: ")
print (idToName.convert(cfRanking))
