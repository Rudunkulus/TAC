import random
import operator
from classes import ANIMATION, DATA, CALC
from methods import botHelp

class Actions:
    def __init__(self, 
                 data:DATA, calc:CALC):
        self.rules = Rules(data, calc)
        self.data = data
        self.calc = calc

    def initGame(self):
        self.rules.createDeck()
        self.rules.createPlayerSequence()
        self.rules.dealCards()
        self.data.board.squares = [-1] * 96 # reset ring
        self.rules.createSquaresXY()
        self.rules.createMarbles()
        self.calc.updateBoard()
        # self.rules.nextTurn()

    def initRandomGame(self):
        self.rules.createDeck()
        self.rules.createPlayerSequence()
        self.rules.dealCards()
        self.data.board.squares = [-1] * 96 # reset ring
        self.rules.createSquaresXY()
        self.rules.createMarblesRandom()
        self.calc.updateBoard()

    def mouseClick(self, x, y):
        square = self.calc.getClosestSquare(x, y)
        card = self.calc.getClosestCard(x,y) # TODO: enable card selecting with click
        if square != -1 and not self.data.board.isDiscardingCards: # selected square
            if square in self.data.board.projectedSquares: # selected projected square
                self.rules.moveMarble(square)
                self.rules.discardCard()
                self.calc.updateBoard()
                self.rules.nextTurn()
                return
            if self.data.board.squares[square] == self.calc.getActivePlayer(): # selected square with own marble
                self.rules.toggleSelectMarble(square)
        if self.calc.isXYInCenterCircle(x, y) and self.data.board.isDiscardingCards and self.data.cards.currentlySelected != -1: # a card is selected for discard
            self.rules.discardCard()
            self.calc.updateBoard()
            self.rules.nextTurn()
            return

    def keyPress(self, key):
        if key == "1" or key == "2" or key == "3" or key == "4" or key == "5":
            cardSelected = int(key)-1 # key one based to zero based
            numberOfCardsInHand = len(self.data.cards.inHand[self.calc.getActivePlayer()])
            if cardSelected < numberOfCardsInHand: # only select if card spot is not empty
                self.rules.toggleSelectCard(cardSelected)

    def botTurn(self, bots):
        # preparation
        players = self.data.board.playerSequence
        activePlayer = self.calc.getActivePlayer()
        cardsInHand = []
        squares = self.data.board.squares
        discardPile = self.data.cards.discardPile
        remainingPile = self.data.cards.remainingPile
        numberOfCardsInHand = [0,0,0,0]
        for player in players:
            numberOfCardsInHand[player] = len(self.data.cards.inHand[player])
            for card in self.data.cards.inHand[player]:
                if player != activePlayer:
                    remainingPile.append(card.value) # add cards of other players to remaining pile since the bot doesn't know if they're in hand or in remaining pile
                else:
                    cardsInHand.append(card.value) # add own cards to hand
        # remaining pile to amount of each card
        remainingCards = [0] * 20 # 20 different cards [including 0]
        for cardValue in remainingPile:
            remainingCards[cardValue] += 1

        # bot decision
        card, marble, square = bots.random.main(players, squares, cardsInHand, numberOfCardsInHand, discardPile, remainingCards)

        # check if move is possible
        self.data.marbles.currentlySelected = marble
        self.data.cards.currentlySelected = card
        self.rules.createProjectedSquares() # recreate possible moves
        if square not in self.data.board.projectedSquares: # move is invalid
            # make random move
            print("Move is invalid")
            pass
        self.rules.moveMarble(square)
        self.rules.discardCard()
        self.calc.updateBoard()
        self.rules.nextTurn()
        return
    
