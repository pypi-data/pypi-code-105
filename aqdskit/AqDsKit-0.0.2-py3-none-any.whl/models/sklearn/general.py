from sklearn import clone


def clone_set_hyperparam(clf, param_name: str = None, param_value = None):
    """Clone clf, set given hyperparameter and return the model.

    """
    clf = clone(clf)
    if hasattr(clf, param_name):
        setattr(clf, param_name, param_value)
    else:
        raise TypeError(f"estimator {clf} has no attribute {param_name}")

    return clf