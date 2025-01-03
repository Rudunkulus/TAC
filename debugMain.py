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

# init specific situation:
actions.initSpecificSituation(data)
draw.waitForAnimation(data, win, clock)

debug.keyPress(data, win, clock, "3")
debug.mouseClick(data, win, clock, 32)
debug.mouseClick(data, win, clock, -1)
debug.keyPress(data, win, clock, "3")
debug.mouseClick(data, win, clock, -1)

# templates
debug.botTurn(data, win, clock)
debug.mouseClick(data, win, clock, 50)
debug.keyPress(data, win, clock, "2")