import pygame #GUI using pygame
from classes import DATA
from bots import *
from methods import draw, debug, initGame

data = DATA.Data()

pygame.init()
if data.parameters.allowResize:
    win=pygame.display.set_mode((data.parameters.width, data.parameters.height), pygame.RESIZABLE)
else:
    win=pygame.display.set_mode((data.parameters.width, data.parameters.height))
pygame.display.set_caption("TAC")

FPS=data.parameters.FPS
clock=pygame.time.Clock()
run=True

######################
# begin editing here #
######################

players = [1,3]
marbles = [[],[68,14,50,32],[],[53,76,38,56]]
cards = [[],[1,7,8,14,15],[],[15,7,1,1,1]]

remainingCards = debug.createRemainingPile(cards)
# for i in range(40):
#     remainingCards.append(10)

# init specific situation or random game:
initGame.initSpecificSituation(data, players, marbles, remainingCards)
# initGame.initRandomPosition(data)

draw.waitForAnimation(data, win, clock)

# templates
debug.botTurn(data, win, clock)
debug.mouseClick(data, win, clock, 50)
debug.keyPress(data, win, clock, "2")