import pandas as pd
from snnClass import SNN

# Test constants
k = 25
eps = 20
min_pts = 10

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Execute test
data = pd.read_csv(dataDirectory + "/csv/Summary/Challenger.csv", sep = ";")

snn = SNN(data, k, eps, min_pts)
snn.plot2D()

# Create statistics
print("Number of clusters: " + str(snn.nClusters))
