from typing import Optional, Union
from .node import Node


class Operand(Node):
    def __init__(self,
                 value: Union[int, float],
                 precision: int = 3,
                 symbol: Optional[str]=None,
                 **kwargs):
        super().__init__(value=value, **kwargs)
        self.symbol: str = str(value) if symbol is None else symbol
        self.width = len(self.symbol)
        self.priority = 20
        self.precision: int = precision

    def __str__(self):
        return f'{self.symbol:^{self.width}.{self.precision}}' if type(self.value) is float else f'{self.symbol:^{self.width}}'

    def __repr__(self) -> str:
        return f'Operand({self.value})'

    def isFull(self) -> bool:
        return True
