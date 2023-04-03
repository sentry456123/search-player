import shlex
import os
from enum import Enum


PATH = os.path.expanduser('~/.searchplayerconf')


class Key(Enum):
    INITIAL_DIRECTORY = 'initial_directory'
    INITIAL_FONTSIZE = 'initial_fontsize'
    PAGE_UPDOWN_SPEED = 'page_updown_speed'
    FONT = 'font'
    THEME = 'theme'
    FRAME_THINNESS = 'frame_thinness'


_DEFAULT_VALUE = {
    Key.INITIAL_DIRECTORY: os.path.expanduser('~'),
    Key.INITIAL_FONTSIZE: '40',
    Key.PAGE_UPDOWN_SPEED: '8',
    Key.FONT: 'None',
    Key.THEME: 'light',
    Key.FRAME_THINNESS: '3',
}


class Config:

    def load(self):
        self._dict.clear()
        with open(PATH, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip('\n')
                words = shlex.split(line)
                length = len(words)
                if length > 2:
                    raise Exception(
                        f'At path "{PATH}", line {i} "{line}": '
                        'Too many words; should be 2')
                if length == 1:
                    raise Exception(
                        f'At path "{PATH}", line {i} "{line}": '
                        'Too few words; should be 2')
                if length == 0:
                    continue
                if not words[0] in [e.value for e in Key]:
                    raise Exception(
                        f'At path "{PATH}", line {i} "{line}": '
                        f'No key called "{words[0]}" found')
                self._dict[words[0]] = words[1]

    def __init__(self):
        self._dict: dict[str, str] = dict()

    def __getitem__(self, key: Key) -> str:
        if key.value in self._dict:
            return self._dict[key.value]
        return _DEFAULT_VALUE[key]
