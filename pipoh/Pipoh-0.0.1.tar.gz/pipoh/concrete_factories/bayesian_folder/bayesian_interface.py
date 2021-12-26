# pylint: disable=too-few-public-methods
"""The Bayesian Interface"""
from abc import ABCMeta, abstractmethod
from pipoh.concrete_factories.bayesian_folder.bayesian_configuration import InitialConfiguration



class InterfaceBayesian(InitialConfiguration, metaclass=ABCMeta):
    """The Chair Interface (Product)"""

    @staticmethod
    @abstractmethod
    def solve_optimization_problem():
        """A static interface method"""


