from basePattern import BasePattern
from nodeResult import NodeResult
from nodeTime import NodeTime
from triangleNode import *
from rpi_ws281x import *
import random
import triangleAnimations
import stripConfig as stripConfig

# find patterns that groupings of triangleNodes will show
# these are attempts to cause groups of triangleNodes to act in concert

# i am a template, do not instantiate me
# copy/paste me to create new patterns
# add new methods as needed for specific patterns
class Template(BasePattern):
    # init is necessary for all patterns
    # add needed pattern specific initialization
    def __init__(self, strip = None, update = False):
        super().__init__(strip, update)

    # run is necessary for all patterns
    # to be called in main while loop
    # control timing within the run loop (see other implementations for examples)
    def run(self):
        pass

class Testing(BasePattern):
    def __init__(self, strip = None, update = False):
        super().__init__(strip, update)

        self.everyOther = 0
        self.color1 = Color(255, 0, 0)
        self.color2 = Color(0, 255, 0)

        for i in range(len(self.triangleNodes)):
            self.triangleNodes[i].mode = triangleAnimations.Temp(colorStart = self.color1 if self.everyOther == 0 else self.color2, colorEnd = self.color2 if self.everyOther == 0 else self.color1, steps = 50, updateRate = 20)
    
    def run(self):
        for i in range(len(self.triangleNodes)):
            result = self.triangleNodes[i].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(i, result)
            if (result.cycleEnd):
                if (i == 0):
                    self.everyOther = 1 if self.everyOther == 0 else 0
                    self.triangleNodes[i].mode = triangleAnimations.Temp(colorStart = self.color1 if self.everyOther == 0 else self.color2, colorEnd = self.color2 if self.everyOther == 0 else self.color1, steps = 50, updateRate = 20)

# one triangle phases between numerous colors
# at a random time, it stops phasing and then all triangles, in order, turn to the current randomized color
# then the process repeats
class RandomizingWipe(BasePattern):
    def __init__(self, strip = None, update = False, colorStart = Color(255, 0, 0)):
        super().__init__(strip, update)

        self.colorStart = colorStart
        self.stages = ["init_background", "randomizing", "wiping"]
        self.patternStage = 0
        self.activeIndex = 0
        self.randomizerStartColor = colorStart
        self.randomizerEndColor = Color(255, 0, 0)

        # paint the triangles to background
        for i in range(len(self.triangleNodes)):
            self.triangleNodes[i].mode = self.getMode(self.stages[self.patternStage])
            result = self.triangleNodes[i].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(i, result)
        
        self.patternStage = 1
        self.triangleNodes[self.activeIndex].mode = self.getMode(self.stages[self.patternStage])

    def getMode(self, stage = None):
        returnValue = None

        # wiping default settings
        wipeUpdateRate = 150
        backgroundUpdateRate = 1000

        # phaser default settings
        phaserSteps = 50
        phaserUpdateRate = 20

        if (stage == self.stages[0]):
            returnValue = triangleAnimations.Solid(color=self.colorStart, updateRate=backgroundUpdateRate)
        if (stage == self.stages[1]):
            self.randomizerStartColor = self.randomizerEndColor
            randRed = random.randint(0, 255)
            randGreen = random.randint(0, 255)
            randBlue = random.randint(0, 255)
            self.randomizerEndColor = Color(randRed, randGreen, randBlue)
            returnValue = triangleAnimations.Phaser(colorStart = self.randomizerStartColor, colorEnd = self.randomizerEndColor, steps = phaserSteps, updateRate = phaserUpdateRate)
        if (stage == self.stages[2]):
            returnValue = triangleAnimations.Wipe(color=self.randomizerEndColor, isBackwards=random.randint(0, 1) == 0, startCorner=random.randint(0, 2), updateRate=wipeUpdateRate)

        return returnValue

    def run(self):
        if (self.patternStage == 0):
            # this should never happen
            self.patternStage = 1
        elif (self.patternStage == 1):
            self.activeIndex = 0
            result = self.triangleNodes[self.activeIndex].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(self.activeIndex, result)
            if (result.cycleEnd):
                changeToWipe = random.randint(1, 10)
                if (changeToWipe != 1):
                    self.triangleNodes[self.activeIndex].mode = self.getMode(self.stages[self.patternStage])
                else:
                    self.patternStage = 2
                    self.activeIndex = 1
                    self.triangleNodes[self.activeIndex].mode = self.getMode(self.stages[self.patternStage])
        elif (self.patternStage == 2):
            result = self.triangleNodes[self.activeIndex].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(self.activeIndex, result)
            if (result.cycleEnd):
                self.activeIndex = self.activeIndex + 1
                if (self.activeIndex < len(self.triangleNodes)):
                    self.triangleNodes[self.activeIndex].mode = self.getMode(self.stages[self.patternStage])
                else:
                    self.patternStage = 1
                    self.activeIndex = 0
                    self.triangleNodes[self.activeIndex].mode = self.getMode(self.stages[self.patternStage])

