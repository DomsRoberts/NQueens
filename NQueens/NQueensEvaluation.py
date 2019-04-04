import math
#from elasticsearch import Elasticsearch


class NQueensEvaluation:

    def __init__(self):
      #  self.es = Elasticsearch()
        self.resultStore = {}
        self.evaluations = 0
        self.duplicates = 0
        self.fails = {}

    def evaluate(self, values):
        result = self.countNumberOfAttackingQueens(values)

        if result < 0.1:
            self.attemptRotations(values)
            self.attemptReflections(values)

        return result

    def attemptReflections(self, board):
        newBoard = self.reflectBoardX(board)
        self.countNumberOfAttackingQueens(newBoard)

        newBoard = self.reflectBoardY(board)
        self.countNumberOfAttackingQueens(newBoard)

    def reflectBoardX(self, board):
        newBoard = []
        halfWay = math.ceil((len(board) - 1) / 2)
        sub = 1 if len(board) % 2 == 0 else 0

        for index in range(0,len(board)):
            value = board[index]
            val = halfWay - value
            newVal = (halfWay + val) - sub
            newBoard.append(newVal)

        return newBoard

    def reflectBoardY(self, board):
        return [x for x in reversed(board)]

    def attemptRotations(self, board):
        newBoard = self.rotateBoard(board)
        self.countNumberOfAttackingQueens(newBoard)

        newBoard = self.rotateBoard(newBoard)
        self.countNumberOfAttackingQueens(newBoard)

        newBoard = self.rotateBoard(newBoard)
        self.countNumberOfAttackingQueens(newBoard)

    def rotateBoard(self, board):
        board_len = len(board)
        rotated = [0 for b in board]
        for index in range(0, board_len):
            rotated[board_len - board[index] - 1] = index

        return rotated

    def countNumberOfAttackingQueens(self, board):
        resultHash = self.createResultHash(board)
 #       if resultHash in self.fails:
 #           self.duplicates += 1
 #           return len(board)

        self.evaluations += 1

        attackingCount = 0
        dimensions = len(board)

        groups = set(board)
        uniqueValues = len(groups)

        attackingCount += dimensions - uniqueValues

        countDiagonals = self.countAttackingDiagonals(board, dimensions)

        attackingCount += countDiagonals

        if attackingCount == 0:
            self.insertResult(board, resultHash)
            return 0

#        self.fails[resultHash] = attackingCount

        return attackingCount

    def insertResult(self, board, resultHash):
        if (resultHash in self.resultStore) is False:
            self.resultStore[resultHash] = board
            print(resultHash + ' ===== ' + str(len(self.resultStore)) + " ----------> " + str(self.evaluations))

    def createResultHash(self, integerBoard):
        result = "#".join((str(v) for v in integerBoard))

        return result

    def countAttackingDiagonals(self, board, boardLength):
        attacking = 0
        for index in range(0, boardLength):
            attacking += self.countAttackingDiagonalsForIndex(board, index)

        return attacking

    def countAttackingDiagonalsForIndex(self, board, index):
        currentPos = board[index]
        length = len(board)
        attacking = 0
        for current in range(0, length):
            if current == index:
                continue

            currentX = current
            currentY = board[current]
            boardY = currentPos
            boardX = index

            if abs(currentX - boardX) == abs(currentY - boardY):
                attacking += 1

        return attacking