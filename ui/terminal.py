import curses

from core.utils.constants import CONSTANTS
from .command_window import Command
from .browser_window import Browser
from .loader import load_url, load_text


class Terminal:
    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.clear()

    def _setup_curses(self):
        curses.noecho()
        curses.cbreak()
        self._stdscr.keypad(True)
        self._create_windows()

    def _stop_curses(self):
        curses.echo()
        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.endwin()

    def _create_windows(self):
        self._browser = Browser().window()
        self._command = Command().window()

    def _load(self, url):
        load_url(url, self._browser)
        load_text("Here is a command window.", self._command)

    def start(self, url):
        self._setup_curses()
        self._load(url)
        while True:
            c = self._browser.getch()
            if c == ord(CONSTANTS.KEYBINDING_QUIT):
                self._stop_curses()
                break
