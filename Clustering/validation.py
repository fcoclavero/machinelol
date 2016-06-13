# Test constants
k = 25
eps = 20
min_pts = 10

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Execute test
X = loadData(dataDirectory)
jpClusters, nClusters = snnCluster(X, k, eps, min_pts)
plotResults(X, jpClusters, nClusters)

print("Number of clusters: " + str(nClusters))
