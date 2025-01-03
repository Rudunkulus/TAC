import random
import operator
from classes import ANIMATION, DATA
from methods import botHelp, calc
from bots import random as botRandom

def initGame(data:DATA.Data):
    _createDeck(data)
    _createPlayerSequence(data)
    _dealCards(data)
    # data.board.squares = [-1] * 96 # reset ring
    _createSquaresXY(data)
    _createMarbles(data)
    _updateSquares(data)
    # nextTurn()

def initSpecificSituation(data:DATA.Data):
    data.cards.remainingPile = [1,1,7,7,8,8,13,13,7,7,7,7,7,7,7]
    data.board.playerSequence = [1,3]
    _dealCards(data)
    _createSquaresXY(data)
    #create marbles player 1
    for square in [68,13,50,32]:
        marble = ANIMATION.Marble() # create marble
        marble.x, marble.y = data.board.squaresXY[square]
        marble.colour = data.colours["green"]
        marble.owner = 1
        marble.square = square
        data.marbles.marbles[1].append(marble) # store marble

    #create marbles player 3
    for square in [76,18,53,63]:
        marble = ANIMATION.Marble() # create marble
        marble.x, marble.y = data.board.squaresXY[square]
        marble.colour = data.colours["red"]
        marble.owner = 3
        marble.square = square
        data.marbles.marbles[3].append(marble) # store marble
    
    _updateSquares(data)

def initRandomGame(data:DATA.Data):
    _createDeck(data)
    _createPlayerSequence(data)
    _dealCards(data)
    # data.board.squares = [-1] * 96 # reset ring
    _createSquaresXY(data)
    _createMarblesRandom(data)
    _updateSquares(data)

def mouseClick(data:DATA.Data, x:float, y:float)->None:
    square = calc.getClickedSquare((x, y), data.board.squaresXY, data.constants.board.squareRadius) # TODO: revert back to (data,...)
    card = calc.getClosestCard(data, x,y)
    if square != -1 and not data.board.isDiscardingCards: # selected square
        if square in data.board.projectedSquares: # selected projected square
            _moveMarble(data, square)
            if data.board.remainderOfPlayedSeven == 0:
                _discardCard(data)
            _nextTurn(data)
            _updateSquares(data)
            return
        if data.board.squares[square] == calc.getActivePlayer(data): # selected square with own marble
            _toggleSelectMarble(data, square)
    if calc.isXYInCenterCircle(data, x, y) and data.board.isDiscardingCards and data.cards.currentlySelected != -1: # a card is selected for discard
        _discardCard(data)
        _updateSquares(data)
        _nextTurn(data)
        return
    if card in range(5): # card in hand was selected
        if data.board.remainderOfPlayedSeven > 0: # in the middle of playing a 7, cant select another card
            return
        _toggleSelectCard(data, card)

def keyPress(data:DATA.Data, key:str)->None:
    if key == "1" or key == "2" or key == "3" or key == "4" or key == "5":
        if data.board.remainderOfPlayedSeven > 0: # in the middle of playing a 7, cant select another card
            return
        cardSelected = int(key)-1 # key one based to zero based
        numberOfCardsInHand = len(data.cards.inHand[calc.getActivePlayer(data)])
        if cardSelected < numberOfCardsInHand: # only select if card spot is not empty
            _toggleSelectCard(data, cardSelected)

