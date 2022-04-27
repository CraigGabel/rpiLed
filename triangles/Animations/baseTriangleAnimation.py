# a single triangleNode is able to run simple patterns (triangleAnimations) among its 12 leds
# this base pattern is to be extended by all triangleAnimations
#   TODO: in process is updating existing triangleAnimations to fulfill the extension of this class
# it contains helper functions all triangleAnimations will need

from triangles.Node.nodeTime import NodeTime

class BaseTriangleAnimation(NodeTime):
    def __init__(self, update = False, numLeds = 12, cooldownSteps = 50, cooldownRate = 20):
        super().__init__(update)
        self.numLeds = numLeds
        self.cooldownSteps = cooldownSteps
        self.cooldownRate = cooldownRate
        self.cooldownStepIndex = 0
        self.cooldownActive = 0
        self.cooldownComplete = 0

    def getNumLeds(self):
        return self.numLeds

    def startCooldown(self):
        self.cooldownStepIndex = 0
        self.cooldownActive = 1
        self.cooldownComplete = 0

    def isCooldownActive(self):
        return self.cooldownActive

    def cooldownRun(self):
        if (self.cooldownActive == 1):
            if (self.compareTime(self.cooldownRate)):
                self.cooldownStepIndex = self.cooldownStepIndex + 1
                if (self.cooldownStepIndex >= self.cooldownSteps):
                    self.cooldownStepIndex = 0
                    self.cooldownComplete = 1
        return self.cooldownComplete