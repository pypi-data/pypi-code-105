# ---- NOTE --------------------------------------------------------------------
# This module contains internal implementation of MlModel enum-like class.
#
# There is some "magic" in here in order to disallow user from modifying
# already created model_types but at the same time allow for registering new
# types on the fly. Tread (somewhat) carefully and make sure you know what
# you're doing.
# ------------------------------------------------------------------------------

from ._utils import has_dependency

from collections import OrderedDict
from copy import deepcopy
import logging
import sys
from types import ModuleType
# import re

# external dependencies go here (i.e. those not in standard library)
if has_dependency("pyspark"):
    import pyspark
    import pyspark.ml
if has_dependency("hyperopt"):
    # import hyperopt
    # import hyperopt.hp
    from hyperopt import hp
    from hyperopt.pyll.base import scope
if has_dependency("sklearn"):
    import sklearn
    import sklearn.ensemble
if has_dependency("xgboost"):
    import xgboost
if has_dependency("sparkdl"):
    import sparkdl
    try:
        import sparkdl.xgboost
        _HAS_SPARKDL_XGBOOST = True
    except:  # noqa: E722
        _HAS_SPARKDL_XGBOOST = False
# end of external dependencies


# IDEA: MlModel.explain() --> print sectioned information, also render hyperopt as
# human-readable

# IDEA: method get_instance() so that people are less confused?

_ALLOWED_FRAMEWORKS = ["sklearn", "spark", "sparkdl", "xgboost"]
_ALLOWED_TASK_TYPES = ["classification", "regression"]

# lookups to be used with MlModel and associated functionality, procees with caution
_LOOKUP_ATTRS = OrderedDict()
_LOOKUP_NAMES = OrderedDict()
_LOOKUP_OBJ_TO_NAMES = OrderedDict()
_LOOKUP_FRAMEWORKS = OrderedDict()
_LOOKUP_CLASSES = OrderedDict()
_LOOKUP_TASK_TYPES = OrderedDict()
_LOOKUP_PARAM_GRID_VALS = OrderedDict()
_LOOKUP_HYPEROPT_SPACES = OrderedDict()
_LOOKUP_USER_DEFINED = OrderedDict()


def _is_dunder(name):
    return (
        len(name) > 4
        and name.startswith("__")
        and name.endswith("__")
    )


# IDEA: infer_model_type(...) ??
# def infer_model_type(model):
#     if type(model) in _LOOKUP_INFERE_MODEL_TYPE:
#         return _LOOKUP_INFERE_MODEL_TYPE[type(model)]
#     else:
#         logging.info(f"Could not infer model type from '{type(model)}'.")
#         return None

def register_model_type(
    name: str,
    attr_name: str,
    framework: str,
    model_class,
    task_type,
    param_grid_vals: dict,
    hyperopt_space: dict,
):
    """
    Register a new model type to MlModel.

    Some parameters, namely :param hyperopt_space and :param param_grid_vals
    are optional e.g. when hyperopt is not installed. Note however that when
    someone tries to access an attribute which was not defined, an error
    might occur.

    :param name: name of the model, usable as MlModel[<name>]
    :param attr_name: new model type will be accessible as MlModel.<attr_name>
    :param framework: model framework, currently "spark" and "sklearn" supported
    :param model_class: class of the model, will be used to make new instances
    :param task_type: machine learning task, currently "classification" and
        "regression" supproted
    :param param_grid_vals: dictionary of "param_name": <list of values>
    :param hyperopt_space: flat (non-nested) dictionary containing valid
        hyperopt parameter definitions as "param_name": <param def>
    """
    # NOTE: customer-facing interface
    _register_model_type(
        name, attr_name, framework, model_class, task_type, param_grid_vals,
        hyperopt_space, user_defined=True,
    )


