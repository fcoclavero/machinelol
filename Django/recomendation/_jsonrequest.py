import requests
import json
import time


class Request:
    def __init__(self, address, outfile, key):
        self.req = requests.get(address + key)
        self.status = self.req.status_code
        self.sleepTime = 60

        # Interpret the response received in the request
        # Successful request
        if self.status == 200:
            print("pass")
            with open(outfile, "w+") as outfile:
                json.dump(self.req.json(), outfile)

        # Diferent errors are displayed in console.
        elif self.status == 429:
            print ("Rate Limit exceded")
            # Wait some time until continue
            time.sleep(self.sleepTime)

        elif self.status == 500:
            print ("Internal server error")

        elif self.status == 503:
            print ("Service Unavailable")

        elif self.status == 404:
            print ("Data not found")

        else:
            print ("ERROR FATAL BRODER " + self.status)
            raise AssertionError("Unknown error response from API request.")
