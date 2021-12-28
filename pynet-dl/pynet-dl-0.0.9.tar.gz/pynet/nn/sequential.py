from typing import List

from pynet.nn.abstract import Module
from pynet.tensor import Tensor


class Sequential(Module):
    """Represents a container for other modules.

    During the forward step, each subsequent module's forward step function is called. 
    Finally, it returns the output of the last module. During the backward step,
    subsequent modules are iterated in reversed order calling backward step function
    for each of them.
    """

    def __init__(self, modules: List[Module]) -> None:
        """Ctor.

        Args:
            modules (List[Module]): List of modules to be added to the sequential container.
        """
        super().__init__()

        self.__modules = modules

    def forward(self, x: Tensor) -> Tensor:
        for module in self.__modules:
            x = module.forward(x)

        return x

    def backward(self, y: Tensor) -> Tensor:
        for module in reversed(self.__modules):
            y = module.backward(y)

        return y

    def get(self, idx: int) -> Module:
        """Returns a module at the <idx> position within the container.

        Args:
            idx (int): Index of a module within the container.

        Returns:
            Module: Module at the <idx> position within the container.
        """
        return self.__modules[idx]

    def get_parameters(self) -> List[Tensor]:
        params = []

        for module in self.__modules:
            mparams = module.get_parameters()
            if mparams:
                params.extend(mparams)

        return params
