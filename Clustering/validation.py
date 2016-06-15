import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import snn

from numpy import genfromtxt
from sklearn.preprocessing import StandardScaler
from matplotlib.pyplot import cm
from mpl_toolkits.mplot3d import Axes3D

def loadData(dataDirectory):
    # Read data from csv file
    data = pd.read_csv(dataDirectory + "/csv/Summary/Challenger.csv", sep = ";")

    # Parse data, drops id column
    X = (data.drop('id', 1)).as_matrix()
    return data, StandardScaler().fit_transform(X)

# Result visualization
def plotResults(data, X, jpClusters, nClusters):
    n = X.shape[0]
    headers = data.columns.values.tolist()

    color = cm.rainbow(np.linspace(0, 1, nClusters))

    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    ax = fig.add_subplot(111)

    # Plot data points
    for i in range(n):
        col = 'k' if jpClusters[i] == 0 else color[jpClusters[i]]
        # ax.scatter(X[i][0], X[i][1], X[i][2], 'o', c=col)
        ax.scatter(X[i][0], X[i][1], c=col)

    plt.show()

# Test constants
k = 25
eps = 20
min_pts = 10

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Execute test
data, X = loadData(dataDirectory)
jpClusters, nClusters = snn.snnCluster(X, k, eps, min_pts)
plotResults(data, X, jpClusters, nClusters)

# Create statistics


print("Number of clusters: " + str(nClusters))
