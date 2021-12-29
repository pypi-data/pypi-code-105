import numpy as np
import pandas as pd

from scipy.optimize import minimize


def smc(corr_mtx):
    """
    主因子法：第一种估计h的方法
    :param corr_mtx:
    :param sort:
    :return:
    """
    corr_inv = np.linalg.inv(corr_mtx)
    # r_ii = R^-1
    # std = 1/r_ii
    # h = 1 - std
    smc = 1 - 1 / np.diag(corr_inv)
    return smc


def corr(x: np.array):
    x = (x - x.mean(0)) / x.std(0)
    return np.cov(x, rowvar=False, ddof=0)


class Factor:
    def __init__(self,
                 n_factors=3,
                 rotaion='promax',
                 method='ml',
                 use_smc=True,
                 bounds=(0.005, 1)):
        """
            use_smc 是否使用平方多重相关作为因子分析的起始猜测
        """
        self.bounds = bounds
        self.use_smc = use_smc
        self.method = method
        self.rotaion = rotaion
        self.n_factors = n_factors

        self.loadings_ = None
        self.rotation_matrix_ = None

    def fit(self, X):
        if isinstance(X, pd.DataFrame):
            X = X.values.copy()
        else:
            X = X.copy()

        # 获取相关矩阵
        corr_mtx = corr(X)
        self.std_ = np.std(X, axis=0)
        self.mean_ = np.mean(X, axis=0)

        if self.method == 'principal':
            loadings = self._fit_principal(corr_mtx)
        else:
            loadings = self._fit_ml(corr_mtx)

        self.loadings_ = loadings
        return self.loadings_

    def _fit_principal(self, corr_mtx):

        pass

    def _fit_ml(self, corr_mtx):
        """
        估计值的预处理
        :param corr_mtx:
        :return:
        """
        # 估计误差的值
        if self.use_smc:
            smc_mtx = smc(corr_mtx)
            # 随机初始化ψ_0值
            start = (np.diag(corr_mtx) - smc_mtx.T).squeeze()
        else:
            # 随机值设置0.5
            start = [0.5 for _ in range(corr_mtx.shape[0])]

        # this must be a list passed to `minimize()`
        bounds = self.bounds

        # 将随机估计的误差值，通过 minimize进最小化(梯度下降，巨呃度下降，牛顿下降)
        objective = self._fit_ml_objective
        res = minimize(objective,
                       start,
                       method='CG',
                       bounds=bounds,
                       options={'maxiter': 1000},
                       args=(corr_mtx, self.n_factors))

        # 求因子载荷，通过极小误差
        return self._normalize_ml(res.x, corr_mtx, self.n_factors)

    @staticmethod
    def _fit_ml_objective(psi, corr_mtx, n_factors):
        """
        求估计误差极小值
        :param psi: 主因子法估计的误差值
        :param corr_mtx:
        :param n_factors:
        :return:
        """
        std_0_ = np.diag(1 / np.sqrt(psi))
        std_s_std = np.dot(np.dot(std_0_, corr_mtx), std_0_)

        feature, _ = np.linalg.eigh(std_s_std)
        feature = feature[::-1][n_factors:]

        error = -(np.sum(np.log(feature) - feature) - n_factors + corr_mtx.shape[0])
        return error

    def _normalize_ml(self, x, corr_mtx, n_factors):
        """
        通过ψ_0 求 Λ_0 , Λ_0 -> ψ_1
        :param x:
        :param corr_mtx:
        :param n_factors:
        :return:
        """
        std_0_ = np.diag(1 / np.sqrt(x))
        std_s_std = np.dot(np.dot(std_0_, corr_mtx), std_0_)

        feature, vector = np.linalg.eigh(std_s_std)
        feature = feature[::-1][:n_factors]
        vector = vector[:, ::-1][:, :n_factors]

        feature = np.maximum(feature - 1, 0)

        loadings = np.dot(vector, np.diag(np.sqrt(feature)))

        return np.dot(np.diag(np.sqrt(x)), loadings)


if __name__ == '__main__':
    data = pd.read_excel('../../data/pathanalysis.xlsx', index_col=0)
    fa = Factor(n_factors=1)
    loading = fa.fit(data)
    print(loading)
