import math


class Statistics:
    """Class used to preserve discrete statistics."""

    def __init__(self, name: str) -> None:
        """Ctor.

        Args:
            name (str): Name of the statistic.
        """
        self.name = name

        self.__n = 0
        self.__min = float("inf")
        self.__max = float("-inf")
        self.__sum = 0
        self.__old_mean = 0
        self.__new_mean = 0
        self.__old_square_sum = 0
        self.__new_square_sum = 0

    def n(self) -> int:
        """Returns number of samples within the statistic.

        Returns:
            int: Number of samples within the statistic.
        """
        return self.__n

    def mean(self) -> float:
        """Returns statistic's mean.

        Returns:
            float: Statistic's mean.
        """
        return self.__new_mean if self.__n > 0 else 0.0

    def min(self) -> float:
        """Returns minimum sample value.

        Returns:
            float: Minimum sample value.
        """
        return self.__min

    def max(self) -> float:
        """Returns maximum sample value.

        Returns:
            float: Maximum sample value.
        """
        return self.__max

    def variance(self) -> float:
        """Returns statistic's variance.

        Returns:
            float: Statistic's variance.
        """
        return self.__new_square_sum / (self.__n - 1.0) if self.__n > 1 else 0.0

    def std(self) -> float:
        """Returns statistic's standard deviation.

        Returns:
            float: Statistic's standard deviation.
        """
        return math.sqrt(self.variance())

    def sum(self) -> float:
        """Returns sum of samples.

        Returns:
            float: Sum of samples.
        """
        return self.__sum

    def add(self, x: float) -> None:
        """Adds new sample to the statistic.

        Args:
            x (float): New sample to be added.
        """
        self.__n += 1

        if x < self.__min:
            self.__min = x

        if x > self.__max:
            self.__max = x

        self.__sum += x

        if self.__n == 1:
            self.__old_mean = self.__new_mean = x
            self.__old_square_sum = 0.0
        else:
            self.__new_mean = self.__old_mean + (x - self.__old_mean) / self.__n
            self.__new_square_sum = self.__old_square_sum + (x - self.__old_mean) * (
                x - self.__new_mean
            )

            self.__old_mean = self.__new_mean
            self.__old_square_sum = self.__new_square_sum

    def reset(self) -> None:
        """Resets statistic."""
        self.__n = 0
        self.__min = float("inf")
        self.__max = float("-inf")
        self.__sum = 0.0
