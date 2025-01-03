import pygame #GUI using pygame
from classes import DATA
from bots import *
from methods import actions, draw, debug
# from classes import ANIMATION

# animation = ANIMATION.Animation()
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

players = [1,3]
squares = [[],[68,13,50,32],[],[53,76,18,56]]
remainingCards = [1,7,7,1,8,1,13,1,10,1]

# init specific situation:
actions.initSpecificSituation(data, players, squares, remainingCards)
draw.waitForAnimation(data, win, clock)

debug.keyPress(data, win, clock, "3")
debug.mouseClick(data, win, clock, 32)
debug.mouseClick(data, win, clock, 40)
debug.botTurn(data, win, clock)

# templates
debug.botTurn(data, win, clock)
debug.mouseClick(data, win, clock, 50)
debug.keyPress(data, win, clock, "2")