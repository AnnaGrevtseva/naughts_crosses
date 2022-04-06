from enum import Enum
import computer_player as cp


class Symbols(str, Enum):
    X = "X"
    O = "O"


class GameManager:
    """Controls the game, stores the current field state, checks if the game finished"""

    def __init__(self, numRows: int, numCols: int, userSymbol: str):
        self.__numRows = numRows
        self.__numCols = numCols
        self.__stepCount = 0
        self.__userSymbol = userSymbol
        self.__computerSymbol = Symbols.X if Symbols.O == userSymbol else Symbols.O
        self.__field = [[" "]*numCols for i in range(0, numRows)]
        self.__computerPlayer = cp.ComputerPlayer(numRows, numCols)
        self.__finished = False

        self.__winningCrossesStr = Symbols.X * min(numRows, numCols)
        self.__winningNaughtsStr = Symbols.O * min(numRows, numCols)

    def step(self, userStep):
        self.__stepCount += 1

        stepRow, stepCol = userStep
        self.__field[stepRow][stepCol] = self.__userSymbol

        self.__checkFinish(stepRow, stepCol, self.__userSymbol)

        if not self.__finished:
            self.__stepCount += 1

            self.__computerPlayer.register_step(userStep)

            stepRow, stepCol = self.__computerPlayer.play()
            self.__field[stepRow][stepCol] = self.__computerSymbol

            self.__checkFinish(stepRow, stepCol, self.__computerSymbol)

    def isAlreadySet(self, step):
        row = step[0]
        col = step[1]
        symbol = self.__field[row][col]
        return symbol in (Symbols.O, Symbols.X)

    def finished(self):
        return self.__finished

    def setField(self, field):
        self.__field = field
        self.__stepCount = 0
        for row in range(self.__numRows):
            for col in range(self.__numCols):
                symbol = self.__field[row][col]
                if Symbols.X == symbol or Symbols.O == symbol:
                    self.__stepCount += 1
                    self.__computerPlayer.register_step((row, col))
                    self.__checkFinish(row, col, symbol)

    def getField(self):
        return self.__field

    def __containsWinningCombinationInRow(self, stepRow, symbol):
        fieldRow = self.__field[stepRow]
        fieldRowStr = "".join(fieldRow)
        return self.__containsWinningCombination(fieldRowStr, symbol)

    def __containsWinningCombinationInColumn(self, stepCol, symbol):
        fieldColStr = ''
        for i in range(self.__numRows):
            fieldColStr += self.__field[i][stepCol]

        return self.__containsWinningCombination(fieldColStr, symbol)

    def __containsWinningCombinationInMainDiagonal(self, stepRow, stepCol, symbol):
        fieldDiagStr = ''
        diagRow = stepRow - min(stepRow, stepCol)
        diagCol = stepCol - min(stepCol, stepRow)

        while diagCol < self.__numCols and diagRow < self.__numRows:
            fieldDiagStr += self.__field[diagRow][diagCol]
            diagRow += 1
            diagCol += 1

        return self.__containsWinningCombination(fieldDiagStr, symbol)

    def __containsWinningCombinationInSecondaryDiagonal(self, stepRow, stepCol, symbol):
        fieldDiagStr = ''
        diagRow = stepRow + min(self.__numRows - 1 - stepRow, stepCol)
        diagCol = stepCol - min(self.__numRows - 1 - stepRow, stepRow)

        while diagCol < self.__numCols and diagRow >= 0:
            fieldDiagStr += self.__field[diagRow][diagCol]
            diagRow -= 1
            diagCol += 1

        return self.__containsWinningCombination(fieldDiagStr, symbol)

    def __checkFinish(self, stepRow, stepCol, symbol):
        finishResultStr = "You won!" if symbol == self.__userSymbol else "You lost!"

        self.__finished = \
            self.__containsWinningCombinationInRow(stepRow, symbol) or \
            self.__containsWinningCombinationInColumn(stepCol, symbol) or \
            self.__containsWinningCombinationInMainDiagonal(stepRow, stepCol, symbol) or \
            self.__containsWinningCombinationInSecondaryDiagonal(stepRow, stepCol, symbol)

        if self.__finished:
            print(finishResultStr)
        else:
            self.__finished = self.__stepCount >= self.__numRows * self.__numCols

            if self.__finished:
                print("No more free points! It is a draw!")

    def __containsWinningCombination(self, string: str, symbol: str):
        return string.find(self.__winningCrossesStr if Symbols.X == symbol else self.__winningNaughtsStr) != -1
