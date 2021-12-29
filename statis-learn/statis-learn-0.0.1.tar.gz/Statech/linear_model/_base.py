from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from Statech.metrics import *
from typing import Union

from Statech.spssbase import SpssPro
from Statech.pojo.errors import AlgorithmError


class LinearModel(SpssPro, metaclass=ABCMeta):
    """Base class for Linear Models"""

    def __init__(self):
        self.multi_model_ = []

    @abstractmethod
    def fit(self, X, y, *args):
        """Fit model."""
        pass

    def _validate_data(self, X, y=None) -> np.mat:
        """
        数据类型检验转换，
        :param X:
        :param y:
        :return: 矩阵X,矩阵y
        """
        if not isinstance(X, (pd.DataFrame, np.ndarray, list)):
            raise AlgorithmError("类型错误")

        if isinstance(X, pd.DataFrame):
            X_val = np.mat(X.values)
        elif isinstance(X, (np.ndarray, list)):
            X_val = np.mat(X)

        if y is not None:
            if isinstance(y, (pd.DataFrame, pd.Series)):
                y_val = np.mat(y.values)
            elif isinstance(X, (np.ndarray, list)):
                y_val = np.mat(y)
            return X_val, y_val
        return X_val

    def add_constant(self, X):
        X = self._validate_data(X)
        one_vector = np.ones((X.shape[0], 1))
        return np.hstack((one_vector, X))

    def _decision_function(self, X):
        """
        计算预测值
        :param X:
        :return:
        """
        return X.dot(self.coef_) + self.intercept_

    def predict(self, X):
        X = self._validate_data(X)
        return self._decision_function(X)

    def _set_intercept(self, theta):
        """Set the intercept_"""
        self.intercept_ = theta[0]

    def _set_coef(self, theta):
        self.coef_ = theta[1:]

    def _set_multi_model(self, model):
        self.multi_model_.append(model)


class RegressorMixin:
    def score(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], *args) -> pd.DataFrame:
        """
        获取commom回归分析结果
        :param X:
        :param y:
        :return: 系数，标准误，标准化系数，t，p，R2，调整R2，F
        """
        # 原始值
        X, y = self._validate_data(X, y)
        n, k = X.shape
        # 可能需要的值
        y_pred = self.predict(X)
        x_add = self.add_constant(X)
        intercept_ = self.intercept_
        coef_ = self.coef_
        theta = np.append(intercept_, coef_)
        # 结果
        result_bse = pd.Series(bse(x_add, y, y_pred, n, k), name='标准误')
        result_std_coef = pd.Series(std_coef(coef_, X, y), name='标准化系数')
        result_t = pd.Series(t(theta, x_add, y, y_pred, n, k), name='t')
        result_t_p = pd.Series(t_p(theta, x_add, result_t, n, k), name='p')
        result_r_square = pd.Series(r_square(y, y_pred), name='R2')
        result_adjust_r_square = pd.Series(adjust_r_square(y, y_pred, n, k), name='调整R2')
        result_f = pd.Series(f(y, y_pred, n, k), name='F')
        result_theta = pd.Series(theta, name='B')
        score_1 = pd.concat([result_theta,
                             result_bse,
                             result_std_coef,
                             result_t,
                             result_t_p],
                            axis=1)
        score_2 = pd.concat([result_r_square, result_adjust_r_square, result_f], axis=1)
        return score_1, score_2
