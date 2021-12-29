import cmath

import numpy as np
import pandas as pd
from scipy.stats import f
from sympy.matrices import Matrix as sy_matrix


def matrixPower(A, n):
    v, Q = np.linalg.eig(A)
    V = np.diag(v ** (n))
    T = Q * V * np.linalg.inv(Q)
    # T = Q * V * (Q ** (-1))
    return T.copy()


def multi(lambdas, k):
    r = len(lambdas)
    sum = 1
    for i in range(k, r):
        sum *= (1 - lambdas[i] ** 2)
    return sum


class CCAs:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.X = X
        self.y = y
        self.n = len(X)
        # corr : 数据标准化后的协方差矩阵
        # cov : 数据的协方差矩阵
        self.R = pd.concat([X, y], axis=1).cov()
        r = self.R.to_numpy()
        self.Sxx = np.mat(r[:X.shape[1], :X.shape[1]])
        self.Syy = np.mat(r[X.shape[1]:, X.shape[1]:])
        self.Sxy = np.mat(r[:X.shape[1]:, X.shape[1]:])
        self.Syx = self.Sxy.T
        self.s = min(X.shape[1], y.shape[1])
        self.p = X.shape[1]
        self.q = y.shape[1]

    def fecth_n(self):
        # 正交求解法
        # self.Nb = QRsolve(self.Syy, self.Syx) * QRsolve(self.Sxx, self.Sxy)
        self.Nb = sy_matrix(self.Syy).QRsolve(sy_matrix(self.Syx)) * sy_matrix(self.Sxx).QRsolve(sy_matrix(self.Sxy))

    def fecth_m(self):
        self.M = matrixPower(self.Sxx, -0.5) * self.Sxy * matrixPower(self.Syy, -0.5)

    def eig(self, m):
        # 注意上面矩阵的列向量才是特征向量，l2范数为 1
        return np.linalg.eig(m)

    def fetch_a_b_fv(self):
        b_feature, b_vector = self.eig(np.mat(self.Nb).astype(np.float64))
        a_feature, a_vector = b_feature, np.mat(sy_matrix(self.Sxx).QRsolve(sy_matrix(self.Sxy))).astype(
            np.float64) * b_vector
        a_vector = (a_vector[:, a_feature.argsort()[::-1]])[:, :self.s]
        b_vector = (b_vector[:, a_feature.argsort()[::-1]])[:, :self.s]
        a_feature = np.sqrt((a_feature[a_feature.argsort()[::-1]])[:self.s])
        b_feature = a_feature
        self.lambdas = b_feature
        canvarx = np.mat(self.X) * a_vector
        canvary = np.mat(self.y) * b_vector
        sdx = np.std(canvarx, axis=0)
        sdy = np.std(canvary, axis=0)
        canvarx /= sdx
        canvary /= sdy
        a_vector /= sdx
        b_vector /= sdy
        xstructcorr = np.corrcoef(self.X, canvarx, False)[:self.p, self.p:]
        ystructcorr = np.corrcoef(self.y, canvary, False)[:self.q, self.q:]
        xcrosscorr = np.corrcoef(self.X, canvary, False)[:self.p, self.p:]
        ycrosscorr = np.corrcoef(self.y, canvarx, False)[:self.q, self.q:]

        xstructcorrsp = np.sum(xstructcorr ** 2, axis=1) / self.p
        ystructcorrsp = np.sum(ystructcorr ** 2, axis=1) / self.q
        xcrosscorrsp = np.sum(xcrosscorr ** 2, axis=1) / self.p
        ycrosscorrsp = np.sum(ycrosscorr ** 2, axis=1) / self.p
        return self.lambdas, a_vector, b_vector, xstructcorr, ystructcorr, xcrosscorr, ycrosscorr, xstructcorrsp, ystructcorrsp, xcrosscorrsp, ycrosscorrsp

    def fetch_a_b_svd(self):
        u, s, v = np.linalg.svd(self.M)
        A = matrixPower(self.Sxx, -0.5) * u
        B = matrixPower(self.Syy, -0.5) * v.T
        self.lambdas = s
        A = A[:, :self.s]
        B = B[:, :self.s]
        canvarx = np.mat(self.X) * A
        canvary = np.mat(self.y) * B
        sdx = np.std(canvarx, axis=0)
        sdy = np.std(canvary, axis=0)
        canvarx /= sdx
        canvary /= sdy
        xstructcorr = np.corrcoef(self.X, canvarx, False)[:self.p, self.p:]
        ystructcorr = np.corrcoef(self.y, canvary, False)[:self.q, self.q:self.q + self.s]
        xcrosscorr = np.corrcoef(self.X, canvary, False)[:self.p, self.p:self.p + self.s]
        ycrosscorr = np.corrcoef(self.y, canvarx, False)[:self.q, self.q:]
        xstructcorrsp = np.sum(xstructcorr ** 2, axis=1) / self.p
        ystructcorrsp = np.sum(ystructcorr ** 2, axis=1) / self.q
        xcrosscorrsp = np.sum(xcrosscorr ** 2, axis=1) / self.p
        ycrosscorrsp = np.sum(ycrosscorr ** 2, axis=1) / self.p
        return self.lambdas, A, B, xstructcorr, ystructcorr, xcrosscorr, ycrosscorr, xstructcorrsp, ystructcorrsp, xcrosscorrsp, ycrosscorrsp

    def wilks(self):
        w_contians = []
        df1 = []
        df2 = []
        f_contians = []
        p_contians = []
        for k in range(0, self.s):
            v = multi(self.lambdas, k)
            r = (self.n - self.s - 1) - ((abs(self.p - self.q) + 1) / 2)
            ndf = (self.p - k) * (self.q - k)
            u = (ndf - 2) / 4
            xx = ((self.p - k) ** 2 + (self.q - k) ** 2) - 5
            t = cmath.sqrt(((self.p - k) ** 2 * (self.q - k) ** 2 - 4) / xx if xx > 0 else 1)
            iv = v ** (1 / t)
            ddf = (r * t) - (2 * u)
            fstat = ((1 - iv) / iv) * (ddf / ndf)
            p = f.sf(abs(fstat), ndf, round(ddf.real))
            w_contians.append(v.real)
            df1.append(ndf.real)
            df2.append(ddf.real)
            f_contians.append(fstat.real)
            p_contians.append(p.real)
        return w_contians, df1, df2, f_contians, p_contians


