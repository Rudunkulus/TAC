

def getPossibleSquares(board:list[int], marbleSquare:int, cardValue:int, player:int, isAbleToFinish:bool):
    """ Return list of possible squares the given marble could reach with the given card.\n
    Return empty list if no move is possible with current combination"""
    print("Using new method")
    possibleSquares = []
    homeSquares = getHomeSquares(player)
    if marbleSquare in homeSquares:
        if cardValue in [1,13]: # different rules
            possibleSquares = [getEntrySquare(player)]
    else:
        for nextSquare in _getNextSquares(player, marbleSquare, isAbleToFinish):
            movesLeft = cardValue
            # waypoints = [[],[]] # first list for all moves on ring, second list for all moves in finish
            _tryNextSquare(board, player, nextSquare, movesLeft, isAbleToFinish, possibleSquares)
    return possibleSquares

def _tryNextSquare(board:list[int], player:int, square:int, movesLeft:int, isAbleToFinish:bool, possibleSquares:list[int]):
    """Recursive process of trying next squares until\n
    - another marble is in the way -> not valid\n
    - the end of the finish is reached -> not valid\n
    - the move is valid -> return a non-empty list"""
    movesLeft -= 1
    if movesLeft == 0: # this square is accessible
        possibleSquares.append(square)
        movesLeft += 1
        print("Found a square")
        return possibleSquares
    
    # check if marble is blocking:
    if board[square] != -1 and movesLeft > 0: # a marble is blocking. it would be ok if this was the landing space (movesLeft == 1) TODO: check redundancy of movesleft>1
        movesLeft += 1
        print("A marble is in the way")
        return possibleSquares
    
    for nextSquare in _getNextSquares(player, square, isAbleToFinish):
        _tryNextSquare(board, player, nextSquare, movesLeft, isAbleToFinish, possibleSquares)
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
        return getEntrySquare(player) # just return entry square. This case shouldn't be possible going backwards, so no extra check needed
    
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
            squaresBetween.append(square)
            square = _getPreviousSquare(square)
    return squaresBetween

def saturate(square:int)->int:
    """ saturates looping squares to [0,63]\n
     64 -> 0 and -1 -> 63 """
    while square > 63:
        square -= 64
    while square < 0:
        square += 64
    return square

def getOwner(square:int)->int:
    """Return the player who is the owner of the home/finish of the given square\n
    square must be between 64 and 95\n
    Return -1 if square exceeds domain"""
    if square < 64 or square > 95:
        print("WARNING: square " + str(square) + " exceeded domain (64-95). Returning -1")
        return -1
    else:
        return int((square - 64) % 16 / 4)

def getEntrySquare(player:int)->int:
    """Returns home square of player. \n
    player must be a number between 0 and 3"""
    if player in range(4):
        return 16*player
    else:
        print("WARNING: player " + str(player) + " exceeded domain (0-3). Returning -1")
        return -1

def getHomeSquares(player:int)->list[int]:
    """Return list of all squares part of players base. \n
    player must be a number between 0 and 3 """
    if player in range(4):
        homeSquares = list(range(4))
        homeSquares = [x+64+4*player for x in homeSquares]
        return homeSquares
    else:
        print("WARNING: player " + str(player) + " exceeded domain (0-3). Returning empty list")
        return []

def getFinishSquares(player:int)->list[int]:
    """Return list of all squares part of players finish. \n
    player must be a number between 0 and 3  """
    if player in range(4):
        finishSquares = list(range(4))
        finishSquares = [x+80+4*player for x in finishSquares]
        return finishSquares
    else:
        print("WARNING: player (" + str(player) + ") exceeded domain (0-3). Returning empty list")
        return []