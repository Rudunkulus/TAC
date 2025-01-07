import random
import operator
from classes import ANIMATION, DATA
from methods import botHelp, calc
from bots import random as botRandom
from bots import template as botTemplate

def mouseClick(data:DATA.Data, x:float, y:float)->None:
    square = calc.getClickedSquare((x, y), data.board.squaresXY, data.constants.board.squareRadius) # TODO: revert back to (data,...)
    card = calc.getClosestCard(data, x,y)
    if square != -1 and not data.board.isForcedToSkip: # selected square
        if square in data.board.projectedSquares: # selected projected square
            # player move
            _doAction(data, calc.getActiveCard(data), calc.getMarble(data, data.board.selectedSquare), square, False)
            if data.board.remainderOfPlayedSeven == 0: # keep card if in middle of playing 7
                _discardCard(data)
            _nextTurn(data)
            _updateSquares(data)
            return
        # selected square with own marble or selected any marble on ring if playing trickser:
        if data.board.squares[square] == calc.getActivePlayer(data) or (calc.getActiveCard(data).value == 14 and data.board.squares[square] != -1 and square < 64):
            _toggleSelectMarble(data, square)
            return
    if calc.isXYInCenterCircle(data, x, y) and data.cards.currentlySelected != -1: # clicked in center circle while a card was selected
        # order is important: check tac first, in case of reversing a skip

        # if playing TAC:
        if calc.getActiveCard(data).value == 15:
            data.board.isPlayingTac = True
            # calc.getActiveCard(data).value = data.cards.discardPileTopCard.value # TODO: handle multiple TACs in a row
            _undoPreviousMove(data)
            _updateSquares
            return
        
        # if forced to skip: discard
        if data.board.isForcedToSkip:
            data.board.isForcedToSkip = False
            _discardCard(data)
            _nextTurn(data)
            return
        
        if calc.getActiveCard(data).value == 8 and botHelp.canPlayerPlaySpecialCards:
            data.board.isForcedToSkip = True
            _discardCard(data)
            _nextTurn(data)
        return
    
    # card in hand was selected and player is not in the middle of playing a seven or a tac
    if card in range(5) and data.board.remainderOfPlayedSeven == 0 and not data.board.isPlayingTac: 
        _toggleSelectCard(data, card)
        
def keyPress(data:DATA.Data, key:str)->None:
    # card in hand was selected and player is not in the middle of playing a seven or a tac
    if key in ["1","2","3","4","5"] and data.board.remainderOfPlayedSeven == 0 and not data.board.isPlayingTac:
        cardSelected = int(key)-1 # key one based to zero based
        numberOfCardsInHand = len(data.cards.inHand[calc.getActivePlayer(data)])
        if cardSelected < numberOfCardsInHand: # only select if card spot is not empty
            _toggleSelectCard(data, cardSelected)

def botTurn(data:DATA.Data, cardIndex=-1, marbleIndex=-1):
    botData = _getBotData(data)
    botDecision:DATA.BotDecision = botTemplate.main(botData) # (cardIndex, marbleIndex, landingSquare, isDiscarding) #TODO: validate structure of botDecision
    if not _isMoveValid(data, botDecision):
        print("Move is invalid, falling back to random move")
        botDecision = botRandom.main(botData, cardIndex, marbleIndex)
    if not botData.isPlayingASeven: # new card selected
        data.cards.currentlySelected = botDecision.cardIndex
    card:ANIMATION.Card = data.cards.inHand[calc.getActivePlayer(data)][data.cards.currentlySelected]
    marble:ANIMATION.Marble = data.marbles.marbles[calc.getActivePlayer(data)][botDecision.marbleIndex]

    if card.value == 15:
        _undoPreviousMove(data)
    _doAction(data, card, marble, botDecision.landingSquare, botDecision.isDiscarding)

    # rest of the move
    if data.board.remainderOfPlayedSeven == 0:
        _discardCard(data)
    _updateSquares(data)
    _nextTurn(data)
    return

