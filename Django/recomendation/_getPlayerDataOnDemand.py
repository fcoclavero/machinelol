import recomendation._jsonrequest as jr
import os


class getPlayerData():
    ''' Extrae summary, ranked y masteries para el player con que se instancia la clase.
    Datos se guardan en dataDir.'''

    def __init__(self, playerId, dataDir, region='las', year='2016', key='v'):
        # Set param
        self.playerId = playerId
        self.dataDir = dataDir
        self.keys = {'c': "9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", 'v': "0b808dbd-c044-43db-88a0-829dbd390aa7"}
        self.region = region
        self.year = year
        self.key = self.keys[key]

        # Get player data
        self.getSummary()
        self.getMasteries()
        self.getRanked()

        print('Success')

    def getMasteries(self):
        if self.region == "las":
            reqregion = "LA2"
        else:
            reqregion = "LA1"

        outPath = self.dataDir + "/PlayerMasteries/" + self.region + "/"
        # Checks if the saving directory exists and creates it if needed.
        if not os.path.exists(outPath):
            print ("Creating folder: " + outPath)
            os.makedirs(outPath)

        address = "https://" + self.region + ".api.pvp.net/championmastery/location/" + reqregion + "/player/" + str(
            self.playerId) + "/champions?api_key="

        outfile = outPath + str(self.playerId) + ".json"

        req = jr.Request(address, outfile, self.key)
        # Handle the request response for different cases
        self.handleRequestResponse(req, address, outfile)

    def getSummary(self):
        # Checks if the saving directory exists and creates it if needed.
        dirPath = self.dataDir + "/" + "playerSummary" + "/" + self.region + "/"
        if not os.path.exists(dirPath):
            print ("Creating folder: " + dirPath)
            os.makedirs(dirPath)

        address = "https://" + self.region + ".api.pvp.net/api/lol/" + self.region + "/v1.3/stats/by-summoner/" + str(
            self.playerId) + "/summary?season=SEASON2016&api_key="

        outfile = dirPath + str(self.playerId) + ".json"

        req = jr.Request(address, outfile, self.key)
        # Handle the request response for different cases
        self.handleRequestResponse(req, address, outfile)

    def getRanked(self):
        # Checks if the saving directory exists and creates it if needed.
        outPath = self.dataDir + "/" + "PlayerRanked" + "/" + self.region + "/" + self.year + "/"
        if not os.path.exists(outPath):
            print ("Creating folder: " + outPath)
            os.makedirs(outPath)

        address = "https://" + self.region + ".api.pvp.net/api/lol/" + self.region + \
                  "/v1.3/stats/by-summoner/" + str(self.playerId) + "/ranked?season=SEASON" + self.year + "&api_key="

        outfile = outPath + str(self.playerId) + ".json"

        req = jr.Request(address, outfile, self.key)
        # Handle the request response for different cases
        self.handleRequestResponse(req, address, outfile)

    def handleRequestResponse(self, req, address, outfile):
        ''' Raise errors if needed depending of the response from the LOL API'''
        timeout = 0
        while req.status in (429, 500, 503) and timeout < 100:
            # If the request answer is: Internal server error, Service unavailable or Rate limit exceded try again
            req = jr.Request(address, outfile, self.key)
            timeout += 1

        if timeout >= 100 and req.status in (429, 500, 503):
            # After 100 tries error continue
            if req.status == 429:
                # Rate limit exceded despues de 100 intentos => Raro
                raise AssertionError("Rate limit still exceded after 100 slow tries. FATAL ERROR.")
            raise AssertionError("Conection problem.")

        if req.status == 404:
            # Data Not Found
            raise AssertionError("User Summary not found.")

        elif req.status != 200:
            # Unknown error
            raise AssertionError("User summary couldn't process.")

        else:
            # Status == 200: Success!
            pass
