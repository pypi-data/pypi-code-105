from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from numpy import expm1, log1p

class RightUnskewedLinearRegression(LinearRegression):
    def predict(self, X):
        return expm1(super().predict(X))
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class RightUnskewedRidgeCV(RidgeCV):
    def predict(self, X):
        return expm1(super().predict(X))
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class RightUnskewedLassoCV(LassoCV):
    def predict(self, X):
        return expm1(super().predict(X))
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class LeftUnskewedLinearRegression(LinearRegression):
    def predict(self, X):
        prediction = super().predict(X)
        if all(prediction > 0):
            return prediction ** (1/2)
        else:
            return 0
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 2, sample_weight=sample_weight)

class LeftUnskewedRidgeCV(RidgeCV):
    def predict(self, X):
        prediction = super().predict(X)
        if all(prediction > 0):
            return prediction ** (1/2)
        else:
            return 0
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 2, sample_weight=sample_weight)

class LeftUnskewedLassoCV(LassoCV):
    def predict(self, X):
        prediction = super().predict(X)
        if all(prediction > 0):
            return prediction ** (1/2)
        else:
            return 0
    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 2, sample_weight=sample_weight)
