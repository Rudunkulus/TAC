import math
from classes import ANIMATION, DATA
from methods import botHelp

def getClickedSquare(xyMouse:tuple[int], xySquares:list[tuple], radiusSquare:float)->int:
    """Find square that was clicked on and return index.\n
    Return -1 if no square was clicked"""
    for square in range(len(xySquares)):
        if _getDistance(xyMouse, xySquares[square]) <= radiusSquare:
            return square
    return -1

def _getDistance(xy1:tuple[float], xy2:tuple[float])->float:
    """ returns distance between two coordinates """
    return math.sqrt((xy1[0]-xy2[0])**2 + (xy1[1]-xy2[1])**2)

def getClosestCard(data:DATA.Data, xMouse:float, yMouse:float)->int:
    """Find card that was clicked on and return index of card in players hand.\n
    Return -1 if no card was clicked\n
    Return 6 if discard pile was clicked"""
    player = getActivePlayer(data)
    width = data.constants.cards.width
    height = data.constants.cards.height
    for i in range(len(data.cards.inHand[player])): # check cards in active player's hand
        card = data.cards.inHand[player][i]
        if xMouse > card.x-width/2 and xMouse < card.x+width/2 and yMouse > card.y-height/2 and yMouse < card.y+height/2:
            print("clicked on card " + str(i))
            return i
    # check discard pile
    if data.cards.discardPile: # only check if discard pile is not empty
        card = data.cards.discardPileTopCard
        if xMouse > card.x-width/2 and xMouse < card.x+width/2 and yMouse > card.y-height/2 and yMouse < card.y+height/2:
            print(" clicked on discard pile ")
            return 6
    return -1

def isXYInCenterCircle(data:DATA.Data, x, y):
    """ returns true if xy coordinates are within center circle """
    distance = _getDistance((x, y), (data.constants.xCenter, data.constants.yCenter))
    if distance < data.constants.board.centerRadius:
        return True
    else:
        return False

def updateEntityMovement(data:DATA.Data, entity:ANIMATION.Card)->None:
    """ moves all entities that are not at their target loaction \n
    works for cards and marbles"""
    distance = _getDistanceToWaypoint(entity)
    if distance != -1: # still moving to next waypoints
        data.isAnyEntityStillMoving = True
        if _getDistanceToWaypoint(entity) > 10 * entity.vel: # if far away from final destination, triple speed
            velocity = 3 * entity.vel
        else:
            velocity = entity.vel
        if distance > velocity:
            moveCloserToWaypoint(entity, velocity)
        else :# too close to current waypoint -> select next waypoint
            if len(entity.waypoints) > 1: # still wayoints after this one
                entity.waypoints.pop(0)
                moveCloserToWaypoint(entity, velocity)
            else: # reached target
                (xTarget, yTarget) = entity.waypoints[0]
                entity.x = xTarget
                entity.y = yTarget
                entity.waypoints = []
                entity.vel = data.constants.cards.speedSlow # TODO: differentiate between marble and card

def moveCloserToWaypoint(entity:ANIMATION.Card, velocity:float):
    xCur, yCur = entity.x, entity.y
    distance = _getDistanceToWaypoint(entity)
    (xTarget, yTarget) = entity.waypoints[0]
    dx = xTarget - xCur
    dy = yTarget - yCur
    v = min(velocity, distance)
    vx = dx * v / math.sqrt(dx**2+dy**2)
    vy = dy * v / math.sqrt(dx**2+dy**2)
    entity.x += vx
    entity.y += vy

def isAnyMovePossible(data:DATA.Data):
    """checks if player could make any move or needs to discard cards"""
    player = getActivePlayer(data)
    possibleMoves = []
    card:ANIMATION.Card
    marble:ANIMATION.Marble
    for card in data.cards.inHand[player]:
        for marble in data.marbles.marbles[player]: # tries every combination of card and marble
            if card.value in [8,14,15] and botHelp.isAbleToPlaySpecialCards(data.board.squares, player):
                return True
            possibleMoves = botHelp.getPossibleSquares(data.board.squares, player, marble.square, card.value, marble.isAbleToFinish, card.value)
            if possibleMoves: # a move is possible
                return True
    print("No move possible. Forced to discard")
    return False

def _getDistanceToWaypoint(entity:ANIMATION.Card)->float:
    """ returns distance to current waypoint.\n
    returns -1 if no waypoint exists\n
    works for cards and marbles"""
    if entity.waypoints: # TODO: maybe redundant but better safe than sorry
        xyCurrent = (entity.x, entity.y)
        xyTarget = entity.waypoints[0]
        distance = _getDistance(xyCurrent, xyTarget)
        return distance
    else:
        return -1

def getXYDrawnCard(data:DATA.Data, player:int, cardsInHand:int)->tuple:
    """Return the target position of newly drawn card depending on hand size and player"""
    xMiddleOfAll = data.constants.xCenter + data.playerSpecific.x[player] * data.constants.cards.xHandDistance
    yMiddle = data.constants.yCenter + data.playerSpecific.y[player] * data.constants.cards.yHandDistance
    xMostLeft = xMiddleOfAll - 2.5 * data.constants.cards.width + 2 * data.constants.cards.xSpace
    y = yMiddle
    x = xMostLeft + cardsInHand * data.constants.cards.xStep
    return x, y

def square2xy(data:DATA.Data, square:int)->tuple[int,int]:
    """ returns the xy coordinates of any square on large circle """
    phi = 2*math.pi/64*square
    xCircle = data.constants.xCenter + math.cos(phi) * data.constants.board.midCircleRadius
    yCircle = data.constants.yCenter + math.sin(phi) * data.constants.board.midCircleRadius
    return xCircle, yCircle

def getMarble(data:DATA.Data, square:int)->ANIMATION.Marble:
    """Return marble that is on given square.\n
    Return None if square is empty"""
    for player in data.board.playerSequence: # also check other players in case of trickster
        index = 0
        for marble in data.marbles.marbles[player]:
            if marble.square == square:
                return marble
            index += 1
    return None

def getActiveMarble(data:DATA.Data)->ANIMATION.Marble:
    """ shortcut, returns currently selected marble as class.\n
    WARNING: make sure data.marbles.currentlySelected != -1 """
    _, marbleIndex = botHelp.getMarbleIndex(data.marbles.marbles, data.board.selectedSquare)
    return data.marbles.marbles[getActivePlayer(data)][marbleIndex]

def getActiveCard(data:DATA.Data)->ANIMATION.Card:
    """ shortcut, returns currently selected card as class.\n
    WARNING: make sure data.cards.currentlySelected != -1 """
    return data.cards.inHand[getActivePlayer(data)][data.cards.currentlySelected]

def getActivePlayer(data:DATA.Data)->int:
    """ shortcut, returns currently selected player """
    return data.board.playerSequence[0]