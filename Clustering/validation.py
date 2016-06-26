import pandas as pd
from snnClass import SNN

# Test constants
k = 25
eps = 20
min_pts = 10

dataDirectory = "C:/Users/Vichoko/Documents/GitHub/machinelol/machinelol/Data"

# Test user
requested = 100017

# Execute test
data = pd.read_csv(dataDirectory + "/csv/Summary/las.csv", sep = ";")

snn = SNN(data, k, eps, min_pts)
snn.plot2D()

# Create statistics
print("Number of clusters: " + str(snn.nClusters))

print("User " + str(requested) + "'s cluser:/n")
for user in snn.getCluster(requested):
    print(user)
