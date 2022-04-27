# these are the actual "triangles"

from triangles.Node.nodeTime import NodeTime

class TriangleNode(NodeTime):
    NUM_LEDS = 12

    def __init__(self):
        super().__init__()
        self.mode = None
