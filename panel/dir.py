import pygame
import os
from panel.ipanel import IPanel
import irenderer
from irenderer import IRenderer
import config
from iapp import IApp
import subprocess
import sys
from enum import Enum
import re


def _start_file(filename: str):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, filename])


def _is_file(dirpath: str, name: str) -> bool:
    abs = os.path.join(dirpath, name)
    return os.path.isfile(abs)


def _is_dir(dirpath: str, name: str) -> bool:
    return not _is_file(dirpath, name)


def _list_dir(path: str) -> list[str]:
    result = ['./', '../']
    listed = os.listdir(path)
    for name in listed:
        if _is_dir(path, name):
            result.append(name + '/')
    for name in listed:
        if _is_file(path, name):
            result.append(name)
    return result


def _search(text: str, pattern: str, regex=False) -> bool:
    if regex:
        try:
            return re.search(pattern, text) is not None
        except Exception:
            return False

    pos = 0
    for c in pattern:
        if c not in text[pos:]:
            return False
        pos = text.index(c, pos) + 1
    return True


class Result(Enum):
    IS_FILE = 0
    IS_DIR = 1


class DirPanel(IPanel):

    def on_keydown(self, key: int, mod: int, unicode: str):
        ctrl = mod & pygame.KMOD_CTRL
        shift = mod & pygame.KMOD_SHIFT

        if ctrl:
            match key:
                case pygame.K_RETURN:
                    result = self._open_selected()
                    if result == Result.IS_DIR:
                        self._buf = ''
                case pygame.K_h:
                    self._parentdir()
                    self._buf = ''
                case pygame.K_j:
                    self.selection += 1
                case pygame.K_k:
                    self.selection -= 1
                case pygame.K_d:
                    self.selection += self._page_updown_speed
                case pygame.K_u:
                    self.selection -= self._page_updown_speed
                case pygame.K_l:
                    self._open_selected()
                case pygame.K_r:
                    self._regex = not shift
                case pygame.K_BACKSPACE:
                    self._buf = ''
                case pygame.K_g:
                    if shift:
                        self.selection = len(self._files()) - 1
                    else:
                        self.selection = 0
        else:
            match key:
                case pygame.K_RETURN | pygame.K_TAB:
                    result = self._open_selected()
                    if result == Result.IS_DIR:
                        self._buf = ''
                case pygame.K_RIGHT:
                    self._open_selected()
                case pygame.K_UP:
                    self.selection += -1
                case pygame.K_DOWN:
                    self.selection += 1
                case pygame.K_LEFT:
                    self._parentdir()
                    self._buf = ''
                case pygame.K_PAGEUP:
                    self.selection -= self._page_updown_speed
                case pygame.K_PAGEDOWN:
                    self.selection += self._page_updown_speed
                case pygame.K_HOME:
                    self.selection = 0
                case pygame.K_END:
                    self.selection = len(self._files()) - 1
                case pygame.K_BACKSPACE:
                    self._buf = self._buf[:-1]
                    self.selection = 0
                case _:
                    if len(unicode) != 0 and unicode in irenderer.TYPABLE:
                        self._buf += unicode
                        self.selection = 0

    def on_mousebuttondown(self, x: int, y: int, button: int):
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        font_size = self._app.get_font_size()
        match button:
            case pygame.BUTTON_LEFT:
                self.selection = int(y / font_size - self._render_offset - self._header_size)
            case pygame.BUTTON_RIGHT:
                self._open_selected()
            case pygame.BUTTON_WHEELDOWN:
                if not ctrl:
                    self.selection += 1
            case pygame.BUTTON_WHEELUP:
                if not ctrl:
                    self.selection -= 1
            case pygame.BUTTON_MIDDLE:
                self._buf = ''
            case pygame.BUTTON_X1:
                self._parentdir()
                self._buf = ''
            case pygame.BUTTON_X2:
                self._open_selected()

    def update(self):
        super().update()

    def render(self, r: IRenderer):
        width, height = r.panel_size()
        font_size = r.font_size()
        font = r.font()
        theme = self._app.get_configvalue(config.Key.THEME)
        frame_thinness = int(self._app.get_configvalue(config.Key.FRAME_THINNESS))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        try:
            files = self._files()
        except Exception:
            files = ['./', '../']

        self._render_offset = 0
        if self.selection >= (height / font_size) / 2:
            self._render_offset = -self.selection + (height / font_size) / 2 - 1

        for i, name in enumerate(files):
            if self.selection == i:
                color = (120, 120, 120) if theme == 'dark' else (200, 200, 200)
            elif int(mouse_y / font_size - self._render_offset - self._header_size) == i:
                color = (80, 80, 80) if theme == 'dark' else (225, 225, 225)
            else:
                color = r.background_color()
            r.rect((0, (i + self._header_size + self._render_offset) * font_size, width, font_size), color)
            if name[-1] == '/':
                color = irenderer.MODERN_YELLOW if theme == 'dark' else irenderer.DARK_YELLOW
            else:
                color = r.font_color()
            r.text(name, (0, (i + self._header_size + self._render_offset) * font_size), color)

        r.rect((0, 0, width, font_size), r.background_color())
        if width > font.size(self._path)[0]:
            offset = 0
        else:
            offset = width - font.size(self._path)[0]
        r.text(self._path, (offset, 0), r.font_color())

        r.rect((0, font_size, width, font_size), irenderer.MODERN_BLUE)
        r.rect((frame_thinness, font_size + frame_thinness, width - frame_thinness*2, font_size - frame_thinness*2),
               r.background_color())

        buf = self._buf
        cursor_width = r.font_size() * 0.3
        if self._regex:
            buf = 'Regex: ' + buf
        if width + cursor_width > font.size(buf)[0]:
            offset = 0
        else:
            offset = width - font.size(buf)[0] - cursor_width
        r.text(buf, (offset, font_size), r.font_color())

        buflen = font.size(buf)[0]
        r.rect((offset + buflen, font_size, cursor_width, font_size), r.font_color())

    def receive(self, retval):
        return super().receive(retval)

    @property
    def selection(self) -> int:
        return self._selection

    @selection.setter
    def selection(self, value: int):
        length = len(self._files())

        self._selection = value
        if self._selection >= length:
            self._selection = length - 1
        if self._selection < 0:
            self._selection = 0

    def _open_selected(self) -> Result:
        result: Result
        files = self._files()
        if len(files) <= 0:
            return
        path = files[self.selection]
        if _is_file(self._path, path):
            _start_file(os.path.join(self._path, path))
            result = Result.IS_FILE
        else:
            self._change_dir(path)
            result = Result.IS_DIR
        return result

    def _parentdir(self):
        self._change_dir('../')

    def _change_dir(self, path: str) -> str:
        abs_dist = os.path.abspath(self._path)
        new_path = os.path.join(abs_dist, path)
        self._path = os.path.abspath(new_path)
        self.selection = 0

    def _files(self) -> list[str]:
        result = []
        for name in _list_dir(self._path):
            if _search(name.lower(), self._buf.lower(), regex=self._regex):
                result.append(name)
        return result

    @property
    def _page_updown_speed(self) -> int:
        return int(self._app.get_configvalue(config.Key.PAGE_UPDOWN_SPEED))

    def __init__(self, initial_path: str, app: IApp):
        self._path = initial_path
        self._app = app
        self._render_offset = 0
        self._header_size = 2
        self._selection = 0
        self._buf = ''
        self._regex = False
