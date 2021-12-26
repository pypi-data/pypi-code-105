"""The Abstract Factory Interface"""
from abc import ABCMeta, abstractmethod


class InterfaceStrategyFactory(metaclass=ABCMeta):
    """Abstract Strategy Factory Interface"""

    @staticmethod
    @abstractmethod
    def get_strategy(strategy_selected):
        """The static Abstract factory interface method"""

    @staticmethod
    @abstractmethod
    def initial_configuration(strategy_selected):
        """The static Abstract factory interface method"""
