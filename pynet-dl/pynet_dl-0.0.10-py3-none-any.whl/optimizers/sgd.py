import numpy as np
from typing import List

from pynet.optimizers.abstract import Optimizer
from pynet.tensor import Tensor


class SGD(Optimizer):
    """Represents Stochastic Gradient Descent (SGD) optimization algorithm with momentum.

    Stochastic Gradient Descent (SGD) is an iterative method for optimizing an objective 
    function with suitable smoothness properties (e.g. differentiable or subdifferentiable).
    Step of SGD with momentum is defined as:

    v(t + 1) = β * v(t) + g(t + 1)
    p(t + 1) = p(t) - α * v(t + 1)

    where p, g, v, α, β, t represent parameters, gradient, velocity, learning rate, momentum and
    number of algorithm's step respectively.
    """

    def __init__(self, learning_rate: float, momentum: float) -> None:
        """Ctor.

        Args:
            learning_rate (float): Learning rate.
            momentum (float): Momentum.
        """
        super().__init__()

        self.hyperparameters["lr"] = learning_rate
        self.hyperparameters["momentum"] = momentum

        self.__t = 0
        self.__params = None
        self.__velocities = None

    def register_parameters(self, params: List[Tensor]) -> None:
        self.__params = params
        self.__velocities = self.__create_velocities(params)

    def step(self) -> None:
        if not self.__params:
            raise ValueError(
                "Parameters not registered, call register_parameters function to register the parameters"
            )

        lr = self.hyperparameters["lr"]
        momentum = self.hyperparameters["momentum"]

        for i, (param, velocity) in enumerate(zip(self.__params, self.__velocities)):
            grad = param.grad

            if momentum > 0.0:
                if self.__t > 0:
                    velocity = momentum * velocity + (1.0 - momentum) * grad
                else:
                    velocity = grad.copy()

                grad = velocity
                self.__velocities[i] = velocity

            weights = param.ndarray - lr * grad
            self.__params[i].ndarray = weights
            self.__params[i].grad = None
            self.__t += 1

    def __create_velocities(self, params: List[Tensor]) -> List[np.ndarray]:
        velocities = []

        for param in params:
            velocities.append(np.zeros_like(param.ndarray))

        return velocities
