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


def _preprocess(text: str) -> str:
    lines = text.split('\n')
    defines = {}
    new_lines = []
    for line in lines:
        for key, value in defines.items():
            line = line.replace('$' + key, value)
        parts = line.split()
        if len(parts) == 0:
            continue
        match parts[0]:
            case '#define':
                if len(parts) >= 3:
                    for i in range(len(parts)):
                        defines[parts[1]] = ' '.join(parts[2:])
                else:
                    raise Exception(
                        'The preprocessor keyword "#define" used, '
                        'but the argument is wrong')
                continue
        new_lines.append(line)

    return '\n'.join(new_lines)


class Config:

    def load(self):
        self._dict = dict()
        with open(PATH, 'r') as file:
            parsed_text = _preprocess(file.read())

            for i, line in enumerate(parsed_text.split("\n")):
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

    def save(self):
        with open(PATH, 'w') as file:
            for key, value in self._dict.items():
                if ' ' in key:
                    key = f'\'{key}\''
                if ' ' in value:
                    value = f'\'{value}\''
                file.write(f'{key} {value}\n')

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
