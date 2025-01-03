import pygame #GUI using pygame
from classes import DATA
from bots import *
from methods import actions, draw, calc
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


actions.keyPress(data, "2")
draw.waitForAnimation(data, win, clock)
x, y = calc.square2xy(data, 13)
actions.mouseClick(data, x, y) # select marble
# draw.waitForAnimation(data, win, clock)
x, y = calc.square2xy(data, 18)
actions.mouseClick(data, x, y) # select marble
draw.waitForAnimation(data, win, clock)


# actions.keyPress(data, key)
# actions.mouseClick(data, x_mouse,y_mouse)
# actions.botTurn(data)

pass