def _register_model_type(
    name, attr_name, framework, model_class, task_type, param_grid_vals, hyperopt_space,
    user_defined=False,
):
    # NOTE: actual implementation wrapped with register_model_type

    # TODO: if we don't have hyperopt, we shouldn't use it,
    # if we do, the hyperopt_space should either be provided or there should be
    # checks in the code if it is set... (otherwise hard to track down bug in
    # the making)

    # TODO: something like re.match("[a-zA-Z]+(_[a-zA-Z]+)*", attr_name)  + docstring mention snake_case
    # TODO: name constraints?

    # IDEA: loop through model classes, if it's there, produce a warning
    # (...must be a combination, e.g. GLM binomial for both classification and regression)

    # user input sanitization
    if attr_name in _LOOKUP_ATTRS:
        raise ValueError(f"Attribute name '{attr_name}' already exists in MlModel")

    if name in _LOOKUP_NAMES:
        raise ValueError(f"Name '{name}' already exists in MlModel")

    if framework not in _ALLOWED_FRAMEWORKS:
        raise ValueError(
            f"Framework '{framework}' is not among allowed frameworks "
            + f"'{_ALLOWED_FRAMEWORKS}'"
        )

    # IDEA: check class (it's a class or at least callable, maybe framework-based checks?

    if task_type not in _ALLOWED_TASK_TYPES:
        raise ValueError(
            f"Type '{task_type}' is not among allowed types '{_ALLOWED_TASK_TYPES}'."
        )

    # IDEA: some additional checks for param-grid?
    if param_grid_vals and not isinstance(param_grid_vals, dict):
        raise ValueError(
            "Parameter 'param_grid_vals' must be of type 'dict'."
        )

    # IDEA: some additional checks for hyperopt space?
    if hyperopt_space and not isinstance(hyperopt_space, dict):
        raise ValueError(
            "Parameter 'hyperopt_space' must be of type 'dict'."
        )

    new_model = object.__new__(MlModel)
    new_model.__init__()  # if we decide to implement custom __init__

    _LOOKUP_ATTRS[attr_name] = new_model
    _LOOKUP_NAMES[name] = new_model
    _LOOKUP_OBJ_TO_NAMES[new_model] = deepcopy(name)
    _LOOKUP_FRAMEWORKS[new_model] = framework
    _LOOKUP_CLASSES[new_model] = deepcopy(model_class)
    _LOOKUP_TASK_TYPES[new_model] = deepcopy(task_type)
    _LOOKUP_PARAM_GRID_VALS[new_model] = deepcopy(param_grid_vals)
    _LOOKUP_HYPEROPT_SPACES[new_model] = deepcopy(hyperopt_space)
    _LOOKUP_USER_DEFINED[new_model] = user_defined


class MlModelMeta(type):
    # "constructors" and call behaviour ... not needed
    # def __new__(metacls, cls, bases, classdict, **kwargs)  # *args??
    # def __init__(...)
    # def __call__(cls, value, names=None, *, module=None, qualname=None, ...)

    # collection behaviour
    def __getitem__(cls, name):
        if name in _LOOKUP_NAMES:
            return _LOOKUP_NAMES[name]
        else:
            raise KeyError(name)

    def __contains__(cls, member):
        return member in _LOOKUP_ATTRS.values()

    def __len__(cls):
        return len(_LOOKUP_ATTRS)

    def __iter__(cls):
        return (model for model in _LOOKUP_ATTRS.values())

    def __reversed__(cls):
        return (model for model in reversed(_LOOKUP_ATTRS.values()))

    # attribute access
    def __setattr__(cls, attr, value):
        raise AttributeError(f"Class {cls.__name__} does not support direct changes.")

    def __delattr__(cls, attr):
        raise AttributeError(f"Class {cls.__name__} does not support direct changes.")

    def __dir__(cls):
        return [deepcopy(name) for name in _LOOKUP_NAMES]

    def __getattr__(cls, attr):
        if _is_dunder(attr):
            return super().__getattr__(attr)
        else:
            if attr in _LOOKUP_ATTRS:
                return _LOOKUP_ATTRS[attr]
            else:
                raise AttributeError(attr)

    def __getattribute__(cls, attr):
        if _is_dunder(attr):
            return super().__getattribute__(attr)
        else:
            if attr in _LOOKUP_ATTRS:
                return _LOOKUP_ATTRS[attr]
            else:
                raise AttributeError(attr)

    # miscellaneous
    def __bool__(cls):
        return True


