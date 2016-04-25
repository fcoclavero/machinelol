import numpy as np
import json

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]

root = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol"

file = open(root + "/caracteristicasUsuario.txt", "r")
characteristics = file.read().split(",") - 10           # -10 to account for header files
# print(len(characteristics))

dataSize = 10 * 200
array = np.zeros(shape = (dataSize,characteristics.length))

for region in regions:

    with open("Challenger2016/"+region+"/"+region+"_players.json", "r") as readfile:
        data = json.load(readfile)
