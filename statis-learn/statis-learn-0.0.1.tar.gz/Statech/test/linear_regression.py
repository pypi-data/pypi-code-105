from Statech.linear_model import LinearRegression
import pandas as pd
import numpy as np


def main(X: pd.DataFrame, y: pd.Series):
    reg = LinearRegression()
    x_constant = reg.add_constant(X)
    reg.fit(x_constant, y)
    score = reg.score(X, y)
    vif = VIF(X)
    print(pd.concat([score[0], vif], axis=1))
    print(score[1])


def VIF(X: pd.DataFrame):
    from Statech.metrics import r_square
    k = X.shape[1]
    assert k > 1, '特征数 > 1'
    col_list = np.arange(k)
    vif = [0]
    reg = LinearRegression()
    for i in range(k):
        y = X.iloc[:, i]
        x_list = np.delete(col_list, i)
        x_vif = X.iloc[:, x_list]
        x_constant = reg.add_constant(x_vif)
        reg.fit(x_constant, y)
        y_hat = reg.predict(x_vif)
        vif.append(1 / (1 - r_square(y.values, y_hat)))
    return pd.Series(vif, name='VIF')


if __name__ == '__main__':
    data = pd.read_excel('../data/dianxing.xlsx')
    X = data.iloc[:, 4:8]
    y = data.iloc[:, 1]
    main(X, y)
