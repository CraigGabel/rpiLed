class NodeResult:
    def __init__(self):
        self.ledsChanged = {} # should look like {num: Color(x, x, x), num: Color(x, x, x)}
        self.cycleEnd = False