import random


class ComputerPlayer:
    """Simulates the computer's moves"""

    def __init__(self, rows: int, cols: int):
        self.__rows = rows
        self.__cols = cols
        self.__freePoints = [(i, j) for j in range(self.__cols) for i in range(self.__rows)]
        random.shuffle(self.__freePoints)

    def register_step(self, userStep):
        self.__freePoints.remove(userStep)

    def play(self):
        return self.__freePoints.pop()

