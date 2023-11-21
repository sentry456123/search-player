import os
from configparser import ConfigParser
from typing import Optional


PATH = os.path.expanduser('~/.searchplayerconf.ini')


initial_directory = os.path.expanduser('~')
initial_fontsize = 40
page_updown_speed = 8
font = 'None'
theme = 'light'
frame_thinness = 3
err: Optional[str] = None


def get(parser: ConfigParser, section: str, key: str) -> Optional[str]:
    if not (section in parser):
        return None
    if not (key in parser[section]):
        return None
    return parser[section][key]


def load_all():
    global initial_directory
    global initial_fontsize
    global page_updown_speed
    global font
    global theme
    global frame_thinness

    parser = ConfigParser()
    try:
        parser.read(PATH)
    except Exception as e:
        global err
        err = str(e)

    tmp = get(parser, 'fs', 'initial_directory')
    if tmp:
        initial_directory = tmp
    tmp = get(parser, 'visual', 'initial_fontsize')
    if tmp:
        try:
            initial_fontsize = int(tmp)
        except Exception:
            pass
    tmp = get(parser, 'key', 'page_updown_speed')
    if tmp:
        try:
            page_updown_speed = int(tmp)
        except Exception:
            pass
    tmp = get(parser, 'visual', 'font')
    if tmp:
        font = tmp
    tmp = get(parser, 'visual', 'theme')
    if tmp:
        theme = tmp
    tmp = get(parser, 'visual', 'frame_thinness')
    if tmp:
        try:
            frame_thinness = int(tmp)
        except Exception:
            pass


load_all()
