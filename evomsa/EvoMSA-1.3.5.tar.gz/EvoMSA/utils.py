# Copyright 2017 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Union, Dict, Tuple, Callable
from sklearn.model_selection import BaseCrossValidator
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import recall_score
import os
import hashlib
from urllib import request
from microtc.utils import load_model
import numpy as np


class LabelEncoderWrapper(object):
    """Wrapper of LabelEncoder. The idea is to keep the order when the classes are numbers
    at some point this will help improve the performance in ordinary classification problems

    :param classifier: Specifies whether it is a classification problem
    :type classifier: bool
    """

    def __init__(self, classifier=True):
        self._m = {}
        self._classifier = classifier

    @property
    def classifier(self):
        """Whether EvoMSA is acting as classifier"""

        return self._classifier

    def fit(self, y):
        """Fit the label encoder

        :param y: Independent variables
        :type y: list or np.array
        :rtype: self
        """

        if not self.classifier:
            return self
        try:
            n = [int(x) for x in y]
        except ValueError:
            return LabelEncoder().fit(y)
        self.classes_ = np.unique(n)
        self._m = {v: k for k, v in enumerate(self.classes_)}
        self._inv = {v: k for k, v in self._m.items()}
        return self

    def transform(self, y):
        if not self.classifier:
            return np.array([float(_) for _ in y])
        return np.array([self._m[int(x)] for x in y])

    def inverse_transform(self, y):
        if not self.classifier:
            return y
        return np.array([self._inv[int(x)] for x in y])


class Cache(object):
    """Store the output of the text models"""

    def __init__(self, basename):
        if basename is None:
            self._cache = None
        else:
            dirname = os.path.dirname(basename)
            if len(dirname) and not os.path.isdir(dirname):
                os.mkdir(dirname)
            self._cache = basename

    def __iter__(self):
        if self._cache is None:
            while True:
                yield None
        for i in self.textModels:
            yield i

    @property
    def textModels(self):
        try:
            return self._textModels
        except AttributeError:
            self._textModels = list()
        return self._textModels

    @property
    def ml(self):
        try:
            return self._classifiers
        except AttributeError:
            self._classifiers = list()
        return self._classifiers

    def ml_train(self):
        if self._cache is None or len(self.ml) == 0:
            while True:
                yield None
        for i in self.ml:
            yield i

    def ml_kfold(self):
        if self._cache is None or len(self.ml) == 0:
            while True:
                yield None
        for i in self.ml:
            yield i + '-K'

    @staticmethod
    def get_name(value):
        if isinstance(value, str):
            return hashlib.md5(value.encode()).hexdigest()
        else:
            try:
                vv = value.__name__
            except AttributeError:
                vv = value.__class__.__name__
            return vv

    def append(self, value, ml=None):
        if self._cache is None:
            return
        name = self._cache + "-%s" % self.get_name(value)
        if ml is not None:
            self.ml.append(name + '-' + self.get_name(ml))
        self.textModels.append(name)


def download(model_fname, force=False):
    if os.path.isfile(model_fname) and not force:
        return model_fname
    dirname = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fname = os.path.join(dirname, model_fname)
    if not os.path.isfile(fname) or force:
        request.urlretrieve("https://github.com/INGEOTEC/EvoMSA/raw/master/EvoMSA/models/%s" % model_fname,
                            fname)
    return fname


def get_model(model_fname):
    fname = download(model_fname)
    return load_model(fname)


def linearSVC_array(classifiers):
    """Transform LinearSVC into weight stored in array.array

    :param classifers: List of LinearSVC where each element is binary
    :type classifers: list
    """

    import array
    intercept = array.array('d', [x.intercept_[0] for x in classifiers])
    coef = np.vstack([x.coef_[0] for x in classifiers])
    coef = array.array('d', coef.T.flatten())
    return coef, intercept


def compute_p(syss):
    from scipy.stats import wilcoxon
    p = []
    mu = syss.mean(axis=0)
    best = mu.argmax()
    for i in range(syss.shape[1]):
        if i == best:
            p.append(np.inf)
            continue
        try:
            pv = wilcoxon(syss[:, best], syss[:, i])[1]
            p.append(pv)
        except ValueError:
            p.append(np.inf)
    ps = np.argsort(p)
    alpha = [np.inf for _ in ps]
    m = ps.shape[0] - 1
    for r, i in enumerate(ps[:-1]):
        alpha_c = (0.05 / (m + 1 - (r + 1)))
        if p[i] > alpha_c:
            break
        alpha[i] = alpha_c
    return p, alpha


def bootstrap_confidence_interval(y: np.ndarray,
                                  hy: np.ndarray,
                                  metric: Callable[[float, float], float]=lambda y, hy: recall_score(y, hy,
                                                                                           average="macro"),
                                  alpha: float=0.05,
                                  nbootstrap: int=500) -> Tuple[float, float]:
    """Confidence interval from predictions"""
    B = []
    for _ in range(nbootstrap):
        s = np.random.randint(hy.shape[0], size=hy.shape[0])
        _ = metric(y[s], hy[s])
        B.append(_)
    return (np.percentile(B, alpha * 100), np.percentile(B, (1 - alpha) * 100))



class ConfidenceInterval(object):
    """Estimate the confidence interval

    >>> from EvoMSA import base
    >>> from EvoMSA.utils import ConfidenceInterval
    >>> from microtc.utils import tweet_iterator
    >>> import os
    >>> tweets = os.path.join(os.path.dirname(base.__file__), 'tests', 'tweets.json')
    >>> D = list(tweet_iterator(tweets))
    >>> X = [x['text'] for x in D]
    >>> y = [x['klass'] for x in D]
    >>> kw = dict(stacked_method="sklearn.naive_bayes.GaussianNB") 
    >>> ci = ConfidenceInterval(X, y, evomsa_kwargs=kw)
    >>> result = ci.estimate()

    """

    def __init__(self, X: List[str], y: Union[np.ndarray, list],
                 Xtest: List[str]=None, y_test: Union[np.ndarray, list]=None,
                 evomsa_kwargs: Dict=dict(), 
                 folds: Union[None, BaseCrossValidator]=None, ) -> None:
        self._X = X
        self._y = np.atleast_1d(y)
        self._Xtest = Xtest
        self._y_test = y_test
        self._evomsa_kwargs = evomsa_kwargs
        self._folds = folds

    @property
    def gold(self):
        if self._y_test is not None:
            return self._y_test
        return self._y
    
    @property
    def hy(self):
        from .base import EvoMSA
        try:
            return self._hy
        except AttributeError:
            if self._Xtest is not None:
                m = EvoMSA(**self._evomsa_kwargs)
                m.fit(self._X, self._y)
                hy = m.predict(self._Xtest)
                self._hy = hy
                return hy
            folds = self._folds
            if folds is None:
                folds = StratifiedKFold(n_splits=5,
                                        shuffle=True, random_state=0)
            hy = np.empty_like(self._y)
            X, y = self._X, self._y
            for tr, ts in folds.split(X, y):
                m = EvoMSA(**self._evomsa_kwargs)
                m.fit([X[x] for x in tr], y[tr])
                hy[ts] = m.predict([X[x] for x in ts])
            self._hy = hy
            return self._hy

    def estimate(self, alpha: float=0.05,
                       metric: Callable[[float, float], float]=lambda y, hy: recall_score(y, hy,
                                                                                          average="macro"),
                       nbootstrap: int=500)->Tuple[float, float]:
        return bootstrap_confidence_interval(self.gold, self.hy,
                                             metric=metric,
                                             alpha=alpha,
                                             nbootstrap=nbootstrap)