import os
import jsonrequest as jr
import time
import threading
import sys

keys = {'c': "9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", 'v': "0b808dbd-c044-43db-88a0-829dbd390aa7"}
 # regions = ["br", "eune", "euw", "kr", "las", "lan", "na", "oce", "ru", "tr"]
year = "2015"
regions = ["LA2", "LA1"]

## This script get UserIDs from a directory with the form: /<region>/<id>.json and requests the Player Mastery to the API.

def main(region, key):
    # Check if the region dir is contained in the source directory.
    if region == "LA2":
        foldername = "las"
    else:
        foldername = "lan"
    regionPath = os.getcwd() + "/" + sourceDir + "/" + foldername
    # If not, then pass to the next region.
    if not os.path.exists(regionPath):
        print ("The region " + foldername + "(" + region + ")" + "doesn't exist in the directory.")
        return

    # Iterate over the files in the region directory.
    for entry in os.listdir(regionPath):

        #Store the initial time
        t0 = time.time()
        #Split the filename of the form "<str>.<str>"
        (fileName, fileType) = entry.split('.')

        if fileType == "json":
            playerId = fileName

            # Checks if the saving directory exists and creates it if needed.
            outPath = os.getcwd() + "/" + "PlayerMasteries" + "/" + foldername + "/"
            if not os.path.exists(outPath):
                print ("Creating folder: " + outPath)
                os.makedirs(outPath)

            address = "https://" +  foldername + ".api.pvp.net/championmastery/location/" + region + "/player/" + str(playerId) + "/champions?api_key="

            outFile = outPath + str(playerId) + ".json"

            #Before making the request checks if the playerID was already requested.
            if os.path.exists(outFile):
                # If do exist, continue with the next playerId
                continue

            print("Making request for ID: " + playerId + ". In region: " + region)
            req = jr.Request(address, outFile, key)

            # If the request answer is: Internal server error, Service unavailable or Rate limit exceded
            timeout = 0
            while req.status in (429, 500, 503) or timeout > 100:
                req = jr.Request(address, outFile, key)
                timeout += 1

            # Any other responce just pass to the next playerId (Successful or data not found)
            else:
                pass

            # Synchronization module to prevent rate-limit exceeded response
            tf = time.time()
            dt = tf - t0
            if dt < 1200:
                ##hold until 1.2 secs; argument is in seconds, dt is in ms.
                time.sleep(1.2 - dt / 1000)

            if timeout > 100:
                print ("Timeout error")
                break


# Put here the directory that contains the region/ids.
sourceDir = "PlayerRankedStats"
key = keys['v']

if len(sys.argv) != 2:
    key = keys['v']
##
elif sys.argv[1] == 'c':
    key = keys['c']
else:
    key = keys['v']
print("Key selected: " + key)

threads = list()
for r in regions:
    if r == "las":
        t = threading.Thread(target=main, args=(r,keys['v']))
    else:
        t = threading.Thread(target=main, args=(r,key))        
    threads.append(t)
    t.start()
	
