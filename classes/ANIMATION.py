# class Animation:
#     def __init__(self):
#         # self.card = Card()
#         # self.marble = Marble()
#         pass

class Card:
    def __init__(self):
        self.owner = -1
        self.value = 0
        self.vel = 0
        self.x = 0
        self.y = 0
        self.isSelected = False
        self.isVisible = True
        self.isShowingValue = True
        self.waypoints = [] # tupel e.g. (0,0)

class Marble:
    def __init__(self):
        self.owner = -1
        self.x, self.y = 0, 0
        self.colour = (0,0,0)

        self.square = -1
        self.isSelected = 0
        self.vel = 10
        self.isAbleToFinish = False
        self.waypoints = [] # tupel e.g. (0,0)
        self.radius = 12