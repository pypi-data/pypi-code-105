import time

from sklearn.model_selection import cross_val_score

from AqDsKit.models.sklearn.general import clone_set_hyperparam
from AqDsKit.utils.parallel import delayer, parallel_run


@ delayer
def _set_hyperparam_train(clf, X, y = None, param_name: str = None, param_value = None):
    """Clone clf, set given hyperparameter and train the model.

    :param clf: Clusterer instance that implements ``fit`` method, and an ``n_clusters`` or ``n_components`` hyperparameter.
                    e.g. :class:`sklearn.cluster.KMeans` instance, GaussianMixture instance
    :param X: (array-like, shape (n_samples, n_features)):
                    Data to cluster, where n_samples is the number of samples and
                    n_features is the number of features.
    :param y: y to be fed into the training
    :param param_name: name of the hyperparameter, must be an attribute of clf
    :param param_value: value of the hyperparameter to be set
    :return: fitted clf and time of training
    """

    start = time.time()
    clf = clone_set_hyperparam(clf, param_name, param_value)
    return clf.fit(X, y), time.time() - start

def train_different_hyperparam(clf, X, y = None, param_name: str = None, param_ranges: list = None, n_jobs: int = -1):
    # use parallel run to boost speed, tuples = [(clf1, time1), (clf2, time2), ... (clfn, timen)] where n = len(param_ranges)

    # equivalent to:
    # tuples = Parallel(n_jobs = n_jobs)(delayed(_set_hyperparam_train)(clf, X, y, param_name, param) for param in param_ranges)
    jobs = (_set_hyperparam_train(clf, X, y, param_name, param) for param in param_ranges)
    tuples = parallel_run(jobs, n_jobs = n_jobs)

    clfs, times = zip(*tuples)
    return clfs, times



@ delayer
def _set_hyperparm_cv_score(clf, X, y = None, param_name: str = None, param_value = None, scoring_func = None, cv = 5, n_jobs = -1):
    start = time.time()
    clf = clone_set_hyperparam(clf, param_name, param_value)
    cv_score = cross_val_score(clf, X, y, scoring = scoring_func, cv = cv, n_jobs = n_jobs).mean(),
    return  cv_score, time.time() - start

def cv_score_different_hyperparam(clf, X, y, param_name: str = None, param_ranges: list = None, scoring_func = None, cv: int = 5, n_jobs: int = -1):
    # use parallel run to boost speed, tuples = [(score1, time1), (score2, time2), ... (scoren, timen)] where n = len(param_ranges)

    # equivalent to:
    # tuples = Parallel(n_jobs = n_jobs)(delayed(_set_hyperparm_cv_score)(clf, X, y, param_name, param, scoring_func, cv, n_jobs) for param in param_ranges)
    jobs = (_set_hyperparm_cv_score(clf, X, y, param_name, param, scoring_func, cv, n_jobs) for param in param_ranges)
    tuples = parallel_run(jobs, n_jobs = n_jobs)

    scores, times = zip(*tuples)
    return scores, times