def main(X: pd.DataFrame, y: pd.DataFrame):
    cca = CCAs(X, y)
    cca.fecth_n()
    lambdas, a, b, \
    xstructcorr, ystructcorr, xcrosscorr, \
    ycrosscorr, xstructcorrsp, ystructcorrsp, \
    xcrosscorrsp, ycrosscorrsp = cca.fetch_a_b_fv()

    # cca.fecth_m()
    # lambdas, a, b, \
    # xstructcorr, ystructcorr, xcrosscorr, \
    # ycrosscorr, xstructcorrsp, ystructcorrsp, \
    # xcrosscorrsp, ycrosscorrsp = cca.fetch_a_b_svd()

    s = len(lambdas)
    wilks, ndf, ddf, fstat, p = cca.wilks()
    result1 = pd.DataFrame(np.array([lambdas, wilks, ndf, ddf, fstat, p]).T,
                           columns=['相关性', 'Wilks 统计量', '模型自由的', '误差自由度', 'F', 'Pr > F'])

    result2 = pd.DataFrame(a[:, :s], columns=['典型变量X' + str(i) for i in range(s)])
    result3 = pd.DataFrame(b[:, :s], columns=['典型变量Y' + str(i) for i in range(s)])
    xstructcorr = pd.DataFrame(xstructcorr, columns=['典型变量X' + str(i) for i in range(s)])
    xcrosscorr = pd.DataFrame(xcrosscorr, columns=['交叉典型变量X' + str(i) for i in range(s)])
    ystructcorr = pd.DataFrame(ystructcorr, columns=['典型变量Y' + str(i) for i in range(s)])
    ycrosscorr = pd.DataFrame(ycrosscorr, columns=['交叉典型变量Y' + str(i) for i in range(s)])
    result4 = pd.DataFrame(pd.concat([xstructcorr, xcrosscorr], axis=1))
    result5 = pd.DataFrame(pd.concat([ystructcorr, ycrosscorr], axis=1))

    xstructcorrsp = pd.Series(xstructcorrsp)
    ystructcorrsp = pd.Series(ystructcorrsp)

    xcrosscorrsp = pd.Series(xcrosscorrsp)
    ycrosscorrsp = pd.Series(ycrosscorrsp)

    result6 = pd.concat([xstructcorrsp, ycrosscorrsp], axis=0, ignore_index=True)
    result7 = pd.concat([ystructcorrsp, xcrosscorrsp], axis=0, ignore_index=True)
    result8 = pd.concat([result6, result7], axis=1)
    result8.rename(columns={0: '变量X', 1: '变量Y'}, inplace=True)
    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
    print(result8)


def normalization(data: pd.DataFrame):
    return (data - data.mean())


if __name__ == '__main__':
    # data = pd.read_excel('../../data/CAA.xlsx')
    # X = data[['x1反复横向跳', 'x2纵跳', 'x3背力', 'x4握力', 'x5台阶试验', 'x6立定体前屈', 'x7俯卧上体后仰']]
    # Y = data[['y1 50米跑', 'y2跳远', 'y3投球', 'y4引体向上', 'y5耐力跑']]
    data = pd.read_excel('../../data/dianxing.xlsx')
    X = data[data.columns[:3]]
    Y = data[data.columns[3:]]
    X = normalization(X)
    Y = normalization(Y)
    main(X, Y)
