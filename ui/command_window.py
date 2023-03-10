import curses

from core.utils.constants import CONSTANTS


class Command:
    def __init__(self):
        self.set_window_size()

    def set_window_size(self):
        self._x = CONSTANTS.COMMAND_WIN_X
        self._y = CONSTANTS.COMMAND_WIN_Y
        self._width = CONSTANTS.COMMAND_WIN_WIDTH
        self._height = CONSTANTS.COMMAND_WIN_HEIGHT

        if CONSTANTS.AUTO_RESIZE:
            import os
            size = os.get_terminal_size()
            self._width = size.columns
            self._height = CONSTANTS.COMMAND_WIN_HEIGHT
            self._y = size.lines - CONSTANTS.COMMAND_WIN_HEIGHT

    def window(self):
        self._window = curses.newwin(
            self._height,
            self._width,
            self._y,
            self._x
        )
        return self._window
