import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

import numpy as np
from numpy import genfromtxt

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance

def loadData(dataDirectory):
    # Read data from csv file
    X = genfromtxt(dataDirectory + "/csv/Summary/Challenger.csv", delimiter=',')
    return StandardScaler().fit_transform(X)

# Returns the point furthest from i in the knn array.
def getMax(distances, knn, i):
    maxDistance = -1
    maxIndex = -1
    for index in knn:
        if maxDistance < distances[i,index]:
            maxDistance = distances[i,index]
            maxIndex = index
    return maxIndex

# Computes similarity matrix. Corresponds to a clique in which nodes
# are the dataset points, and the edge's weigths are the similarity
# measure between two points. Euclidean distance is used as the
# similarity measure.
def getDistances(n, X):
    distances = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            distances[i,j] = 0 if i==j else distance.euclidean(X[i], X[j])

    return distances

# Sparsifies matrix: only the k most similar (nearest) neighbors
# are kept (corresponds to keeping the k strongest links of the
# similarity graph)
def sparse(n, distances):
    sparsified = []

    for i in range(n):
        knn = []

        for j in range (n):
            if len(knn) < k:
                knn.append(j)
            else:
                max = getMax(distances, knn, i)
                if distances[i,j] < distances[i,max]:
                    knn[knn.index(max)] = j

        if len(knn) == k:
            sparsified.append(knn)
        else: raise ValueError("Length of nearest neighbor array is "
                                + len(knn) + ", expected " + k)

    return(sparsified)

# Create SNN (similar nearest neighbor) density matrix. SNN
# similarity is defined as:
# similarity(p,q) = size(KNN(p) intersection KNN(q))
# If the similarity between two points is less than eps, then it is
# ignored (set to zero).
def createSnn(n, sparsified):
    snn = np.zeros((n,n))

    for i in range(n):
        for neighbor in sparsified[i]:
            if neighbor == i:
                snn[i,neighbor] = 0
            else:
                aux = len(list(filter(lambda x: x in sparsified[neighbor], sparsified[i])))
                snn[i,neighbor] = 0 if aux < eps else aux

    return snn

# Result visualization
def plotResults(X, jpClusters, nClusters):
    n = X.shape[0]

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

# Cluster the data in dataDirectory based on the similar neatest
# neighbor methodself.
def snnCluster(X, k, eps, min_pts):
    n = X.shape[0]

    # Create distances matrix
    distances = getDistances(n, X)

    # The sparsified array can be used as the adjacency matrix of
    # the shared nearest neighbor graph
    sparsified = sparse(n, distances)

    # Get Snn matrix
    snn = createSnn(n, sparsified)

    # Jarvis-Patrick clustering: clusters are defined from connected
    # points in the SNN graph.

    # jpClusters[i] contains the cluster of point i
    jpClusters = np.zeros(n)
    nClusters = 1

    # Recursively assigns cluster to each point in the same connected
    # component (they belong to the same cluster)
    def cluster(i, clstr):
        # Assign to new cluster if unclustered
        if jpClusters[i] == 0:
            jpClusters[i] = clstr
        else: return

        # Visit i's neighbors and assign them to the same cluster
        for j in range(n):
            # Recursive call
            if (snn[i,j] != 0): cluster(j, clstr)

    for i in range(n):
        if jpClusters[i] == 0:
            cluster(i, nClusters)
            nClusters += 1

    return jpClusters, nClusters