class Rules:
    def __init__(self, data, calc):
        self.data = data
        self.calc = calc

    def createSquaresXY(self):
        # ring
        for i in range(64):
            xy = self.calc.square2xy(i)
            self.data.board.squaresXY.append(xy)

        # homes
        for player in range(4):
            xHomeCenter = self.data.constants.xCenter + self.data.playerSpecific.x[player] * self.data.constants.board.homeDistance
            yHomeCenter = self.data.constants.yCenter + self.data.playerSpecific.y[player] * self.data.constants.board.homeDistance
            for i in range(4):
                xSquare = xHomeCenter + self.data.playerSpecific.x[i] * self.data.constants.board.distanceInHome
                ySquare = yHomeCenter + self.data.playerSpecific.y[i] * self.data.constants.board.distanceInHome
                xy = (xSquare,ySquare)
                self.data.board.squaresXY.append(xy)

        # finishes
        h = self.data.constants.board.heightTriangle
        l = self.data.constants.board.lengthTriangle
        # it is important to define finishes in order of players. otherwise it would be easier to group players (1 and 3) and (2 and 4)
        for player in range(4):
            if player in [1,3]: # top and down player
                sign = self.data.playerSpecific.y[player] # 1 for player 1, -1 for player 3
                x = self.data.constants.xCenter # center between all finished marbles
                y = self.data.constants.yCenter + sign * 2 * h
                self.data.board.squaresXY.append((x, y+2/3*sign*h))
                self.data.board.squaresXY.append((x-sign*1/2*l, y-1/3*sign*h))
                self.data.board.squaresXY.append((x, y-2/3*sign*h))
                self.data.board.squaresXY.append((x+sign*1/2*l, y-1/3*sign*h))
            if player in [0,2]: # right and left player
                sign = self.data.playerSpecific.x[player] # 1 for player 0, -1 for player 2
                x = self.data.constants.xCenter + sign * 2 * l # center between all finished marbles
                y = self.data.constants.yCenter
                self.data.board.squaresXY.append((x, y+sign*h*2/3))
                self.data.board.squaresXY.append((x-sign*l/2, y+sign*h/3))
                self.data.board.squaresXY.append((x-sign*l/2, y-sign*h/3))
                self.data.board.squaresXY.append((x, y-sign*h*2/3))


    def createMarbles(self):
        xCenter = self.data.constants.xCenter
        yCenter = self.data.constants.yCenter
        dHome = self.data.constants.board.homeDistance # from center to home
        dMarble = self.data.constants.board.distanceInHome # from center of home to each marble
        for player in self.data.board.playerSequence: # fore each player
            x = xCenter + self.data.playerSpecific.x[player] * dHome # x,y of center of home
            y = yCenter + self.data.playerSpecific.y[player] * dHome
            colour = self.data.playerSpecific.colour[player]
            for i in range(4): # create 4 marbles per player
                x2 = x + self.data.playerSpecific.x[i] * dMarble # x,y of center of marble in home
                y2 = y + self.data.playerSpecific.y[i] * dMarble
                marble = ANIMATION.Marble() # create marble
                marble.x = x2
                marble.y = y2
                marble.colour = colour
                marble.owner = player
                marble.square = 64+4*player+i
                self.data.marbles.marbles[player].append(marble) # store marble

    def createMarblesRandom(self):
        for player in self.data.board.playerSequence: # for each player
            possibleSquares = list(range(64))
            homeSquares = self.calc.getHomeSquares(player)
            finishsquares = self.calc.getFinishSquares(player)
            colour = self.data.playerSpecific.colour[player]
            for i in range(4):
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
                marble.x, marble.y = self.data.board.squaresXY[square]
                marble.colour = colour
                marble.owner = player
                marble.isAbleToFinish = True
                self.data.marbles.marbles[player].append(marble) # store marble

    def toggleSelectCard(self, cardSelected):
        yOffsetSelected = self.data.constants.cards.yOffsetSelected
        yNormal = self.data.constants.yCenter + self.data.playerSpecific.y[self.calc.getActivePlayer()] * self.data.constants.cards.yHandDistance
        yRaised = yNormal + yOffsetSelected

        if self.data.cards.currentlySelected != cardSelected: # select a card
            if self.data.cards.currentlySelected != -1: # other card was already selected
                card = self.calc.getActiveCard()
                card.isSelected = False # unselect old card
                card.waypoints = [(card.x, yNormal)] # lower card TODO: hard code x position
            self.data.cards.currentlySelected = cardSelected # store new seleection
            card = self.calc.getActiveCard() # active card has changed so request it again
            card.isSelected = True #select card
            card.waypoints = [(card.x, yRaised)] # raise card
        else: # unselect a card
            card = self.calc.getActiveCard()
            card.isSelected = False # unselect card
            y = self.data.constants.yCenter + self.data.playerSpecific.y[self.calc.getActivePlayer()] * self.data.constants.cards.yHandDistance
            card.waypoints = [(card.x, yNormal)] # lower card
            self.data.cards.currentlySelected = -1
        if not self.data.board.isDiscardingCards:
            self.createProjectedSquares() # only need to update if a move is possible

    def nextTurn(self):
        # update board
        self.data.cards.currentlySelected = -1
        self.data.marbles.currentlySelected = -1
        self.data.board.squares[self.data.board.selectedSquare] = -1
        self.data.board.selectedSquare = -1
        self.data.board.projectedSquares = []
        self.data.board.isDiscardingCards = False

        self.selectNextPlayer()
        # check if no more cards in players hand
        if not self.data.cards.inHand[self.calc.getActivePlayer()]:
            self.dealCards()
            self.selectNextPlayer() # 2x selectNextPlayer because Dealer moves

        if self.data.parameters.bots[self.calc.getActivePlayer()]: # current player is abot
            self.data.board.isActivePlayerABot = True
        else:
            self.data.board.isActivePlayerABot = False

        # check if any move is possible
        if not self.isAnyMovePossible():
            self.data.board.isDiscardingCards = True
            print("No move possible. Your are now discarding cards")

        # # TODO: set positions for cards of new player
        # handSizeOfActivePlayer = len(self.data.cards.inHand[self.calc.activePlayer()])
        # xBase = self.data.constants.xCenter - 0.5 * (handSizeOfActivePlayer-1) * self.constants.xCardStep - 0.5 * self.constants.cardWidth
        # for i in range(handSizeOfActivePlayer):
        #     self.cards.cardsInHand[self.calc.activePlayer()][i].y = self.constants.yCardInHand
        #     self.cards.cardsInHand[self.calc.activePlayer()][i].x = xBase + i*self.constants.xCardStep

    def isAnyMovePossible(self):
        """checks if player could make any move or needs to discard cards"""
        player = self.calc.getActivePlayer()
        possibleMoves = []
        for card in self.data.cards.inHand[player]:
            for marble in self.data.marbles.marbles[player]: # tries every combination of card and marble
                homeSquares = self.calc.getHomeSquares(player)
                possibleMoves = botHelp.getPossibleSquares(self.data.board.squares, marble.square, card.value, player, marble.isAbleToFinish)
                # possibleMoves = self.getPossibleMoves(marble, card, player, homeSquares)
                if possibleMoves: # a move is possible
                    return True
        return False

    def createProjectedSquares(self):
        self.data.board.projectedSquares = [] # clear projected squares
        self.data.marbles.waypoints = []
        if self.data.cards.currentlySelected != -1 and self.data.marbles.currentlySelected != -1: # FS: project squares only if card and marble is selected
            card = self.calc.getActiveCard()
            marble = self.calc.getActiveMarble()
            player = self.calc.getActivePlayer()
            homeSquares = self.calc.getHomeSquares(player)
            possibleMoves = botHelp.getPossibleSquares(self.data.board.squares, marble.square, card.value, player, marble.isAbleToFinish)
            # possibleMoves = self.getPossibleMoves(marble, card, player, homeSquares)
            self.data.board.projectedSquares = possibleMoves
    
    def getPossibleMoves(self, marble, card, player, homeSquares):
        """ returns list of possible squares, the selected marble could reach with the selected card. returns empty list if no move is possible """
        possibleMoves = []
        if marble.square in homeSquares:
            if card.value in [1,13]: # different rules
                waypoints = [self.data.playerSpecific.entrySquare[player]]
                possibleMoves = waypoints
        else:
            for nextSquare in self.getNextSquares(player, marble.square, marble.isAbleToFinish):
                movesLeft = card.value -1
                waypoints = []
                self.tryNextSquare(player, nextSquare, movesLeft, marble.isAbleToFinish, waypoints, possibleMoves)
        return possibleMoves

    def getNextSquares(self, player, square, isAbleToFinish):
        """ returns square on board that comes after current one. returns list because multiple squares are possible: go to finish or continue another round """
        nextSquares=[]
        entrySquare = self.data.playerSpecific.entrySquare[player]

        # check homesquares
        if square in self.calc.getHomeSquares(player):
            nextSquares.append(entrySquare)

        # check ring
        if square in range(64):
            nextSquare = self.calc.overflow(square+1)
            nextSquares.append(nextSquare)

            if square == entrySquare and isAbleToFinish:
                nextSquare = 64+16+4*player
                nextSquares.append(nextSquare)

        # check finish
        finishSquares = self.calc.getFinishSquares(player)
        if square in finishSquares[0:3]: # on one of first 3 finish squares
            nextSquare = square +1
            nextSquares.append(nextSquare)
        if square == finishSquares[3]: # on last finish squares 
            print("Reached end of Board")
            pass # TODO: maybe delete if
        return nextSquares

    def tryNextSquare(self, player, square, movesLeft, isAbleToFinish, waypoints, possibleMoves):
        if movesLeft == 0: # this square is accessible
            possibleMoves.append(square)
            self.data.marbles.waypoints = waypoints
            movesLeft += 1
            print("Found a square")
            return possibleMoves
        
        # check if marble is blocking:
        if self.data.board.squares[square] != -1 and movesLeft > 0: # a marble is blocking. it would be ok if this was the landing space (movesLeft == 1) TODO: check redundancy of movesleft>1
            movesLeft += 1
            print("A marble is in the way")
            return possibleMoves
        
        movesLeft -= 1
        for nextSquare in self.getNextSquares(player,square, isAbleToFinish):
            waypoints.append(self.data.board.squaresXY[square])
            self.tryNextSquare(player, nextSquare, movesLeft, isAbleToFinish, waypoints, possibleMoves)
        movesLeft +=1
        return possibleMoves

    def moveMarble(self, square):
        if self.data.board.squares[square] != -1: # square is already occupied
            self.removeMarble(square)
        marble = self.calc.getActiveMarble()
        startSquare = marble.square
        waypoints = botHelp.getSquaresBetween(startSquare, square)

        # create waypoints for marble to travel on
        # x, y = self.data.board.squaresXY[square]
        # if waypoints:
        for waypoint in waypoints:
            tupel = self.data.board.squaresXY[waypoint]
            marble.waypoints.append(tupel)
        # marble.waypoints.append((x, y))
        marble.square = square

    def removeMarble(self, square):
        # find marble that occupies square
        for player in self.data.board.playerSequence:
            for marble in self.data.marbles.marbles[player]:
                if marble.square == square:
                    removedMarble = marble
                    removedMarbleOwner = player
        
        #find available home square
        homeSquares = self.calc.getHomeSquares(removedMarbleOwner)
        for homeSquare in homeSquares:
            if self.data.board.squares[homeSquare] == -1: # empty
                removedMarble.square = homeSquare
                removedMarble.waypoints = [self.data.board.squaresXY[homeSquare]]


    def discardCard(self):
        player = self.calc.getActivePlayer()

        self.data.cards.discardPileTopCard = self.data.cards.inHand[player].pop(self.data.cards.currentlySelected) # take played card and move to discard pile
        dx = len(self.data.cards.discardPile)/4 # offset if pile is high
        dy = len(self.data.cards.discardPile)/4
        self.data.cards.discardPileTopCard.waypoints = [(self.data.constants.cards.xDiscardPile-dx, self.data.constants.cards.yDiscardPile-dy)]
        self.data.cards.discardPileTopCard.vel = self.data.constants.cards.speedFast

        self.data.cards.discardPile.append(self.data.cards.discardPileTopCard.value)

    def toggleSelectMarble(self, square):
        if square == self.data.board.selectedSquare: #unselect marble
            self.data.board.selectedSquare = -1
            self.data.marbles.currentlySelected = -1
            print("Marble Unselected")
        else: # select marble
            self.data.board.selectedSquare = square
            # find index of marble that is on that square
            index = 0
            for x in self.data.marbles.marbles[self.calc.getActivePlayer()]:
                if x.square == square:
                    # print(square)
                    self.data.marbles.currentlySelected = index
                index += 1
            print("Marble Selected")
        self.createProjectedSquares()

    def dealCards(self):
        for cardsInHand in range(5):
            for player in self.data.board.playerSequence:
                if not self.data.cards.remainingPile: # deck is empty
                    self.shuffleDeck()
                value = self.data.cards.remainingPile.pop(0) # take value of top card and remove top card from remaining pile
                card = self.createCard(player, value, cardsInHand)
                self.data.cards.inHand[player].append(card)
        # for player in range(4): TODO: sort cards of player
        #     self.cards.cardsInHand[player].sort(key=operator.attrgetter('value')) # sort cards in hand: smallest is left
        #     # self.cards.cardsInHand[player].sort()
        # print(self.cards.cardsInHand)

    def createCard(self, player, value, cardsInHand)->ANIMATION.Card:
        card = ANIMATION.Card() # create instance of card
        card.value = value # set value
        card.x = self.data.constants.xCenter # card spawning in center
        card.y = self.data.constants.yCenter
        card.owner = player # set owner
        card.vel = self.data.constants.cards.speedFast
        x, y = self.calc.getXYDrawnCard(player, cardsInHand)
        card.waypoints = [(x,y)]
        return card


    def createPlayerSequence(self):
        """creates sequence of players with radnom first player eg. [2,3,0,1]"""
        self.data.board.playerSequence = [x-1 for x in self.data.parameters.players] #from one-based to zero-base
        numberOfPlayers = len(self.data.board.playerSequence)
        r = random.randint(0,numberOfPlayers-1) # random whose turn is it first
        for i in range(r):
            self.selectNextPlayer()

    def selectNextPlayer(self):
        """pop first entry and appends it to last"""
        self.data.board.playerSequence.append(self.data.board.playerSequence.pop(0))

    def createDeck(self):
        """take all cards and put in deck and shuffle"""
        self.data.cards.remainingPile = [] # reset deck
        amount = self.data.parameters.amountPerCardType
        for i in range(len(amount)):
            for _ in range(amount[i]):
                self.data.cards.remainingPile.append(i)
        random.shuffle(self.data.cards.remainingPile)

    def shuffleDeck(self):
        """take all discarded cards, put in deck and shuffle"""
        self.data.cards.remainingPile = self.data.cards.discardPile
        random.shuffle(self.data.cards.remainingPile)
        self.data.cards.discardPile = []