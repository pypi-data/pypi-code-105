from abc import abstractmethod
from typing import Any, List, Optional


class Node:
    def __init__(self,
                 value=None):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self.value: Any = value
        self.height: int = 1
        self.priority: int = -1
        self.width: int = 0

    @abstractmethod
    def isFull(self) -> bool:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    def __lt__(self, otherNode) -> bool:
        return self.priority < otherNode.priority

    def __le__(self, otherNode) -> bool:
        return self.priority <= otherNode.priority

    def __gt__(self, otherNode) -> bool:
        return self.priority > otherNode.priority

    def __ge__(self, otherNode) -> bool:
        return self.priority >= otherNode.priority

    def __call__(self) -> Any:
        return self.value

    @abstractmethod
    def __str__(self) -> str:
        pass