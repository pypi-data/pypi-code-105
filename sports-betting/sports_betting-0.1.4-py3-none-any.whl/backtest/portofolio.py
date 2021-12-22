"""
Create a portofolio and backtest its performance 
using sports betting data.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# License: MIT

from vectorbt import Portfolio
import numpy as np
from sklearn.base import clone
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV


class Bettor:
    def __init__(self, classifier):
        self.classifier = classifier

    def backtest(self, X, Y, O, tscv=None):
        self.classifier_ = clone(self.classifier)
        self.tscv_ = TimeSeriesSplit() if tscv is None else tscv
        for train_ind, test_ind in self.tscv_.split(X):
            gscv = GridSearchCV(
                self.classifier_, {}, cv=TimeSeriesSplit(n_splits=3)
            ).fit(X.take(train_ind), Y.loc[train_ind])
            Y_pred_prob = np.concatenate(
                [
                    prob[:, 1].reshape(-1, 1)
                    for prob in gscv.predict_proba(X.iloc[test_ind])
                ],
                axis=1,
            )
            value_bets = Y_pred_prob * O.iloc[test_ind] > 1

            prices = Y.iloc[test_ind] * O.iloc[test_ind].values + 1
            prices[~value_bets.values] = 2.0
            prices = prices.applymap(lambda price: (2.0, price))
            prices = (
                np.array(prices.values.T.reshape(-1).tolist())
                .reshape(prices.shape[1], -1)
                .T
            )

            orders = value_bets.applymap(lambda value_bet: (+value_bet, -value_bet))
            orders = (
                np.array(orders.values.T.reshape(-1).tolist())
                .reshape(orders.shape[1], -1)
                .T
            )

            portfolio = Portfolio.from_orders(prices, orders)

        return self

    def bet(self, X, O):
        pass
