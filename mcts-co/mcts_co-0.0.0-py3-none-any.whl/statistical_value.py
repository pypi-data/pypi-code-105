from typing import Optional, Union
import math


class StatisticalValue:
    use_var = False

    def __init__(
        self,
        value: Optional[Union[float, "StatisticalValue"]] = None,
    ):
        """Statistical Value

        In a stochastic optimization problem, especially in the best arm
        identification problem, we should maintain the mean, variance, and the
        number of observations to compute the confidence interval of the values.
        This class stores such values.
        """
        if value is None:
            self.sum = 0
            self.sum2 = 0
            self.count = 0
        elif isinstance(value, StatisticalValue):
            self.sum = value.sum
            self.sum2 = value.sum2
            self.count = value.count
        else:
            self.sum = 2 * value
            self.sum2 = 2 * value ** 2
            self.count = 2

    def add(self, value: Union[float, "StatisticalValue"]):
        """Adds new observation

        Parameters
        ----------
        value
            single observation if it is a `float` and multiple observations if
            it is a `StatisticalValue`.
        """
        if isinstance(value, StatisticalValue):
            self.sum += value.sum
            self.sum2 += value.sum2
            self.count += value.count
        else:
            self.sum += value
            self.sum2 += value ** 2
            self.count += 1

    def mean(self) -> float:
        """Returns the population mean of the observations

        The population mean is given by

        .. math:: \\frac{1}{T} \\sum_{i=1}^T X_i

        where :math:`T` is the number of observations and :math:`X_i` is the :math:`i`-th observation.

        """
        if self.count == 0:
            return 0
        return self.sum / self.count

    def var(self) -> float:
        """Returns the population variance of the observations

        The population variance is given by

        .. math:: \\frac{T}{T - 1} \\left[ \\frac{1}{T} \\sum_{i=1}^T X_i^2 - \\left( \\frac{1}{T} \\sum_{i=1}^T X_i \\right) \\right]

        where :math:`T` is the number of observations and :math:`X_i` is the :math:`i`-th observation.

        """
        return max(0.0, self.sum2 / self.count - self.mean() ** 2)

    def beta(
        self, *, a: float = 2.0, b: float = 1.0, count: Optional[int] = None
    ) -> float:
        """Returns the radius of the confidence interval

        In the multi-armed bandit, the radius of the confidence interval is given by the formula

        .. math:: \\beta(T; a, b) = \\sqrt{\\frac{2 a \\sigma^2}{T}} + \\frac{(7/3) a b}{T - 1}

        where :math:`a` and :math:`b` are parameters and :math:`T` is the number of observations of the arm.
        """
        if self.count == 0:
            return math.inf
        if count is not None:
            a *= math.log(count)
        if self.use_var:
            term1 = math.sqrt(a * self.var() / self.count)
            term2 = (7 / 3) * a * b / self.count
            return term1 + term2
        else:
            return math.sqrt(a / self.count)

    def ucb(
        self, *, a: float = 2.0, b: float = 1.0, count: Optional[int] = None
    ) -> float:
        if self.count <= 1:
            return math.inf
        return self.mean() + self.beta(a=a, b=b, count=count)

    def __repr__(self):
        return f"StatisticalValue({self.mean()}, {self.count})"
