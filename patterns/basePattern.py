# all patterns extend this class
# contains basic functionality all patterns need:
#   define how many triangleNodes exist (TBD: do not hard code the number, pass as an argument)
#   create said triangleNodes
#   create strip object if none exists (this is useful for changing patterns for an existing strip without lengthy delays/clearing current colors)
#   methods to paint new colors to strip (calls to which by extending class) and clear (turn off) leds


from triangles.Animations.animationResult import AnimationResult
from triangles.Node.nodeTime import NodeTime
from triangles.Node.triangleNode import *
from rpi_ws281x import *
import random
import triangles.Animations.triangleAnimations as triangleAnimations
import stripConfig as stripConfig

class BasePattern(NodeTime):
    def __init__(self, strip = None, update = False):
        super().__init__(update)

        (self.triangleNodes, ledCount) = self.getNodes()
        if (strip == None):
            self.strip = stripConfig.init(ledCount)     # this is one of the very few places my code interacts with rpi_ws281x/, and anywhere a pattern file references "strip"
        else:
            self.strip = strip
    
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

    def updateStrip(self, triangleIndex, updates):
        for key, value in updates.ledsChanged.items():
            self.strip.setPixelColor(key + triangleIndex*self.triangleNodes[triangleIndex].mode.numLeds, value)
        self.strip.show()
    
    def clear(self):
        clearColor = Color(0, 0, 0)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, clearColor)
        self.strip.show()