def _getBotData(data:DATA.Data):
    players = data.board.playerSequence.copy()
    activePlayer = calc.getActivePlayer(data)
    cardsInHand = []
    squares = data.board.squares.copy()
    discardPile = data.cards.discardPile.copy()
    remainingPile = data.cards.remainingPile.copy()
    numberOfCardsInHand = [0,0,0,0]
    card:ANIMATION.Card
    for player in players:
        numberOfCardsInHand[player] = len(data.cards.inHand[player])
        for card in data.cards.inHand[player]:
            if player != activePlayer:
                remainingPile.append(card.value) # add cards of other players to remaining pile since the bot doesn't know if they're in hand or in remaining pile
            else:
                cardsInHand.append(card.value) # add own cards to hand
    # remaining pile to amount of each card
    remainingCards = [0] * 20 # 20 different cards [including 0]
    for cardValue in remainingPile:
        remainingCards[cardValue] += 1

    # transform marbles to botmarbles
    marblesForBots = [[],[],[],[]]
    marble:ANIMATION.Marble
    for player in players:
        for marble in data.marbles.marbles[player]:
            marbleForBots = ANIMATION.MarbleForBots()
            marbleForBots.owner = player
            marbleForBots.square = marble.square
            marbleForBots.isAbleToFinish = marble.isAbleToFinish
            marblesForBots[player].append(marbleForBots)

    # store in botData # TODO: clean up
    botData = DATA.BotData()
    botData.players = players
    botData.marbles = marblesForBots
    botData.squares = squares
    botData.cardsInHand = cardsInHand
    botData.numberOfCardsInHand = numberOfCardsInHand
    botData.discardPile = discardPile
    botData.remainingCards = remainingCards
    if data.board.remainderOfPlayedSeven > 0:
        botData.isPlayingASeven = True
        botData.remainderOfSeven = data.board.remainderOfPlayedSeven
    else:
        botData.isPlayingASeven = False
        botData.remainderOfSeven = 0
    botData.isForcedToSkipTurn = data.board.isForcedToSkip
    botData.isPlayingTac = data.board.isPlayingTac
    botData.valueOfTac = data.board.valueOfTac
    return botData

def _isMoveValid(data:DATA.Data, botDecision:DATA.BotDecision)->bool:
    """Return True if move is valid"""
    card:ANIMATION.Card = data.cards.inHand[calc.getActivePlayer(data)][botDecision.cardIndex]
    marble:ANIMATION.Marble = data.marbles.marbles[calc.getActivePlayer(data)][botDecision.marbleIndex] 

    # only allowed to discard if forced to or played card is a tac or 8
    if botDecision.isDiscarding and not (data.board.isForcedToSkip or card.value in [8,15]): # false flag
        return True

    _createProjectedSquares(data, card, marble)
    if botDecision.landingSquare in data.board.projectedSquares: # move is valid
        data.board.projectedSquares = []
        return True
    data.board.projectedSquares = []
    return False

def _toggleSelectMarble(data:DATA.Data, clickedSquare:int)->None:
    if clickedSquare == data.board.selectedSquare: # unselect marble
        data.board.selectedSquare = -1
        data.board.projectedSquares = [] # clear projected squares
    else: # select marble
        data.board.selectedSquare = clickedSquare
        marble = calc.getMarble(data, clickedSquare)
        if data.cards.currentlySelected != -1:
            _createProjectedSquares(data, calc.getActiveCard(data), marble)

def _toggleSelectCard(data:DATA.Data, cardIndex:int)->None:
    yOffsetSelected = data.constants.cards.yOffsetSelected
    yNormal = data.constants.yCenter + data.playerSpecific.y[calc.getActivePlayer(data)] * data.constants.cards.yHandDistance
    yRaised = yNormal + yOffsetSelected

    if data.cards.currentlySelected != cardIndex: # select a card #TODO: can't select TAC as first card of round
        card = data.cards.inHand[calc.getActivePlayer(data)][cardIndex]
        if data.cards.currentlySelected != -1:
            # unselect other cards
            print(data.cards.currentlySelected)
            previousCard = calc.getActiveCard(data)
            previousCard.isSelected = False # unselect old card
            previousCard.waypoints = [(previousCard.x, yNormal)] # lower card TODO: hard code x position
            
            # check if switching from trickser to non-trickser and also having a marble of another player selected -> unselect that marble
            if previousCard.value == 14 and card.value != 14 and data.board.squares[data.board.selectedSquare] != calc.getActivePlayer(data):
                data.board.selectedSquare = -1
                data.board.projectedSquares = []
        
        data.cards.currentlySelected = cardIndex # store new selection
        card.isSelected = True #select card
        card.waypoints = [(card.x, yRaised)] # raise card
        
        if data.board.selectedSquare != -1:
            _createProjectedSquares(data, card, calc.getActiveMarble(data))
    else: # unselect a card
        card:ANIMATION.Card = calc.getActiveCard(data)
        card.isSelected = False # unselect card
        card.waypoints = [(card.x, yNormal)] # lower card
        data.cards.currentlySelected = -1
        data.board.projectedSquares = [] # clear projected squares

def _createProjectedSquares(data:DATA.Data, card:ANIMATION.Card, marble:ANIMATION.Marble): #TODO: cant select marlbe in home for trickser
    """Create the possible moves with the given card and marble."""
    if card is None:
        print("ERROR in _createProjectedSquares: no card selected")
        return
    if marble is None:
        print("ERROR in _createProjectedSquares: no marble selected")
        return

    movesLeft = card.value

    # if played TAC: take value of previously played non-tac card
    if card.value == 15:
        movesLeft = botHelp.getValueOfLastNonTacCard(data.cards.discardPile)

    # in the middle of playing a 7
    if data.board.remainderOfPlayedSeven > 0:
        movesLeft = data.board.remainderOfPlayedSeven
    
    data.board.projectedSquares = botHelp.getPossibleSquares(data.board.squares, calc.getActivePlayer(data), marble.square, movesLeft, marble.isAbleToFinish, card.value)

