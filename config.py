import shlex
import os
from typing import Optional


PATH = os.path.expanduser('~/.searchplayerconf')
INITIAL_DIRECTORY_KEY = 'initial_directory'
INITIAL_FONT_SIZE_KEY = 'initial_font_size'
PAGE_UPDOWN_SPEED_KEY = 'page_updown_speed'
FONT_KEY = 'font'


_DEFAULT_VALUE = {
    INITIAL_DIRECTORY_KEY: os.path.expanduser('~'),
    INITIAL_FONT_SIZE_KEY: '40',
    PAGE_UPDOWN_SPEED_KEY: '8',
    FONT_KEY: 'None',
}


class Config:

    def load(self):
        self._dict = dict()
        with open(PATH, 'r') as file:
            for line in file:
                words = shlex.split(line)
                length = len(words)
                if length > 2:
                    raise Exception(
                        f'path "{PATH}", line {i} "{line}": '
                        'Too many words; should be 2')
                if length == 1:
                    raise Exception(
                        f'path "{PATH}", line {i} "{line}": '
                        'Too few words; should be 2')
                if length == 0:
                    continue
                if not words[0] in _DEFAULT_VALUE.keys():
                    raise Exception(
                        f'path "{PATH}", line {i} "{line}": '
                        f'No key called "{words[0]}" found')
                self._dict[words[0]] = words[1]

    def try_get_value(self, key: str) -> Optional[str]:
        if key in self._dict:
            return self._dict[key]
        return None

    def __init__(self):
        self._dict: dict[str, str] = dict()

    def __getitem__(self, key: str) -> str:
        if key in self._dict:
            return self._dict[key]
        return _DEFAULT_VALUE[key]
