import pygame
from collections import deque
from panel.ipanel import IPanel
import config
from typing import Optional
import irenderer
from irenderer import IRenderer
from panel.dir import DirPanel
from panel.error import ErrorPanel
import sys
import wrapper
from iapp import IApp
import numpy as np


class AppRenderer(IRenderer):

    def text(self, text: str, destination, color=irenderer.WHITE):
        font_image = self._app.font.render(text, True, color)
        self._app.surface.blit(font_image, destination)

    def wrapped_text(self, text: str, destination: tuple[int, int, int, int], color=irenderer.WHITE):
        texts = wrapper.wrap_multiline(text, self._app.font, destination[2])
        self.multitext(texts, destination, color)

    def multitext(self, texts: list[str], destination: tuple[int, int, int, int], color=irenderer.WHITE):
        x, y, w, h = destination
        for index, text in enumerate(texts):
            font_image = self._app.font.render(text, True, color)
            self._app.surface.blit(font_image, (x, y + self._app.get_font_size() * index, w, h))

    def rect(self, destination, color):
        pygame.draw.rect(self._app.surface, color, destination)

    def fill(self, color):
        self._app.surface.fill(color)

    def font(self) -> pygame.font.Font:
        return self._app.font

    def font_size(self) -> int:
        return self._app.get_font_size()

    def panel_size(self) -> tuple[int, int]:
        return self._app.surface.get_size()

    def font_color(self) -> tuple[int, int, int]:
        theme = self._app.get_configvalue(config.Key.THEME)
        if theme == 'dark':
            return irenderer.WHITE
        return irenderer.BLACK

    def background_color(self) -> tuple[int, int, int]:
        theme = self._app.get_configvalue(config.Key.THEME)
        if theme == 'dark':
            return irenderer.GRAY
        return irenderer.WHITE

    def __init__(self, app: 'App'):
        self._app = app


class App(IApp):

    def mainloop(self):
        while self._running:
            event = pygame.event.wait()
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.KEYDOWN:
                    panel = self._get_focused_panel()
                    try:
                        panel.on_keydown(event.key, event.mod, event.unicode)
                    except Exception as e:
                        self.display_error(str(e))
                case pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self._on_mousebuttondown(x, y, event.button)
                    panel = self._get_focused_panel()
                    try:
                        panel.on_mousebuttondown(x, y, event.button)
                    except Exception as e:
                        self.display_error(str(e))
            if len(self._panel_stack) <= 0:
                break
            try:
                self._get_focused_panel().update()
            except Exception as e:
                self.display_error(str(e))

            self._renderer.fill(self._renderer.background_color())
            self._get_focused_panel().render(self._renderer)

            pygame.display.update()

    def open_panel(self, panel: IPanel):
        self._panel_stack.append(panel)

    def close_panel(self, retval=None):
        self._panel_stack.pop()
        if retval is not None:
            self._get_focused_panel().receive(retval)

    def display_error(self, msg: str):
        print(f'ERROR: {msg}', file=sys.stderr)
        self.open_panel(ErrorPanel(msg, self))

    def quit(self):
        self._running = False

    def get_font_size(self):
        return self._fontsize

    def update_font_size(self, font_size: int):
        font_size = np.clip(font_size, 20, 100)
        self._fontsize = font_size
        self.font = pygame.font.SysFont(config.get_value(self._conf, config.Key.FONT), int(float(self._fontsize) * 0.75))

    def get_configvalue(self, key: str) -> str:
        return config.get_value(self._conf, key)

    def _on_mousebuttondown(self, x: int, y: int, button: int):
        ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
        wheeldown = button == pygame.BUTTON_WHEELDOWN
        wheelup = button == pygame.BUTTON_WHEELUP
        font_size = self.get_font_size()

        if ctrl and wheeldown:
            font_size -= 2
        if ctrl and wheelup:
            font_size += 2

        self.update_font_size(font_size)

    def _get_focused_panel(self) -> IPanel:
        return self._panel_stack[-1]

    def __init__(self):
        err: Optional[str] = None
        try:
            self._conf = config.load()
        except Exception as e:
            err = f'Failed to load configuration file: {str(e)}'
            self._conf = {}

        pygame.init()
        pygame.display.set_caption('Search Player')
        pygame.display.set_icon(pygame.image.load('icon.png'))

        self._panel_stack = deque[IPanel]()
        self.surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self._fontsize = int(config.get_value(self._conf, config.Key.INITIAL_FONTSIZE))
        self.update_font_size(self._fontsize)
        self._renderer = AppRenderer(self)
        self._running = True

        self.open_panel(DirPanel(config.get_value(self._conf, config.Key.INITIAL_DIRECTORY), self))

        if err is not None:
            self.display_error(err)

    def __del__(self):
        pygame.quit()
