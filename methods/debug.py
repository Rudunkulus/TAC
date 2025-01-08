from methods import draw, actions
from classes import DATA

def createRemainingPile(cardsInHand:list[list[int]])->list[int]:
    remainigPile = []
    for cardIndex in range(5):
        for player in range(4):
            if cardIndex < len(cardsInHand[player]):
                remainigPile.append(cardsInHand[player][cardIndex])
    return remainigPile

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

def botTurn(data:DATA.Data, win, clock, cardIndex=-1, marbleIndex=-1):
    actions.botTurn(data, cardIndex, marbleIndex)
    draw.waitForAnimation(data, win, clock)
    if data.board.remainderOfPlayedSeven > 0:
        botTurn(data, win, clock)