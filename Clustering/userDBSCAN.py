import matplotlib.pyplot as plt
import numpy as np

from DataParser import *

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

dataParser = DataParser()

array = dataParser.parseSummary()

plt.plot(array[1], array[3], 'ro')
plt.xlabel('wins')
plt.ylabel('totalChampionKills')
plt.show()