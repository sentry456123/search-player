from abc import ABC, abstractmethod
from irenderer import IRenderer


class IPanel(ABC):

    @abstractmethod
    def on_keydown(self, key: int, mod: int, unicode: str): ...

    @abstractmethod
    def on_mousebuttondown(self, x: int, y: int, button: int): ...

    @abstractmethod
    def update(self): ...

    @abstractmethod
    def render(self, r: IRenderer): ...

    @abstractmethod
    def receive(self, retval): ...
