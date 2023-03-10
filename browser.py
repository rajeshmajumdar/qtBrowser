import curses

from core import request
from core.utils.constants import CONSTANTS

class Terminal:
    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.clear()

    def _setup_curses(self):
        curses.noecho()
        curses.cbreak()
        self._stdscr.keypad(True)

    def _stop_curses(self):
        curses.echo()
        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.endwin()

    def _load(self, url):
        content = request.load(url)
        for cnt in content:
            if cnt.type() == CONSTANTS.TEXT_OBJECT_TYPE:
                self._stdscr.addstr(cnt.get_str())

        self._stdscr.refresh()

    def start(self, url):
        self._setup_curses()
        self._load(url)
        while True:
            c = self._stdscr.getch()
            if c == ord('q'):
                self._stop_curses()
                break


if __name__ == "__main__":
    import sys
    try:
        url = sys.argv[1]
    except IndexError:
        url = ''

    Terminal().start(url)
