from classes import ANIMATION

def getPossibleSquares(board:list[int], player:int, marbleSquare:int, movesLeft:int, isAbleToFinish:bool, cardValue:int):
    """ Return list of possible squares the given marble could reach with the given card.\n
    Return empty list if no move is possible with current combination"""
    possibleSquares = []
    homeSquares = getHomeSquares(player)

    # coming out of home
    if marbleSquare in homeSquares and cardValue in [1,13]: # different rules
        return [getEntrySquare(player)]
    
    if cardValue == 14 and marbleSquare < 64: # trickser
        if isAbleToPlaySpecialCards(board, player):
            # find all squares on ring that are ocupied by a marble
            for square in range(64):
                if board[square] != -1 and square != marbleSquare:
                    possibleSquares.append(square)
            if len(possibleSquares) > 0: # need at least two marbles to trickser
                return possibleSquares
            else:
                return []
        else:
            return []

    if not marbleSquare in homeSquares: # normal move
        if cardValue != 4:
            for nextSquare in _getNextSquares(player, marbleSquare, isAbleToFinish):
                _tryNextSquare(board, player, nextSquare, movesLeft-1, isAbleToFinish, possibleSquares, cardValue)
        else:
            _tryPreviousSquare(board, marbleSquare, cardValue, possibleSquares)
    return possibleSquares

def _tryPreviousSquare(board:list[int], square:int, movesLeft:int, possibleSquares:list[int]):
    """Recursive process of trying previous squares until\n
    - another marble is in the way -> not valid\n
    - the move is valid -> return a non-empty list"""
    if movesLeft < 0:
        print("ERROR in tryNextSquare(): movesLeft < 0")
    if movesLeft == 0: # this square is accessible
        possibleSquares.append(square)
        movesLeft += 1
        return possibleSquares
    
    # check if marble is blocking:
    if board[square] != -1 and movesLeft < 4: # a marble is blocking. it would be ok if this was the landing space (movesLeft == 1) TODO: check redundancy of movesleft>1
        movesLeft += 1
        return possibleSquares
    
    previousSquare = _getPreviousSquare(square)
    _tryPreviousSquare(board, previousSquare, movesLeft-1, possibleSquares)
    movesLeft +=1
    return possibleSquares

def _tryNextSquare(board:list[int], player:int, square:int, movesLeft:int, isAbleToFinish:bool, possibleSquares:list[int], originalCardValue:int):
    """Recursive process of trying next squares until\n
    - another marble is in the way -> not valid\n
    - the end of the finish is reached -> not valid\n
    - the move is valid -> return a non-empty list"""
    if movesLeft < 0:
        print("ERROR in tryNextSquare(): movesLeft < 0")
    if movesLeft == 0: # this square is accessible
        if board[square] == -1 or square < 64: # if on ring, you can beat another marble
            possibleSquares.append(square)
            movesLeft += 1
            return possibleSquares
        else: # marble in way & outside of ring -> no move possible
            movesLeft += 1
            return possibleSquares
    
    # check if marble is blocking:
    if board[square] != -1 and movesLeft != originalCardValue-1: # a marble is blocking. it would be ok if this was the landing space (movesLeft == 1) TODO: check redundancy of movesleft>1
        movesLeft += 1
        if originalCardValue == 7:
            possibleSquares.append(square)
        print("A marble is in the way")
        return possibleSquares
    
    if originalCardValue == 7:
        possibleSquares.append(square)
    
    for nextSquare in _getNextSquares(player, square, isAbleToFinish):
        _tryNextSquare(board, player, nextSquare, movesLeft-1, isAbleToFinish, possibleSquares, originalCardValue)
    movesLeft +=1
    return possibleSquares

def _getNextSquares(player:int, square:int, isAbleToFinish:bool)->list[int]:
    """Return square on board that comes after current one.\n
    Return list because multiple squares are possible: go to finish or continue another round\n
    Most of the times it is only on entry, though"""
    nextSquares=[]
    entrySquare = getEntrySquare(player)
    finishSquares = getFinishSquares(player)

    # check homesquares
    if square in getHomeSquares(player):
        nextSquares.append(entrySquare)
        return nextSquares

    # check ring
    if square in range(64):
        nextSquare = saturate(square+1) # normal move on ring
        nextSquares.append(nextSquare)

        if square == entrySquare and isAbleToFinish:
            nextSquare = finishSquares[0] # first square of finish
            nextSquares.append(nextSquare)
        return nextSquares

    # check finish
    if square in finishSquares[0:3]: # on one of first 3 finish squares
        nextSquare = square +1
        nextSquares.append(nextSquare)
    if square == finishSquares[3]: # on last finish squares 
        print("Reached end of Board")
        pass # TODO: maybe delete if
    return nextSquares

