"""
    Basic learner for active learning.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 15/12/2021
"""
from abc import ABC, abstractmethod


class Learner(ABC):
    """
    Learner: the basic class for learning process.
    """

    @abstractmethod
    def learn(self, data_x, data_y, n_epoch, batch_size, transform):
        pass

    @abstractmethod
    def infer(self, data, batch_size, is_prob):
        pass
