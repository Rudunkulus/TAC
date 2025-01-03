import pygame
from methods import calc
from classes import DATA
# import os

def init(data:DATA.Data):
    pygame.font.init()
    data.fonts.initFonts()
    # self.my_font = pygame.font.SysFont('Comic Sans MS', 70)
    # self.background = pygame.image.load(os.path.join('images', 'background.jpg'))

def updateWindow(data:DATA.Data, win):
    _drawBoard(data, win)
    _drawCards(data, win)
    _drawMarbles(data, win)
    _drawProjectedSquares(data, win)
    pygame.display.update()

def _drawBoard(data:DATA.Data, win):
    xCenter = data.constants.xCenter
    yCenter = data.constants.yCenter
    activePlayer = calc.getActivePlayer(data)
    colourPlayer = data.playerSpecific.colour[activePlayer]
    black = data.colours["black"]
    white = data.colours["white"]
    grey = data.colours["grey"]
    # wood = data.colours["wood"]
    h = data.constants.board.heightTriangle
    l = data.constants.board.lengthTriangle
    lineThickness = data.constants.lineThickness
    lineThicknessThick = data.constants.lineThicknessThick

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
    pygame.draw.circle(win, white, (xCenter, yCenter), data.constants.board.centerRadius, 0) # filled white
    if ((data.board.isDiscardingCards or data.board.isForcedToSkip) and data.cards.currentlySelected != -1) or (data.cards.isEightSelected):
        pygame.draw.circle(win, colourPlayer, (xCenter, yCenter), data.constants.board.centerRadius, lineThicknessThick)
    else:
        pygame.draw.circle(win, black, (xCenter, yCenter), data.constants.board.centerRadius, lineThickness)

    # draw ring
    pygame.draw.circle(win, white, (xCenter, yCenter), data.constants.board.innerCircleRadius+500, 500) # fill board white except center
    pygame.draw.circle(win, black, (xCenter, yCenter), data.constants.board.outerCircleRadius, lineThickness)
    pygame.draw.circle(win, black, (xCenter, yCenter), data.constants.board.innerCircleRadius, lineThickness)

    # draw squares
    for square in range(len(data.board.squaresXY)): # phi = 0 -> east
        x, y = data.board.squaresXY[square]
        if square == data.board.selectedSquare:
            pygame.draw.circle(win, colourPlayer, (x,y), data.constants.board.squareRadius, lineThicknessThick)
        else:
            pygame.draw.circle(win, black, (x,y), data.constants.board.squareRadius, lineThickness)
        # if square in data.board.projectedSquares: # outsourced to antother method so that it is drawn after marble
        #     pygame.draw.circle(win, black, (x,y), data.constants.board.projectedSquareRadius, 0)

    # draw home bases
    dHome = data.constants.board.homeDistance
    for player in range(4):
        x = xCenter + data.playerSpecific.x[player] * dHome
        y = yCenter + data.playerSpecific.y[player] * dHome
        if player == calc.getActivePlayer(data): # highlight homebase
            pygame.draw.circle(win, colourPlayer, (x, y), data.constants.board.homeRadius, lineThicknessThick) # draw Home
        else:
            pygame.draw.circle(win, black, (x, y), data.constants.board.homeRadius, lineThickness) # draw Home

    # # draw arcs in finish TODO: make it work
    # degree = float(np.pi)/180
    # pygame.draw.arc(win, pygame.Color('orange'), (200,100,250,150), 90 * degree, 180 * degree, width=6)  
    # pygame.draw.arc(win, pygame.Color('orange'), (250,100,300,150), 90 * degree, 270 * degree, width=6)  
    # for player in range(4):
    #     xSign = data.playerSpecific.x[player]
    #     ySign = data.playerSpecific.y[player]
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

def _drawProjectedSquares(data:DATA.Data, win):
    for square in range(len(data.board.squaresXY)): # phi = 0 -> east
        x, y = data.board.squaresXY[square]
        if square in data.board.projectedSquares:
            pygame.draw.circle(win, data.colours["black"], (x,y), data.constants.board.projectedSquareRadius, 0)

def _drawRemainingPile(data:DATA.Data, win):
    if data.cards.remainingPile: # still cards in pile
        x = data.constants.cards.xRemainingPile
        y = data.constants.cards.yRemainingPile
        # emptyText = self.my_font.render("", False, (0, 0, 0))
        # topCard = self.my_font.render("", False, (0, 0, 0)) # don't show top card
        if len(data.cards.remainingPile) > 1:
            for i in range(int(len(data.cards.remainingPile)/4)):
                if i % 2:
                    colour = (255,255,255)
                else:
                    colour = (0,0,0)
                _drawCard(data, win, x-i, y-i, "", colour, True)
            # self.drawCard(win, x-len(data.cards.remainingCards)/4, y-len(data.cards.remainingCards)/4, emptyText, (255,255,255))
        _drawCard(data, win, x-len(data.cards.remainingPile)/4, y-len(data.cards.remainingPile)/4, "", (0,0,0), True)

