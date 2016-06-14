import matplotlib.pyplot as plt
import numpy as np

from numpy import genfromtxt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from matplotlib.pyplot import cm
from mpl_toolkits.mplot3d import Axes3D

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Read data from csv file
X = genfromtxt(dataDirectory + "/csv/Summary/Challenger.csv", delimiter=',')
labels_true = X
X = StandardScaler().fit_transform(X)

# Constantes
eps = 0.33
min_samples = 3

# Compute DBSCAN
db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
#core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
#core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
print(len(labels))

print("labels: " + str(len(labels)))

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

##############################################################################
# Plot result

color=cm.rainbow(np.linspace(0,1,len(set(labels))))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(len(X)):
    #print(str(X[i]))
    col = 'k' if labels[i] == -1 else color[labels[i]]
    ax.scatter(X[i][0], X[i][1], X[i][2], 'o', c=col)

plt.title('Estimated number of clusters: %d' % n_clusters_)

plt.show()
