import math
import pygame
from classes import ANIMATION

class Data:
    def __init__(self):
        # self.animation = ANIMATION
        self.parameters = _Parameters()
        self.constants = _Constants(self.parameters.width, self.parameters.height)
        self.board = _Board()
        self.cards = _Cards()
        self.fonts = _Fonts()
        self.marbles = _Marbles()
        self.colours = {
            "black": (0,0,0,0),
            "red": (255,0,0,0),
            "green": (0,255,0,0),
            "blue": (0,0,255,0),
            "yellow": (255,255,0,0),
            "white": (255,255,255,0),
            "grey": (180,180,180,0),
            "wood": (186, 140, 99)
            }
        self.isAnyEntityStillMoving = False
        self.playerSpecific = _PlayerSpecific(self.colours)
        self.text = _Text()

class _Parameters:
    def __init__(self):
        self.width, self.height = 1740, 900
        self.FPS = 60
        self.allowResize = False
        self.players = [2,4] # one based
        self.bots = [1,0,1,1] # player 1 (zero based) is human
        self.amountPerCardType = [0,9,7,7,7,7,7,8,7,7,7,0,7,9] # for testing: only 1-13
        # self.amountPerCardType = [0,9,7,7,7,7,7,8,7,7,7,0,7,9,7,4,1,1,1,1] # all cards
        # self.amountPerCardType = [0,9,0,0,0,0,0,0,0,0,0,0,0,9] # for testing: only 1 & 13

class _Constants:
    def __init__(self, width, height):
        baseUnit = height/2/15 # 3*4unit triangles + 1*2 unit circle + 1*1 unit border = 15 units per radius
        self.xCenter = width / 2
        self.yCenter =  height / 2

        self.board = _ConstantsBoard(baseUnit)
        self.cards = _ConstantsCards(baseUnit, self.xCenter, self.yCenter, self.board.centerRadius)
        self.marbles = _ConstantsMarbles(self.board.squareRadius)

        self.lineThickness = max(int(0.1 * self.board.squareRadius),1) #at least 1
        self.lineThicknessThick = 5 * self.lineThickness

class _ConstantsBoard:
    def __init__(self, baseUnit):
        self.innerCircleRadius = 12 * baseUnit
        self.midCircleRadius = 13 * baseUnit
        self.outerCircleRadius = 14 * baseUnit
        self.squareRadius = 0.5 * baseUnit
        self.projectedSquareRadius = 0.5 * self.squareRadius
        self.centerRadius = 4 * baseUnit
        self.homeRadius = 2 * baseUnit - self.squareRadius
        self.homeDistance = 12 * baseUnit
        self.distanceInHome = 0.6 * baseUnit

        self.lengthTriangle = 4 * baseUnit
        self.heightTriangle = 2*math.sqrt(3) * baseUnit

class _ConstantsCards:
    def __init__(self, baseUnit, xCenter, yCenter, centerRadius):
        # card
        self.width = 2.5 * baseUnit
        self.height = 4 * baseUnit

        self.xSpace = 0.3*baseUnit
        self.ySpace = 0.3*baseUnit

        self.xStep = self.width + self.xSpace
        self.yStep = self.height + self.ySpace

        self.speedSlow = 5
        self.speedFast = 40
        self.yOffsetSelected = -25

        # red cards
        self.redCards = [1,4,7,8,13]

        # discard pile
        self.xDiscardPile = xCenter - 0.7 * self.xStep
        self.yDiscardPile = yCenter

        # draw pile
        self.xRemainingPile = xCenter + 0.7 * self.xStep
        self.yRemainingPile = self.yDiscardPile # same y position as discard pile

        # in hand
        self.yHandDistance = 12 * baseUnit # distance from center
        self.xHandDistance = yCenter + 2.25 * (self.xStep) # distance from center to middle of cards
        # self.handY = yCenter + centerRadius + baseUnit
        # self.handX -> dynamic

class _ConstantsMarbles:
    def __init__(self, squareRadius):
        self.speed = 5
        self.radius = 0.8 * squareRadius

class _Board:
    def __init__(self):
        self.squares = [-1] * (64 + 4*4 + 4*4) # 64 in ring + 4x 4 homes + 4x 4 finishes
        self.squaresXY = []
        self.selectedSquare = -1
        self.projectedSquares = []
        self.playerSequence = []
        self.isDiscardingCards = False
        self.isActivePlayerABot = False
        self.isForcedToSkip = False
        self.remainderOfPlayedSeven = 0

class _Cards:
    def __init__(self):
        self.remainingPile = []
        self.discardPileTopCard:ANIMATION.Card = [] # TODO: see if that works
        self.discardPile = []
        self.inHand = [[],[],[],[]] # TODO: switch to ([],[],[],[])
        self.currentlySelected = -1
        self.isEightSelected = False
    def __len__(self):
        return len(self.inHand)

class _Fonts:
    def __init__(self):
        self.card = 0
    def initFonts(self):
        self.card = pygame.font.SysFont('Comic Sans MS', 70)

# class Images:
#     def __init__(self):
#         self. background = image=pygame.image.load("man"+str(i+1)+".png")

class _Marbles:
    def __init__(self):
        self.marbles:ANIMATION.Marble = [[],[],[],[]] # TODO: switch to ([],[],[],[])
        self.currentlySelected = -1
        self.possibleWaypoints = [] # tupel list
    def __len__(self):
        return len(self.marbles)
    
class _PlayerSpecific:
    def __init__(self, colours):
        self.x = [1, 1, -1, -1]
        self.y = [-1, 1, 1, -1]
        self.entrySquare = [0, 16, 32, 48] # where first marble is placed
        self.colour = [colours["black"], colours["green"], colours["blue"], colours["red"]]
        # self.colour = [(255,255,0),(255,0,0),(0,0,255),(0,255,0)] # black red blue green
    
class _Text:
    def __init__(self):
        self.cards = ("","1","2","3","4","5","6","7","8","9","10","11","12","13","Tr","TAC","Narr","Krieger","Engel", "Teufel") # 0 is for upside down cards
    
# if you want to prevent edits:
class Static:
    def __init__(self):
        self._attribute = [1,2,3]
    def getAttribute(self):
        return self._attribute
    
class BotData:
    def __init__(self):
        self.players = [] # list[int]
        self.marbles = [[],[],[],[]] # list[list[class]]
        self.squares = [] # list[int]
        self.cardsInHand = [] # list[int]
        self.numberOfCardsInHand = 0 # int
        self.discardPile = [] # list[int]
        self.remainingCards = [] # list[int]
        self.isForcedToSkipTurn = False
        self.isPlayingASeven = False
        self.remainderOfSeven = 0