class MlModel(metaclass=MlModelMeta):
    """
    Enum-like class providing abstraction for model types.

    Instances of this class (accessible as attributes MlModel.attr of by
    indexing MlModel[name]) represent abstraction of model types and provide
    some reusable functionality.

    This includes ability to list all available models, filtering among them,
    retrieving predefined hyperparameter space definitions, create instances
    etc. Some basic possibilities are shown below, instantiating using
    hyperparameters from defined hyperparam space is a bit more involved and
    is used in fit_classification_model for example.

    .. code-block:: python

       for model_type in MlModel:
           if model_type.framework != "spark":
               continue  # skip all non-spark models
           if model_type.task_type != "classification":
               continue  # only models for classification
           print(model_type)  # and print what's available

       model_type = MlModel.spark_logistic_regression  # select a model type
       classifier = model_type.model_class()  # instantiate with default hyperparameters
       print(model_type.default_param_grid_values)
       hypers = model_type.default_hyperopt_param_space  # get default hyperparam space
       hypers["foo"] = hyperopt.hp.choice("foo", ["bar", "baz"])  # ...and change it

    For registering new model types, see ``register_model_type``.
    """
    # "constructors"
    def __new__(cls):
        """Will raise exception, do not instantiate this class, see help(MlModel) for more
        information"""

        raise Exception(
            "Class MlModel cannot be instantiated directly, see help(MlModel)."
        )

    # attribute access
    def __setattr__(self, attr, value):
        raise AttributeError(f"Instances of {self.__class__.__name__} are read-only.")

    def __delattr__(self, attr):
        raise AttributeError("Instances of {self.__class__.__name__} are read-only.")

    # string stuff
    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self)}>"

    def __str__(self):
        return deepcopy(_LOOKUP_OBJ_TO_NAMES[self])

    def __format__(self, format_spec=None):
        # ignore format_spec for now
        return str(self)

    # comparison and miscellaneous
    def __bool__(self):
        return True

    # def __eq__(self, other):
    #     print("__eq__ called")
    #     return self is other

    @property
    def user_defined(self):
        return deepcopy(_LOOKUP_USER_DEFINED[self])

    @property
    def framework(self):
        return deepcopy(_LOOKUP_FRAMEWORKS[self])

    @property
    def model_class(self):
        return deepcopy(_LOOKUP_CLASSES[self])

    @property
    def task_type(self):
        return deepcopy(_LOOKUP_TASK_TYPES[self])

    @property
    def default_param_grid_values(self):
        return deepcopy(_LOOKUP_PARAM_GRID_VALS[self])

    @property
    def default_hyperopt_param_space(self):
        if (_LOOKUP_OBJ_TO_NAMES[self] == "spark_logistic_regression"
                or _LOOKUP_OBJ_TO_NAMES[self] == "spark_linear_regression"):
            # synchronize changes with "spark_logistic_regression" and "spark_linear_regression"
            # definitions
            logging.warning(
                "Spark linear/logistic regression has trivial default hyperopt param space. "
                + "Consider providing a more reasonable one as necessary or limiting "
                + "the number of training evaluations."
            )
        return deepcopy(_LOOKUP_HYPEROPT_SPACES[self])


