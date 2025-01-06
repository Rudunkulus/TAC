import math
from classes import ANIMATION, DATA
from methods import botHelp

def getClickedSquare(xyMouse:tuple[int], xySquares:list[tuple], radiusSquare)->int:
    """ looks for clicked square, returns -1 if none are clicked """
    for square in range(len(xySquares)):
        if _getDistance(xyMouse, xySquares[square]) <= radiusSquare:
            return square
    return -1

def _getDistance(xy1:tuple[float], xy2:tuple[float])->float:
    """ returns distance between two coordinates """
    return math.sqrt((xy1[0]-xy2[0])**2 + (xy1[1]-xy2[1])**2)

def getClosestCard(data:DATA.Data, xMouse:float, yMouse:float)->None:
    """ looks for closest card at click, returns -1 if none of own cards are close and 6 if clicked on discard pile """
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
# def isXYInSquare(xy:tuple[float], xySquare:tuple[float], radiusSquare:float):
#     """ returns true if xy coordinates are within radius of xySquare """
#     xSquare, ySquare = data.board.squaresXY[square]
#     distance = self.distance(x, y, xSquare, ySquare)
#     if distance < data.constants.board.squareRadius:
#         return True
#     else:
#         return False

def isXYInCenterCircle(data:DATA.Data, x, y):
    """ returns true if xy coordinates are within center circle """
    distance = _getDistance((x, y), (data.constants.xCenter, data.constants.yCenter))
    if distance < data.constants.board.centerRadius:
        return True
    else:
        return False

# def getMarbleXY(marble):
#     """ returns xy of class marble after calculating movement """
#     if marble.nextSquares: # still moving to next squares
#         xTarget, yTarget = square2xy(marble.nextSquares[0])
#         dx = xTarget-marble.x
#         dy = yTarget-marble.y
#         distance = distance(marble.x,marble.y,xTarget,yTarget)
#         if distance < data.constants.marbleSpeed: # too close to current target -> select new target
#             marble.nextSquares.pop(0) # remove current target
#         if marble.nextSquares: # still targets remaining
#             v = min(data.constants.marbleSpeed, distance)
#             vx = dx * v / vectorLength(dx,dy)
#             vy = dy * v / vectorLength(dx,dy)
#             marble.x += vx
#             marble.y += vy
#             x = marble.x
#             y = marble.y
#         else:
#             x,y = square2xy(marble.square)
#             marble.x = x
#             marble.y = y
#     else:
#         x,y = square2xy(marble.square)
#     return x, y

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

# def updateBoard(self):
#     """ updates data.board.square with all marbles """
#     data.cards.currentlySelected = -1
#     data.marbles.currentlySelected = -1
#     data.board.squares[data.board.selectedSquare] = -1
#     data.board.selectedSquare = -1
#     data.board.projectedSquares = []

#     for player in data.board.playerSequence:
#         for marble in data.marbles.marbles[player]:
#             data.board.squares[marble.square] = player
#             # print(marble.square)

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

# def square2phi(square):
#     """ returns the angle [0,2pi] of any square on large circle"""
#     phi = 2*np.pi/64*square
#     return phi

# # def phi2xy(phi):
# #     xCircle = data.constants.xCenter + np.cos(phi) * data.constants.boardMidCircleRadius
# #     yCircle = data.constants.yCenter + np.sin(phi) * data.constants.boardMidCircleRadius
# #     return xCircle, yCircle

# # def xy2phi(x,y):
# #     xRel = x-data.constants.xCenter
# #     yRel = y-data.constants.yCenter
# #     phi = np.arctan2(yRel,xRel)
# #     phi = self.overflowPhi(phi)
# #     return phi

# def overflow(square):
#     """ limits looping squared to [0,63] """
#     if square > 63:
#         square -= 64
#     if square < 0:
#         square += 64
#     return square

# # def overflowPhi(phi):
# #     if phi >= 2*np.pi:
# #         phi -= 2*np.pi
# #     if phi < 0:
# #         phi += 2*np.pi
# #     return phi

# def distance(x1, y1, x2, y2):
#     """ """
#     distance = np.sqrt((x1-x2)**2+(y1-y2)**2)
#     return distance

# def vectorLength(dx,dy):
#     length = np.sqrt(dx**2+dy**2)
#     return length

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
    return data.marbles.marbles[getActivePlayer(data)][data.marbles.currentlySelected]

def getActiveCard(data:DATA.Data)->ANIMATION.Card:
    """ shortcut, returns currently selected card as class.\n
    WARNING: make sure data.cards.currentlySelected != -1 """
    return data.cards.inHand[getActivePlayer(data)][data.cards.currentlySelected]

def getActivePlayer(data:DATA.Data)->int:
    """ shortcut, returns currently selected player """
    return data.board.playerSequence[0]

# def getHomeSquares(player):
#     """ returns list of all squares part of players home"""
#     homeSquares = []
#     for i in range(4):
#         homeSquares.append(64+4*player+i)
#     return homeSquares

# def getFinishSquares(player):
#     """ returns list of all squares part of players finish"""
#     finishSquares = []
#     for i in range(4):
#         finishSquares.append(64+16+4*player+i)
#     return finishSquares