def botTurn(data:DATA.Data):
    # preparation
    botData = DATA.BotData()
    players = data.board.playerSequence
    activePlayer = calc.getActivePlayer(data)
    cardsInHand = []
    squares = data.board.squares
    discardPile = data.cards.discardPile
    remainingPile = data.cards.remainingPile
    numberOfCardsInHand = [0,0,0,0]
    for player in players:
        numberOfCardsInHand[player] = len(data.cards.inHand[player])
        for cardIndex in data.cards.inHand[player]:
            if player != activePlayer:
                remainingPile.append(cardIndex.value) # add cards of other players to remaining pile since the bot doesn't know if they're in hand or in remaining pile
            else:
                cardsInHand.append(cardIndex.value) # add own cards to hand
    # remaining pile to amount of each card
    remainingCards = [0] * 20 # 20 different cards [including 0]
    for cardValue in remainingPile:
        remainingCards[cardValue] += 1

    # transform marbles to botmarbles
    marblesForBots = [[],[],[],[]]
    for player in players:
        for marble in data.marbles.marbles[player]:
            marbleForBots = ANIMATION.MarbleForBots()
            marbleForBots.owner = player
            marbleForBots.square = marble.square
            marbleForBots.isAbleToFinish = marble.isAbleToFinish
            marblesForBots[player].append(marbleForBots)

    # store in botData
    botData.players = players
    botData.marbles = marblesForBots
    botData.squares = cardsInHand
    botData.numberOfCardsInHand = numberOfCardsInHand
    botData.discardPile = discardPile
    botData.remainingCards = remainingCards

    # bot decision
    # use bots."name".main()
    cardIndex, marbleIndex, landingSquare, isDiscarding = botRandom.main(botData)

    # check validity of bot move
    overWriteBotDecision = False

    # check if discard flag is correct
    # if any move is possible -> isDiscarding should be false. 
    if isDiscarding == _isAnyMovePossible(data): # false flag
        overWriteBotDecision = True
    # check if discard is possible

    # check if move is possible
    marble = data.marbles.marbles[activePlayer][marbleIndex]
    cardValue = cardsInHand[cardIndex]
    possibleSquares = botHelp.getPossibleSquares(squares, marble.square, cardValue, activePlayer, marble.isAbleToFinish)
    _createProjectedSquares(data) # recreate possible moves
    if landingSquare not in possibleSquares: # move is invalid
        overWriteBotDecision = True
    
    if overWriteBotDecision:
        # make random move
        print("Move is invalid, falling back to random move")
        cardIndex, marbleIndex, landingSquare, isDiscarding = botRandom.main(botData)

    if not isDiscarding:
        #preparing moveMarble()
        data.marbles.currentlySelected = marbleIndex
        data.cards.currentlySelected = cardIndex
        _moveMarble(data, landingSquare)
        if data.board.remainderOfPlayedSeven > 0:
            #TODO: bot handling 7
            data.board.remainderOfPlayedSeven = 0
        data.board.selectedSquare = landingSquare
    # rest of the move
    _discardCard(data)
    _updateSquares(data)
    _nextTurn(data)
    return

def _createSquaresXY(data:DATA.Data):
    """Create a map between each square and its x and y location"""
    # ring
    for i in range(64):
        xy = calc.square2xy(data, i)
        data.board.squaresXY.append(xy)

    # homes
    for player in range(4):
        xHomeCenter = data.constants.xCenter + data.playerSpecific.x[player] * data.constants.board.homeDistance
        yHomeCenter = data.constants.yCenter + data.playerSpecific.y[player] * data.constants.board.homeDistance
        for i in range(4):
            xSquare = xHomeCenter + data.playerSpecific.x[i] * data.constants.board.distanceInHome
            ySquare = yHomeCenter + data.playerSpecific.y[i] * data.constants.board.distanceInHome
            xy = (xSquare,ySquare)
            data.board.squaresXY.append(xy)

    # finishes
    h = data.constants.board.heightTriangle
    l = data.constants.board.lengthTriangle
    # it is important to define finishes in order of players. otherwise it would be easier to group players (1 and 3) and (2 and 4)
    for player in range(4):
        if player in [1,3]: # top and down player
            sign = data.playerSpecific.y[player] # 1 for player 1, -1 for player 3
            x = data.constants.xCenter # center between all finished marbles
            y = data.constants.yCenter + sign * 2 * h
            data.board.squaresXY.append((x, y+2/3*sign*h))
            data.board.squaresXY.append((x-sign*1/2*l, y-1/3*sign*h))
            data.board.squaresXY.append((x, y-2/3*sign*h))
            data.board.squaresXY.append((x+sign*1/2*l, y-1/3*sign*h))
        if player in [0,2]: # right and left player
            sign = data.playerSpecific.x[player] # 1 for player 0, -1 for player 2
            x = data.constants.xCenter + sign * 2 * l # center between all finished marbles
            y = data.constants.yCenter
            data.board.squaresXY.append((x, y+sign*h*2/3))
            data.board.squaresXY.append((x-sign*l/2, y+sign*h/3))
            data.board.squaresXY.append((x-sign*l/2, y-sign*h/3))
            data.board.squaresXY.append((x, y-sign*h*2/3))

