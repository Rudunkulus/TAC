from methods import draw, actions
from classes import DATA

def mouseClick(data:DATA.Data, win, clock, square:int):
    x, y = data.board.squaresXY[square]
    actions.mouseClick(data, x, y)
    draw.waitForAnimation(data, win, clock)

def keyPress(data:DATA.Data, win, clock, key:str):
    actions.keyPress(data, key)
    draw.waitForAnimation(data, win, clock)