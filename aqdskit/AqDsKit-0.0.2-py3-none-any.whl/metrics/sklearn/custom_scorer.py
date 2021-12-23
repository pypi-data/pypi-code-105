#######
# To be compatible with sklearn
# https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
# scorer is a callable object takes estimator, X, y_true and returns a score
# scorer can be used in Gridsearch to automatically find optimal hyperparamters
# scorer can also be used standalone, scorer(model, X_test, y_test) to get a score
#######
from sklearn.metrics import make_scorer

#################### scorer for supervised learning ######################
from AqDsKit.metrics.sklearn.custom_scoring import max_diff

max_diff_scorer = make_scorer(max_diff, greater_is_better = False, needs_proba = False, needs_threshold = False)


#################### scorer for clustering ######################

from sklearn.metrics import silhouette_score

def silhouette_scorer(estimator, X, y_true = None) -> float:
    """can be used to help select best number of clusters while tuning hyperparams for clustering problems
    suitable for K-means, DBSCAN(with predict method implemented), etc.

    :param estimator: must have ``predict`` method which returns predicting class
    :param X:
    :param y_true: Not used
    :return: silhouette score of a given estimation
    """
    if not callable(getattr(estimator, "predict", None)):
        raise TypeError(f"This estimator: {estimator} does not have ``predict`` method, does not support silhouette scoring")
    labels = estimator.predict(X)
    score = silhouette_score(X, labels)
    return score


def aic_scorer(estimator, X, y_true = None) -> float:
    """AIC score for Gaussian Mixture Model Metric
    can be used in GridSearch for hyperparameter tuning

    :param estimator: must have ``aic`` method which returns aic score
    :param X:
    :param y_true:
    :return: the protocol requires greater the better, so it will return negative aic score
    """
    if not callable(getattr(estimator, "aic", None)):
        raise TypeError(f"This estimator: {estimator} does not have ``aic`` method, does not support aic metric")

    aic = estimator.aic(X)
    return -aic


def bic_scorer(estimator, X, y_true = None) -> float:
    """BIC score for Gaussian Mixture Model Metric
    can be used in GridSearch for hyperparameter tuning

    :param estimator: must have ``bic`` method which returns bic score
    :param X:
    :param y_true:
    :return: the protocol requires greater the better, so it will return negative bic score
    """
    if not callable(getattr(estimator, "bic", None)):
        raise TypeError(f"This estimator: {estimator} does not have ``aic`` method, does not support aic metric")

    bic = estimator.bic(X)
    return -bic