import random
from classes import DATA, ANIMATION
from methods import calc, actions, botHelp

def initGame(data:DATA.Data):
    """ Init the game:\n
    - all cards are shuffled\n
    - all marbles start at home"""
    _createDeck(data)
    _createPlayerSequence(data)
    actions.dealCards(data)
    _createSquaresXY(data)
    _createMarbles(data)
    actions._updateSquares(data)

def initSpecificSituation(data:DATA.Data, playerSequence, marbles, remainingPile):
    """ Creates the position as specified in the given parameters """
    data.cards.remainingPile = remainingPile
    data.board.playerSequence = playerSequence
    actions.dealCards(data)
    _createSquaresXY(data)
    for player in playerSequence:
        #create marbles player 1
        for square in marbles[player]:
            marble = ANIMATION.Marble() # create marble
            marble.x, marble.y = data.board.squaresXY[square]
            marble.colour = data.playerSpecific.colour[player]
            marble.owner = player
            marble.square = square
            marble.previousSquare = square
            marble.isAbleToFinish = True
            data.marbles.marbles[player].append(marble) # store marble
    actions._updateSquares(data)

def initRandomPosition(data:DATA.Data)->None:
    """ Creates a random position that could occur during a real game"""
    _createDeck(data)
    _createPlayerSequence(data)
    actions.dealCards(data)
    _createSquaresXY(data)
    _createMarblesRandom(data)
    actions._updateSquares(data)

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
    
def _createDeck(data:DATA.Data)->None:
    """take all cards as specified in amountperCardType, put in deck and shuffle"""
    data.cards.remainingPile = [] # reset deck
    for cardValue in range(len(data.parameters.amountPerCardType)):
        for _ in range(data.parameters.amountPerCardType[cardValue]):
            data.cards.remainingPile.append(cardValue)
    random.shuffle(data.cards.remainingPile)

def _createPlayerSequence(data:DATA.Data)->None:
    """creates sequence of players with random first player eg. [2,3,0,1]"""
    data.board.playerSequence = [x-1 for x in data.parameters.players] #from one-based to zero-base
    numberOfPlayers = len(data.board.playerSequence)
    r = random.randint(0,numberOfPlayers-1) # random whose turn is it first
    data.board.playerSequence = data.board.playerSequence[r:] + data.board.playerSequence[:r]