def _drawDiscardPile(data:DATA.Data, win):
    if len(data.cards.discardPile) > 1: # at least one card in pile apart from top card
        x = data.constants.cards.xDiscardPile
        y = data.constants.cards.yDiscardPile
        # emptyText = self.my_font.render("", False, (0, 0, 0))
        # valueText = self.my_font.render(str(data.cards.discardPile[-2]), False, (0, 0, 0))
        if len(data.cards.discardPile) > 2:
            for i in range(int(len(data.cards.discardPile)/4)):
                if i % 2:
                    colour = (255,255,255)
                else:
                    colour = (0,0,0)
                _drawCard(data, win, x-i, y-i, "", colour, True)
        # top card is animated so don't need to draw it here
        _drawCard(data, win, x-len(data.cards.discardPile)/4, y-len(data.cards.discardPile)/4, "", (255,255,255), True) # first cover with white
        _drawCard(data, win, x-len(data.cards.discardPile)/4, y-len(data.cards.discardPile)/4, "", (0,0,0), False) # then blck outline

def _drawCards(data:DATA.Data, win):
    _drawRemainingPile(data, win)
    _drawDiscardPile(data, win)
    _drawHand(data, win)

    # top card of discard pile
    if data.cards.discardPile:
        card = data.cards.discardPileTopCard
        _drawCardEntity(data, win, card)

def _drawHand(data:DATA.Data, win):
    for player in data.board.playerSequence:
        for card in data.cards.inHand[player]:
            _drawCardEntity(data, win, card)

def _drawCardEntity(data:DATA.Data, win, card):
    if card.value in data.constants.cards.redCards:
        textColour = data.colours["red"]
    else:
        textColour = data.colours["black"]
    if card.isShowingValue:
        text = str(data.text.cards[card.value])
    else:
        text = ""

    calc._updateEntityMovement(data, card)
    x = card.x - 0.5 * data.constants.cards.width
    y = card.y - 0.5 * data.constants.cards.height

    pygame.draw.rect(win, (255,255,255), (x, y, data.constants.cards.width, data.constants.cards.height), 0, 10) # first cover with white
    pygame.draw.rect(win, (0,0,0), (x, y, data.constants.cards.width, data.constants.cards.height), data.constants.lineThickness, 10)
    writeText(win, data.fonts.card, text, textColour, (x, y), 7)
    # win.blit(text_value, (x, y))

def _drawCard(data:DATA.Data, win, x, y, text_surface, colour, isFilled):
    x -= 0.5 * data.constants.cards.width
    y -= 0.5 * data.constants.cards.height
    # win.blit(text_surface, (x, y))
    pygame.draw.rect(win, colour, (x, y, data.constants.cards.width, data.constants.cards.height), int(not isFilled), 10)

def writeText(win, font, text:str, colour:tuple, xy:tuple[float,float], orientation:int)->None:
    """Write the given Text in given font and colour at given coordinates.\n
    orientation describes the exact position relativ to xy in phone number keys:\n
    eg 7->top left, 6->right, 5->center"""
    font = pygame.font.SysFont('Comic Sans MS', 70)
    text = font.render(text, True, colour)
    textRect = text.get_rect()
    match orientation:
        case 7:
            textRect.topleft = xy
        case 8:
            textRect.midtop = xy
        case 9:
            textRect.topright = xy
        case 4:
            textRect.midleft = xy
        case 5:
            textRect.center = xy
        case 6:
            textRect.midright = xy
        case 1:
            textRect.bottomleft = xy
        case 2:
            textRect.midbottom = xy
        case 3:
            textRect.bottomright = xy
        case _:
            print("Warning: orientation ("+ str(orientation) + ") exceeds domain (1-9). Falling back to central ")
            textRect.center = xy
    win.blit(text, textRect)
    
def _drawMarbles(data:DATA.Data, win):
    # use opportunity to refresh board squares
    # data.board.squares = [-1] * 64
    for player in data.board.playerSequence: # for each player
        for marble in data.marbles.marbles[player]: # for each marble of player
            calc._updateEntityMovement(data, marble)
            x = marble.x
            y = marble.y
            # x,y = calc.getMarbleXY(marble)
            pygame.draw.circle(win, marble.colour, (x,y), marble.radius, 0)
            # data.board.squares[marble.square] = player

# def drawCircleProjected(data:DATA.Data, win, square, colour):
#     x,y = calc.square2xy(square)
#     pygame.draw.circle(win, colour, (x,y), data.constants.board.projectedSquareRadius, 0)

# def drawCircleOutline(data:DATA.Data, win, square, colour):
#     x,y = calc.square2xy(square)
#     pygame.draw.circle(win, colour, (x,y), data.constants.board.squareRadius, data.constants.lineThickness)

def waitForAnimation(data:DATA.Data, win, clock):
    data.isAnyEntityStillMoving = True
    while data.isAnyEntityStillMoving:
        clock.tick(data.parameters.FPS)
        data.isAnyEntityStillMoving = False
        updateWindow(data, win)