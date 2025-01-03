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

debug.keyPress(data, win, clock, "2")
debug.mouseClick(data, win, clock, 13)
debug.mouseClick(data, win, clock, 18)
debug.mouseClick(data, win, clock, 18)
debug.mouseClick(data, win, clock, 20)

pass