# a single triangleNode is able to run simple patterns (triangleAnimations) among its 12 leds
# these are those animations


from triangles.Animations.triangleAnimationResult import TriangleAnimationResult
from triangles.Node.nodeTime import NodeTime
from triangles.Animations.baseTriangleAnimation import BaseTriangleAnimation
from rpi_ws281x import *
import random

logBrightnessCurve = [
    0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0, 
    0,   0,   1,   1,   1,   1,   1,   1,
    1,   1,   1,   1,   1,   1,   1,   1, 
    1,   1,   1,   1,   1,   1,   1,   1,
    1,   1,   2,   2,   2,   2,   2,   2, 
    2,   2,   2,   2,   2,   2,   2,   2,
    2,   3,   3,   3,   3,   3,   3,   3, 
    3,   3,   3,   3,   3,   4,   4,   4,
    4,   4,   4,   4,   4,   4,   5,   5, 
    5,   5,   5,   5,   5,   5,   6,   6,
    6,   6,   6,   6,   6,   7,   7,   7, 
    7,   7,   8,   8,   8,   8,   8,   9,
    9,   9,   9,   9,  10,  10,  10,  10, 
   11,  11,  11,  11,  12,  12,  12,  12,
   13,  13,  13,  14,  14,  14,  15,  15, 
   15,  16,  16,  16,  17,  17,  18,  18,
   18,  19,  19,  20,  20,  21,  21,  22, 
   22,  23,  23,  24,  24,  25,  25,  26,
   26,  27,  28,  28,  29,  30,  30,  31, 
   32,  32,  33,  34,  35,  35,  36,  37,
   38,  39,  40,  40,  41,  42,  43,  44, 
   45,  46,  47,  48,  49,  51,  52,  53,
   54,  55,  56,  58,  59,  60,  62,  63, 
   64,  66,  67,  69,  70,  72,  73,  75,
   77,  78,  80,  82,  84,  86,  88,  90, 
   91,  94,  96,  98, 100, 102, 104, 107,
  109, 111, 114, 116, 119, 122, 124, 127, 
  130, 133, 136, 139, 142, 145, 148, 151,
  155, 158, 161, 165, 169, 172, 176, 180, 
  184, 188, 192, 196, 201, 205, 210, 214,
  219, 224, 229, 234, 239, 244, 250, 255
]