def _doAction(data:DATA.Data, card:ANIMATION.Card, marble:ANIMATION.Marble, landingSquare:int, isDiscarding:bool) -> None:
    """Do the action of given card and marble or discard.\n
    Careful: this method doesn't check if combination is a valid move!""" #TODO: implement FS checks

    # store state
    marbleTemp:ANIMATION.Marble
    for player in data.board.playerSequence:
        for marbleTemp in data.marbles.marbles[player]:
            marbleTemp.previousSquare = marbleTemp.square
            marbleTemp.wasAbleToFinish = marbleTemp.isAbleToFinish

    # if discarding: other checks aren't necessary
    if isDiscarding:
        # if playing 8 and allowed to use abilities: force next player to skip
        data.board.isForcedToSkip = card.value == 8 and botHelp.canPlayerPlaySpecialCards(data.board.squares, calc.getActivePlayer(data))
        return

    # if using Trickser: swap marbles
    if card.value == 14:
        marble2 = calc.getMarble(data, landingSquare)

        marble2.square = marble.square
        marble2.waypoints.append(data.board.squaresXY[marble.square])
        marble2.isAbleToFinish = True
        
        marble.square = landingSquare
        marble.waypoints.append(data.board.squaresXY[landingSquare])
        marble.isAbleToFinish = True
        return
    
    ###############
    # normal move #
    ###############

    # if landing square is already occupied: remove marble
    if data.board.squares[landingSquare] != -1:
        _removeMarble(data, landingSquare)
    
    # if marble starts from home: can't finish directly
    marble.isAbleToFinish = (marble.square > 63 and marble.square < 80)

    # if playing 4: move backwards
    isMovingForwards = card.value != 4

    # create waypoints for marble to travel on
    waypoints = botHelp.getSquaresBetween(marble.square, landingSquare, isMovingForwards)
    for waypoint in waypoints:
        marble.waypoints.append(data.board.squaresXY[waypoint])
    marble.square = landingSquare
    marble.isAbleToFinish = True

    # if playing 7: check if moves remaining
    if card.value == 7:
        if data.board.remainderOfPlayedSeven == 0: #first move of the 7
            data.board.remainderOfPlayedSeven = 7 - len(marble.waypoints)
            if data.board.remainderOfPlayedSeven < 0:
                print("ERROR in doAction(): remainderOfSeven < 0")
        else:
            data.board.remainderOfPlayedSeven = data.board.remainderOfPlayedSeven - len(marble.waypoints)

def _removeMarble(data:DATA.Data, square:int)->None:
    """Find marble that is on given square and return it to home square"""
    # find marble that occupies square
    marble:ANIMATION.Marble
    for player in data.board.playerSequence:
        for marble in data.marbles.marbles[player]:
            if marble.square == square:
                removedMarble = marble
                removedMarbleOwner = player
    
    #find available home square
    homeSquares = botHelp.getHomeSquares(removedMarbleOwner)
    for homeSquare in homeSquares:
        if data.board.squares[homeSquare] == -1: # empty
            removedMarble.square = homeSquare
            removedMarble.waypoints = [data.board.squaresXY[homeSquare]]
            return # take first empty square

def _undoPreviousMove(data:DATA.Data):
    """Undo previous Move:\n
    - swap squares\n
    - swap isAbleToFinish flag\n
    - create waypoints"""
    marble:ANIMATION.Marble
    for player in data.board.playerSequence:
        for marble in data.marbles.marbles[player]:
            if marble.square != marble.previousSquare:
                tempSquare = marble.square # swap current and previous square
                marble.square = marble.previousSquare
                marble.previousSquare = tempSquare
                tempBool = marble.isAbleToFinish # swap current and previous ability to finish
                marble.isAbleToFinish = marble.wasAbleToFinish
                marble.wasAbleToFinish = tempBool
                if data.cards.discardPileTopCard.value == 14: # reversing a trickser means direct path
                    marble.waypoints.append(data.board.squaresXY[marble.square])
                else:
                    if data.cards.discardPileTopCard.value == 4: # revert the move means going forward
                        isMovingForwards = True
                    else:
                        isMovingForwards = False
                    for square in botHelp.getSquaresBetween(marble.previousSquare, marble.square, isMovingForwards):
                        marble.waypoints.append(data.board.squaresXY[square])
    _updateSquares(data)

