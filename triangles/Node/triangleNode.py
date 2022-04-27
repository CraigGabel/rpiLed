# these are the actual "triangles"

from triangles.Animations.animationResult import AnimationResult
from triangles.Node.nodeTime import NodeTime
from rpi_ws281x import *
import random

class TriangleNode(NodeTime):
    NUM_LEDS = 12

    def __init__(self):
        super().__init__()
        self.mode = None
