import pygame
import os
from panel.ipanel import IPanel
import irenderer
from irenderer import IRenderer
import config
from searchengine import SearchEngine
from iapp import IApp


class DirPanel(IPanel):

    def on_keydown(self, key: int, mod: int, unicode: str):
        if mod & pygame.KMOD_CTRL:
            match key:
                case pygame.K_c:
                    self._engine.buf = ''
                case pygame.K_h:
                    self._parentdir()
                    self._engine.buf = ''
                case pygame.K_j:
                    self._engine.move_selection(1)
                case pygame.K_k:
                    self._engine.move_selection(-1)
                case pygame.K_d:
                    self._engine.move_selection(self._page_updown_speed)
                case pygame.K_u:
                    self._engine.move_selection(-self._page_updown_speed)
                case pygame.K_l:
                    self._open_selected()
                case pygame.K_r:
                    self._engine.regex = not (mod & pygame.KMOD_SHIFT)
                case pygame.K_BACKSPACE:
                    while len(self._engine.buf) <= 0:
                        self._engine.buf = self._engine.buf[:-1]
                        if self._engine.buf[-1] == ' ':
                            break
                    self._engine.set_selection(0)
        else:
            match key:
                case pygame.K_RETURN | pygame.K_TAB:
                    self._open_selected(erase_buf_on_dir=True)
                case pygame.K_RIGHT:
                    self._open_selected()
                case pygame.K_UP:
                    self._engine.move_selection(-1)
                case pygame.K_DOWN:
                    self._engine.move_selection(1)
                case pygame.K_LEFT:
                    self._parentdir()
                    self._engine.buf = ''
                case pygame.K_PAGEUP:
                    self._engine.move_selection(-self._page_updown_speed)
                case pygame.K_PAGEDOWN:
                    self._engine.move_selection(self._page_updown_speed)
                case pygame.K_HOME:
                    self._engine.set_selection(0)
                case pygame.K_END:
                    self._engine.set_selection(len(self._engine.words) - 1)
                case pygame.K_BACKSPACE:
                    self._engine.buf = self._engine.buf[:-1]
                    self._engine.set_selection(0)
                case _:
                    if len(unicode) != 0 and unicode in irenderer.TYPABLE:
                        self._engine.buf += unicode
                        self._engine.set_selection(0)

    def on_mousebuttondown(self, x: int, y: int, button: int):
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        font_size = self._app.get_font_size()
        match button:
            case pygame.BUTTON_LEFT:
                self._engine.set_selection(int(y / font_size - self._render_offset - self._header_size))
            case pygame.BUTTON_RIGHT:
                self._open_selected()
            case pygame.BUTTON_WHEELDOWN:
                if not ctrl:
                    self._engine.move_selection(1)
            case pygame.BUTTON_WHEELUP:
                if not ctrl:
                    self._engine.move_selection(-1)
            case pygame.BUTTON_MIDDLE:
                self._engine.buf = ''
            case pygame.BUTTON_X1:
                self._parentdir()
                self._engine.buf = ''
            case pygame.BUTTON_X2:
                self._open_selected()

    def update(self):
        self._engine.sort_words(self._list_dir())
        self._engine.set_selection(self._engine.selection)

    def render(self, r: IRenderer):
        width, height = r.panel_size()
        font_size = r.font_size()
        font = r.font()
        theme = self._app.get_configvalue(config.Key.THEME)

        self._render_offset = 0
        if self._engine.selection >= (height / font_size) / 2:
            self._render_offset = -self._engine.selection + (height / font_size) / 2 - 1

        color = (120, 120, 120) if theme == 'dark' else (200, 200, 200)
        r.rect((0, (self._engine.selection + self._header_size + self._render_offset) * font_size, width, font_size), color)

        for i, name in enumerate(self._engine.words):
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

        frame_thinness = int(self._app.get_configvalue(config.Key.FRAME_THINNESS))
        r.rect((0, font_size, width, font_size), irenderer.MODERN_BLUE)
        r.rect((frame_thinness, font_size + frame_thinness, width - frame_thinness*2, font_size - frame_thinness*2),
               r.background_color())

        buf = self._engine.buf
        if self._engine.regex:
            buf = 'Regex: ' + buf
        if width > font.size(buf)[0]:
            offset = 0
        else:
            offset = width - font.size(buf)[0]
        r.text(buf, (offset, font_size), r.font_color())

    def receive(self, retval):
        return super().receive(retval)

    def _open_selected(self, erase_buf_on_dir=False):
        if len(self._engine.words) <= 0:
            return
        path = self._engine.get_selected()
        if self._is_file(path):
            os.startfile(os.path.join(self._path, path))
        else:
            self._change_dir(path)
            if erase_buf_on_dir:
                self._engine.buf = ''

    def _parentdir(self):
        self._change_dir('../')

    def _change_dir(self, path: str) -> str:
        abs_dist = os.path.abspath(self._path)
        new_path = os.path.join(abs_dist, path)
        self._path = os.path.abspath(new_path)
        self._engine.set_selection(0)

    def _list_dir(self) -> list[str]:
        result = ['./', '../']

        listeddir = os.listdir(self._path)

        for name in listeddir:
            if self._is_dir(name):
                result.append(name + '/')

        for name in listeddir:
            if self._is_file(name):
                result.append(name)

        return result

    def _is_file(self, path) -> bool:
        abs = os.path.join(self._path, path)
        return os.path.isfile(abs)

    def _is_dir(self, path) -> bool:
        return not self._is_file(path)

    def __init__(self, initial_path: str, app: IApp):
        self._path = initial_path
        self._app = app
        self._page_updown_speed = int(app.get_configvalue(config.Key.PAGE_UPDOWN_SPEED))
        self._render_offset = 0
        self._header_size = 2
        self._engine = SearchEngine()
