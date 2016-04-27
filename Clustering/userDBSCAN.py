import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from numpy import genfromtxt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Read data from csv file
array = genfromtxt(dataDirectory + "/csv/Summary/Challenger.csv", delimiter=',')

plt.plot(array[1], array[3], 'ro')
plt.xlabel('wins')
plt.ylabel('totalChampionKills')
plt.show()