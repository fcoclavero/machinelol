import os
import jsonrequest as jr
import time
import sys
import json

keys = {'c': "9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", 'v': "0b808dbd-c044-43db-88a0-829dbd390aa7"}
regions = ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"]
year = "2015"

## This script get UserIDs from a directory with the form: /<region>/<id>.json and deletes its file if the request is "dirty".

# Put here the directory that contains the region/ids.
sourceDir = "PlayerSummary"
key = keys['v']

if len(sys.argv) != 2:
    key = keys['v']
##
else:
    if sys.argv[1] == 'c':
        key = keys['c']
    else:
        key = keys['v']
print("Key selected: " + key)

for region in regions:

    # Check if the region dir is contained in the source directory.
    regionPath = os.getcwd() + "/" + sourceDir + "/" + region
    # If not, then pass to the next region.
    if not os.path.exists(regionPath):
        print ("The region " + region + " doesn't exist in the directory.")
        continue

    # Iterate over the files in the region directory.
    for entry in os.listdir(regionPath):

        #Store the initial time
        t0 = time.time()
        #Split the filename of the form "<str>.<str>"
        (fileName, fileType) = entry.split('.')

        if fileType == "json":

            # Load the json fle.
            with open(regionPath + "/" + entry, "r") as readfile:
                print(regionPath + "/" + entry)
                data = json.load(readfile)

            requiredKey = 'playerStatSummaries'
            # Tries to adquire the needed value.
            try:
                stats = data[requiredKey]
            except KeyError:
                os.remove(regionPath + "/" + entry)