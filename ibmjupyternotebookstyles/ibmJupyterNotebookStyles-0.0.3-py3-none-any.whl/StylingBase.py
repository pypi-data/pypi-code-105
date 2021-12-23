from __future__ import annotations
from abc import ABC, abstractmethod


class StyleComponent(ABC):
    def accept(self, visitor: Visitor):
        visitor.visit(self)

    def apply(self) -> None:
        pass


class Visitor(ABC):
    @abstractmethod
    def visit(self, element: StyleComponent) -> None:
        pass


class ConcreteVisitor(Visitor):
    def visit(self, element) -> None:
        element.apply()