def ColorLinear(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue


def ColorLog(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	# return (white << 24) | (red << 16)| (green << 8) | blue
	return (logBrightnessCurve[white] << 24) | (logBrightnessCurve[red] << 16)| (logBrightnessCurve[green] << 8) | logBrightnessCurve[blue]

def ColorLinearToLog(color):
    white = (color >> 24) & 0xFF
    red = (color >> 16) & 0xFF
    green = (color >> 8) & 0xFF
    blue = (color >> 0) & 0xFF
    return (logBrightnessCurve[white] << 24) | (logBrightnessCurve[red] << 16)| (logBrightnessCurve[green] << 8) | logBrightnessCurve[blue]

class Solid(NodeTime):

    def __init__(self, color = Color(255, 0, 0), updateRate = 1000, numLeds = 12, update = False):
        self.init(color, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), updateRate = 1000, numLeds = 12, update = False):
        super().__init__(update)
        # self.solidColor = ColorLinearToLog(color)
        self.solidColor = color
        self.updateRate = updateRate
        self.numLeds = numLeds

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            for i in range(self.numLeds):
                returnValue.ledsChanged[i] = self.solidColor
            returnValue.cycleEnd = True
        return returnValue
        
class SingleCircle(NodeTime):

    def __init__(self, color = Color(255, 0, 0), isBackwards = False, startIndex = 0, updateRate = 40, numLeds = 12, update = False):
        self.init(color, isBackwards, startIndex, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), isBackwards = False, startIndex = 0, updateRate = 40, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        # self.singleCircleColor = ColorLinearToLog(color)
        self.singleCircleColor = color
        self.isBackwards = isBackwards
        self.singleCircleStartIndex = startIndex
        self.singleCircleLedIndex = self.singleCircleStartIndex

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            thisIndex = self.numLeds - 1 - self.singleCircleLedIndex if self.isBackwards else self.singleCircleLedIndex
            returnValue.ledsChanged[thisIndex] = self.singleCircleColor
            self.singleCircleLedIndex = self.singleCircleLedIndex + 1
            if ((self.singleCircleLedIndex >= self.numLeds)):
                self.singleCircleLedIndex = 0
            if (self.singleCircleLedIndex == self.singleCircleStartIndex):
                returnValue.cycleEnd = True
            
        return returnValue
        
class TripleCircle(NodeTime):

    def __init__(self, colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)], isBackwards = False, startIndex = 0, updateRate = 50, numLeds = 12, update = False):
        self.init(colors, isBackwards, startIndex, updateRate, numLeds, update)

    def init(self, colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)], isBackwards = False, startIndex = 0, updateRate = 50, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        self.tripleCircleColors = colors

        for i in range(len(self.tripleCircleColors)):
            self.tripleCircleColors[i] = ColorLinearToLog(self.tripleCircleColors[i])

        self.isBackwards = isBackwards
        self.tripleCircleStartIndex = startIndex
        self.tripleCircleLedIndex = self.tripleCircleStartIndex

        self.tripleCircleColorIndex = 0

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            index0 = self.numLeds - 1 - self.tripleCircleLedIndex if self.isBackwards else self.tripleCircleLedIndex
            index1 = (index0 + (1*self.numLeds//3)) % (self.numLeds)
            index2 = (index1 + (1*self.numLeds//3)) % (self.numLeds)
            if (self.isBackwards):
                index1, index2 = index2, index1
            returnValue.ledsChanged[index0] = self.tripleCircleColors[self.tripleCircleColorIndex]
            returnValue.ledsChanged[index1] = self.tripleCircleColors[(self.tripleCircleColorIndex+1)%len(self.tripleCircleColors)]
            returnValue.ledsChanged[index2] = self.tripleCircleColors[(self.tripleCircleColorIndex+2)%len(self.tripleCircleColors)]
            self.tripleCircleLedIndex = self.tripleCircleLedIndex + 1
            if (self.tripleCircleLedIndex >= self.numLeds):
                self.tripleCircleLedIndex = 0
            if (self.tripleCircleLedIndex == self.tripleCircleStartIndex):
                returnValue.cycleEnd = True
        return returnValue      

class Wipe(NodeTime):

    def __init__(self, color = Color(255, 0, 0), isBackwards = False, startCorner = 0, updateRate = 100, numLeds = 12, update = False):
        self.init(color, isBackwards, startCorner, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), isBackwards = False, startCorner = 0, updateRate = 100, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        # self.wipeColor = ColorLinearToLog(color)
        self.wipeColor = color
        self.isBackwards = isBackwards
        self.wipeStartCorner = startCorner
        self.wipeLedIndex = self.numLeds//3 if (self.isBackwards) else 0

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            startIndex0 = 0 + self.wipeStartCorner*self.numLeds//3
            startIndex1 = (startIndex0 if (startIndex0 != 0) else self.numLeds) - 1
            endIndex = (startIndex0 + self.numLeds//3) % self.numLeds
            
            index0 = startIndex0 + self.wipeLedIndex
            index1 = startIndex1 - self.wipeLedIndex
            
            if (self.wipeLedIndex >= self.numLeds // 3):
                for i in range(self.numLeds//3):
                    returnValue.ledsChanged[endIndex + i] = self.wipeColor
            else:
                returnValue.ledsChanged[index0] = self.wipeColor
                returnValue.ledsChanged[index1] = self.wipeColor
            
            self.wipeLedIndex = self.wipeLedIndex + (-1 if (self.isBackwards) else 1)
            if (self.wipeLedIndex > self.numLeds // 3):
                self.wipeLedIndex = 0
                returnValue.cycleEnd = True
            elif (self.wipeLedIndex < 0):
                self.wipeLedIndex = self.numLeds // 3
                returnValue.cycleEnd = True
                
        return returnValue

class Breathe(NodeTime):

    def __init__(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        self.init(color, steps, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        self.breatheColor = color
        self.steps = steps

        self.breatheStepIndex = 0
        self.breatheAdjustment = 1

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            tempR = (self.breatheColor >> 16) & 255
            tempG = (self.breatheColor >> 8) & 255
            tempB = (self.breatheColor >> 0) & 255
            tempR = self.breatheStepIndex * tempR // self.steps
            tempG = self.breatheStepIndex * tempG // self.steps
            tempB = self.breatheStepIndex * tempB // self.steps
            newColor = ColorLinearToLog(tempR, tempG, tempB)
            self.breatheStepIndex = self.breatheStepIndex + self.breatheAdjustment
            if (self.breatheStepIndex >= self.steps):
                self.breatheAdjustment = -1 * self.breatheAdjustment
            if (self.breatheStepIndex <= 0):
                self.breatheAdjustment = -1 * self.breatheAdjustment
                returnValue.cycleEnd = True
            for i in range(self.numLeds):
                returnValue.ledsChanged[i] = newColor
                
        return returnValue

class BreatheLog(NodeTime):

    def __init__(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        self.init(color, steps, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        self.breatheColor = color
        self.steps = steps

        self.breatheStepIndex = 0
        self.breatheAdjustment = 1

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            tempR = (self.breatheColor >> 16) & 255
            tempG = (self.breatheColor >> 8) & 255
            tempB = (self.breatheColor >> 0) & 255
            tempR = self.breatheStepIndex * tempR // self.steps
            tempG = self.breatheStepIndex * tempG // self.steps
            tempB = self.breatheStepIndex * tempB // self.steps
            newColor = ColorLog(tempR, tempG, tempB)
            self.breatheStepIndex = self.breatheStepIndex + self.breatheAdjustment
            if (self.breatheStepIndex >= self.steps):
                self.breatheAdjustment = -1 * self.breatheAdjustment
            if (self.breatheStepIndex <= 0):
                self.breatheAdjustment = -1 * self.breatheAdjustment
                returnValue.cycleEnd = True
            for i in range(self.numLeds):
                returnValue.ledsChanged[i] = newColor
                
        return returnValue

class BreatheLinear(NodeTime):

    def __init__(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        self.init(color, steps, updateRate, numLeds, update)

    def init(self, color = Color(255, 0, 0), steps = 50, updateRate = 20, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        self.breatheColor = color
        self.steps = steps

        self.breatheStepIndex = 0
        self.breatheAdjustment = 1

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            tempR = (self.breatheColor >> 16) & 255
            tempG = (self.breatheColor >> 8) & 255
            tempB = (self.breatheColor >> 0) & 255
            tempR = self.breatheStepIndex * tempR // self.steps
            tempG = self.breatheStepIndex * tempG // self.steps
            tempB = self.breatheStepIndex * tempB // self.steps
            newColor = ColorLinear(tempR, tempG, tempB)
            self.breatheStepIndex = self.breatheStepIndex + self.breatheAdjustment
            if (self.breatheStepIndex >= self.steps):
                self.breatheAdjustment = -1 * self.breatheAdjustment
            if (self.breatheStepIndex <= 0):
                self.breatheAdjustment = -1 * self.breatheAdjustment
                returnValue.cycleEnd = True
            for i in range(self.numLeds):
                returnValue.ledsChanged[i] = newColor
                
        return returnValue

class Phaser(NodeTime):

    def __init__(self, colorStart = Color(255, 0, 0), colorEnd = Color(0, 0, 255), steps = 50, cooldownSteps = 20, updateRate = 20, numLeds = 12, update = False):
        self.init(colorStart, colorEnd, steps, cooldownSteps, updateRate, numLeds, update)

    def init(self, colorStart = Color(255, 0, 0), colorEnd = Color(0, 0, 255), steps = 50, cooldownSteps = 20, updateRate = 20, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

        self.phaserColorStart = colorStart
        self.phaserColorEnd = colorEnd
        self.phaserSteps = steps

        self.cooldownSteps = cooldownSteps
        self.cooldownStepIndex = 0
        self.cooldownStage = 0

        self.phaserOffsetR = 0
        self.phaserOffsetG = 0
        self.phaserOffsetB = 0
        self.phaserStepR = 0
        self.phaserStepG = 0
        self.phaserStepB = 0
        self.phaserStepIndex = 0

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            if (self.cooldownStage == 1):
                self.cooldownStepIndex = self.cooldownStepIndex + 1
                if (self.cooldownStepIndex >= self.phaserSteps):
                    self.cooldownStepIndex = 0
                    self.cooldownStage = 0
                    returnValue.cycleEnd = True
            else:
                newColor = Color(0,0,0)
                if (self.phaserStepIndex == 0):
                    self.phaserOffsetR = (self.phaserColorStart >> 16) & 0xFF
                    self.phaserOffsetG = (self.phaserColorStart >> 8) & 0xFF
                    self.phaserOffsetB = (self.phaserColorStart >> 0) & 0xFF
                    endR = (self.phaserColorEnd >> 16) & 0xFF
                    endG = (self.phaserColorEnd >> 8) & 0xFF
                    endB = (self.phaserColorEnd >> 0) & 0xFF
                    self.phaserStepR = (endR - self.phaserOffsetR) // self.phaserSteps
                    self.phaserStepG = (endG - self.phaserOffsetG) // self.phaserSteps
                    self.phaserStepB = (endB - self.phaserOffsetB) // self.phaserSteps
                    newColor = self.phaserColorStart
                else:
                    tempR = self.phaserOffsetR + self.phaserStepR*self.phaserStepIndex
                    if (tempR > 255):
                        tempR = 255
                    if (tempR < 0):
                        tempR = 0                
                    tempG = self.phaserOffsetG + self.phaserStepG*self.phaserStepIndex
                    if (tempG > 255):
                        tempG = 255
                    if (tempG < 0):
                        tempG = 0
                    tempB = self.phaserOffsetB + self.phaserStepB*self.phaserStepIndex
                    if (tempB > 255):
                        tempB = 255
                    if (tempB < 0):
                        tempB = 0
                    newColor = Color(tempR, tempG, tempB)

                # newColor = ColorLinearToLog(newColor)

                self.phaserStepIndex = self.phaserStepIndex + 1
                if (self.phaserStepIndex >= self.phaserSteps):
                    self.phaserStepIndex = 0
                    # returnValue.cycleEnd = True
                    self.cooldownStage = 1
                
                for i in range(self.numLeds):
                    returnValue.ledsChanged[i] = newColor
                
        return returnValue

class Randy(NodeTime):

    def __init__(self, updateRate = 500, numLeds = 12, update = False):
        self.init(updateRate, numLeds, update)

    def init(self, updateRate = 500, numLeds = 12, update = False):
        super().__init__(update)
        self.updateRate = updateRate
        self.numLeds = numLeds

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            tempR = random.randint(0, 255)
            tempG = random.randint(0, 255)
            tempB = random.randint(0, 255)
            newColor = ColorLinearToLog(tempR, tempG, tempB)
            for i in range(self.numLeds):
                returnValue.ledsChanged[i] = newColor
                
        return returnValuey

class Temp(BaseTriangleAnimation):

    def __init__(self, colorStart = Color(255, 0, 0), colorEnd = Color(0, 0, 255), steps = 50, cooldownSteps = 20, updateRate = 20, update = False):
        self.init(colorStart, colorEnd, steps, cooldownSteps, updateRate, update)

    def init(self, colorStart = Color(255, 0, 0), colorEnd = Color(0, 0, 255), steps = 50, cooldownSteps = 20, updateRate = 20, update = False):
        super().__init__(update = update)
        self.updateRate = updateRate

        self.phaserColorStart = colorStart
        self.phaserColorEnd = colorEnd
        self.phaserSteps = steps

        self.cooldownSteps = cooldownSteps
        self.cooldownStepIndex = 0
        self.cooldownStage = 0

        self.phaserOffsetR = 0
        self.phaserOffsetG = 0
        self.phaserOffsetB = 0
        self.phaserStepR = 0
        self.phaserStepG = 0
        self.phaserStepB = 0
        self.phaserStepIndex = 0

        print(str(self.getNumLeds()))
        print('wtf')

    def run(self):
        returnValue = TriangleAnimationResult()
        if (self.compareTime(self.updateRate)):
            if (self.isCooldownActive() == 1):
                result = self.cooldownRun()
                if (result == 1):
                    returnValue.cycleEnd = True

                # print('cooldown')
                # self.cooldownStepIndex = self.cooldownStepIndex + 1
                # if (self.cooldownStepIndex >= self.cooldownSteps):
                #     self.cooldownStepIndex = 0
                #     self.cooldownStage = 0
                #     returnValue.cycleEnd = True
            else:
                print('normal')
                newColor = Color(0,0,0)
                if (self.phaserStepIndex == 0):
                    self.phaserOffsetR = (self.phaserColorStart >> 16) & 0xFF
                    self.phaserOffsetG = (self.phaserColorStart >> 8) & 0xFF
                    self.phaserOffsetB = (self.phaserColorStart >> 0) & 0xFF
                    endR = (self.phaserColorEnd >> 16) & 0xFF
                    endG = (self.phaserColorEnd >> 8) & 0xFF
                    endB = (self.phaserColorEnd >> 0) & 0xFF
                    self.phaserStepR = (endR - self.phaserOffsetR) // self.phaserSteps
                    self.phaserStepG = (endG - self.phaserOffsetG) // self.phaserSteps
                    self.phaserStepB = (endB - self.phaserOffsetB) // self.phaserSteps
                    newColor = self.phaserColorStart
                else:
                    tempR = self.phaserOffsetR + self.phaserStepR*self.phaserStepIndex
                    if (tempR > 255):
                        tempR = 255
                    if (tempR < 0):
                        tempR = 0                
                    tempG = self.phaserOffsetG + self.phaserStepG*self.phaserStepIndex
                    if (tempG > 255):
                        tempG = 255
                    if (tempG < 0):
                        tempG = 0
                    tempB = self.phaserOffsetB + self.phaserStepB*self.phaserStepIndex
                    if (tempB > 255):
                        tempB = 255
                    if (tempB < 0):
                        tempB = 0
                    newColor = Color(tempR, tempG, tempB)

                # newColor = ColorLinearToLog(newColor)

                self.phaserStepIndex = self.phaserStepIndex + 1
                if (self.phaserStepIndex >= self.phaserSteps):
                    self.phaserStepIndex = 0
                    # returnValue.cycleEnd = True
                    self.startCooldown()
                
                for i in range(self.getNumLeds()):
                    returnValue.ledsChanged[i] = newColor
                
        return returnValue
        