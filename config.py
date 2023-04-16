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


def load(path=PATH) -> dict[Key, str]:
    result = {}
    with open(path, 'r') as file:
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

            found = False
            for key in Key:
                if key.value == words[0]:
                    result[key] = words[1]
                    found = True
                    break

            if not found:
                raise Exception(
                    f'At path "{PATH}", line {i} "{line}": '
                    f'No key called "{words[0]}" found')

    return result


def get_value(conf: dict[Key, str], key: Key) -> str:
    return conf[key] if key in conf else _DEFAULT_VALUE[key]
