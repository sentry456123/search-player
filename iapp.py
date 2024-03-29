from panel.ipanel import IPanel
from abc import ABC, abstractmethod


class IApp(ABC):

    @abstractmethod
    def open_panel(self, panel: IPanel): ...

    @abstractmethod
    def close_panel(self, retval=None): ...

    @abstractmethod
    def display_error(self, msg: str): ...

    @abstractmethod
    def get_font_size(self) -> int: ...

    @abstractmethod
    def update_font_size(self, font_size: int): ...

    @abstractmethod
    def quit(self): ...