def _discardCard(data:DATA.Data)->None:
    player = calc.getActivePlayer(data)

    data.cards.discardPileTopCard = data.cards.inHand[player].pop(data.cards.currentlySelected) # take played card and move to discard pile
    data.cards.currentlySelected = -1

    dx = len(data.cards.discardPile)/4 # offset if pile is high
    dy = len(data.cards.discardPile)/4
    data.cards.discardPileTopCard.waypoints = [(data.constants.cards.xDiscardPile-dx, data.constants.cards.yDiscardPile-dy)]
    data.cards.discardPileTopCard.vel = data.constants.cards.speedFast

    data.cards.discardPile.append(data.cards.discardPileTopCard.value)

def _nextTurn(data:DATA.Data):
    # update board
    data.marbles.currentlySelected = -1
    data.board.selectedSquare = -1
    data.board.projectedSquares = []

    if data.board.remainderOfPlayedSeven == 0: # keep playing while still some of 7 left
        _selectNextPlayer(data)
        # check if no more cards in players hand
        if not data.cards.inHand[calc.getActivePlayer(data)]:
            dealCards(data)
            _selectNextPlayer(data) # 2x selectNextPlayer because Dealer moves

        # check if any move is possible
        if not _isAnyMovePossible(data):
            data.board.isForcedToSkip = True
            print("No move possible. Your are now discarding cards")

    # # TODO: set positions for cards of new player
    # handSizeOfActivePlayer = len(data.cards.inHand[calc.activePlayer()])
    # xBase = data.constants.xCenter - 0.5 * (handSizeOfActivePlayer-1) * constants.xCardStep - 0.5 * constants.cardWidth
    # for i in range(handSizeOfActivePlayer):
    #     cards.cardsInHand[calc.activePlayer()][i].y = constants.yCardInHand
    #     cards.cardsInHand[calc.activePlayer()][i].x = xBase + i*constants.xCardStep

def _selectNextPlayer(data:DATA.Data)->None:
    """pop first entry of playerSequence and appends it to last\n
    also set flag if the player is a bot """
    data.board.playerSequence.append(data.board.playerSequence.pop(0))
    if data.parameters.bots[calc.getActivePlayer(data)]: # current player is abot
        data.board.isActivePlayerABot = True
    else:
        data.board.isActivePlayerABot = False

def _updateSquares(data:DATA.Data)->None:
    """ updates data.board.squares with all marbles from data.marbles.marbles"""
    data.board.squares = [-1] * 96 # delete old marbles
    for player in data.board.playerSequence:
        for marble in data.marbles.marbles[player]:
            data.board.squares[marble.square] = player

def dealCards(data:DATA.Data):
    for numberOfCardsInHand in range(5):
        for player in data.board.playerSequence:
            if not data.cards.remainingPile: # deck is empty
                _shuffleDeck(data)
            value = data.cards.remainingPile.pop(0) # take value of top card and remove top card from remaining pile
            card = _createCard(data, player, value, numberOfCardsInHand)
            data.cards.inHand[player].append(card)
    # for player in range(4): TODO: sort cards of player
    #     cards.cardsInHand[player].sort(key=operator.attrgetter('value')) # sort cards in hand: smallest is left
    #     # cards.cardsInHand[player].sort()
    # print(.cards.cardsInHand)

def _createCard(data:DATA.Data, player:int, value:int, numberOfCardsInHand:int)->ANIMATION.Card:
    """ Creates a card for the given player with the given value\n
    It Spawns in center and moves to correct position in players hand"""
    card = ANIMATION.Card() # create instance of card
    card.value = value # set value
    card.x = data.constants.xCenter # card spawning in center
    card.y = data.constants.yCenter
    card.owner = player # set owner
    card.vel = data.constants.cards.speedFast
    x, y = calc.getXYDrawnCard(data, player, numberOfCardsInHand)
    card.waypoints = [(x,y)]
    return card

def _shuffleDeck(data:DATA.Data)->None:
    """take all discarded cards, put in deck and shuffle"""
    data.cards.remainingPile = data.cards.discardPile
    random.shuffle(data.cards.remainingPile)
    data.cards.discardPile = []

def _isAnyMovePossible(data:DATA.Data):
    """checks if player could make any move or needs to discard cards"""
    player = calc.getActivePlayer(data)
    possibleMoves = []
    card:ANIMATION.Card
    marble:ANIMATION.Marble
    for card in data.cards.inHand[player]:
        for marble in data.marbles.marbles[player]: # tries every combination of card and marble
            # homeSquares = botHelp.getHomeSquares(player)
            possibleMoves = botHelp.getPossibleSquares(data.board.squares, player, marble.square, card.value, marble.isAbleToFinish, card.value)
            # possibleMoves = getPossibleMoves(marble, card, player, homeSquares)
            if possibleMoves: # a move is possible
                return True
    return False