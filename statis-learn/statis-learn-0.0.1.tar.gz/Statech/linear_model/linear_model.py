import pandas as pd
import numpy as np
from typing import Union
import itertools
from ._base import LinearModel, RegressorMixin


class LinearRegression(RegressorMixin, LinearModel):
    def fit(self, X, y):
        X, y = self._validate_data(X, y)
        theta = np.linalg.inv(X.T * X) * X.T * y.T
        np_theta = np.array(theta).T.ravel()
        self._set_intercept(np_theta)
        self._set_coef(np_theta)
        return self


class HierarchicalRegression(RegressorMixin, LinearModel):
    def fit(self, X, y, *args):
        layers = args[0]
        k = 0
        for step in layers:
            k += step
            # 回归
            reg = LinearRegression()
            x_constant = reg.add_constant(X.iloc[:, 0:k])
            self._set_multi_model(reg.fit(x_constant, y))
        return self

    def score(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], *args) -> pd.DataFrame:
        nrow, ncol = X.shape
        k, ssr_old = 0, 0
        result = {}
        layers = args[0]
        f_change_value = pd.Series(0, name='F_change').astype(float)
        f_p_value = pd.Series(0, name='F_change_p').astype(float)
        for model, step, j in zip(self.multi_model_, layers, range(ncol)):
            k += step
            # 普通值
            score = model.score(X.iloc[:, 0:k], y)
            y_pred = model.predict(X.iloc[:, 0:k])
            # 计算f增量
            from Statech.metrics import ssr, mse, f_change, f_p
            mse_value = mse(y.values, y_pred, nrow, k)
            ssr_new = ssr(y.values, y_pred)
            f_change_value[0] = f_change(ssr_old, ssr_new, mse_value, step)
            f_p_value[0] = f_p(f_change_value, step, nrow, k)
            ssr_old = ssr_new
            # 结果
            result['layer' + str(j)] = [score[0], pd.concat([score[1], f_change_value, f_p_value], axis=1)]
        return result


class MediatingEffect(RegressorMixin, LinearModel):
    def fit(self, X, y, *args):
        # 设置变量
        x = X
        m = args[0]
        c = None
        if len(args) > 1:
            c = args[1]
            x = pd.concat([c, x], axis=1)

        # x->y
        reg = LinearRegression()
        x_constant = reg.add_constant(x)
        self._set_multi_model(reg.fit(x_constant, y))

        # x->m
        for i in range(m.shape[1]):
            y_m = m.iloc[:, i]
            reg = LinearRegression()
            self._set_multi_model(reg.fit(x_constant, y_m))

        # x_m->y
        x = pd.concat([x, m], axis=1)
        reg = LinearRegression()
        x_constant = reg.add_constant(x)
        self._set_multi_model(reg.fit(x_constant, y))
        return self

    def score(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], *args) -> pd.DataFrame:
        # 设置样本
        x = X
        m = args[0]
        c = None
        if len(args) > 1:
            c = args[1]
            x_c = pd.concat([x, c], axis=1)

        # 获x->y
        x_y_mode = self.multi_model_.pop(0)
        x_y_m_mode = self.multi_model_.pop()

        # x->y
        xcol = x.shape[1]
        x_y_result = x_y_mode.score(x_c, y)[0]
        c_ = x_y_result.iloc[-xcol:, 0].rename('c')

        # x->m
        mcol = m.shape[1]
        a_ = []
        for i in range(mcol):
            y_m = m.iloc[:, i]
            x_m_result = self.multi_model_[i].score(x_c, y_m)[0]
            a_.append(x_m_result.iloc[-xcol:, 0].values)
        cross_a = a_[0]
        for i in range(1, mcol):
            cross_a = list(itertools.chain.from_iterable(zip(cross_a, a_[i])))
        a_ = pd.Series(np.array(cross_a), name='a')

        # x_m->y
        x_c_m = pd.concat([x_c, m], axis=1)
        x_y_m_result = x_y_m_mode.score(x_c_m, y)[0]
        b_ = x_y_m_result.iloc[-mcol:, 0]