# in this pattern:
# most triangles are background color
# periodically (random timing) a triangle will change colors, then later change back to background
class RandomTemporarySwitcher(BasePattern):
    def __init__(self, strip = None, colorBackground = Color(255, 0, 0), colorSpecial = Color(0, 255, 0)):
        super().__init__(strip)

        # pattern specific definitions
        self.randoTime = random.randint(1000, 4000)
        self.colorBackground = colorBackground
        self.colorSpecial = colorSpecial
        self.stages = ["background", "switching", "cooldown", "unswitching"]
        self.triangleStage = [0] * len(self.triangleNodes)

        # paint the triangles to background
        for i in range(len(self.triangleNodes)):
            self.triangleNodes[i].mode = self.getMode(self.stages[self.triangleStage[i]])
            result = self.triangleNodes[i].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(i, result)
    
    # used to set individual triangleNode's painting pattern based on the pattern stage they are in
    def getMode(self, stage = None):
        returnValue = None
        wipeUpdateRate = 150
        singleCircleUpdateRate = 83
        cooldownUpdateRate = 2500
        backgroundUpdateRate = 1000

        if (stage == self.stages[0]):
            returnValue = triangleAnimations.Solid(color=self.colorBackground, updateRate=backgroundUpdateRate)
        if (stage == self.stages[1]):
            randVal = random.randint(0, 1)
            if (randVal == 0):
                returnValue = triangleAnimations.SingleCircle(color=self.colorSpecial, isBackwards=random.randint(0, 1) == 0, startIndex=random.randint(0, 11), updateRate=singleCircleUpdateRate)
            elif (randVal == 1):
                returnValue = triangleAnimations.Wipe(color=self.colorSpecial, isBackwards=random.randint(0, 1) == 0, startCorner=random.randint(0, 2), updateRate=wipeUpdateRate)
            else:
                returnValue = triangleAnimations.Solid(color=self.colorSpecial, updateRate=backgroundUpdateRate)
        if (stage == self.stages[2]):
            returnValue = triangleAnimations.Solid(color=self.colorSpecial, updateRate=cooldownUpdateRate, update=True)
        if (stage == self.stages[3]):
            randVal = random.randint(0, 1)
            if (randVal == 0):
                returnValue = triangleAnimations.SingleCircle(color=self.colorBackground, isBackwards=random.randint(0, 1) == 0, startIndex=random.randint(0, 11), updateRate=singleCircleUpdateRate)
            elif (randVal == 1):
                returnValue = triangleAnimations.Wipe(color=self.colorBackground, isBackwards=random.randint(0, 1) == 0, startCorner=random.randint(0, 2), updateRate=wipeUpdateRate)
            else:
                returnValue = triangleAnimations.Solid(color=self.colorBackground, updateRate=backgroundUpdateRate)

        return returnValue
    
    #
    def run(self):
        if (self.compareTime(self.randoTime)):
            self.randoTime = random.randint(1000, 4000)
            randnum = -1
            while (randnum == -1):
                randnum = random.randint(0, len(self.triangleNodes)-1)
                if (self.triangleStage[randnum] != 0):
                    randnum = -1
            self.triangleStage[randnum] = 1
            self.triangleNodes[randnum].mode = self.getMode(self.stages[self.triangleStage[randnum]])
        for i in range(len(self.triangleNodes)):
            result = self.triangleNodes[i].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(i, result)
            if (result.cycleEnd):
                # print(i)
                if (self.triangleStage[i] != 0):
                    self.triangleStage[i] = (self.triangleStage[i] + 1) % (len(self.stages))
                self.triangleNodes[i].mode = self.getMode(self.stages[self.triangleStage[i]])

# in this pattern:
# i dont remember
class IncrementingColorSwitch(BasePattern):

    def __init__(self, strip = None, startIndex = 0, switcherMode = triangleAnimations.Wipe, switcherColor = Color(255, 0, 0)):
        super().__init__(strip)

        self.switcherMode = switcherMode
        self.switcherColor = switcherColor

        self.triangleIndex = startIndex

        self.triangleNodes[self.triangleIndex].mode = self.switcherMode(color=self.switcherColor)

    def run(self):
        returnValue = False
        if ((self.triangleIndex < len(self.triangleNodes)) and (self.triangleNodes[self.triangleIndex].mode != None)):
            result = self.triangleNodes[self.triangleIndex].mode.run()
            if (len(result.ledsChanged) > 0):
                self.updateStrip(self.triangleIndex, result)
            if (result.cycleEnd):
                self.triangleIndex = self.triangleIndex + 1
                if (self.triangleIndex >= len(self.triangleNodes)):
                    returnValue = True
                else:
                    self.triangleNodes[self.triangleIndex].mode = self.switcherMode(color=self.switcherColor)
                    self.triangleNodes[self.triangleIndex-1].mode = None
                    
        return returnValue
