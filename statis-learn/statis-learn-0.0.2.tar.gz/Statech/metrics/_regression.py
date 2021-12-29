import numpy as np


def ssr(y_true, y_pred):
    y_mean = np.mean(y_true)
    return np.sum(np.power((y_pred - y_mean), 2))


def sse(y_true, y_pred):
    return np.sum(np.power((y_true - y_pred), 2))


def sst(y_true, y_pred):
    return ssr(y_true, y_pred) + sse(y_true, y_pred)


def mse(y_true, y_pred, n, k):
    """
    :param y_true: 真实值
    :param y_pred: 预测值
    :param n: 自由度
    :param k: 可控自由
    :return:
    """
    return sse(y_true, y_pred) / (n - k - 1)


def mst(y_true, y_pred, n, k):
    return sst(y_true, y_pred) / (n - k - 1)


def msr(y_true, y_pred, k):
    """

    :param y_true: 真实值
    :param y_pred: 预测值
    :param k: 可控自由度
    :return:
    """
    return ssr(y_true, y_pred) / k


def r_square(y_true, y_pred):
    return ssr(y_true, y_pred) / sst(y_true, y_pred)


def adjust_r_square(y_true, y_pred, n, k):
    return 1 - (1 - r_square(y_true, y_pred)) * (n - 1) / (n - k - 1)


def f(y_true, y_pred, n, k):
    return msr(y_true, y_pred, k) / mse(y_true, y_pred, n, k)


def bse(X: np.ndarray, y_true, y_pred, n, k):
    normalized_cov_params = np.linalg.inv(np.dot(X.T, X))
    cov_p = normalized_cov_params * mse(y_true, y_pred, n, k)
    return np.sqrt(np.diag(cov_p))


def t(theta, X: np.ndarray, y_true, y_pred, n, k):
    return theta / bse(X, y_true, y_pred, n, k)


def t_p(theta, X: np.ndarray, t_value, n, k):
    from scipy.stats import t
    return t.sf(abs(t_value), n - k - 1) * 2


def std_coef(coef, X: np.ndarray, y):
    x_std = np.std(X, axis=0)
    y_std = np.std(y)
    return np.append(0, np.multiply(coef, (x_std / y_std)))


def f_change(ssr_old, ssr, mse, gap):
    return ((ssr - ssr_old) / gap) / mse


def f_p(f_change, gap, n, k):
    from scipy.stats import f
    return f.sf(abs(f_change), gap, n - k - 1)
