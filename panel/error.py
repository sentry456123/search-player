from panel.ipanel import IPanel
import irenderer
from irenderer import IRenderer
from iapp import IApp


class ErrorPanel(IPanel):

    def on_keydown(self, key: int, mod: int, unicode: str):
        self._app.close_panel()

    def on_mousebuttondown(self, x: int, y: int, button: int):
        self._app.close_panel()

    def update(self):
        super().update()

    def render(self, r: IRenderer):
        r.fill(r.background_color())
        width, height = r.panel_size()
        r.wrapped_text(self._message, (0, 0, width, height), irenderer.MODERN_RED)

    def receive(self, retval):
        return super().receive(retval)

    def __init__(self, message: str, app: IApp):
        self._app = app
        self._message = message
