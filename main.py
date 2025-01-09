import pygame #GUI using pygame
from classes import DATA
from bots import *
from methods import actions, draw, initGame
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

initGame.initGame(data)
# initGame.initRandomPosition(data)

while run:
    clock.tick(FPS)
    draw.updateWindow(data, win)

    if data.parameters.bots[data.board.playerSequence[0]]: # TODO: don't use parameters
        try:
            draw.waitForAnimation(data, win, clock)
            actions.botTurn(data)
        except Exception as e: print(e)
        # actions.botTurn(data)

    for event in pygame.event.get(): # Triggering the event
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            try:
                actions.mouseClick(data, x_mouse,y_mouse)
            except Exception as e: print(e)
            
            # actions.mouseClick(data, x_mouse,y_mouse)

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            try:
                actions.keyPress(data, key)
            except Exception as e: print(e)

# debugging
_marbles = [[],[],[],[]]
for square in range(96):
    if data.board.squares[square] != -1:
        _marbles[data.board.squares[square]].append(square)

_cards = [[],[],[],[]]
for player in range (4):
    for cardIndex in range(len(data.cards.inHand[player])):
        _cards[player].append(data.cards.inHand[player][cardIndex].value)
pygame.quit()