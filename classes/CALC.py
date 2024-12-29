import numpy as np

class Calc:
    def __init__(self, data):
        self.data = data

    # @staticmethod
    def getClosestSquare(self, xMouse, yMouse):#->int:
        """ looks for closest square at click, returns -1 if none are close """
        for i in range(len(self.data.board.squaresXY)):
            if self.isXYInSquare(xMouse, yMouse, i):
                return i
        return -1
    
    def getClosestCard(self, xMouse, yMouse):
        """ looks for closest card at click, returns -1 if none of own cards are close and 6 if clicked on discard pile """
        player = self.getActivePlayer()
        width = self.data.constants.cards.width
        height = self.data.constants.cards.height
        for i in range(len(self.data.cards.inHand[player])): # check cards in active player's hand
            card = self.data.cards.inHand[player][i]
            if xMouse > card.x-width/2 and xMouse < card.x+width/2 and yMouse > card.y-height/2 and yMouse < card.y+height/2:
                print("clicked on card " + str(i))
                return i
        # check discard pile
        if self.data.cards.discardPile: # only check if discard pile is not empty
            card = self.data.cards.discardPileTopCard
            if xMouse > card.x-width/2 and xMouse < card.x+width/2 and yMouse > card.y-height/2 and yMouse < card.y+height/2:
                print(" clicked on discard pile ")
                return 6
        return -1
    
    def isXYInSquare(self, x, y, square):
        """ returns true if xy coordinates are within selected square """
        xSquare, ySquare = self.data.board.squaresXY[square]
        distance = self.distance(x, y, xSquare, ySquare)
        if distance < self.data.constants.board.squareRadius:
            return True
        else:
            return False
    
    def isXYInCenterCircle(self, x, y):
        """ returns true if xy coordinates are within center circle """
        distance = self.distance(x, y, self.data.constants.xCenter, self.data.constants.yCenter)
        if distance < self.data.constants.board.centerRadius:
            return True
        else:
            return False

    def getMarbleXY(self, marble):
        """ returns xy of class marble after calculating movement """
        if marble.nextSquares: # still moving to next squares
            xTarget, yTarget = Calc.square2xy(marble.nextSquares[0])
            dx = xTarget-marble.x
            dy = yTarget-marble.y
            distance = Calc.distance(marble.x,marble.y,xTarget,yTarget)
            if distance < self.data.constants.marbleSpeed: # too close to current target -> select new target
                marble.nextSquares.pop(0) # remove current target
            if marble.nextSquares: # still targets remaining
                v = min(self.data.constants.marbleSpeed, distance)
                vx = dx * v / Calc.vectorLength(dx,dy)
                vy = dy * v / Calc.vectorLength(dx,dy)
                marble.x += vx
                marble.y += vy
                x = marble.x
                y = marble.y
            else:
                x,y = Calc.square2xy(marble.square)
                marble.x = x
                marble.y = y
        else:
            x,y = Calc.square2xy(marble.square)
        return x, y
    
    def updateEntityMovement(self, entity):
        """ moves all entities that are not at their target loaction """
        distance = self.getDistanceToWayPoint(entity)
        if distance != -1: # still moving to next waypoints
            if distance > entity.vel:
                self.moveCloserToWaypoint(entity)
            else :# too close to current waypoint -> select next waypoint
                if len(entity.waypoints) > 1: # still wayoints after this one
                    entity.waypoints.pop(0)
                    self.moveCloserToWaypoint(entity)
                else: # reached target
                    (xTarget, yTarget) = entity.waypoints[0]
                    entity.x = xTarget
                    entity.y = yTarget
                    entity.waypoints = []
                    entity.vel = self.data.constants.cards.speedSlow # TODO: differentiate between marble and card
    
    def updateBoard(self):
        """ updates data.board.square with all marbles """
        self.data.cards.currentlySelected = -1
        self.data.marbles.currentlySelected = -1
        self.data.board.squares[self.data.board.selectedSquare] = -1
        self.data.board.selectedSquare = -1
        self.data.board.projectedSquares = []

        for player in self.data.board.playerSequence:
            for marble in self.data.marbles.marbles[player]:
                self.data.board.squares[marble.square] = player
                # print(marble.square)

    def moveCloserToWaypoint(self, entity):
        xCur, yCur = entity.x, entity.y
        distance = self.getDistanceToWayPoint(entity)
        (xTarget, yTarget) = entity.waypoints[0]
        dx = xTarget - xCur
        dy = yTarget - yCur
        v = min(entity.vel, distance)
        vx = dx * v / self.vectorLength(dx,dy)
        vy = dy * v / self.vectorLength(dx,dy)
        entity.x += vx
        entity.y += vy


    def getDistanceToWayPoint(self, entity):
        """ returns distance to current waypoint. returns -1 if no waypoint exists"""
        if entity.waypoints: # maybe redundant but better safe than sorry
            xCur, yCur = entity.x, entity.y
            (xTarget, yTarget) = entity.waypoints[0]
            dx = xTarget - xCur
            dy = yTarget - yCur
            distance = self.vectorLength(dx,dy)
            return distance
        else:
            return -1

    def getXYDrawnCard(self, player, cardsInHand):
        """returns the target position of newly drawn card depending on hand size"""
        xMiddleOfAll = self.data.constants.xCenter + self.data.playerSpecific.x[player] * self.data.constants.cards.xHandDistance
        yMiddle = self.data.constants.yCenter + self.data.playerSpecific.y[player] * self.data.constants.cards.yHandDistance
        xMostLeft = xMiddleOfAll - 2.5 * self.data.constants.cards.width + 2 * self.data.constants.cards.xSpace
        y = yMiddle
        x = xMostLeft + cardsInHand * self.data.constants.cards.xStep
        return x, y


    # @staticmethod
    def square2xy(self, square):
        """ returns the xy coordinates of any square on large circle """
        phi = 2*np.pi/64*square
        xCircle = self.data.constants.xCenter + float(np.cos(phi)) * self.data.constants.board.midCircleRadius
        yCircle = self.data.constants.yCenter + float(np.sin(phi)) * self.data.constants.board.midCircleRadius
        return xCircle, yCircle
    
    def square2phi(self, square):
        """ returns the angle [0,2pi] of any square on large circle"""
        phi = 2*np.pi/64*square
        return phi
    
    # def phi2xy(self, phi):
    #     xCircle = self.data.constants.xCenter + np.cos(phi) * self.data.constants.boardMidCircleRadius
    #     yCircle = self.data.constants.yCenter + np.sin(phi) * self.data.constants.boardMidCircleRadius
    #     return xCircle, yCircle
    
    # def xy2phi(self, x,y):
    #     xRel = x-self.data.constants.xCenter
    #     yRel = y-self.data.constants.yCenter
    #     phi = np.arctan2(yRel,xRel)
    #     phi = self.overflowPhi(phi)
    #     return phi

    def overflow(self, square):
        """ limits looping squared to [0,63] """
        if square > 63:
            square -= 64
        if square < 0:
            square += 64
        return square
    
    # def overflowPhi(phi):
    #     if phi >= 2*np.pi:
    #         phi -= 2*np.pi
    #     if phi < 0:
    #         phi += 2*np.pi
    #     return phi

    def distance(self, x1, y1, x2, y2):
        """ """
        distance = np.sqrt((x1-x2)**2+(y1-y2)**2)
        return distance
    
    def vectorLength(self, dx,dy):
        length = np.sqrt(dx**2+dy**2)
        return length
    
    def getActiveMarble(self):
        """ shortcut, returns currently selected marble as class. WARNING: make sure self.data.marbles.currentlySelected != -1 """
        return self.data.marbles.marbles[self.getActivePlayer()][self.data.marbles.currentlySelected]
    
    def getActiveCard(self):
        """ shortcut, returns currently selected card as class. WARNING: make sure self.data.cards.currentlySelected != -1 """
        return self.data.cards.inHand[self.getActivePlayer()][self.data.cards.currentlySelected]
    
    def getActivePlayer(self):
        """ shortcut, returns currently selected player """
        return self.data.board.playerSequence[0]
    
    def getHomeSquares(self, player):
        """ returns list of all squares part of players home"""
        homeSquares = []
        for i in range(4):
            homeSquares.append(64+4*player+i)
        return homeSquares
    
    def getFinishSquares(self, player):
        """ returns list of all squares part of players finish"""
        finishSquares = []
        for i in range(4):
            finishSquares.append(64+16+4*player+i)
        return finishSquares