import matplotlib.pyplot as plt
import numpy as np

from numpy import genfromtxt

dataDirectory = "C:/Users/fcocl_000/Dropbox/Workspace/Python/Aprendizaje Bayesiano/machinelol/Data"

# Read data from csv file
array = genfromtxt(dataDirectory + "/csv/Summary/Challenger.csv", delimiter=',')

plt.plot(array[1], array[3], 'ro')
plt.xlabel('wins')
plt.ylabel('totalChampionKills')
plt.show()
