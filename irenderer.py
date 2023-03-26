import pygame
import string
from abc import ABC, abstractmethod


MODERN_GREEN = (30, 255, 30)
MODERN_BLUE = (30, 30, 255)
MODERN_CYAN = (30, 255, 255)
MODERN_RED = (255, 30, 30)
MODERN_YELLOW = (255, 255, 30)
GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TYPABLE = string.digits + string.ascii_letters + string.punctuation + ' '


class IRenderer(ABC):

    @abstractmethod
    def text(self, text: str, destination, color=WHITE): ...

    @abstractmethod
    def wrapped_text(self, text: str, destination: tuple[int, int, int, int], color=WHITE): ...

    @abstractmethod
    def multitext(self, texts: list[str], destination: tuple[int, int, int, int], color=WHITE): ...

    @abstractmethod
    def rect(self, destination, color): ...

    @abstractmethod
    def fill(self, color): ...

    @abstractmethod
    def font(self) -> pygame.font.Font: ...

    @abstractmethod
    def font_size(self) -> int: ...

    @abstractmethod
    def panel_size(self) -> tuple[int, int]: ...
