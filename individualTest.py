from nodeResult import NodeResult
from nodeTime import NodeTime
from triangleNode import *
from rpi_ws281x import *
import random
import triangleAnimations
import stripConfig as stripConfig

class IndividualTest(NodeTime):
    def __init__(self):
        super().__init__()

        (self.triangleNodes, ledCount) = self.getNodes()
        self.strip = stripConfig.init(ledCount)

        self.colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
        self.colorIndex = 0

        # self.triangleNodes[0].mode = triangleAnimations.BreatheLinear(color=self.colors[self.colorIndex])
        # self.triangleNodes[1].mode = triangleAnimations.BreatheLinear(color=self.colors[self.colorIndex])
        # self.triangleNodes[2].mode = triangleAnimations.Breathe(color=self.colors[self.colorIndex])
        # self.triangleNodes[3].mode = triangleAnimations.Breathe(color=self.colors[self.colorIndex])
        # self.triangleNodes[4].mode = triangleAnimations.BreatheLog(color=self.colors[self.colorIndex])
        # self.triangleNodes[5].mode = triangleAnimations.BreatheLog(color=self.color

        self.triangleNodes[0].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))
        self.triangleNodes[1].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))
        self.triangleNodes[2].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))
        self.triangleNodes[3].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))
        self.triangleNodes[4].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))
        self.triangleNodes[5].mode = triangleAnimations.Phaser(colorStart=Color(255, 0, 0), colorEnd=Color(0,0,255))

        # self.triangleNodes[0].mode = triangleAnimations.Solid()
        # self.triangleNodes[1].mode = triangleAnimations.Solid()
        # self.triangleNodes[2].mode = triangleAnimations.Solid()
        # self.triangleNodes[3].mode = triangleAnimations.Solid()
        # self.triangleNodes[4].mode = triangleAnimations.Solid()
        # self.triangleNodes[5].mode = triangleAnimations.Solid()
        

    def getNodes(self):
        nodes = []
        nodes.append(TriangleNode())
        nodes.append(TriangleNode())
        nodes.append(TriangleNode())
        nodes.append(TriangleNode())
        nodes.append(TriangleNode())
        nodes.append(TriangleNode())

        count = 0
        for i in range(len(nodes)):
            count = count + nodes[i].NUM_LEDS
        
        return (nodes, count)

    def run(self):
        for i in range(len(self.triangleNodes)):
            result = self.triangleNodes[i].mode.run()
            if (len(result.ledsChanged) > 0):
                    for key, value in result.ledsChanged.items():
                        self.strip.setPixelColor(key + i*self.triangleNodes[i].mode.numLeds, value)
                    self.strip.show()
            
    def clear(self):
        clearColor = Color(0, 0, 0)
        # colorWipe(strip, clearColor, 10)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, clearColor)
        self.strip.show()
