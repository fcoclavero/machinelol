import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy import genfromtxt
from matplotlib.pyplot import cm
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

class SNN:
    def __init__(self, data, k, eps, min_pts):
        # Get list of point id's
        self.ids = data["id"]

        self.X = self.fitData(data)
        self.n = self.X.shape[0]
        self.snnCluster(k, eps, min_pts)

    # Drops id column and fits data
    def fitData(self, data):
        data = data.drop('id', 1)
        self.headers = data.columns.values.tolist()
        return StandardScaler().fit_transform(data.as_matrix())

    # Returns the point furthest from i in the knn array.
    def getMax(self, distances, knn, i):
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
    def getDistances(self):
        distances = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                distances[i,j] = 0 if i==j else distance.euclidean(self.X[i], self.X[j])

        return distances

    # Sparsifies matrix: only the k most similar (nearest) neighbors
    # are kept (corresponds to keeping the k strongest links of the
    # similarity graph)
    def sparse(self, k, distances):
        sparsified = []

        for i in range(self.n):
            knn = []

            for j in range (self.n):
                if len(knn) < k:
                    knn.append(j)
                else:
                    max = self.getMax(distances, knn, i)
                    if distances[i,j] < distances[i,max]:
                        knn[knn.index(max)] = j

            if len(knn) == k:
                sparsified.append(knn)
            else: raise ValueError("Length of nearest neighbor array is " + len(knn) + ", expected " + k)

        return(sparsified)

    # Create SNN (similar nearest neighbor) density matrix. SNN
    # similarity is defined as:
    # similarity(p,q) = size(KNN(p) intersection KNN(q))
    # If the similarity between two points is less than eps, then it is
    # ignored (set to zero).
    def createSnn(self, eps, sparsified):
        snn = np.zeros((self.n,self.n))

        for i in range(self.n):
            for neighbor in sparsified[i]:
                if neighbor == i:
                    snn[i,neighbor] = 0
                else:
                    aux = len(list(filter(lambda x: x in sparsified[neighbor], sparsified[i])))
                    snn[i,neighbor] = 0 if aux < eps else aux

        return snn

    # Cluster the data in dataDirectory based on the similar neatest
    # neighbor methodself.
    def snnCluster(self, k, eps, min_pts):
        # Create distances matrix
        distances = self.getDistances()

        # The sparsified array can be used as the adjacency matrix of
        # the shared nearest neighbor graph
        sparsified = self.sparse(k, distances)

        # Get Snn matrix
        snn = self.createSnn(eps, sparsified)

        # Jarvis-Patrick clustering: clusters are defined from connected
        # points in the SNN graph.

        # jpClusters[i] contains the cluster of point i
        jpClusters = np.zeros(self.n)
        nClusters = 1

        # Recursively assigns cluster to each point in the same connected
        # component (they belong to the same cluster)
        def cluster(i, clstr):
            # Assign to new cluster if unclustered
            if jpClusters[i] == 0:
                jpClusters[i] = clstr
            else: return

            # Visit i's neighbors and assign them to the same cluster
            for j in range(self.n):
                # Recursive call
                if (snn[i,j] != 0): cluster(j, clstr)

        for i in range(self.n):
            if jpClusters[i] == 0:
                cluster(i, nClusters)
                nClusters += 1

        self.labels = jpClusters
        self.nClusters = nClusters

    # Result visualization
    def plot2D(self):
        color = cm.rainbow(np.linspace(0, 1, self.nClusters))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Plot data points
        for i in range(self.n):
            col = 'k' if self.labels[i] == 0 else color[self.labels[i]]
            ax.scatter(self.X[i][0], self.X[i][1], c=col)

        plt.show()

    # Result visualization
    def plot3D(self):
        color = cm.rainbow(np.linspace(0, 1, self.nClusters))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot data points
        for i in range(self.n):
            col = 'k' if self.labels[i] == 0 else color[self.labels[i]]
            ax.scatter(self.X[i][0], self.X[i][1], self.X[i][2], 'o', c=col)

        plt.show()
