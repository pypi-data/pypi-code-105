import numpy as np
from sklearn.base import ClassifierMixin, BaseEstimator
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.validation import check_is_fitted, _check_sample_weight, _deprecate_positional_args


class PredictableDBSCAN(DBSCAN):
    """DBSCAN in sklearn does not have predict() method, so this version implements predict method
    """

    @_deprecate_positional_args
    def __init__(
            self,
            eps = 0.5,
            *,
            min_samples = 5,
            metric = 'euclidean',
            metric_params = None,
            algorithm = 'auto',
            leaf_size = 30,
            p = None,
            n_jobs = None,
            clf: BaseEstimator = KNeighborsClassifier(),
        ):
        """
        parameters can be checked here:
        https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN

        :param clf: sklearn implementation of classifier instance, by default it use KNN
        :param eps:
        :param min_samples:
        :param metric:
        :param metric_params:
        :param algorithm:
        :param leaf_size:
        :param p:
        :param n_jobs:
        """
        super().__init__(eps = eps, min_samples=min_samples, metric=metric,
                 metric_params=metric_params, algorithm=algorithm, leaf_size=leaf_size, p=p,
                 n_jobs=n_jobs)
        self.clf = clf

    def fit(self, X, y = None, sample_weight = None):
        """Will train the custom classifier on the output of DBSCAN

        :param X:
        :param y: not used
        :param sample_weight:
        :return:
        """
        super().fit(X, y, sample_weight = sample_weight)
        self.clf.fit(self.components_, self.labels_[self.core_sample_indices_])
        return self


    def predict(self, X, sample_weight=None):
        """Predict the closest cluster each sample in X belongs to.

        A custom classifier is trained on the components_ (X) and predictions of the DBSCAN labels_ (y)
        And this trained classifier is used to predict the labels

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            New data to predict.

        sample_weight : array-like of shape (n_samples,), default=None
            The weights for each observation in X. If None, all observations
            are assigned equal weight.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        check_is_fitted(self)

        X = self._validate_data(X, accept_sparse='csr', reset=False,
                                dtype=[np.float64, np.float32],
                                order='C', accept_large_sparse=False)

        sample_weight = _check_sample_weight(sample_weight, X, dtype = X.dtype)
        return self.clf.predict(X)