import random
from methods import botHelp
from classes import DATA, ANIMATION

def main(botData:DATA.BotData, cardIndex=-1, marbleIndex=-1)->tuple[int,int,int, bool]:
    """Return (cardIndex, marbleIndex, landingSquare, isDiscarding)"""
    decision = DATA.BotDecision()

    if botData.isForcedToSkipTurn:
        discardCard(botData, decision, cardIndex)
    if botData.isPlayingASeven:
        continuePlayedSeven(botData, decision, marbleIndex)
    # elif botData.isPlayingTac:
    #     continuePlayedTac(botData, decision, marbleIndex)
    else:
        playCard(botData, decision, cardIndex, marbleIndex)
    return decision

def playCard(botData:DATA.BotData, decision:DATA.BotDecision, cardIndex=-1, marbleIndex=-1):
    if cardIndex != -1 and marbleIndex != -1: # play specific move
        if tryCombination(botData, decision, cardIndex, marbleIndex): # if move is invalid, continue
            return

    currentPlayer = botData.players[0]
    marblesOfPlayer = botData.marbles[currentPlayer]

    # randomise indices
    randomIndicesCard = list(range(botData.numberOfCardsInHand[currentPlayer]))
    randomIndicesMarble = list(range(len(marblesOfPlayer)))
    random.shuffle(randomIndicesCard)
    random.shuffle(randomIndicesMarble)

    for cardIndex in randomIndicesCard:
        for marbleIndex in randomIndicesMarble:
            if tryCombination(botData, decision, cardIndex, marbleIndex):
                return
    discardCard(botData, decision) # no valid move was found

def continuePlayedSeven(botData:DATA.BotData, decision:DATA.BotDecision, marbleIndex=-1):
    currentPlayer = botData.players[0] # currentPlayer
    marblesOfPlayer = botData.marbles[currentPlayer]

    randomIndicesMarble = list(range(len(marblesOfPlayer)))
    random.shuffle(randomIndicesMarble)

    for marbleIndex in randomIndicesMarble:
        # check if combination is valid
        movesLeft = botData.remainderOfSeven
        marble:ANIMATION.Marble = marblesOfPlayer[marbleIndex]
        possibleSquares = botHelp.getPossibleSquares(botData.squares, currentPlayer, marble.square, movesLeft, marble.isAbleToFinish, 7)
        if possibleSquares: # takes first possible combination
            print("BOT chose following move: cardValue: " + str(movesLeft) + ", marbleSquare = " + str(marble.square) + ", landingSquare = " + str(possibleSquares[-1]))
            decision.marbleIndex = marbleIndex
            decision.landingSquare = possibleSquares[-1]  # take last square if multiple are possible -> prefer going in finish
            return
    discardCard(botData) # no valid move was found

def discardCard(botData:DATA.BotData, decision:DATA.BotDecision, cardIndex=-1):
    if cardIndex == -1: # default: random card
        decision.cardIndex = random.randint(0,len(botData.cardsInHand)-1)
    else:
        decision.cardIndex = cardIndex
    decision.isDiscarding = True

def tryCombination(botData:DATA.BotData, decision:DATA.BotDecision, cardIndex:int, marbleIndex:int)->bool:
    """Try combination of marble and card and if valid, sets decision\n
    Return True if there is one or multiple valid moves.\n
    If multiple moves are possible, take furthest advanced."""
    currentPlayer = botData.players[0] # currentPlayer
    marblesOfPlayer = botData.marbles[currentPlayer]
    marble:ANIMATION.Marble = marblesOfPlayer[marbleIndex]
    cardValue = botData.cardsInHand[cardIndex]

    if cardValue == 15: # if played TAC: take value of previously played non-tac card
        index = -1
        while cardValue == 15:
            cardValue = botData.discardPile[index]
            index -= 1

    possibleSquares = botHelp.getPossibleSquares(botData.squares, currentPlayer, marble.square, cardValue, marble.isAbleToFinish, cardValue)
    if possibleSquares: # takes first possible combination
        print("BOT chose following move: cardValue: " + str(cardValue) + ", marbleSquare = " + str(marble.square) + ", landingSquare = " + str(possibleSquares[-1]))
        decision.cardIndex = cardIndex
        decision.marbleIndex = marbleIndex
        decision.landingSquare = possibleSquares[-1]  # take last square if multiple are possible -> prefer going in finish
        return True
    return False