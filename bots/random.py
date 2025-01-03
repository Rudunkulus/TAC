from methods import botHelp
from classes import DATA

def main(botData:DATA.BotData)->tuple[int,int,int, bool]:
    """Return (cardIndex, marbleIndex, landingSquare, isDiscarding)"""

    ############################################################################################################################################################
    # players: players is a list of all players in order of sequence.
    # eg [3,0,1] -> currently it is player 3's turn, after that it is player 0's turn and after that player 1
    # (zero based: player 0 ^= player #1)

    # marbles: list of lists of classes of marbles
    # has follwing attributes:
    # owner: range 0-3
    # square: position on board, range 0-95 (see next paragraph)
    # isAbleToFinish: specifies whether the marble is able to enter the finish squares (is enabled after its first move)

    # squares: describes the current board. it has 96 entries:
    # 0-63: ring
    # 64-67: home base of player 0 (top right corner)
    # 68-79: home bases of players 1-3
    # 80-83: finishing squares of player 0 (in middle to the right)
    # 84-95: finishing squares of players 1-3
    # 0,16,32,48: home squares of players 0-3
    # the entry is -1 if no marble occupies that square and 0-3 if a marble of a player occupies that square
    # eg squares[16] = 2 -> the homesquare of player 1 is occupied by a marble of player 2

    # cardsInHand: a list of cards currently held in hand
    # list length may range from 1 (only one card in hand) to 5 (freshly dealt cards)
    # value of entry shows what card it is:
    # 1-13: cards with value 1-13
    # 14: Trickser
    # 15: TAC
    # 16: Engel 
    # 17: Teufel
    # 18: Krieger
    # 19: Narr
    # eg [7,1,7,14] -> player has one "1", two "7"s and one "Trickser"

    # numberOfCardsInHand: a list showing how many cards each player has
    # careful: length of list is always 4, regardless of how many players are in game
    # careful: first entry is for player 0, not the for active player -> different to "players" list

    # discardPile: a list of all played or discarded cards
    # first entry is first played card (bottom of pile)
    # last entry is last played card (top of pile)

    # remainingCards: a list showing the amount of each card left
    # eg remainingCards[2]=4 -> there are 4 "2"s remaining
    # reminder: some of these cards could be in other player's hand
    # remainingCards[0] and remainingCards[11] are always =0 since there are no "0"s and "11"s in the game

    # botHelp: contains useful functions
    # TODO: explain more

    # for returning:

    # card: index of card in cardsInHand that you want to play
    # domain is from 0 to number of cards in hand minus 1
    # eg card=1 -> play the second card in hand
    
    # marble: index of marble that you want to play
    # domain is from 0 to 3
    # careful: marble 0 is not the furthest advanced marble but the marble that started at the top right square of your home base

    # landingSquare: square that you want your marble to land on after playing your card
    # the program will check if the combination of marble, card and landingSquare is valid
    # if the combination is not valid or any value exceeds its domain, a random valid move will be chosen
    # if no valid move is possible, the returned card will be discarded
    # if the returned card exceeds its domain and no valid move is possible, a random card will be discarded
    #########################################################################################################################################################

    if botData.isForcedToSkipTurn:
        discardCard(botData)
    if botData.isPlayingASeven:
        continuePlayedSeven(botData)
    else:
        playCard(botData)

def playCard(botData:DATA.BotData):
    currentPlayer = botData.players[0] # currentPlayer
    marblesOfPlayer = botData.marbles[currentPlayer]
    for cardIndex in range(len(botData.cardsInHand)):
        for marbleIndex in range(len(marblesOfPlayer)):
            # check if combination is valid
            cardValue = botData.cardsInHand[cardIndex]
            marble = marblesOfPlayer[marbleIndex]
            possibleSquares = botHelp.getPossibleSquares(botData.squares, marble.square, cardValue, currentPlayer, marble.isAbleToFinish, cardValue==7)
            if possibleSquares: # takes first possible combination
                print("BOT decided following move: cardValue: " + str(cardValue) + ", marbleSquare = " + str(marble.square) + ", landingSquare = " + str(possibleSquares[0]))
                return cardIndex, marbleIndex, possibleSquares[0], False # take first square if multiple are possible
    discardCard(botData) # no valid move was found

def discardCard(botData:DATA.BotData):
    cardIndex = 0 # discard first card
    return cardIndex, 0, 0, True # marbleIndex and landingSquare don't matter

def continuePlayedSeven(botData:DATA.BotData):
    currentPlayer = botData.players[0] # currentPlayer
    marblesOfPlayer = botData.marbles[currentPlayer]
    for marbleIndex in range(len(marblesOfPlayer)):
        # check if combination is valid
        cardValue = botData.remainderOfSeven
        marble = marblesOfPlayer[marbleIndex]
        if cardValue == 7 or botData.isPlayingASeven:
            isPlayingASeven = True
        else:
            isPlayingASeven = False
        possibleSquares = botHelp.getPossibleSquares(botData.squares, marble.square, cardValue, currentPlayer, marble.isAbleToFinish, isPlayingASeven)
        if possibleSquares: # takes first possible combination
            print("BOT decided following move: cardValue: " + str(cardValue) + ", marbleSquare = " + str(marble.square) + ", landingSquare = " + str(possibleSquares[0]))
            return 0, marbleIndex, possibleSquares[0], False # take first square if multiple are possible
    discardCard(botData) # no valid move was found