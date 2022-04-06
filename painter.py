from curses import wrapper


class Painter:
    """Paints the current field state into the terminal"""

    def __init__(self, rows: int, cols: int):
        self.__rows = rows
        self.__cols = cols

    def paint(self, field):
        wrapper(self.__paint, field)

    def __paint(self, stdscr, field):
        stdscr.clear()
        for i in range(self.__rows):
            fieldRow = field[i]
            stdscr.addstr('|' + ''.join([(fieldRow[j] + '|') for j in range(0, self.__cols)]) + '\n')
        stdscr.refresh()
        stdscr.getkey()
