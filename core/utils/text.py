from abc import ABC, abstractmethod

from .constants import CONSTANTS


class Objects(ABC):
    @abstractmethod
    def get_str(self):
        pass

    @abstractmethod
    def type(self):
        pass


class Text(Objects):
    def __init__(self, text):
        self._text = text

    def get_str(self):
        return self._text

    def type(self):
        return CONSTANTS.TEXT_OBJECT_TYPE


class Tag:
    def __init__(self, tag):
        self._tag = tag

    def get_str(self):
        return self._tag

    def type(self):
        return CONSTANTS.TAG_OBJECT_TYPE
