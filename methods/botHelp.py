# def getLandingSquares(board, marbleSquare, cardValue):
#     landingSquares = [] # clear landing squares
#     waypoints = [[],[]] # list of list because sometimes there are two options: continuing on ring [0] or go to finish [1]
#     if self.data.cards.currentlySelected != -1 and self.data.marbles.currentlySelected != -1: # FS: project squares only if card and marble is selected
#         card = self.calc.getActiveCard()
#         marble = self.calc.getActiveMarble()
#         player = self.calc.getActivePlayer()
#         homeSquares = self.calc.getHomeSquares(player)
#         possibleMoves = self.getPossibleMoves(marble, card, player, homeSquares)
#         self.data.board.projectedSquares = possibleMoves

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
        for nextSquare in getNextSquares(player, marbleSquare, isAbleToFinish):
            movesLeft = cardValue
            # waypoints = [[],[]] # first list for all moves on ring, second list for all moves in finish
            tryNextSquare(board, player, nextSquare, movesLeft, isAbleToFinish, possibleSquares)
    return possibleSquares

def tryNextSquare(board:list[int], player:int, square:int, movesLeft:int, isAbleToFinish:bool, possibleSquares:list[int]):
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
    
    for nextSquare in getNextSquares(player, square, isAbleToFinish):
        tryNextSquare(board, player, nextSquare, movesLeft, isAbleToFinish, possibleSquares)
    movesLeft +=1
    return possibleSquares

def getNextSquares(player:int, square:int, isAbleToFinish:bool)->list[int]:
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

def saturate(square:int)->int:
    """ saturates looping squares to [0,63]\n
     64 -> 0 and -1 -> 63 """
    while square > 63:
        square -= 64
    while square < 0:
        square += 64
    return square

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

def getFinishSquares(player)->list[int]:
    """Return list of all squares part of players finish. \n
    player must be a number between 0 and 3  """
    if player in range(4):
        finishSquares = list(range(4))
        finishSquares = [x+80+4*player for x in finishSquares]
        return finishSquares
    else:
        print("WARNING: player (" + str(player) + ") exceeded domain (0-3). Returning empty list")
        return []