def _getPreviousSquare(square:int)->int:
    """Return the previous square.\n
    Not a list because going backwards, there are no junctions"""
    if square > 63: # in player specific territory
        player = getOwner(square)
        finishSquares = getFinishSquares(player)
        if square == finishSquares[0]: # first square of finish
            return getEntrySquare(player)
        if square in finishSquares[1:4]: # not the first square of finish
            return square-1
    return saturate(square-1)

def getSquaresBetween(startSquare:int, endSquare:int, isMovingForwards=True)->list[int]:
    """ return list of squares that marble travels on\n
    from one square to another including the end square """
    player = -1
    # check domain of landingSquare:
    if endSquare > 63 and endSquare < 80: # endSquare in base -> not possible
        print("ERROR: end square in home squares -> not possible")
        return []

    # find the player if any square is player specific:
    if startSquare > 63:
        if endSquare > 79:
            if getOwner(startSquare) != getOwner(endSquare): # start and end in different players home/finish
                print("ERROR: start square and end square are in different player's home/finish")
                return []
        else:
            player = getOwner(startSquare)
    else:
        if endSquare > 79:
            player = getOwner(endSquare)

    if startSquare in getHomeSquares(player):
        return [getEntrySquare(player)] # just return entry square. This case shouldn't be possible going backwards, so no extra check needed
    
    squaresBetween = []
    if isMovingForwards:
        square = endSquare
        while square != startSquare:
            squaresBetween.append(square)
            square = _getPreviousSquare(square)
        squaresBetween.reverse() # because we went backwards, the entries have to be reversed
    else:
        square = startSquare
        while square != endSquare:
            square = _getPreviousSquare(square)
            squaresBetween.append(square)
    return squaresBetween

def isAbleToPlaySpecialCards(board:list[int], player:int)->bool:
    """Return True if player has at least one own marble on ring"""
    for square in range(64):
        if board[square] != player:
            return True
    return False

def isFirstTurnOfRound(cardsInHand:list[list[int]])->bool:
    """Return True if it's the first move of the round"""
    for player in range(4):
        if len(cardsInHand[player]) not in [0,5]: # at the beginning of the round, all players have either 0 or 5 cards
            return False
    return True

def saturate(square:int)->int:
    """ saturates looping squares to [0,63]\n
     64 -> 0 and -1 -> 63 """
    while square > 63:
        square -= 64
    while square < 0:
        square += 64
    return square

def getValueOfLastNonTacCard(discardPile:list[int])->int:
    """Return value of last played card that wasn't a TAC"""
    index = -1
    cardValue = 15
    while cardValue == 15:
        cardValue = discardPile[index]
        index -= 1
    return cardValue

def getMarbleIndex(marbles:list[list[ANIMATION.Marble]], square:int)->tuple[int,int]:
    """Return player and marble index of marble that is on given square.\n
    Return None if square is empty"""
    for player in range(4): # always checks all for players. Advantage: don't have to inherit player variable
        marbleIndex = 0
        for marble in marbles[player]:
            if marble.square == square:
                return player, marbleIndex
            marbleIndex += 1
    return None

def getOwner(square:int)->int:
    """Return the player who is the owner of the home/finish of the given square\n
    square must be between 64 and 95\n
    Return -1 if square exceeds domain"""
    if square < 64 or square > 95:
        print("WARNING in getOwner(): square " + str(square) + " exceeded domain (64-95). Returning -1")
        return -1
    else:
        return int((square - 64) % 16 / 4)

def getEntrySquare(player:int)->int:
    """Returns home square of player. \n
    player must be a number between 0 and 3"""
    if player in range(4):
        return 16*player
    else:
        print("WARNING in getEntrySquare(): player " + str(player) + " exceeded domain (0-3). Returning -1")
        return -1

def getHomeSquares(player:int)->list[int]:
    """Return list of all squares part of players base. \n
    player must be a number between 0 and 3 """
    if player in range(4):
        homeSquares = list(range(4))
        homeSquares = [x+64+4*player for x in homeSquares]
        return homeSquares
    else:
        print("WARNING in getHomeSquares(): player " + str(player) + " exceeded domain (0-3). Returning empty list")
        return []

def getFinishSquares(player:int)->list[int]:
    """Return list of all squares part of players finish. \n
    player must be a number between 0 and 3  """
    if player in range(4):
        finishSquares = list(range(4))
        finishSquares = [x+80+4*player for x in finishSquares]
        return finishSquares
    else:
        print("WARNING in getFinishSquares(): player (" + str(player) + ") exceeded domain (0-3). Returning empty list")
        return []