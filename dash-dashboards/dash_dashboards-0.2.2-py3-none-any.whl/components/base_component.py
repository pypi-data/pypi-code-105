from abc import ABC, abstractmethod

from dash.development.base_component import Component


class BaseComponent(ABC):
    @property
    @abstractmethod
    def layout(self) -> Component:
        pass
