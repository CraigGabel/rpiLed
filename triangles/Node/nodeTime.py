# a simple class to allow time comparisons
# all triangleNodes must extend this class

import time

class NodeTime:
    def __init__(self, update=False):
        self.previousTime = self.getTimeMs() if (update) else 0

    def getTimeMs(self):
        return int(time.time() * 1000)

    def compareTime(self, difference):
        currentTime = self.getTimeMs()
        if ((currentTime - self.previousTime) >= difference):
            self.previousTime = currentTime
            return True
        return False