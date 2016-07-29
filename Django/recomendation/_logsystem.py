import os

class Log:
    def __init__(self, path, enable=True):
        self.loaded = 0
        self.folder = "logs/"
        self.path = self.folder + path
        self.enable = enable
        if self.enable:
            # Check logs folder existence
            if not os.path.exists(self.folder):
                print ("Creating log folder: " + self.folder)
                os.makedirs(self.folder)

            try:  # Tries to load the log to continue where it stopped before
                print("Loading log...")
                self.log = open(self.path, "r")
                self.loaded = 1

            except ValueError:
                print ("The log is corrupt.")

            except IOError:
                print ("IO error")

    def write(self, content):
        if self.enable:
            try:
                log = open(self.path, "w")
                log.write(content)
            except:
                print ("Error in content or path. Try enter content as a string.")

    def read(self):
        if self.enable:
            return self.log.read()
        else:
            return str(0)

    def disable(self):
        self.enable = False