def _createMarbles(data:DATA.Data)->None:
    """Spawn marbles for each player in game\n
    Spawn Location is each player's home"""
    xCenter = data.constants.xCenter
    yCenter = data.constants.yCenter
    dHome = data.constants.board.homeDistance # from center to home
    dMarble = data.constants.board.distanceInHome # from center of home to each marble
    for player in data.board.playerSequence: # fore each player
        x = xCenter + data.playerSpecific.x[player] * dHome # x,y of center of home
        y = yCenter + data.playerSpecific.y[player] * dHome
        colour = data.playerSpecific.colour[player]
        for i in range(4): # create 4 marbles per player
            x2 = x + data.playerSpecific.x[i] * dMarble # x,y of center of marble in home
            y2 = y + data.playerSpecific.y[i] * dMarble
            marble = ANIMATION.Marble() # create marble
            marble.x = x2
            marble.y = y2
            marble.colour = colour
            marble.owner = player
            marble.square = 64+4*player+i
            data.marbles.marbles[player].append(marble) # store marble

def _createMarblesRandom(data:DATA.Data)->None:
    """Spawn marbles in random locations, setting up a possible game snapshot\n
    One marble is guaranteed to spawn at home\n
    This method is only used for testing\n
    some bugs are known: multiple marbles could spawn on one square"""
    for player in data.board.playerSequence: # for each player
        possibleSquares = list(range(64))
        homeSquares = botHelp.getHomeSquares(player)
        finishsquares = botHelp.getFinishSquares(player)
        colour = data.playerSpecific.colour[player]
        for i in range(4): # add home and finish to each players possible location
            possibleSquares.append(homeSquares[i])
            possibleSquares.append(finishsquares[i])
        random.shuffle(possibleSquares)

        for i in range(4): # for each marble (hardcode for first marble to be in home)
            if i == 1:
                square = homeSquares[0]
            else:
                square = possibleSquares[i]
            marble = ANIMATION.Marble()
            marble.square = square
            marble.x, marble.y = data.board.squaresXY[square]
            marble.colour = colour
            marble.owner = player
            marble.isAbleToFinish = True
            data.marbles.marbles[player].append(marble) # store marble

def _updateSquares(data:DATA.Data)->None:
    """ updates data.board.squares with all marbles from data.marbles.marbles"""
    data.board.squares = [-1] * 96 # delete old marbles
    for player in data.board.playerSequence:
        for marble in data.marbles.marbles[player]:
            data.board.squares[marble.square] = player

def _toggleSelectCard(data:DATA.Data, cardSelected:int)->None:
    yOffsetSelected = data.constants.cards.yOffsetSelected
    yNormal = data.constants.yCenter + data.playerSpecific.y[calc.getActivePlayer(data)] * data.constants.cards.yHandDistance
    yRaised = yNormal + yOffsetSelected

    if data.cards.currentlySelected != cardSelected: # select a card
        if data.cards.currentlySelected != -1: # other card was already selected
            card = calc.getActiveCard(data)
            card.isSelected = False # unselect old card
            card.waypoints = [(card.x, yNormal)] # lower card TODO: hard code x position
        data.cards.currentlySelected = cardSelected # store new seleection
        card = calc.getActiveCard(data) # active card has changed so request it again
        card.isSelected = True #select card
        card.waypoints = [(card.x, yRaised)] # raise card
    else: # unselect a card
        card:ANIMATION.Card = calc.getActiveCard()
        card.isSelected = False # unselect card
        y = data.constants.yCenter + data.playerSpecific.y[calc.getActivePlayer(data)] * data.constants.cards.yHandDistance
        card.waypoints = [(card.x, yNormal)] # lower card
        data.cards.currentlySelected = -1
    if not data.board.isDiscardingCards:
        _createProjectedSquares(data) # only need to update if a move is possible

