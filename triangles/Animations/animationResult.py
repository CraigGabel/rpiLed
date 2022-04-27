# this is used by animations to tell triangleNodes what leds need to be updated

class AnimationResult:
    def __init__(self):
        self.ledsChanged = {} # should look like {num: Color(x, x, x), num: Color(x, x, x)}
        self.cycleEnd = False