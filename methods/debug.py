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
    """Simulate mouse click.\n
    Square must be a number between -1 and 95\n
    -1 represents the center circle"""
    if square == -1: # center
        x, y = data.constants.xCenter, data.constants.yCenter
    else:
        x, y = data.board.squaresXY[square]
    actions.mouseClick(data, x, y)
    draw.waitForAnimation(data, win, clock)

def keyPress(data:DATA.Data, win, clock, key:str):
    """Simulate key press.\n
    Key must be a string between 1 and number of cards in hand."""
    actions.keyPress(data, key)
    draw.waitForAnimation(data, win, clock)

def botTurn(data:DATA.Data, win, clock, cardIndex=-1, marbleIndex=-1):
    """Simulate a bot turn.\n
    Optional parameters of specific card and marble index can be given.\n
    Defaults to random move if given move is not valid."""
    actions.botTurn(data, cardIndex, marbleIndex)
    draw.waitForAnimation(data, win, clock)
    while data.board.remainderOfPlayedSeven > 0 or data.board.isPlayingATac: # continue move
        actions.botTurn(data)
        draw.waitForAnimation(data, win, clock)