def _nextTurn(data:DATA.Data):
    # update board
    if data.board.remainderOfPlayedSeven == 0: # keep 7 selected if still moves remaining
        data.cards.currentlySelected = -1
    data.marbles.currentlySelected = -1
    data.board.squares[data.board.selectedSquare] = -1
    data.board.selectedSquare = -1
    data.board.projectedSquares = []
    data.board.isDiscardingCards = False

    if data.board.remainderOfPlayedSeven == 0: # keep playing while still some of 7 left
        _selectNextPlayer(data)
        # check if no more cards in players hand
        if not data.cards.inHand[calc.getActivePlayer(data)]:
            _dealCards(data)
            _selectNextPlayer(data) # 2x selectNextPlayer because Dealer moves

        # check if any move is possible
        if not _isAnyMovePossible(data):
            data.board.isDiscardingCards = True
            print("No move possible. Your are now discarding cards")

    # # TODO: set positions for cards of new player
    # handSizeOfActivePlayer = len(data.cards.inHand[calc.activePlayer()])
    # xBase = data.constants.xCenter - 0.5 * (handSizeOfActivePlayer-1) * constants.xCardStep - 0.5 * constants.cardWidth
    # for i in range(handSizeOfActivePlayer):
    #     cards.cardsInHand[calc.activePlayer()][i].y = constants.yCardInHand
    #     cards.cardsInHand[calc.activePlayer()][i].x = xBase + i*constants.xCardStep

def _isAnyMovePossible(data:DATA.Data):
    """checks if player could make any move or needs to discard cards"""
    player = calc.getActivePlayer(data)
    possibleMoves = []
    for card in data.cards.inHand[player]:
        for marble in data.marbles.marbles[player]: # tries every combination of card and marble
            # homeSquares = botHelp.getHomeSquares(player)
            possibleMoves = botHelp.getPossibleSquares(data.board.squares, marble.square, card.value, player, marble.isAbleToFinish)
            # possibleMoves = getPossibleMoves(marble, card, player, homeSquares)
            if possibleMoves: # a move is possible
                return True
    return False

def _createProjectedSquares(data:DATA.Data):
    data.board.projectedSquares = [] # clear projected squares
    # data.marbles.waypoints = []
    if data.cards.currentlySelected != -1 and data.marbles.currentlySelected != -1: # FS: project squares only if card and marble is selected
        card:ANIMATION.Card = calc.getActiveCard(data)
        cardValue = card.value
        marble:ANIMATION.Marble = calc.getActiveMarble(data)
        player = calc.getActivePlayer(data)
        # homeSquares = botHelp.getHomeSquares(player)

        if data.board.remainderOfPlayedSeven > 0: # in the middle of playing a 7
            cardValue = data.board.remainderOfPlayedSeven # overwrite card value with remaining value
        if data.board.remainderOfPlayedSeven > 0 or cardValue == 7:
            isCardASeven = True
        else:
            isCardASeven = False
        possibleMoves = botHelp.getPossibleSquares(data.board.squares, marble.square, cardValue, player, marble.isAbleToFinish, isCardASeven)
        # possibleMoves = getPossibleMoves(marble, card, player, homeSquares)
        data.board.projectedSquares = possibleMoves

