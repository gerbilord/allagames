class chessPiece:
    def __init__(self, color='none', piece='empty', startSide='none', justDoubleMoved=False, hasMoved=False):
        self.color = color
        self.piece = piece
        self.hasMoved = hasMoved
        self.startSide = startSide
        self.justDoubleMoved = justDoubleMoved

    def toTuple(self):
        return (self.color, self.piece)


class shrinkChess:
    def __init__(self):
        self.board = [[] for i in range(8)]
        self.setupBoard()
        self.intToLet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.letToInt = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
        self.curTurn = 'white'
        self.legalMoves = self.generateLegalMoves()
        self.lastMovedPiece = chessPiece() # Dummy piece

    def setupBoard(self):
        for i in range(8):
            for j in range(8):
                self.board[i].append(chessPiece())

        self.board[0][0] = chessPiece('white', 'rook', 'left')
        self.board[1][0] = chessPiece('white', 'knight')
        self.board[2][0] = chessPiece('white', 'bishop')
        self.board[3][0] = chessPiece('white','queen')
        self.board[4][0] = chessPiece('white','king')
        self.board[5][0] = chessPiece('white', 'bishop')
        self.board[6][0] = chessPiece('white', 'knight')
        self.board[7][0] = chessPiece('white', 'rook', 'right')
        self.board[0][7] = chessPiece('black', 'rook', 'left')
        self.board[1][7] = chessPiece('black', 'knight')
        self.board[2][7] = chessPiece('black', 'bishop')
        self.board[3][7] = chessPiece('black','queen')
        self.board[4][7] = chessPiece('black','king')
        self.board[5][7] = chessPiece('black', 'bishop')
        self.board[6][7] = chessPiece('black', 'knight')
        self.board[7][7] = chessPiece('black', 'rook', 'right')
        self.board[0][1] = chessPiece('white', 'pawn')
        self.board[1][1] = chessPiece('white', 'pawn')
        self.board[2][1] = chessPiece('white', 'pawn')
        self.board[3][1] = chessPiece('white', 'pawn')
        self.board[4][1] = chessPiece('white', 'pawn')
        self.board[5][1] = chessPiece('white', 'pawn')
        self.board[6][1] = chessPiece('white', 'pawn')
        self.board[7][1] = chessPiece('white', 'pawn')
        self.board[0][6] = chessPiece('black', 'pawn')
        self.board[1][6] = chessPiece('black', 'pawn')
        self.board[2][6] = chessPiece('black', 'pawn')
        self.board[3][6] = chessPiece('black', 'pawn')
        self.board[4][6] = chessPiece('black', 'pawn')
        self.board[5][6] = chessPiece('black', 'pawn')
        self.board[6][6] = chessPiece('black', 'pawn')
        self.board[7][6] = chessPiece('black', 'pawn')

    def switchPlayer(self):
        if(self.curTurn == 'white'):
            self.curTurn = 'black'
        else:
            self.curTurn = 'white'

    def inCheck(self):
        return False

    def isLegal(self, move):
        if(move in self.legalMoves):
            return True
        return False

    def convertMoveToTuple(self, moveString):
        return (self.letToInt[moveString[0]], int(moveString[1]) - 1)

    def playMove(self, moveFromString, moveToString):
        width = len(self.board)
        height = len(self.board[0])
        moveFrom = self.convertMoveToTuple(moveFromString)
        moveTo = self.convertMoveToTuple(moveToString)
        move = (moveFrom, moveTo)

        if (not self.isLegal(move)):
            return False

        oldPiece = self.board[moveTo[0]][moveTo[1]]
        curPiece = self.board[moveFrom[0]][moveFrom[1]]

        self.board[moveTo[0]][moveTo[1]] = self.board[moveFrom[0]][moveFrom[1]]
        self.board[moveFrom[0]][moveFrom[1]] = chessPiece('none')

        curPiece = self.board[moveTo[0]][moveTo[1]]
        curPiece.hasMoved = True

        # on possante stuff here
        yMovement = moveTo[1] - moveFrom[1]
        xMovement = moveTo[0] - moveFrom[0]

        if(curPiece.piece == 'pawn'):
            if(abs(yMovement) == 2):
                curPiece.justDoubleMoved = True
            if(oldPiece.color == 'none' and abs(xMovement) > 0):
                if (yMovement > 0):
                    yDead = -1
                else:
                    yDead = 1
                self.board[moveTo[0]][moveTo[1]+yDead] = chessPiece('none')

        self.lastMovedPiece.justDoubleMoved = False

        # Castle stuff here
        if(curPiece.piece == 'king' and abs(xMovement) == 2):
            if(xMovement > 0):
                sideMovement = -1
                xCorner = width-1
            else:
                sideMovement = 1
                xCorner = 0

            self.board[moveTo[0]+sideMovement][moveTo[1]] = self.board[xCorner][moveTo[1]]
            self.board[xCorner][moveTo[1]] = chessPiece()

        # preparing for next turn stuff
        self.lastMovedPiece = curPiece
        # SPECIAL STUFF HERE (castle, on possante, pawn upgrade)
        self.shrinkBoard(moveFrom)
        self.upgradePawns()
        self.switchPlayer()
        self.legalMoves = self.generateLegalMoves()

        return True

    def getBoardState(self):
        board =[]

        for x in range(len(self.board)):
            board.append([])
            for y in range(len(self.board[0])):
                board[x].append(self.board[x][y].toTuple())

        return board

    def upgradePawns(self):
        width = len(self.board)
        height = len(self.board[0]) - 1

        if(self.curTurn == 'white'):
            whiteUpgrade = 'queen'
            blackUpgrade = 'bishop'
        else:
            whiteUpgrade = 'bishop'
            blackUpgrade = 'queen'


        for x in range(width):
            if(self.board[x][height].piece == 'pawn' and self.board[x][height].color == 'white'):
                self.board[x][height] = chessPiece('white', whiteUpgrade, hasMoved=True)

            if(self.board[x][0].piece == 'pawn' and self.board[x][0].color == 'black'):
                self.board[x][0] = chessPiece('black', blackUpgrade, hasMoved=True)


    def shrinkBoard(self, lastMove):
        isRowShrinkable = True
        isColShrinkable = True

        for x in range(len(self.board)):
            if(self.board[x][lastMove[1]].color != 'none'):
                isRowShrinkable = False

        for y in range(len(self.board[0])):
            if(self.board[lastMove[0]][y].color != 'none'):
                isColShrinkable = False

        width = len(self.board)

        if(isRowShrinkable):
            for i in range(width):
                del self.board[i][lastMove[1]]

        if(isColShrinkable):
            del self.board[lastMove[0]]

    def generateLegalMoves(self):
        # self.curPlayer
        # (color, piece)

        width = len(self.board)
        height = len(self.board[0])
        legalMoves = [] # (moveFrom, moveTo)

        for x in range(width):
            for y in range(height):
                if(self.board[x][y].color == self.curTurn):
                    pieceMoves = self.generatePieceMoves(x, y) # Generate moves based on piece
                    for legalMove in pieceMoves:
                        legalMoves.append(legalMove)

        return legalMoves

    def inBounds(self, x, y):
        width = len(self.board)
        height = len(self.board[0])

        if(x < width and x > -1 and y < height and y > -1):
            return True

        return False

    def generatePieceMoves(self, pieceX, pieceY):
        piece = self.board[pieceX][pieceY]
        width = len(self.board)
        height = len(self.board[0])
        pieceMoves = []

        def useMoveLoop(directions, maxDist):
            for direction in directions:
                curX = pieceX
                curY = pieceY
                counter = 0

                while(counter < maxDist):
                    curX += direction[0]
                    curY += direction[1]
                    if(not self.inBounds(curX, curY) or self.board[curX][curY].color == piece.color):
                        break
                    elif(self.board[curX][curY].color != 'none'):
                        pieceMoves.append(((pieceX, pieceY),(curX, curY)))
                        break

                    pieceMoves.append(((pieceX, pieceY),(curX, curY)))
                    counter += 1

        def generateBishopMoves():
            directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
            useMoveLoop(directions, 10)

        def generateRookMoves():
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
            useMoveLoop(directions, 10)

        def generateQueenMoves():
            generateBishopMoves()
            generateRookMoves()

        def generateKingMoves():
            directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            useMoveLoop(directions, 1)

            # castle stuff here
            if(not piece.hasMoved):
                # checkRightSide
                cornerPiece = self.board[width-1][pieceY]
                if(cornerPiece.piece == 'rook' and not cornerPiece.hasMoved and width-pieceX > 3):
                    canCastle = True
                    for x in range(pieceX+1, width-1):
                        if(self.board[x][pieceY].color != 'none'):
                            canCastle = False
                            break

                    if(canCastle):
                        pieceMoves.append(((pieceX, pieceY),(pieceX+2,pieceY)))

                # checkLeftSide
                cornerPiece = self.board[0][pieceY]
                if(cornerPiece.piece == 'rook' and not cornerPiece.hasMoved and pieceX > 2):
                    canCastle = True
                    for x in range(1, pieceX):
                        if(self.board[x][pieceY].color != 'none'):
                            canCastle = False
                            break

                    if(canCastle):
                        pieceMoves.append(((pieceX, pieceY),(pieceX-2,pieceY)))

        def generateKnightMoves():
            directions = [(2,1),(1,2),(2,-1),(-1,2),(-2,1),(1,-2),(-2,-1),(-1,-2)]
            useMoveLoop(directions, 1)

        def generatePawnMoves():
            if(piece.color == 'white'):
                direction = 1
            else:
                direction = -1

            # Generate forward pawn moves
            if(self.board[pieceX][pieceY+direction].color == 'none'):
                pieceMoves.append(((pieceX,pieceY),(pieceX,pieceY+direction)))
                if(piece.hasMoved is False and self.board[pieceX][pieceY+direction+direction].color == 'none'):
                    pieceMoves.append(((pieceX,pieceY),(pieceX,pieceY+direction+direction)))

            # generate attack moves / onpossante
            directions = [(1,direction), (-1,direction)]
            for movement in directions:
                curX = pieceX + movement[0]
                curY = pieceY + movement[1]

                if(not self.inBounds(curX, pieceY)):
                    continue

                closePiece = self.board[curX][pieceY]
                diagPiece = self.board[curX][curY]
                enemyColor = 'white'
                if(piece.color == 'white'):
                    enemyColor = 'black'

                if(diagPiece.color == enemyColor or closePiece.color == enemyColor and closePiece.piece == 'pawn' and closePiece.justDoubleMoved is True):
                    pieceMoves.append(((pieceX, pieceY),(curX,curY)))

        # BACK TO GENERATE PIECE MOVES
        if(piece.piece == 'pawn'):
            generatePawnMoves()
        elif(piece.piece == 'rook'):
            generateRookMoves()
        elif(piece.piece == 'knight'):
            generateKnightMoves()
        elif(piece.piece == 'bishop'):
            generateBishopMoves()
        elif(piece.piece == 'queen'):
            generateQueenMoves()
        elif(piece.piece == 'king'):
            generateKingMoves()

        return pieceMoves