# register all by-default available model types here
if has_dependency("pyspark"):
    _register_model_type(
        name="spark_logistic_regression",
        attr_name="spark_logistic_regression",
        framework="spark",
        model_class=pyspark.ml.classification.LogisticRegression,
        task_type="classification",
        param_grid_vals={"regParam": [0.0, 1.0], "elasticNetParam": [0.0, 0.5, 1.0]},
        hyperopt_space={  # synchronize changes with MlModel implementation
            "regParam": hp.choice("regParam", [0.0]),
            "elasticNetParam": hp.choice("elasticNetParam", [0.0]),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_GBT_classifier",
        attr_name="spark_GBT_classifier",
        framework="spark",
        model_class=pyspark.ml.classification.GBTClassifier,
        task_type="classification",
        param_grid_vals={
            "maxDepth": [5, 10, 20],
            "maxBins": [2, 4, 6],
            "maxIter": [10],
            "subsamplingRate": [1, 0.8],
        },
        hyperopt_space={
            "maxDepth": scope.int(hp.quniform("maxDepth", 2, 20, 1)),
            "maxBins": scope.int(hp.quniform("maxBins", 2, 40, 1)),
            "maxIter": scope.int(hp.quniform("maxIter", 3, 10, 1)),
            "subsamplingRate": hp.uniform("subsamplingRate", 0.5, 1),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_decision_tree_classifier",
        attr_name="spark_decision_tree_classifier",
        framework="spark",
        model_class=pyspark.ml.classification.DecisionTreeClassifier,
        task_type="classification",
        param_grid_vals={
            "impurity": ["entropy", "gini"],
            "maxBins": [2, 4, 6],
            "maxDepth": [2, 5, 10],  # TODO: check if these values make sense
        },
        hyperopt_space={
            "impurity": hp.choice("impurity", ["entropy", "gini"]),
            "maxBins": scope.int(hp.quniform("maxBins", 2, 50, 1)),
            "maxDepth": scope.int(hp.quniform("maxDepth", 2, 30, 1)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_random_forest_classifier",
        attr_name="spark_random_forest_classifier",
        framework="spark",
        model_class=pyspark.ml.classification.RandomForestClassifier,
        task_type="classification",
        param_grid_vals={"impurity": ["entropy", "gini"], "numTrees": [100]},
        hyperopt_space={
            "impurity": hp.choice("impurity", ["entropy", "gini"]),
            "numTrees": scope.int(hp.quniform("numTrees", 1, 100, 1)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_GLM_binomial",  # TODO: naming - "binomial"??
        attr_name="spark_GLM_binomial",
        framework="spark",
        model_class=pyspark.ml.regression.GeneralizedLinearRegression,
        task_type="classification",
        param_grid_vals={
            "regParam": [0.0, 1.0],
            "family": ["binomial"],
            "link": ["logit"],
        },
        hyperopt_space={
            "regParam": hp.uniform("regParam", 0.0, 1.0),
            "family": hp.choice("family", ["binomial"]),
            "link": hp.choice("link", ["logit"]),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_linear_regression",
        attr_name="spark_linear_regression",
        framework="spark",
        model_class=pyspark.ml.regression.LinearRegression,
        task_type="regression",
        param_grid_vals={
            "regParam": [0.0, 1.0],
            "elasticNetParam": [0.0, 0.5, 1.0]},
        hyperopt_space={  # synchronize changes with MlModel implementation
            "regParam": hp.choice("regParam", [0.0]),
            "elasticNetParam": hp.choice("elasticNetParam", [0.0]),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_decision_tree_regressor",
        attr_name="spark_decision_tree_regressor",
        framework="spark",
        model_class=pyspark.ml.regression.DecisionTreeRegressor,
        task_type="regression",
        param_grid_vals={
            "maxBins": [5, 10],
            "maxDepth": [2, 3, 5, 10],
        },
        hyperopt_space={
            "maxBins": scope.int(hp.quniform("maxBins", 2, 40, 1)),
            "maxDepth": scope.int(hp.quniform("maxDepth", 2, 10, 1)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_random_forest_regressor",
        attr_name="spark_random_forest_regressor",
        framework="spark",
        model_class=pyspark.ml.regression.RandomForestRegressor,
        task_type="regression",
        param_grid_vals={
            "bootstrap": [True, False],
            "maxBins": [5, 10],
            "maxDepth": [5, 10],
            "numTrees": [50, 100],
            "subsamplingRate": [0.75, 1]
        },
        hyperopt_space={
            "bootstrap": hp.choice("bootstrap", [True, False]),
            "maxBins": scope.int(hp.quniform("maxBins", 2, 32, 1)),
            "maxDepth": scope.int(hp.quniform("maxDepth", 2, 20, 1)),
            "numTrees": scope.int(hp.quniform("numTrees", 1, 100, 1)),
            "subsamplingRate": hp.uniform("subsamplingRate", 0.5, 1),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="spark_gbt_regressor",
        attr_name="spark_gbt_regressor",
        framework="spark",
        model_class=pyspark.ml.regression.GBTRegressor,
        task_type="regression",
        param_grid_vals={
            "maxIter": [10, 20, 30],
            "maxBins": [5, 10],
            "maxDepth": [5, 10],
            "subsamplingRate": [0.75, 1],
        },
        hyperopt_space={
            "maxIter": scope.int(hp.quniform("maxIter", 10, 50, 1)),
            "maxBins": scope.int(hp.quniform("maxBins", 8, 32, 1)),
            "maxDepth": scope.int(hp.quniform("maxDepth", 2, 20, 1)),
            "subsamplingRate": hp.uniform("subsamplingRate", 0.5, 1),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

if has_dependency("sparkdl") and _HAS_SPARKDL_XGBOOST:
    _register_model_type(
        name="sparkdl_xgboost_classifier",
        attr_name="sparkdl_xgboost_classifier",
        framework="sparkdl",
        model_class=sparkdl.xgboost.XgboostClassifier,
        task_type="classification",
        param_grid_vals={
            "n_estimators": [50, 100],
            "learning_rate": [0.01, 0.05],
            "max_depth": [3, 5, 10],
            "subsample": [0.75, 1],
            "colsample_bytree": [0.5, 0.75],
        },
        hyperopt_space={
            "n_estimators": scope.int(hp.quniform("n_estimators", 5, 50, 1)),
            "learning_rate": hp.uniform("learning_rate", 0, 0.1),
            "max_depth": scope.int(hp.quniform("max_depth", 1, 20, 1)),
            "subsample": hp.uniform("subsample", 0.5, 1),
            "colsample_bytree": hp.uniform("colsample_bytree", 0.5, 1),
            "reg_alpha": hp.uniform("reg_alpha", 0, 10),
            "reg_lambda": hp.uniform("reg_lambda", 0, 10),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sparkdl_xgboost_regressor",
        attr_name="sparkdl_xgboost_regressor",
        framework="sparkdl",
        model_class=sparkdl.xgboost.XgboostRegressor,
        task_type="regression",
        param_grid_vals={
            "n_estimators": [50, 100],
            "learning_rate": [0.01, 0.05],
            "max_depth": [3, 5, 10],
            "subsample": [0.75, 1],
            "colsample_bytree": [0.5, 0.75],
        },
        hyperopt_space={
            "n_estimators": scope.int(hp.quniform("n_estimators", 5, 50, 1)),
            "learning_rate": hp.uniform("learning_rate", 0, 0.1),
            "max_depth": scope.int(hp.quniform("max_depth", 1, 20, 1)),
            "subsample": hp.uniform("subsample", 0.5, 1),
            "colsample_bytree": hp.uniform("colsample_bytree", 0.5, 1),
            "reg_alpha": hp.uniform("reg_alpha", 0, 10),
            "reg_lambda": hp.uniform("reg_lambda", 0, 10),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

if has_dependency("sklearn"):
    _register_model_type(
        name="sklearn_random_forest_classifier",
        attr_name="sklearn_random_forest_classifier",
        framework="sklearn",
        model_class=sklearn.ensemble.RandomForestClassifier,
        task_type="classification",
        param_grid_vals={
            "max_depth": [2, 3, 5, 10, 15, 20, 25, 30, 40, 50],
            "n_estimators": [1, 5, 10, 20, 40, 60, 80, 100],
        },
        hyperopt_space={
            "max_depth": scope.int(hp.quniform("max_depth", 2, 50, 1)),
            "n_estimators": scope.int(hp.quniform("n_estimators", 1, 100, 1)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sklearn_random_forest_regressor",
        attr_name="sklearn_random_forest_regressor",
        framework="sklearn",
        model_class=sklearn.ensemble.RandomForestRegressor,
        task_type="regression",
        param_grid_vals={
            "max_depth": [2, 3, 5, 10, 15, 20, 25, 30, 40, 50],
            "n_estimators": [1, 5, 10, 20, 40, 60, 80, 100],
        },
        hyperopt_space={
            "max_depth": scope.int(hp.quniform("max_depth", 2, 50, 1)),
            "n_estimators": scope.int(hp.quniform("n_estimators", 1, 100, 1)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sklearn_gradient_boosting_classifier",
        attr_name="sklearn_gradient_boosting_classifier",
        framework="sklearn",
        model_class=sklearn.ensemble.GradientBoostingClassifier,
        task_type="classification",
        param_grid_vals={
            "max_depth": [2, 3, 5, 10],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "n_estimators": [100, 200, 300],
        },
        hyperopt_space={
            "max_depth": scope.int(hp.quniform("max_depth", 1, 10, 1)),
            "learning_rate": scope.int(hp.uniform("learning_rate", 0.001, 0.3)),
            "n_estimators": scope.int(hp.quniform("n_estimators", 100, 300, 50)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sklearn_linear_regression",
        attr_name="sklearn_linear_regression",
        framework="sklearn",
        model_class=sklearn.linear_model.LinearRegression,
        task_type="regression",
        param_grid_vals={
            "normalize": [False, True],
        },
        hyperopt_space={
            "normalize": hp.choice("normalize", [False, True]),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sklearn_logistic_regression",
        attr_name="sklearn_logistic_regression",
        framework="sklearn",
        model_class=sklearn.linear_model.LogisticRegression,
        task_type="classification",
        param_grid_vals={
            "class_weight": [None, "balanced"],
        },
        hyperopt_space={
            "class_weight": hp.choice("class_weight", [None, "balanced"]),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="sklearn_gradient_boosting_regressor",
        attr_name="sklearn_gradient_boosting_regressor",
        framework="sklearn",
        model_class=sklearn.ensemble.GradientBoostingRegressor,
        task_type="regression",
        param_grid_vals={
            "max_depth": [2, 3, 5, 10],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "n_estimators": [100, 200, 300],
        },
        hyperopt_space={
            "max_depth": scope.int(hp.quniform("max_depth", 1, 10, 1)),
            "learning_rate": scope.int(hp.uniform("learning_rate", 0.001, 0.3)),
            "n_estimators": scope.int(hp.quniform("n_estimators", 100, 300, 50)),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

if has_dependency("xgboost"):
    _register_model_type(
        name="xgboost_xgbclassifier",
        attr_name="xgboost_xgbclassifier",
        framework="xgboost",
        model_class=xgboost.XGBClassifier,
        task_type="classification",
        param_grid_vals={
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "max_depth": [3, 5, 10],
            "subsample": [0.75, 1.0],
            "colsample_bytree": [0.5, 0.75, 1.0],
        },
        hyperopt_space={
            "n_estimators": scope.int(hp.quniform("n_estimators", 100, 300, 50)),
            "learning_rate": hp.uniform("learning_rate", 0.001, 0.3),
            "max_depth": scope.int(hp.quniform("max_depth", 1, 10, 1)),
            "subsample": hp.uniform("subsample", 0.75, 1),
            "colsample_bytree": hp.uniform("colsample_bytree", 0.75, 1),
            "reg_alpha": hp.uniform("reg_alpha", 0, 10),
            "reg_lambda": hp.uniform("reg_lambda", 0, 10),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )

    _register_model_type(
        name="xgboost_xbgregressor",
        attr_name="xgboost_xbgregressor",
        framework="xgboost",
        model_class=xgboost.XGBRegressor,
        task_type="regression",
        param_grid_vals={
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.05],
            "max_depth": [3, 5, 10],
            "subsample": [0.75, 1.0],
            "colsample_bytree": [0.5, 0.75, 1.0],
        },
        hyperopt_space={
            "n_estimators": scope.int(hp.quniform("n_estimators", 100, 300, 50)),
            "learning_rate": hp.uniform("learning_rate", 0.001, 0.3),
            "max_depth": scope.int(hp.quniform("max_depth", 1, 10, 1)),
            "subsample": hp.uniform("subsample", 0.75, 1),
            "colsample_bytree": hp.uniform("colsample_bytree", 0.75, 1),
            "reg_alpha": hp.uniform("reg_alpha", 0, 10),
            "reg_lambda": hp.uniform("reg_lambda", 0, 10),
        } if has_dependency("hyperopt") else None,
        user_defined=False,
    )
# end of default models registration


# restrict attribute access to this module
def _is_public(attr):
    # anything apart from dunders and whitelisted identifiers is not public
    if len(attr) > 4 and attr.startswith("__") and attr.endswith("__"):
        # dunder
        return True
    elif attr in set(["MlModel", "register_model_type"]):
        return True
    else:
        return False


class ModuleAccessHandler(ModuleType):
    def __getattribute__(self, attr):
        if _is_public(attr):
            return super().__getattribute__(attr)
        else:
            raise AttributeError(attr)

    def __getattr__(self, attr):
        if _is_public(attr):
            return super().__getattr__(attr)
        else:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        raise AttributeError("readonly attribute")

    def __delattr__(self, attr):
        raise AttributeError("readonly attribute")

    def __dir__(self):
        return [attr for attr in super().__dir__() if _is_public(attr)]


sys.modules[__name__].__class__ = ModuleAccessHandler