def _moveMarble(data:DATA.Data, square:int)->None:
    """ Move currently selected marble to square.\n
    If square is occupied, kick out occupier\n
    Reminder: data.marbles.currentlySelected needs to be set!"""
    if data.board.squares[square] != -1: # square is already occupied
        _removeMarble(data, square)
    marble:ANIMATION.Marble = calc.getActiveMarble(data)
    startSquare = marble.square
    waypoints = botHelp.getSquaresBetween(startSquare, square)

    # create waypoints for marble to travel on
    for waypoint in waypoints:
        tupel = data.board.squaresXY[waypoint]
        marble.waypoints.append(tupel)

    if calc.getActiveCard(data).value == 7:
        if data.board.remainderOfPlayedSeven == 0: #first move of the 7
            data.board.remainderOfPlayedSeven = 7 - len(marble.waypoints)
        else:
            data.board.remainderOfPlayedSeven = data.board.remainderOfPlayedSeven - len(marble.waypoints)
        print(data.board.remainderOfPlayedSeven)
    
    marble.square = square
    if startSquare > 63 and startSquare < 80: # marble starts from home
        marble.isAbleToFinish = False
    else:
        marble.isAbleToFinish = True

def _removeMarble(data:DATA.Data, square:int)->None:
    # find marble that occupies square
    for player in data.board.playerSequence:
        for marble in data.marbles.marbles[player]:
            if marble.square == square:
                removedMarble:ANIMATION.Marble = marble
                removedMarbleOwner = player
    
    #find available home square
    homeSquares = botHelp.getHomeSquares(removedMarbleOwner)
    for homeSquare in homeSquares:
        if data.board.squares[homeSquare] == -1: # empty
            removedMarble.square = homeSquare
            removedMarble.waypoints = [data.board.squaresXY[homeSquare]]
            break # take first empty square

def _discardCard(data:DATA.Data)->None:
    player = calc.getActivePlayer(data)

    data.cards.discardPileTopCard = data.cards.inHand[player].pop(data.cards.currentlySelected) # take played card and move to discard pile
    dx = len(data.cards.discardPile)/4 # offset if pile is high
    dy = len(data.cards.discardPile)/4
    data.cards.discardPileTopCard.waypoints = [(data.constants.cards.xDiscardPile-dx, data.constants.cards.yDiscardPile-dy)]
    data.cards.discardPileTopCard.vel = data.constants.cards.speedFast

    data.cards.discardPile.append(data.cards.discardPileTopCard.value)

def _toggleSelectMarble(data:DATA.Data, square):
    if square == data.board.selectedSquare: #unselect marble
        data.board.selectedSquare = -1
        data.marbles.currentlySelected = -1
        print("Marble Unselected")
    else: # select marble
        data.board.selectedSquare = square
        # find index of marble that is on that square
        index = 0
        for x in data.marbles.marbles[calc.getActivePlayer(data)]:
            if x.square == square:
                # print(square)
                data.marbles.currentlySelected = index
            index += 1
        print("Marble Selected")
    _createProjectedSquares(data)

def _dealCards(data:DATA.Data):
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
    
def _createDeck(data:DATA.Data)->None:
    """take all cards as specified in amountperCardType, put in deck and shuffle"""
    data.cards.remainingPile = [] # reset deck
    for cardValue in range(len(data.parameters.amountPerCardType)):
        for _ in range(data.parameters.amountPerCardType[cardValue]):
            data.cards.remainingPile.append(cardValue)
    random.shuffle(data.cards.remainingPile)

def _shuffleDeck(data:DATA.Data)->None:
    """take all discarded cards, put in deck and shuffle"""
    data.cards.remainingPile = data.cards.discardPile
    random.shuffle(data.cards.remainingPile)
    data.cards.discardPile = []

def _createPlayerSequence(data:DATA.Data)->None:
    """creates sequence of players with random first player eg. [2,3,0,1]"""
    data.board.playerSequence = [x-1 for x in data.parameters.players] #from one-based to zero-base
    numberOfPlayers = len(data.board.playerSequence)
    r = random.randint(0,numberOfPlayers-1) # random whose turn is it first
    for i in range(r): # select the next player a random amount of times
        _selectNextPlayer(data)

def _selectNextPlayer(data:DATA.Data)->None:
    """pop first entry of playerSequence and appends it to last\n
    also set flag if the player is a bot """
    data.board.playerSequence.append(data.board.playerSequence.pop(0))
    if data.parameters.bots[calc.getActivePlayer(data)]: # current player is abot
        data.board.isActivePlayerABot = True
    else:
        data.board.isActivePlayerABot = False