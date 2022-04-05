import time

# a simple class to allow time comparisons
# calls to compareTime return true if _difference_ time has passed since the last time compareTime returned true

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