import pygame
import numpy as np
# import os

class Draw:
    def __init__(self, data, calc):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 70)
        # self.background = pygame.image.load(os.path.join('images', 'background.jpg'))

        self.data = data
        self.calc = calc

    def updateWindow(self, win):
        self.drawBoard(win)
        self.drawCards(win)
        self.drawMarbles(win)
        self.drawProjectedSquares(win)
        pygame.display.update()

    def drawBoard(self, win):
        xCenter = self.data.constants.xCenter
        yCenter = self.data.constants.yCenter
        colourPlayer = self.data.playerSpecific.colour[self.calc.getActivePlayer()]
        black = self.data.colours["black"]
        white = self.data.colours["white"]
        grey = self.data.colours["grey"]
        # wood = self.data.colours["wood"]
        h = self.data.constants.board.heightTriangle
        l = self.data.constants.board.lengthTriangle
        lineThickness = self.data.constants.lineThickness
        lineThicknessThick = self.data.constants.lineThicknessThick

        # draw Background
        win.fill(white)  # display with white color
        # win.blit(self.background, (xCenter-yCenter, 0))
        xLeft = xCenter - 3*l
        xRight = xCenter + 3*l
        for i in range(-3,6): # 7 lines per orientation
            pygame.draw.line(win, black, (xLeft,yCenter+i*h), (xRight,yCenter+i*h), lineThickness) # horizontal
            pygame.draw.line(win, black, (xLeft,yCenter-6*h+i*2*h), (xRight,yCenter+6*h+i*2*h), lineThickness) # top left to bottom right
            pygame.draw.line(win, black, (xLeft,yCenter+6*h+i*2*h), (xRight,yCenter-6*h+i*2*h), lineThickness) # bottom left to top right
        # draw silver circles
        for row in range(-4,5):
            for col in range(-3,4):
                if row % 2:
                    xOffset = l/2
                else:
                    xOffset = 0
                x = xCenter + col * l + xOffset
                y = yCenter + row * h
                pygame.draw.circle(win, grey, (x, y), l, 2*lineThickness)
                

        # draw center circle
        pygame.draw.circle(win, white, (xCenter, yCenter), self.data.constants.board.centerRadius, 0) # filled white
        if self.data.board.isDiscardingCards and self.data.cards.currentlySelected != -1:
            pygame.draw.circle(win, colourPlayer, (xCenter, yCenter), self.data.constants.board.centerRadius, lineThicknessThick)
        else:
            pygame.draw.circle(win, black, (xCenter, yCenter), self.data.constants.board.centerRadius, lineThickness)

        # draw ring
        pygame.draw.circle(win, white, (xCenter, yCenter), self.data.constants.board.innerCircleRadius+500, 500) # fill board white except center
        pygame.draw.circle(win, black, (xCenter, yCenter), self.data.constants.board.outerCircleRadius, lineThickness)
        pygame.draw.circle(win, black, (xCenter, yCenter), self.data.constants.board.innerCircleRadius, lineThickness)

        # draw squares
        for square in range(len(self.data.board.squaresXY)): # phi = 0 -> east
            x, y = self.data.board.squaresXY[square]
            if square == self.data.board.selectedSquare:
                pygame.draw.circle(win, colourPlayer, (x,y), self.data.constants.board.squareRadius, lineThicknessThick)
            else:
                pygame.draw.circle(win, black, (x,y), self.data.constants.board.squareRadius, lineThickness)
            # if square in self.data.board.projectedSquares: # outsourced to antother method so that it is drawn after marble
            #     pygame.draw.circle(win, black, (x,y), self.data.constants.board.projectedSquareRadius, 0)

        # draw home bases
        dHome = self.data.constants.board.homeDistance
        for player in range(4):
            x = xCenter + self.data.playerSpecific.x[player] * dHome
            y = yCenter + self.data.playerSpecific.y[player] * dHome
            if player == self.calc.getActivePlayer(): # highlight homebase
                pygame.draw.circle(win, colourPlayer, (x, y), self.data.constants.board.homeRadius, lineThicknessThick) # draw Home
            else:
                pygame.draw.circle(win, black, (x, y), self.data.constants.board.homeRadius, lineThickness) # draw Home

        # # draw arcs in finish TODO: make it work
        # degree = float(np.pi)/180
        # pygame.draw.arc(win, pygame.Color('orange'), (200,100,250,150), 90 * degree, 180 * degree, width=6)  
        # pygame.draw.arc(win, pygame.Color('orange'), (250,100,300,150), 90 * degree, 270 * degree, width=6)  
        # for player in range(4):
        #     xSign = self.data.playerSpecific.x[player]
        #     ySign = self.data.playerSpecific.y[player]
        #     xFinishCenter = xCenter + xSign*2*l
        #     yFinishCenter = yCenter + ySign*2*l
        #     print(xFinishCenter)
        #     print(yFinishCenter)
        #     rect = (xFinishCenter - 0.4*l, yFinishCenter - 0.4*l, xFinishCenter + 0.4*l, yFinishCenter + 0.4*l)
        #     match player:
        #         case 0:
        #             pygame.draw.arc(win, grey, rect, 0 * degree, 290 * degree)
        #         case 1:
        #             pygame.draw.arc(win, grey, rect, 90 * degree, 340 * degree)
        #         case 2:
        #             pygame.draw.arc(win, grey, rect, 180 * degree, 110 * degree)
        #         case 3:
        #             pygame.draw.arc(win, grey, rect, 270 * degree, 160 * degree)

    def drawProjectedSquares(self,win):
        for square in range(len(self.data.board.squaresXY)): # phi = 0 -> east
            x, y = self.data.board.squaresXY[square]
            if square in self.data.board.projectedSquares:
                pygame.draw.circle(win, self.data.colours["black"], (x,y), self.data.constants.board.projectedSquareRadius, 0)

    def drawRemainingPile(self, win):
        if self.data.cards.remainingPile: # still cards in pile
            x = self.data.constants.cards.xRemainingPile
            y = self.data.constants.cards.yRemainingPile
            emptyText = self.my_font.render("", False, (0, 0, 0))
            topCard = self.my_font.render("", False, (0, 0, 0)) # don't show top card
            if len(self.data.cards.remainingPile) > 1:
                for i in range(int(len(self.data.cards.remainingPile)/4)):
                    if i % 2:
                        colour = (255,255,255)
                    else:
                        colour = (0,0,0)
                    self.drawCard(win, x-i, y-i, emptyText, colour, True)
                # self.drawCard(win, x-len(self.data.cards.remainingCards)/4, y-len(self.data.cards.remainingCards)/4, emptyText, (255,255,255))
            self.drawCard(win, x-len(self.data.cards.remainingPile)/4, y-len(self.data.cards.remainingPile)/4, topCard, (0,0,0), True)

    def drawDiscardPile(self, win):
        if len(self.data.cards.discardPile) > 1: # at least one card in pile apart from top card
            x = self.data.constants.cards.xDiscardPile
            y = self.data.constants.cards.yDiscardPile
            emptyText = self.my_font.render("", False, (0, 0, 0))
            valueText = self.my_font.render(str(self.data.cards.discardPile[-2]), False, (0, 0, 0))
            if len(self.data.cards.discardPile) > 2:
                for i in range(int(len(self.data.cards.discardPile)/4)):
                    if i % 2:
                        colour = (255,255,255)
                    else:
                        colour = (0,0,0)
                    self.drawCard(win, x-i, y-i, emptyText, colour, True)
            # top card is animated so don't need to draw it here
            self.drawCard(win, x-len(self.data.cards.discardPile)/4, y-len(self.data.cards.discardPile)/4, emptyText, (255,255,255), True) # first cover with white
            self.drawCard(win, x-len(self.data.cards.discardPile)/4, y-len(self.data.cards.discardPile)/4, valueText, (0,0,0), False) # then blck outline

    def drawCards(self, win):
        self.drawRemainingPile(win)
        self.drawDiscardPile(win)
        self.drawHand(win)

        # top card of discard pile
        if self.data.cards.discardPile:
            card = self.data.cards.discardPileTopCard
            self.drawCardEntity(win, card)

    def drawHand(self, win):
        for player in self.data.board.playerSequence:
            for card in self.data.cards.inHand[player]:
                self.drawCardEntity(win, card)

    def drawCardEntity(self, win, card):
        if card.value in self.data.constants.cards.redCards:
            textColour = self.data.colours["red"]
        else:
            textColour = self.data.colours["black"]
        if card.isShowingValue:
            text_value = self.my_font.render(str(card.value), False, textColour)
        else:
            text_value = self.my_font.render("", False, textColour)

        self.calc.updateEntityMovement(card)
        x = card.x - 0.5 * self.data.constants.cards.width
        y = card.y - 0.5 * self.data.constants.cards.height

        pygame.draw.rect(win, (255,255,255), (x, y, self.data.constants.cards.width, self.data.constants.cards.height), 0, 10) # first cover with white
        pygame.draw.rect(win, (0,0,0), (x, y, self.data.constants.cards.width, self.data.constants.cards.height), self.data.constants.lineThickness, 10)
        win.blit(text_value, (x, y))

    def drawCard(self, win, x, y, text_surface, colour, isFilled):
        x -= 0.5 * self.data.constants.cards.width
        y -= 0.5 * self.data.constants.cards.height
        win.blit(text_surface, (x, y))
        pygame.draw.rect(win, colour, (x, y, self.data.constants.cards.width, self.data.constants.cards.height), int(not isFilled), 10)

        
    def drawMarbles(self, win):
        # use opportunity to refresh board squares
        # self.data.board.squares = [-1] * 64
        for player in self.data.board.playerSequence: # for each player
            for marble in self.data.marbles.marbles[player]: # for each marble of player
                self.calc.updateEntityMovement(marble)
                x = marble.x
                y = marble.y
                # x,y = self.calc.getMarbleXY(marble)
                pygame.draw.circle(win, marble.colour, (x,y), marble.radius, 0)
                # self.data.board.squares[marble.square] = player

    # def drawCircleProjected(self, win, square, colour):
    #     x,y = self.calc.square2xy(square)
    #     pygame.draw.circle(win, colour, (x,y), self.data.constants.board.projectedSquareRadius, 0)

    # def drawCircleOutline(self, win, square, colour):
    #     x,y = self.calc.square2xy(square)
    #     pygame.draw.circle(win, colour, (x,y), self.data.constants.board.squareRadius, self.data.constants.lineThickness)