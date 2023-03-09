from .constants import CONSTANTS


def DEBUG(string):
    if CONSTANTS.DEBUG:
        print(string)
    else:
        pass
