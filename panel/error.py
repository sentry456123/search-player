from panel.ipanel import IPanel
import irenderer
from irenderer import IRenderer
from iapp import IApp
import pygame
import config


class ErrorPanel(IPanel):

    def on_keydown(self, key: int, mod: int, unicode: str):
        font_size = self._app.get_font_size()
        match key:
            case pygame.K_j:
                self.offset -= font_size
            case pygame.K_k:
                self.offset += font_size
            case pygame.K_d:
                self.offset -= int(self._app.get_configvalue(config.Key.PAGE_UPDOWN_SPEED)) * font_size
            case pygame.K_u:
                self.offset += int(self._app.get_configvalue(config.Key.PAGE_UPDOWN_SPEED)) * font_size
            case pygame.K_ESCAPE:
                self._app.close_panel()

    def on_mousebuttondown(self, x: int, y: int, button: int):
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        font_size = self._app.get_font_size()
        match button:
            case pygame.BUTTON_WHEELDOWN:
                if not ctrl:
                    self.offset -= font_size
            case pygame.BUTTON_WHEELUP:
                if not ctrl:
                    self.offset += font_size
            case pygame.BUTTON_RIGHT:
                self._app.close_panel()

    def update(self):
        super().update()

    def render(self, r: IRenderer):
        r.fill(r.background_color())
        width, height = r.panel_size()
        r.wrapped_text(self._message, (0, self.offset, width, height), irenderer.MODERN_RED)

    def receive(self, retval):
        return super().receive(retval)

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, value: int):
        self._offset = value

    def __init__(self, message: str, app: IApp):
        self._app = app
        self._message = message
        self._offset = 0
