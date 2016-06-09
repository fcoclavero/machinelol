import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance

# Constants
k = 20

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Read data from csv file
X = genfromtxt(dataDirectory + "/csv/Summary/Challenger.csv", delimiter=',')
labels_true = X
X = StandardScaler().fit_transform(X)

# Compute similarity matrix. Corresponds to a clique in which nodes
# are the dataset points, and the edge's weigths are the similarity
# measure between two points. Euclidean distance is used as the
# similarity measure.
n = X.shape[0]

distances = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        distances[i,j] = 0 if i==j else distance.euclidean(X[i], X[j])

# Matrix is sparsified: only the k most similar (nearest) neighbors are
# kept (corresponds to keeping the k strongest links of the similarity
# graph)

def getMax(knn, i):
    maxDistance = -1
    maxIndex = -1
    for index in knn:
        if maxDistance < distances[i,index]:
            maxDistance = distances[i,index]
            maxIndex = index
    return maxIndex

sparsified = []

for i in range(n):
    knn = []

    for j in range (n):
        if len(knn) < k:
            knn.append(j)
        else:
            max = getMax(knn, i)
            if distances[i,j] < distances[i,max]:
                knn[knn.index(max)] = j

    if len(knn) == k:
        sparsified.append(knn)
    else: raise ValueError("Length of nearest neighbor array is " +
                            len(knn) + ", expected " + k)

# The sparsified object can be used as the adjacency matrix of
# the shared nearest neighbor graph

# Create SNN (similar nearest neighbor) density matrix. SNN similarity
# is defined as:
# similarity(p,q) = size(KNN(p) intersection KNN(q))

similarity = np.zeros((n,n))

for i in range(n):
    for neighbor in sparsified[i]:
        similarity[i,neighbor] = len(list(filter(lambda x: x in sparsified[neighbor], sparsified[i])))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot data points
for i in range(len(X)):
    ax.scatter(X[i][0], X[i][1], X[i][2], 'o', c='k')

'''
for i in range(n):
    knn = sparsified[i]
    for j in knn:
        plt.plot(X[i],X[j])
'''

#   plt.show()
