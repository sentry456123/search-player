from ipanel import IPanel
import irenderer
from irenderer import IRenderer
from iapp import IApp
import wrapper
import pygame
import config
import re


def _search_string(text: str, pattern: str, regex=False) -> bool:
    if regex:
        return re.search(pattern, text) is not None

    text_pos = 0
    for pattern_char in pattern:
        if pattern_char not in text[text_pos:]:
            return False
        text_pos = text.index(pattern_char, text_pos) + 1
    return True


class SelectInputPanel(IPanel):

    def on_keydown(self, key: int, mod: int, unicode: str):
        if mod & pygame.KMOD_CTRL:
            match key:
                case pygame.K_c:
                    self._buf = ''
                case pygame.K_j:
                    self._move_selection(1)
                    self._move_selection(1)
                case pygame.K_k:
                    self._move_selection(-1)
                case pygame.K_d:
                    self._move_selection(self._page_updown_speed)
                case pygame.K_u:
                    self._move_selection(-self._page_updown_speed)
                case pygame.K_r:
                    self._regex = not (mod & pygame.KMOD_SHIFT)
                case pygame.K_BACKSPACE:
                    while len(self._buf) <= 0:
                        self._buf = self._buf[:-1]
                        if self._buf[-1] == ' ':
                            break
                    self._set_selection(0)
        else:
            match key:
                case pygame.K_RETURN | pygame.K_TAB:
                    self._return_value(self._get_selected())
                case pygame.K_UP:
                    self._move_selection(-1)
                case pygame.K_DOWN:
                    self._move_selection(1)
                case pygame.K_PAGEDOWN:
                    self._move_selection(self._page_updown_speed)
                case pygame.K_PAGEUP:
                    self._move_selection(-self._page_updown_speed)
                case pygame.K_HOME:
                    self._set_selection(0)
                case pygame.K_END:
                    self._set_selection(len(self._words) - 1)
                case pygame.K_BACKSPACE:
                    self._buf = self._buf[:-1]
                    self._set_selection(0)
                case _:
                    if len(unicode) != 0 and unicode in irenderer.TYPABLE:
                        self._buf += unicode
                        self._set_selection(0)

    def on_mousebuttondown(self, x: int, y: int, button: int):
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        font_size = self._app.get_font_size()
        match button:
            case pygame.BUTTON_LEFT:
                self._set_selection(int(y / font_size - self._render_offset - self._header_size))
            case pygame.BUTTON_RIGHT:
                self._return_value(self._get_selected())
            case pygame.BUTTON_WHEELDOWN:
                if not ctrl:
                    self._move_selection(-1)
            case pygame.BUTTON_WHEELUP:
                if not ctrl:
                    self._move_selection(1)
            case pygame.BUTTON_MIDDLE:
                self._buf = ''

    def update(self):
        self._sort_words(self._initial_words)
        self._set_selection(self._selection)

    def render(self, r: IRenderer):
        width, height = r.panel_size()
        font_size = r.font_size()
        font = r.font()

        self._render_offset = 0
        if self._selection >= (height / font_size) / 2:
            self._render_offset = -self._selection + (height / font_size) / 2 - 1

        r.rect((0, (self._selection + self._header_size + self._render_offset) * font_size, width, font_size), irenderer.MODERN_RED)

        for i, name in enumerate(self._words):
            color = irenderer.MODERN_YELLOW if name[-1] == '/' else irenderer.WHITE
            r.text(name, (0, (i + self._header_size + self._render_offset) * font_size), color=color)

        r.rect((0, 0, width, font_size), irenderer.WHITE)
        r.text(self._words, (width - font.size(self._words)[0], 0), color=irenderer.BLACK)

        color = irenderer.MODERN_BLUE
        r.rect((0, font_size, width, font_size), color)
        buf = self._buf
        if self._regex:
            buf = 'Regex: ' + buf
        r.text(wrapper.cut(buf, font, width), (0, font_size))

    def receive(self, retval):
        return super().receive(retval)

    def _get_selected(self):
        selected = self._get_selected()
        self._app.close_panel(retval=selected)

    def _return_value(self, retval):
        self._app.close_panel(retval=retval)

    def _sort_words(self, new_words: list[str]):
        self._words = []
        for word in new_words:
            if _search_string(word.lower(), self._buf.lower(), self._regex):
                self._words.append(word)

    def _set_selection(self, selection):
        self._selection = selection
        if self._selection >= len(self._words):
            self._selection = len(self._words) - 1
        if self._selection < 0:
            self._selection = 0

    def _move_selection(self, offset: int):
        self._set_selection(self._selection + offset)

    def _get_selected(self) -> str:
        if len(self._words) == 0:
            return ''
        return self._words[self._selection]

    def __init__(self, title: str, words: list[str], app: IApp):
        self._title = title
        self._initial_words = words
        self._app = app
        self._words: list[str] = []
        self._header_size = 2
        self._page_updown_speed = self._app.get_configvalue(config.PAGE_UPDOWN_SPEED_KEY)
        self._selection = 0
        self._buf = ''
        self._regex = False
