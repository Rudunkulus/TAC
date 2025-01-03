from methods import draw, actions
from classes import DATA

def mouseClick(data:DATA.Data, win, clock, square:int):
    if square == -1: # center
        x, y = data.constants.xCenter, data.constants.yCenter
    else:
        x, y = data.board.squaresXY[square]
    actions.mouseClick(data, x, y)
    draw.waitForAnimation(data, win, clock)

def keyPress(data:DATA.Data, win, clock, key:str):
    actions.keyPress(data, key)
    draw.waitForAnimation(data, win, clock)

def botTurn(data:DATA.Data, win, clock):
    actions.botTurn(data)
    draw.waitForAnimation(data, win, clock)