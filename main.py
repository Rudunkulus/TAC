import pygame #GUI using pygame
from classes import ACTIONS, CALC, DATA, DRAW
from bots import *
# from classes import ANIMATION

# animation = ANIMATION.Animation()
data = DATA.Data()
calc = CALC.Calc(data)
draw = DRAW.Draw(data, calc)
actions = ACTIONS.Actions(data, calc)
colours = {'blue':(0,0,255), }
colours['blue']

pygame.init()
if data.parameters.allowResize:
    win=pygame.display.set_mode((data.parameters.width, data.parameters.height), pygame.RESIZABLE)
else:
    win=pygame.display.set_mode((data.parameters.width, data.parameters.height))
pygame.display.set_caption("TAC")

FPS=data.parameters.FPS
clock=pygame.time.Clock()
run=True

# actions.initGame()
actions.initRandomGame()

while run:
    clock.tick(FPS)
    draw.updateWindow(win)

    if data.board.isActivePlayerABot:
        # try:
        #     actions.botTurn()
        # except Exception as e: print(e)
        actions.botTurn()

    for event in pygame.event.get(): # Triggering the event
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            try:
                actions.mouseClick(x_mouse,y_mouse)
            except Exception as e: print(e)
            
            # actions.mouseClick(x_mouse,y_mouse)

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            try:
                actions.keyPress(key)
            except Exception as e: print(e)
pygame.quit()