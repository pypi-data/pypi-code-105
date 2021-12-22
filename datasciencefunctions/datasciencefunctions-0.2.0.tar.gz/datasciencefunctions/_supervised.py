from . import __version__
from . import MlModel
from ._utils import copy_docstring_from
from .utils import _ERR_INVALID_DF_TYPE
from .utils import experimental
from .utils import has_dependency
from .utils import requires
from .data_exploration import get_categorical_and_numeric_cols
from .data_processing import apply_transformation_pipeline
from .data_processing import fit_transformation_pipeline
from .data_processing import train_test_split

from copy import deepcopy
import json
import logging
import os
import re
import tempfile
import traceback


# external dependencies go here (i.e. those not in standard library)
if has_dependency("mlflow"):
    import mlflow

if has_dependency("sklearn"):
    import sklearn

if has_dependency("pandas"):
    import pandas as pd

if has_dependency("pyspark"):
    import pyspark

    if pyspark.__version__.startswith("2"):
        _SPARK_VERSION = 2
        logging.warning("Spark version 2 is not officially supported, some things might break.")
    elif pyspark.__version__.startswith("3"):
        _SPARK_VERSION = 3
    else:
        logging.warning(
            "Spark version different from 2 and 3 detected. Unexpected errors might occur."
        )

    import pyspark.ml
    # import pyspark.ml.param.shared
    import pyspark.ml.evaluation
    import pyspark.sql.functions as F

if has_dependency("sparkdl"):
    import sparkdl
    try:
        import sparkdl.xgboost
        _HAS_SPARKDL_XGBOOST = True
    except:   # noqa: E722
        _HAS_SPARKDL_XGBOOST = False
# end of external dependencies


def _get_metric_by_name(metric_name, framework, get_metric=False, fail_when_not_found=False):
    """
    Returns an pySpark evaluator / sklearn scorer based on the given metric name.
    When get_metric == True and framework == "sklearn", returns the metric instead
    (in sklearn scorers are used for training and metrics for evaluation on a scored dataset)
    """

    # NOTE: make sure metric names are in sync!!!
    # metrics will most likely be logged to MLflow and nobody's gonna
    # want to change them retrospectively etc.
    # TODO: Evaluators should be defined elsewhere...something like MlModel class for metrics?

    if framework == "spark":
        if not has_dependency("pyspark"):
            raise ImportError("Framework 'spark' specified but 'pyspark' not installed.")

        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml.evaluation import MulticlassClassificationEvaluator
        from pyspark.ml.evaluation import RegressionEvaluator

        _EVALUATORS = {
            "accuracy": MulticlassClassificationEvaluator(metricName="accuracy"),
            "auprc": BinaryClassificationEvaluator(metricName="areaUnderPR"),
            "auroc": BinaryClassificationEvaluator(metricName="areaUnderROC"),
            "f1": MulticlassClassificationEvaluator(metricName="f1"),
            "lift_10": LiftEvaluatorSpark(binCount=10),
            "lift_100": LiftEvaluatorSpark(binCount=100),
            "mae": RegressionEvaluator(metricName="mae"),
            "mse": RegressionEvaluator(metricName="mse"),
            "r2": RegressionEvaluator(metricName="r2"),
            "rmse": RegressionEvaluator(metricName="rmse"),
            "weighted_precision": MulticlassClassificationEvaluator(metricName="weightedPrecision"),
            "weighted_recall": MulticlassClassificationEvaluator(metricName="weightedRecall"),
        }

        evaluator = _EVALUATORS.get(metric_name, None)

        if fail_when_not_found and evaluator is None:
            raise RuntimeError(f"Metric '{metric_name}' not defined.")

    elif framework == "sklearn":
        if not has_dependency("sklearn"):
            raise ImportError("Framework 'sklearn' specified but 'sklearn' not installed.")

        import sklearn.metrics as skmetrics
        from functools import partial

        def _calc_lift(y_true, y_pred, n_bins):
            df = pd.DataFrame()
            df["label"] = y_true
            df["probability"] = y_pred
            df_lift = lift_curve_pandas(
                df,
                bin_count=n_bins,
                label_col="label",
                probability_col="probability",
            )
            return float(df_lift[df_lift["bucket"] == 1].iloc[0]["cum_lift"])

        _EVALUATORS = {
            "accuracy": {
                "score_func": skmetrics.accuracy_score,
                "metric_params": {},
                "scorer_params": {},
            },
            "auroc": {
                "score_func": skmetrics.roc_auc_score,
                "metric_params": {},
                "scorer_params": {"needs_threshold": True},
            },
            "auprc": {
                "score_func": skmetrics.average_precision_score,
                "metric_params": {"average": None},
                "scorer_params": {},
            },
            "balanced_accuracy": {
                "score_func": skmetrics.balanced_accuracy_score,
                "metric_params": {},
                "scorer_params": {},
            },
            "f1": {
                "score_func": skmetrics.f1_score,
                "metric_params": {},
                "scorer_params": {},
            },
            "lift_10": {
                "score_func": _calc_lift,
                "metric_params": {"n_bins": 10},
                "scorer_params": {"needs_proba": True},
            },
            "lift_100": {
                "score_func": _calc_lift,
                "metric_params": {"n_bins": 100},
                "scorer_params": {"needs_proba": True},
            },
            "mae": {
                "score_func": skmetrics.mean_absolute_error,
                "metric_params": {},
                "scorer_params": {"greater_is_better": False},
            },
            "mse": {
                "score_func": skmetrics.mean_squared_error,
                "metric_params": {},
                "scorer_params": {"greater_is_better": False},
            },
            "rmse": {
                "score_func": skmetrics.mean_squared_error,
                "metric_params": {"squared": False},
                "scorer_params": {"greater_is_better": False},
            },
            "r2": {
                "score_func": skmetrics.r2_score,
                "metric_params": {},
                "scorer_params": {},
            },
            "weighted_precision": {
                "score_func": skmetrics.precision_score,
                "metric_params": {"average": 'weighted'},
                "scorer_params": {},
            },
            "weighted_recall": {
                "score_func": skmetrics.recall_score,
                "metric_params": {"average": 'weighted'},
                "scorer_params": {},
            },
        }

        metric = _EVALUATORS.get(metric_name, None)

        if fail_when_not_found and metric is None:
            raise RuntimeError(f"Metric '{metric_name}' not defined.")

        evaluator = None

        if metric and get_metric:
            evaluator = partial(metric["score_func"], **metric["metric_params"])

        elif metric:
            evaluator = skmetrics.make_scorer(metric["score_func"],
                                              **metric["metric_params"],
                                              **metric["scorer_params"],
                                              )

    else:
        raise ValueError("Wrong framework, expected one of 'spark', 'sklearn'.")

    return evaluator


# TODO: add tests!!! (loop over several models and available metrics)
@requires("pyspark")
def _set_spark_model_evaluator_col(model, evaluator):
    from pyspark.ml.param.shared import HasPredictionCol
    from pyspark.ml.param.shared import HasRawPredictionCol
    from pyspark.ml.evaluation import BinaryClassificationEvaluator
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator
    from pyspark.ml.evaluation import RegressionEvaluator

    warn_incompatible = False

    if isinstance(evaluator, (BinaryClassificationEvaluator, LiftEvaluatorSpark)):
        # binary - rawPredictionCol, continuous probability
        if isinstance(model, HasRawPredictionCol):
            evaluator.setParams(rawPredictionCol=model.getRawPredictionCol())
        elif isinstance(model, HasPredictionCol):
            evaluator.setParams(rawPredictionCol=model.getPredictionCol())
        else:
            warn_incompatible = True
    elif isinstance(evaluator, RegressionEvaluator):
        # regression - Prediction, continuous value
        if isinstance(model, HasRawPredictionCol):
            # in future we might use probabilityCol if it exists
            evaluator.setParams(predictionCol=None)
            warn_incompatible = True  # intentionally, it will fail anyways
        elif isinstance(model, HasPredictionCol):
            evaluator.setParams(predictionCol=model.getPredictionCol())
        else:
            warn_incompatible = True
    elif isinstance(evaluator, MulticlassClassificationEvaluator):
        # multiclass - Prediction, discrete label
        if isinstance(model, HasPredictionCol):
            evaluator.setParams(predictionCol=model.getPredictionCol())
            # if model is not instance of HasRawPredictionCol,
            # prediction is continuous, needs to be handled somewhere else
        else:
            warn_incompatible = True
    else:
        warn_incompatible = True

    if warn_incompatible:
        logging.warning(f"The specified model {type(model).__name__} and evaluator \
{evaluator.getMetricName()} do not appear compatible due to expected output columns mismatch.")


@requires("hyperopt", strict=False)  # noqa C901 TODO: simplify this?
def fit_supervised_model(model_type: MlModel,  # noqa C901 TODO: simplify this?
                         train_data_transformed,
                         param_space_search: str = "hyperopt",
                         validation_technique: str = "cross_val",
                         metric_name: str = None,
                         max_evals: int = 30,
                         custom_params: dict = None,
                         ):
    """
    Train ML model on given training data using specified hyperparameter
    optimization technique.

    Creates parameter space (based on default values if :param custom_params is
    not set) depending on the type of MlModel provided. The parameter space is
    then searched based on the chosen optimization technique (hyperopt for
    stochastic search, crossval for exhaustive search) using validation
    technique (currently only cross-validation).

    :param model_type: model type from MlModel
    :param train_data_transformed: PySpark DataFrame with columns "label" and "features",
        for example by the get_classification_df function.
    :param param_space_search: technique to be used to optimize hyperparameters,
        currently supports "hyperopt" and "param_grid"
    :param validation_technique: technique to be used for validation split
        during hyperparameter evaluation
    :param metric_name: metric to be used as a training objective
    :param max_evals: maximum number of trainings allowed in case of stochastic
        hyperparameter search (for hyperopt)
    :param custom_params: parameter space to be used instead of default values,
        see MlModel for more information

    :return: ML model trained using the best hyperparameters found
    """

    # TODO: docstring update

    # TODO: this function is turning out to be a bit of a monster... split it,
    # move crossvalidation to framework-specific functions, move hyperopt itself to a separate
    # function with callback, deduplicate code, ...

    # TODO: parametrize... numFolds, parallelism, ...
    # TODO: implement different validation_technique options

    # IDEA: log hyperopt trials?

    # user input sanitation
    if validation_technique != "cross_val":
        raise NotImplementedError("Unsupported 'validation_technique'.")

    if param_space_search not in ["hyperopt", "param_grid"]:
        err_msg = (
            f"Hyperparameter search '{param_space_search}' not among supported 'hyperopt', 'param_grid'. "
            "Using '{new_search}' instead."  # intentionally not formatted, will be done later
        )
        if has_dependency("hyperopt"):
            param_space_search = "hyperopt"
        else:
            param_space_search = "param_grid"

        logging.warning(err_msg.format(new_search=param_space_search))

    if param_space_search == "hyperopt" and not has_dependency("hyperopt"):
        logging.warning(
            "Hyperopt selected for hyperparam space search but it is not installed, "
            "using param grid as backup option."
        )
        param_space_search = "param_grid"

    if model_type.framework in ["sklearn", "xgboost"]:
        if not has_dependency("sklearn"):
            raise ImportError("sklearn not installed but model from sklearn framework specified")
        if model_type.framework == "xgboost" and not has_dependency("xgboost"):
            raise ImportError("xgboost not installed but model from xgboost framework specified")

        from sklearn.base import is_classifier
        from sklearn.base import is_regressor

        if not metric_name:
            if is_classifier(model_type.model_class()):
                metric_name = 'auroc'
            elif is_regressor(model_type.model_class()):
                metric_name = 'mse'
            else:
                metric_name = 'accuracy'

        evaluator = _get_metric_by_name(metric_name, "sklearn", fail_when_not_found=True)

        if param_space_search == "hyperopt" and has_dependency("hyperopt"):
            import hyperopt
            if custom_params is not None:
                param_space = custom_params
            else:
                param_space = model_type.default_hyperopt_param_space

            def train(params):
                """function to be passed to hyperopt.fmin for optimization"""

                model = model_type.model_class(**params)
                scores = sklearn.model_selection.cross_val_score(
                    model,
                    train_data_transformed[0],
                    train_data_transformed[1],
                    scoring=evaluator,
                    cv=6,
                    n_jobs=-1,
                )

                # evaluator should be either string with name or from make_scorer
                # either way it's "the higher is better" so we negate it

                # TODO: Check that the above comment is really true. It should
                # be since sklearn scorers in _get_metric_by_name are set
                # with the correct value of "greater_is_better" bit a double
                # check won't hurt.
                return {"loss": -scores.mean(), "status": hyperopt.STATUS_OK}

            # not used anywhere, but let's keep this here for now
            # we might want to log hyperopt trials ... or not
            trials = hyperopt.Trials()

            best_params = hyperopt.fmin(
                fn=train,
                space=param_space,
                algo=hyperopt.tpe.suggest,
                max_evals=max_evals,
                verbose=True,
                trials=trials,
            )
            logging.debug(f"best parameters as found by hyperopt: {best_params}")

            # TODO: save model to trials, retrieve from there
            return (
                model_type
                .model_class(**hyperopt.space_eval(param_space, best_params))
                .fit(train_data_transformed[0], train_data_transformed[1])
            )

        elif param_space_search == "param_grid":
            if custom_params is not None:
                param_space = custom_params
            else:
                param_space = model_type.default_param_grid_values

            grid_search = sklearn.model_selection.GridSearchCV(
                model_type.model_class(),
                param_space,
                n_jobs=-1,  # parametrize? maybe OK to leave it at -1
                verbose=2,  # good default?
                cv=6,  # parametrize this
                scoring=evaluator,
            )
            grid_search.fit(train_data_transformed[0], train_data_transformed[1])
            return (
                model_type
                .model_class(**grid_search.best_params_)
                .fit(train_data_transformed[0], train_data_transformed[1])
            )

    elif model_type.framework in ["spark", "sparkdl"]:
        from pyspark.ml.tuning import CrossValidator
        from pyspark.ml.tuning import ParamGridBuilder

        # breaking change between 3.0 and 3.1 :facepalm:
        # `JavaRegressor` and `JavaClassifier` prepended with underscore
        # new base classes `Regressor` and `Classifier` added instead
        if _SPARK_VERSION == 3 and not pyspark.__version__.startswith("3.0"):  # >= 3.1
            from pyspark.ml.regression import Regressor as BaseRegressor
            from pyspark.ml.classification import Classifier as BaseClassifier
        else:  # < 3.1
            from pyspark.ml.regression import JavaRegressor as BaseRegressor
            from pyspark.ml.classification import JavaClassifier as BaseClassifier

        if not metric_name:
            if issubclass(model_type.model_class, BaseClassifier):
                metric_name = 'auroc'
            elif issubclass(model_type.model_class, BaseRegressor):
                metric_name = 'mse'
            else:
                metric_name = 'accuracy'

        if param_space_search == "hyperopt" and has_dependency("hyperopt"):
            import hyperopt
            if custom_params is not None:
                param_space = custom_params
            else:
                param_space = model_type.default_hyperopt_param_space

            def train(params):
                """function to be passed to hyperopt.fmin for optimization"""

                model = model_type.model_class(**params)
                evaluator = _get_metric_by_name(metric_name, "spark", fail_when_not_found=True)
                _set_spark_model_evaluator_col(model, evaluator)

                # no param grid, it is supplied by hyperopt in params
                param_grid = ParamGridBuilder().build()
                validator = CrossValidator(estimator=model,
                                           estimatorParamMaps=param_grid,
                                           evaluator=evaluator,
                                           parallelism=4,
                                           numFolds=6
                                           )
                models = validator.fit(train_data_transformed)
                model = models.bestModel
                score = -models.avgMetrics[0]

                return {"loss": score, "model": model, "status": hyperopt.STATUS_OK}

            # not used anywhere, but let's keep this here for now
            # we might want to log hyperopt trials ... or not
            trials = hyperopt.Trials()

            best_params = hyperopt.fmin(
                fn=train,
                space=param_space,
                algo=hyperopt.tpe.suggest,
                max_evals=max_evals,
                verbose=True,
                trials=trials,
            )
            logging.debug(f"best parameters as found by hyperopt: {best_params}")

            # TODO: save model to trials, retrieve from there
            return (
                model_type
                .model_class(**hyperopt.space_eval(param_space, best_params))
                .fit(train_data_transformed)
            )

        elif param_space_search == "param_grid":
            param_grid_builder = ParamGridBuilder()
            model = model_type.model_class()

            evaluator = _get_metric_by_name(metric_name, "spark", fail_when_not_found=True)
            _set_spark_model_evaluator_col(model, evaluator)

            if custom_params is not None:
                param_space = custom_params
            else:
                param_space = model_type.default_param_grid_values

            for param_name, param_values in param_space.items():
                param_grid_builder.addGrid(
                    model.__getattribute__(param_name),
                    param_values,
                )

            validator = CrossValidator(estimator=model,
                                       estimatorParamMaps=param_grid_builder.build(),
                                       evaluator=evaluator,
                                       parallelism=4,
                                       numFolds=6,
                                       )

            return validator.fit(train_data_transformed).bestModel
        else:
            raise ValueError("Incorrect optimization technique specified.")
    else:
        raise NotImplementedError(f"Model framework {model_type.framework} not supported.")


# TODO: more models than just GLM have training summaries, use HasTrainingSummary
# mixin, try to implement for others as well --> experimental for now
@requires("pyspark")
def get_spark_glm_summary(model, feat_dict: dict):
    """
    Extract training summary from trained GLM model and parse into Python structures.

    Takes a fitted GLM :param model and a dictionary :param feat_dict of
    feature names (terms of the model) and returns an R-like summary with
    coef. estimate (value), std. error, t-value and p-value for each feature.
    Also outputs the Akaike information criterion of the model. Output format
    is specified below.

    .. code-block:: python

       "coef_name": {"value": estimate, "std_err": err, "t_value": t_val, "p_value": p_val}

    .. Note: The summary is not always created. This can be caused by
        multicollinearity in the data or if the data are too large. In such
        cases, None's will be returned instead.

    :param model: trained Spark GLM model
    :type model: pyspark.ml.regression.GeneralizedLinearRegressionModel
    :param feat_dict: mapping of indices to feature names, can be obtained from
        index_to_feature_mapper_spark function

    :return: dictionary coefficient: values (documented above) and AIC, both can be
        None if summary does not exist
    :rtype: (dict, float)
    """
    # get an ordered list of predictors
    ordered_feature_indices = sorted(feat_dict.keys())
    ordered_feature_names = [
        feat_dict[index]
        for index in ordered_feature_indices
    ]

    # ugly but functional, this is rare but sometimes shit happens...
    try:
        _ = str(model.summary)
    except Exception:
        logging.warning(
            "GLM model does not have summary (can happen based on matrix properties...)"
        )
        return None, None  # no summary to be had...

    coefficients = {
        name: {
            "value": value,
            "std_err": std_err,
            "t_value": t_value,
            "p_value": p_value,
        } for name, value, std_err, t_value, p_value in zip(
            ordered_feature_names + ["intercept"],
            list(model.coefficients) + [model.intercept],
            model.summary.coefficientStandardErrors,
            model.summary.tValues,
            model.summary.pValues,
        )
    }

    return coefficients, model.summary.aic


# TODO: sklearn version?
@experimental  # noqa: C901
@requires("pyspark")  # noqa: C901
def index_to_feature_mapper_spark(  # noqa: C901
    df_transform, model,
) -> dict:
    """
    Maps feature names and their indices in a classification or regression model.

    :param df_transform: any PySpark dataFrame with the correct columns
        to be transformed by the model (e.g. the testing set of the model)
    :param model: any PySpark classifier or regressor model

    :return: dictionary in the form {feature_index: feature_name}
    """
    from itertools import chain
    from pyspark.ml.param.shared import HasPredictionCol
    from pyspark.ml.param.shared import HasRawPredictionCol
    from pyspark.ml.param.shared import HasProbabilityCol
    from pyspark.ml.param.shared import HasVarianceCol

    # the output of the assembler before scaling is necessary
    # scalers do not preserve the metadata

    # TODO: param features_col: str = None, try to infer if not present
    # TODO: this is an expectation that should be noted somewhere...
    # ...does the model have it as featuresCol? could be solved easily then
    if "raw_features" in df_transform.columns:
        assembler_out = "raw_features"
    else:
        assembler_out = "features"

    transformed = df_transform
    if isinstance(model, HasPredictionCol):
        col = model.getPredictionCol()
        if col:
            transformed = transformed.drop(col)
    if isinstance(model, HasRawPredictionCol):
        col = model.getRawPredictionCol()
        if col:
            transformed = transformed.drop(col)
    if isinstance(model, HasProbabilityCol):
        col = model.getProbabilityCol()
        if col:
            transformed = transformed.drop(col)
    if isinstance(model, HasVarianceCol):
        if model.isDefined("varianceCol"):
            col = model.getVarianceCol()
            if col:
                transformed = transformed.drop(col)

    # TODO: does this work on all models?
    attrs = (transformed
             .schema[assembler_out]
             .metadata["ml_attr"]["attrs"]
             .values()
             )

    # TODO: why sort this when it's converted into dict?? (ordering prob not
    # guaranteed anyways)
    # TODO: is the chain needed?
    mapped = sorted((attr["idx"], attr["name"]) for attr in (chain(*attrs)))
    mapped = dict(mapped)

    return mapped


def get_model_metrics(
    model,
    test_data,
    metrics: list = None,
    regression_threshold: float = 0.5,
):
    """
    Calculate specified metrics and return them in format from get_summary_layout (under metrics).

    Note that not all metrics are supported for all model frameworks.
    For sklearn they are "accuracy_score" and "mean_squared_error" (all binary).

    If :param metrics is None, it will be replaced by the default set of metrics
    suitable for given model. To skip calculating all metrics, pass an empty list.

    :param model: trained model to evaluate
    :param test data: data to evaluate model on, should be type Spark Dataframe (for Spark model)
        or list/tuple of Pandas DataFrames (for sklearn models)
    :param metrics: list of metric names
    :param regression_threshold: threshold for categorizing continuous values

    :return: dictionary with metric names and their values, format follows get_summary_layout()
    """
    # NOTE: docstring is copied into more specific functions, make sure to update it

    # TODO: Both specific functions rely on hardcoded lists of metrics defined
    # inside them for each model type. This should be defined elsewhere globally as a constant.

    if has_dependency("pyspark") and _is_spark_model(model):
        return get_model_metrics_spark(
            model, test_data, metrics=metrics, regression_threshold=regression_threshold
        )
    elif has_dependency("sklearn") and _is_sklearn_model(model):
        return get_model_metrics_sklearn(
            model, test_data, metrics=metrics, regression_threshold=regression_threshold
        )
    else:
        raise NotImplementedError("Only Spark and sklearn models supproted currently.")


@requires("pyspark")  # noqa: C901
@copy_docstring_from(get_model_metrics)
def get_model_metrics_spark(  # noqa: C901
    model,
    test_data,
    metrics: list = None,
    regression_threshold: float = 0.5,
):
    # NOTE: docstring copied from get_model_metrics, make sure to update it

    import pyspark.sql.functions as F
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator

    # breaking change between 3.0 and 3.1 :facepalm:
    # `JavaRegressionModel` and `JavaClassificationModel` prepended with underscore
    # new base classes `RegressionModel` and `ClassificationModel` added instead
    if _SPARK_VERSION == 3 and not pyspark.__version__.startswith("3.0"):  # >= 3.1
        from pyspark.ml.regression import RegressionModel as BaseRegressionModel
        from pyspark.ml.regression import GeneralizedLinearRegressionModel as GLM
        from pyspark.ml.classification import ClassificationModel as BaseClassificationModel
    else:  # < 3.1
        from pyspark.ml.regression import JavaRegressionModel as BaseRegressionModel
        from pyspark.ml.regression import GeneralizedLinearRegressionModel as GLM
        from pyspark.ml.classification import JavaClassificationModel as BaseClassificationModel

    if metrics is None:
        if isinstance(model, BaseClassificationModel) or\
                (has_dependency('sparkdl') and _HAS_SPARKDL_XGBOOST
                 and isinstance(model, sparkdl.xgboost.XgboostClassifierModel)):
            metrics = ['accuracy', 'f1', 'weighted_recall', 'weighted_precision']
            if hasattr(model, 'numClasses') and model.numClasses == 2:
                metrics = ['auroc', 'auprc', 'lift_10', 'lift_100'] + metrics
        elif isinstance(model, GLM) and model.getFamily() == 'binomial':
            metrics = ['auroc', 'mse', 'rmse', 'mae', 'r2']
            # TODO possibly AUPRC might also work here as well as lift, check...
        elif isinstance(model, BaseRegressionModel) or\
                (has_dependency('sparkdl') and _HAS_SPARKDL_XGBOOST
                 and isinstance(model, sparkdl.xgboost.XgboostRegressorModel)):
            metrics = ['mse', 'rmse', 'mae', 'r2']
        else:
            logging.warning("The specified model is neither classification\
                             nor regression spark native model.")
            return {}

    df_predictions = model.transform(test_data)
    df_predictions.cache()

    metrics_summary = get_summary_layout()['metrics']

    for metric_name in metrics:
        evaluator = _get_metric_by_name(metric_name, 'spark', fail_when_not_found=False)
        if evaluator is None:
            logging.warning(f"Metric '{metric_name}' currently not supported for spark.")
            continue
        _set_spark_model_evaluator_col(model, evaluator)
        try:
            if (isinstance(model, BaseRegressionModel)
                    and isinstance(evaluator, MulticlassClassificationEvaluator)):
                metrics_summary[metric_name] = evaluator.evaluate(
                    df_predictions.withColumn(
                        model.getPredictionCol(),
                        (F.col(model.getPredictionCol()) > regression_threshold).cast('double')
                    )
                )
            else:
                metrics_summary[metric_name] = evaluator.evaluate(df_predictions)
        except:  # noqa: E722
            logging.warning(f"Metric '{metric_name}' is not compatible with current model.\n\
                              Exception traceback:\n\
                              {traceback.format_exc()}")

    df_predictions.unpersist()

    return metrics_summary


@requires("sklearn")
@copy_docstring_from(get_model_metrics)
def get_model_metrics_sklearn(
    model,
    test_data,
    metrics: list = None,
    regression_threshold: float = 0.5,
):
    # NOTE: docstring copied from get_model_metrics, make sure to update it

    if metrics is None:
        if model._estimator_type == 'classifier':
            metrics = ['accuracy', 'auroc', 'auprc', 'balanced_accuracy',
                       'f1', 'lift_10', 'lift_100',
                       'weighted_precision', 'weighted_recall'
                       ]
        elif model._estimator_type == 'regressor':
            metrics = ['mse', 'rmse', 'mae', 'r2']
        else:
            logging.warning("The specified model is neither classification\
                             nor regression sklearn-compatible model.")

    predictions = model.predict(test_data[0])
    probabilities = model.predict_proba(test_data[0])[:, 1]

    metrics_summary = get_summary_layout()["metrics"]

    for metric_name in metrics:
        metric = _get_metric_by_name(metric_name, 'sklearn',
                                     get_metric=True,
                                     fail_when_not_found=False)
        if metric is None:
            logging.warning(f"Metric '{metric_name}' currently not supported.")
            continue
        try:
            if metric_name in ["auroc", "auprc"]:
                metrics_summary[metric_name] = metric(test_data[1], probabilities)
            else:
                metrics_summary[metric_name] = metric(test_data[1], predictions)
        except:  # noqa: E722
            logging.warning(f"Metric '{metric_name}' is not compatible with current model.\n\
                              Exception traceback:\n\
                              {traceback.format_exc()}")

    return metrics_summary


def get_model_properties(
    model,
    test_data,
):
    """
    Return various properties of given model such as coefficient values (and
    p-values etc.) and feature importances.

    Actual properties returned depend on the model type. For information on
    summary format, see documentation in get_summary_layout.

    :param model: trained model from one of the supported frameworks
        (currently spark and sklearn)
    :param test_data: transformed test data ready to be predicted by the model

    :return: summary with model properties
    """

    # NOTE: docstring is copied into more specific functions, make sure to update it

    if has_dependency("pyspark") and _is_spark_model(model):
        return get_model_properties_spark(model, test_data)
    elif has_dependency("sklearn") and _is_sklearn_model(model):
        return get_model_properties_sklearn(model, test_data)
    else:
        raise NotImplementedError("Only Spark and sklearn models supproted currently.")


@requires("pyspark")
@copy_docstring_from(get_model_properties)
def get_model_properties_spark(
    model,
    test_data,
):
    # NOTE: docstring copied from get_model_properties, make sure to update it

    # IDEA: hyperparameters

    # IDEA: calculate other values for coefficients (p-values, t-values, ...)
    # for other models as well?

    summary = get_summary_layout()

    summary["params"]["model_class"] = type(model).__module__ + '.' + type(model).__name__
    summary["params"]["model_framework"] = "spark"
    summary['params'].update({param.name: value
                              for param, value in model.extractParamMap().items()}
                             )

    feat_dict = index_to_feature_mapper_spark(test_data, model)

    if isinstance(model, pyspark.ml.regression.GeneralizedLinearRegressionModel):
        glm_coefs, glm_aic = get_spark_glm_summary(model, feat_dict)

        if glm_coefs:
            summary["artifacts"]["coefficients"] = glm_coefs

        if glm_aic:
            summary["metrics"]["AIC"] = glm_aic
    else:

        if isinstance(model, pyspark.ml.classification.LogisticRegressionModel) or\
                isinstance(model, pyspark.ml.regression.LinearRegressionModel):
            reg_coefficients = list(model.coefficients)

            summary["artifacts"]["coefficients"] = {
                feat_dict[idx]: reg_coefficients[idx]
                for idx in feat_dict.keys()
            }

            if "intercept" in summary["artifacts"]["coefficients"]:
                # uh-oh, some feature is called intercept...
                logging.warning("name 'intercept' already in coefficients\n\
                                 of logistic/linear regression, overwriting")

            if "intercept_vector" in summary["artifacts"]["coefficients"]:
                # uh-oh again, some feature is called intercept_vector...
                logging.warning("name 'intercept_vector' already in coefficients\n\
                                 of logistic/linear regression, overwriting")

            summary["artifacts"]["coefficients"]["intercept"] = model.intercept
            if isinstance(model, pyspark.ml.classification.LogisticRegressionModel):
                summary["artifacts"]["coefficients"]["intercept_vector"] = list(model.interceptVector)

        elif hasattr(model, 'featureImportances'):
            feature_importances = list(model.featureImportances)

            summary["artifacts"]["feature_importances"] = {
                feat_dict[idx]: feature_importances[idx]
                for idx in feat_dict.keys()
            }

        else:
            logging.warning("The model has neither coefficients not feature importances.")

    return summary


@requires("sklearn")
@copy_docstring_from(get_model_properties)
def get_model_properties_sklearn(
    model,
    test_data,
):
    # NOTE: docstring copied from get_model_properties, make sure to update it
    # ...implement more functionality here (coefficients, feature importances, ...) now

    # it's just a stub
    summary = get_summary_layout()

    summary["params"]["model_class"] = type(model).__module__ + '.' + type(model).__name__
    summary["params"]["model_framework"] = "sklearn"
    summary["params"].update({paramName: value for paramName, value in model.get_params().items()})

    return summary


# IDEA: this function below --> can be used to deploy model (or as part of deployment)
# def load_model_from_mlflow(experiment, run_id, model_name="model"):
#     # this is only some pseudocode written in 5 minutes, treat accordingly
#     # <mlflow run metadata>...??
#     lookup = {"spark": mlflow.spark, "sklearn": mlflow.sklearn}
#     flavour = lookup.get(run_meta.params("model_framework", None), None)
#     if flavour:
#         try:
#             return flavour.load_model(model_name)
#         except Exception:
#             logging.error(traceback.format_exc())
#             return None
#     else:
#         # look at artifact, etc.


# TODO: do we need _spark and _sklearn versions? doesn't get_model_summary suffice
def get_model_summary(model, pipeline, test_data, metrics=None):
    """
    Prepare comprehensive model summary including metrics and various artifacts.

    Calculates various metrics, retrieves model properties such as feature
    importances or coefficients (inspired by R), creates LIFT curve (both the
    dataframe as artifact and highest bin value as metric). Model,
    preprocessing pipeline, and the whole pipeline (including the model) are
    also stored.

    Note that not everything is supported for all frameworks or models.

    For summary layout see documentation of get_summary_layout. The result of
    this function can be passed to log_model_summary to log everything to
    MLflow. It is also possible to add custom metrics, etc. before doing so.
    In that case please keep to the standard layout. Functions
    merge_summaries and get_summary_layout can be helpful.

    :param model: trained PySpark of sklearn model
    :param pipeline: preprocessing pipeline (without the model)
    :param test_data: data to be used for evaluating the model, should
        already be transformed using the preprocessing pipeline
    :param metrics: metrics to be calculated in model summary

    :return: model summary, format documented in get_summary_layout
    """
    # NOTE: docstring is copied into more specific functions, make sure to update it

    # IDEA: conversions (e.g. sklearn model and pyspark df --> convert to pandas)
    if has_dependency("pyspark") and _is_spark_model(model):
        return get_model_summary_spark(model, pipeline, test_data, metrics=metrics)
    # elif ... sklearn models??
    elif has_dependency("sklearn") and _is_sklearn_model(model):
        return get_model_summary_sklearn(model, pipeline, test_data, metrics=metrics)
    else:
        raise NotImplementedError("Only Spark and sklearn models supproted currently.")


@requires("pyspark")
@copy_docstring_from(get_model_summary)
def get_model_summary_spark(model, pipeline, test_data, metrics=None):
    # NOTE: docstring copied from get_model_summary, make sure to update it

    # IDEA: extended=False (if there are some long-running, expensive things, ...)
    # NOTE: do we need train data? will we need them in the future?

    from pyspark.ml import PipelineModel

    predictions = model.transform(test_data)
    predictions.cache()

    df_lift = lift_curve(predictions, bin_count=10)
    lift_summary = get_summary_layout()
    lift_summary["artifacts"]["lift"] = df_lift

    # TODO: model params
    # TODO: duplicate name "metrics", rename...
    metrics = get_model_metrics_spark(model, test_data, metrics=metrics)
    metrics_summary = get_summary_layout()
    metrics_summary["metrics"] = metrics

    props_summary = get_model_properties_spark(model, test_data)

    # eh... naming clash :D
    models_summary = get_summary_layout()
    if _is_spark_model(pipeline.stages[-1]):
        # warn user but don't remove it so that we don't lose something
        logging.warning(
            "Last stage in pipeline is a Spark model. "
            "Maybe you forgot to remove it and pass only the preprocessing pipeline? "
            "I'm going to keep it including the model *and* add the passed model."
        )
    models_summary["models"]["model"] = model
    models_summary["models"]["preprocessing_pipeline"] = pipeline
    models_summary["models"]["pipeline"] = PipelineModel(pipeline.stages + [model])

    return merge_summaries(lift_summary, metrics_summary, props_summary, models_summary)


@requires("sklearn")
@copy_docstring_from(get_model_summary)
def get_model_summary_sklearn(model, pipeline, test_data, metrics=None):
    # NOTE: docstring copied from get_model_summary, make sure to update it

    from sklearn.pipeline import Pipeline
    # TODO: lift...

    # TODO: duplicate name "metrics", rename...
    metrics = get_model_metrics_sklearn(model, test_data, metrics=metrics)
    metrics_summary = get_summary_layout()
    metrics_summary["metrics"] = metrics

    props_summary = get_model_properties_sklearn(model, test_data)

    models_summary = get_summary_layout()
    _, step = pipeline.steps[-1]  # pipeline indexing supported only since sklearn 0.21
    if _is_sklearn_model(step):
        # warn user but don't remove it so that we don't lose something
        logging.warning(
            "Last stage in pipeline is an sklearn model. "
            "Maybe you forgot to remove it and pass only the preprocessing pipeline? "
            "I'm going to keep it including the model *and* add the passed model."
        )
    models_summary["models"]["model"] = model
    models_summary["models"]["preprocessing_pipeline"] = pipeline
    models_summary["models"]["pipeline"] = (
        Pipeline([("preprocessing", pipeline), ("model", model)])
    )

    return merge_summaries(metrics_summary, props_summary, models_summary)


# IDEA: list of metrics (potentially also mappings to framework-specific names)??
def get_summary_layout():
    """
    Create an empty summary layout of a model.

    This function is treated as the definition of format for all functions
    operating on model summary. Function get_model_summary for example uses
    this function and inserts individual entries. This function can then be
    used when you want to create a summary from scratch (to later use
    log_model_summary for example) or to define only some values which can be
    merged with another summary using merge_summaries.

    Top-level keys are mandatory, others will be ignored. Some of the nested
    keys are predefined but no rules are enforced except those listed below.

    Top-level keys "metrics" and "params" can contain nested dictionaries.
    For metrics, the values at the end must be of type float or convertible
    to float (they are to be logged to MLflow as metrics). Params must be
    either strings or convertible to strings.

    Top-level keys "models" and "artifacts" are viewed as flat (not nested)
    dictionaries. Each entry will be logged to MLflow as model and
    JSON-serialized dictionary.

    :return: summary layout as nested dictionaries
    """
    return {
        "metrics": {
        },
        "params": {
            "data_science_functions": {
                "version": __version__,
            }
        },
        "models": {
            "model": None,  # just model
            "preprocessing_pipeline": None,  # just pipeline without model
            "pipeline": None,  # pipeline including model
        },
        "artifacts": {
            "coefficients": {},  # can be anything really, mapping "name": {"val1": val1, ...}
            "feature_importances": {},  # mapping "feature_name": feature_importance
        },
    }


def merge_summaries(*summaries):
    """
    Merge dictionaries one by one.

    Dictionaries are expected to follow layout defined in get_summary_layout.
    Merging happens from left to right with dictionary on the right
    overwriting values of dictionary on the left.

    :param summaries: individual summaries to be merged
    """

    # TODO: only certain parts of dictionaries should be merged as dicts? (e.g.
    # what about artifacts?)

    merged_summary = get_summary_layout()

    for summary in summaries:
        _merge_dicts_recursive(merged_summary, summary)

    return merged_summary


def _merge_dicts_recursive(result_dict, dict_to_merge):
    # NOTE: think about this, is it safe? we're (kinda) overwriting collection we're iteration over.
    # TODO: tests

    keys = [key for key in dict_to_merge.keys()]  # better safe than sorry (updates and iterating)
    for key in keys:
        if key not in result_dict:
            # not there, just copy
            result_dict[key] = _deepcopy_wrapper(dict_to_merge[key])
        else:
            # merge depending on the type
            if isinstance(result_dict[key], dict) and isinstance(dict_to_merge[key], dict):
                _merge_dicts_recursive(result_dict[key], dict_to_merge[key])
            else:
                result_dict[key] = _deepcopy_wrapper(dict_to_merge[key])


@requires("pyspark")
def _is_spark_pipeline(obj):
    """
    Test if :param obj is a *fitted* Spark pipeline, i.e. PipelineModel.

    :param obj: any object
    """
    # PipelineModel is in pyspark.ml (imported from pyspark.ml.pipeline) in both Spark 2 and 3
    return isinstance(obj, pyspark.ml.PipelineModel)


@requires("pyspark")
def _is_spark_model(obj):
    """
    Test if :param obj is a *fitted* Spark ML model.

    Works for sparkdl xgboost as well.

    :param obj: any object
    """
    return isinstance(obj, pyspark.ml.Model)


@requires("sklearn")
def _is_sklearn_pipeline(obj):
    """
    Test if :param obj is an sklearn pipeline.

    Works for xgboost library as well.

    :param obj: any object
    """
    return isinstance(obj, sklearn.pipeline.Pipeline)


@requires("sklearn")
def _is_sklearn_model(obj):
    """
    Test if :param obj is an sklearn ML model.

    :param obj: any object
    """
    return (
        isinstance(obj, sklearn.base.BaseEstimator)
        and not isinstance(obj, sklearn.base.TransformerMixin)
    )


def _deepcopy_wrapper(obj):
    """
    Wrapper for making deep copies.

    PySpark Dataframes (but also models and pipelines) cannot be copied using the standard
    copy.deepcopy function. They fail with somewhat useless error message "TypeError:
    cannot pickle '_thread.RLock' object". It's probably due to the fact that these
    objects are only wrappers of Py4J and JVM objects.

    We circumvent this issue by simply returning the object itself instead of using
    deepcopy. For Spark DataFrames this doesn't matter as they are immutable anyways.
    Spark models and pipelines should deserve some attention though.

    :param obj: any object
    """

    # IDEA: also for pandas df using copy(deep=True) ?
    # TODO: find some way to copy spark pipelines and models
    # (shouldn't matter but it would be better just to be sure)?

    if has_dependency("pyspark") and isinstance(obj, pyspark.sql.dataframe.DataFrame):
        # Spark DataFrames raise "TypeError: cannot pickle '_thread.RLock' object" for
        # some reason just return them as they are immatable anyways
        # UPDATE: seems like general Spark issue (Py4J maybe?), pipelines and models do it
        # too
        return obj
    elif has_dependency("pyspark") and _is_spark_pipeline(obj):
        return obj
    elif has_dependency("pyspark") and _is_spark_model(obj):
        return obj
    else:
        return deepcopy(obj)


def _make_dict_serializable(summary_obj):
    # TODO: docstring (recursive...)

    if has_dependency("pyspark") and isinstance(summary_obj, pyspark.sql.dataframe.DataFrame):
        return [row.asDict() for row in summary_obj.collect()]
    elif has_dependency("pandas") and isinstance(summary_obj, pd.core.frame.DataFrame):
        return summary_obj.to_dict(orient="records")
    elif isinstance(summary_obj, dict):
        dict_copy = dict()
        for key in summary_obj:
            dict_copy[key] = _make_dict_serializable(summary_obj[key])
        return dict_copy
    else:
        try:
            _ = json.dumps(summary_obj)
            return deepcopy(summary_obj)
        except TypeError as e:  # noqa: F841
            # not serializable
            logging.warning(f"object of type {type(summary_obj)} is not serializable, ignoring it")
            return None


def _flatten_dict(dictionary: dict):  # noqa: C901
    # TODO: docstring (recursive, deepcopy should work...)
    # TODO: tests
    #   - should be easily testable and worth it to do so...,
    #   - test edge-cases - also for documenting the functionality
    # TODO: simplify? (cyclomatic complexity 13, hence C901)

    # let's do it breadth-first since we don't need to pass the state around...

    _dict = deepcopy(dictionary)

    re_invalid_chars = re.compile("[^a-zA-Z0-9_]")

    def normalize_key(key):
        # regex is nonlocal but whatever...
        if not isinstance(key, str):
            logging.warning(f"key '{key}' is not of type str, converting")
            key = str(key)

        if re_invalid_chars.search(key):
            logging.warning(f"key '{key}' contains invalid characters, \
                              removing (valid are alphanumerical, hyphen, and underscore)")
            key = re_invalid_chars.sub("", key)
        return key

    # normalize top-level keys now, we won't have a chance later
    _dict = {
        normalize_key(key): value
        for key, value in _dict.items()
    }

    # a wise man once said: if at the first 65536 times you don't succeed, don't try again please
    _max_iters = 65536
    for _iter_num in range(_max_iters):
        # are we done yet?
        for key, value in _dict.items():
            if isinstance(value, dict):
                break  # found nested dict --> continue iterations
        else:
            break  # no nested dicts, stop iterations

        # still got work to do
        keys_to_drop = set()
        keys_to_add = dict()
        for key, value in _dict.items():
            if isinstance(value, dict):
                keys_to_drop.add(key)
                for nested_key, nested_value in value.items():
                    composed_key = f"{key}.{normalize_key(nested_key)}"
                    if composed_key in keys_to_add:
                        logging.warning(f"key '{composed_key}' already present, skipping")
                    else:
                        keys_to_add[composed_key] = nested_value

        _dict = {
            key: value
            for key, value in _dict.items()
            if key not in keys_to_drop
        }

        for key, value in keys_to_add.items():
            if key in _dict.keys():
                logging.warning(f"key '{key}' already present, skipping")
            else:
                _dict[key] = value

    else:
        logging.error(f"could not flatten dictionary in {_max_iters} iterations, \
                        please check if there are no loops")
        return None

    return _dict


# IDEA: deserialize summary from MLflow metadata? (it's well-defined...)


@requires("mlflow")
def _log_metrics(metrics_summary: dict):
    # TODO: docstring
    for name, value in _flatten_dict(metrics_summary).items():
        if not isinstance(value, float):
            try:
                value = float(value)
            except ValueError as e:  # noqa: F841
                logging.warning(f"metric named '{name}' has invalid value, \
                                  could not cast to float, skipping")
                continue  # skip to next metric

        mlflow.log_metric(name, value)


@requires("mlflow")
def _log_params(params_summary: dict):
    for name, value in _flatten_dict(params_summary).items():
        if not isinstance(value, str):
            try:
                value = str(value)
            except Exception as e:  # noqa: F841
                logging.warning(f"param named '{name}' has invalid value, \
                                  could not cast to string, skipping")
                continue  # skip to next param

        mlflow.log_param(name, value)


@requires("mlflow")
def _log_models(models: dict):
    for name, model in models.items():
        if has_dependency("pyspark") and (_is_spark_model(model) or _is_spark_pipeline(model)):
            import mlflow.spark  # make sure spark submodule is loaded
            mlflow.spark.log_model(model, name)
        elif has_dependency("sklearn") and (_is_sklearn_model(model) or _is_sklearn_pipeline(model)):
            import mlflow.sklearn  # make sure sklearn submodule is loaded
            mlflow.sklearn.log_model(model, name)
        else:
            logging.warning(f"Logging model of type '{type(model)}' not supported.")


@requires("mlflow")
def _log_artifacts(artifacts: dict):
    # TODO: docstring (expects artifacts to be json-serializable
    # IDEA: change into user-facing function? maybe could be handy...)

    with tempfile.TemporaryDirectory(prefix="artifacts-") as tmpdir:
        workdir_before = os.getcwd()
        os.chdir(tmpdir)
        for name, obj in artifacts.items():
            file_name = f"{name}.json"
            with open(os.path.join(tmpdir, file_name), "w") as outfile:
                json.dump(obj, outfile)
            mlflow.log_artifact(file_name)
        os.chdir(workdir_before)  # must change back inside the with clause or bad things will happen


@requires("mlflow")
def log_model_summary(summary):
    """
    Log model summary to MLflow.

    Summary is expected to follow format defined in get_summary_layout. Keys
    "params" and "metrics" are flattened by concatenating keys using a dot
    ("."), thus creating unique single-level key-value mapping. For example:

    .. code-block:: text

      # before
      {
          "a": {
              "b": 1,
           },
           "c": 42,
      }

      # after
      {
          "a.b": 1,
          "c": 42,
      }

    The resulting value for metrics must be float or convertible to float,
    for params it must be string or convertible to string.

    Models and artifacts dictionaries are treated as if they were flat. Model
    types are infered and logged to MLflow using the appropriate
    `mlflow.<flavour>.log_model`. Artifacts are serialized using JSON (i.e.
    nested dictionary will be serialized as a single entity)

    :param summary: summary to be logged to MLflow
    """
    if "metrics" in summary:
        _log_metrics(summary["metrics"])

    if "params" in summary:
        _log_params(summary["params"])

    if "artifacts" in summary:
        # need to call _make_dict_serializable first since
        # _flatten_dict expects a well-behaved dict to deepcopy
        _log_artifacts(_make_dict_serializable(summary["artifacts"]))

    if "models" in summary:
        _log_models(summary["models"])


# IDEA: just paste this into an example notebook...
# def _deserialize_dataframe(obj: dict, framework: str = None):
#     if framework == "spark" and not has_dependency("pyspark"):
#         pass  # raise error
#     if framework == "pandas" and not has_dependency("pandas"):
#         pass  # raise error
#
#     # example data... [{'a': 1, 'b': 'foo'}, {'a': 2, 'b': 'bar'}, {'a': 3, 'b': 'baz'}]
#
#     if has_dependency("pandas") and framework == "pandas":
#         return pd.DataFrame.from_records(data)
#     elif has_dependency("pyspark") and framework == "spark":
#         from pyspark.sql import Row
#         return spark.createDataFrame([
#             Row(**datum) for datum in data
#         ])


if has_dependency("pyspark"):

    # TODO: HasRawPredictionCol introduces potentially a whole slew of problems
    # actually implement this... (works now)
    class LiftEvaluatorSpark(
        pyspark.ml.evaluation.Evaluator,
        pyspark.ml.param.shared.HasRawPredictionCol
    ):
        # TODO: docstrings
        def __init__(self, rawPredictionCol="rawPrediction", labelCol="label", binCount=10):
            self.rawPredictionCol = rawPredictionCol
            self.labelCol = labelCol
            self.binCount = binCount

        def _evaluate(self, dataset):
            return (
                lift_curve(
                    dataset,
                    label_col=self.labelCol,
                    bin_count=self.binCount,
                    probability_col=self.rawPredictionCol,
                )
                .filter(F.col("bucket") == 1)
                .select('cum_lift')
                .collect()[0][0]
            )

        def setParams(self, rawPredictionCol=None, labelCol=None, binCount=None):
            """
            custom setParams implementation that behaves like setParams in PySpark
            """
            # NOTE: we should probably check types...
            if rawPredictionCol is not None:
                self.rawPredictionCol = rawPredictionCol
            if labelCol is not None:
                self.labelCol = labelCol
            if binCount is not None:
                self.binCount = binCount

        def isLargerBetter(self):
            return True

        def getMetricName(self):
            return 'lift_' + str(self.binCount)


def lift_curve(
    df_predictions,
    bin_count: int = 10,
    label_col: str = "label",
    probability_col: str = None,
):
    """
    Lift curve approximation for binary classification model.

    Function for calculating lift of binary classification model. Predicted probabilities should
    be given in column :param probability_col and column :param label_col should specify
    belonging to target (1 for target, 0 otherwise).

    For Pandas version, :param probability_col is required and its values should be probabilities
    as floats.

    For Spark version, if :param probability_col is not specified, it will try to infer the name
    from those commonly used by Spark ML models. Also, it the column is of type vector, the
    second element will be extracted as the probability of belonging to target (as is usual in
    Spark classifiers outpus).

    Only the order of predicted probabilities is taken into account, the
    actual values are not. Cummulative lift and related metrics are then
    calculated for every bin. Computation details in the :return description.

    :param df_predictions: Spark or Pandas DataFrame with columns given by label_col and
        probability_col
    :param bin_count: number of bins you want the data to be split into
    :param label_col: name of the label column (required)
    :param probability_col: name of the column containing probabilities (required for Pandas)

    :return: spark dataframe with columns:

    .. code-block:: text

      bucket                    bucket number
      num_subj                  number of subjects in corresponding bucket
      num_target                number of subjects with label == 1 in corresponding bucket
      avg_probability           average predicted probability for subjects in corresponding bucket
      cum_avg_target            average number of subjects with label == 1 in buckets with number
                                    less than or equal to the corresponding bucket number merged together
      cum_lift                  lift metric for buckets with number less than or equal to the corresponding
                                    bucket number merget together, calculated as

            cum_lift        = cum_avg_target / avg_target_rate ,
            avg_target_rate = sum(num_subj) / bin_count

    """

    if has_dependency("pyspark") and isinstance(df_predictions, pyspark.sql.dataframe.DataFrame):
        return lift_curve_spark(
            df_predictions,
            bin_count=bin_count,
            label_col=label_col,
            probability_col=probability_col,
        )
    elif has_dependency("pandas") and isinstance(df_predictions, pd.core.frame.DataFrame):
        return lift_curve_pandas(
            df_predictions,
            bin_count=bin_count,
            label_col=label_col,
            probability_col=probability_col,
        )
    else:
        raise ValueError(_ERR_INVALID_DF_TYPE)


@requires("pyspark")
@copy_docstring_from(lift_curve)
def lift_curve_spark(
    df_predictions,
    bin_count: int = 10,
    label_col: str = "label",
    probability_col: str = None,
):
    from pyspark.sql.window import Window
    import pyspark.sql.functions as F
    from pyspark.ml.functions import vector_to_array

    if type(bin_count) != int or bin_count < 0:
        raise ValueError("Invalid 'bin_count' param value. \
                          Expected int >= 0, got '{}'.".format(bin_count))

    if not probability_col:
        if "rawPrediction" in df_predictions.columns:
            logging.info("'probability_col' not provided, \
                          found 'rawPrediction', using 'probability'.")
            probability_col = F.element_at(vector_to_array("probability"), 2)
        elif "prediction" in df_predictions.columns:
            logging.info("'probability_col' not provided, haven't found 'rawPrediction', \
                          using 'prediction'.")
            probability_col = F.col("prediction")
        else:
            raise ValueError("Param 'probability_col' not supplied \
                              and could not infer column name.")
    else:
        if probability_col not in df_predictions.columns:
            raise ValueError("Value given in 'probability_col' is not among dataframe columns.")

        _dtype = [_dtype for col, _dtype in df_predictions.dtypes if col == probability_col][0]
        if _dtype == "vector":
            probability_col = F.element_at(vector_to_array(probability_col), 2)
        else:
            probability_col = F.col(probability_col)

    df_lift = (df_predictions
               .select(probability_col.alias("class_1_probability"), label_col)
               .withColumn("rank",
                           F.ntile(bin_count).over(Window.orderBy(F.desc("class_1_probability")))
                           )
               .select("class_1_probability", "rank", label_col)
               .groupBy("rank")
               .agg(F.count(label_col).alias("num_subj"),
                    F.sum(label_col).alias("num_target"),
                    F.avg("class_1_probability").alias("avg_probability")
                    )
               .withColumn("cum_avg_target",
                           (F.avg("num_target").over(Window.orderBy("rank").
                                                     rangeBetween(Window.unboundedPreceding, 0)
                                                     )
                            )
                           )
               )

    avg_lead_rate = (df_lift
                     .filter(F.col("rank") == bin_count)
                     .select("cum_avg_target")
                     .collect()[0][0]
                     )

    df_cum_lift = (df_lift
                   .withColumn("cum_lift", F.col("cum_avg_target").cast("double") / avg_lead_rate)
                   .selectExpr("rank as bucket", "num_subj", "num_target",
                               "avg_probability", "cum_avg_target", "cum_lift"
                               )
                   )

    return df_cum_lift


@requires("pandas")
@copy_docstring_from(lift_curve)
def lift_curve_pandas(
    df_predictions,
    bin_count: int = 10,
    label_col: str = "label",
    probability_col: str = None,
):

    # IDEA: rename label_col and probability_col to make sure there are no collisions??

    # user input sanitization
    if not probability_col:
        raise ValueError("Parameter 'prediction_col' is required for Pandas version of lift_curve.")

    if not label_col:
        raise ValueError("Parameter 'label_col' is required.")

    # inplace=False so that we don't change the original data!!
    df_predictions = df_predictions.copy(deep=True)

    df_predictions["rank"] = df_predictions[probability_col].rank(method="first", ascending=False)
    # +1 so that we start from 1 (same as Spark version)
    df_predictions["bucket"] = 1 + pd.cut(df_predictions["rank"], bin_count, labels=False)

    df_lift = (
        df_predictions
        .groupby("bucket", sort=True)
        .agg({
            "bucket": ["first"],
            label_col: ["count", "sum"],
            probability_col: ["mean"],
        })
    )

    df_lift.columns = ["_".join(col).strip() for col in df_lift.columns.values]

    df_lift.rename(
        columns={
            "bucket_first": "bucket",
            f"{label_col}_count": "num_subj",
            f"{label_col}_sum": "num_target",
            f"{probability_col}_mean": "avg_probability",
        },
        inplace=True,
    )

    # this is wrong (not taking into account number of entries in bucket
    # but it's consistent with Spark implementation and error is negligible
    df_lift["cum_avg_target"] = df_lift["num_target"].expanding().mean()
    avg_lead_rate = df_lift[df_lift["bucket"] == bin_count].iloc[0]["cum_avg_target"]
    df_lift["cum_lift"] = df_lift["cum_avg_target"] / avg_lead_rate

    return df_lift


# TODO: supervised_wrapper - Pandas version
@requires("mlflow", strict=False)  # noqa C901, TODO: simplify this
def supervised_wrapper(  # noqa C901, TODO: simplify this
    df,  # noqa C901, TODO: simplify this
    model_type: MlModel,
    use_mlflow: bool = True,
    label_col: str = "label",
    skip_cols: list = None,
    params_get_cat_num_columns: dict = None,
    params_fit_pipeline: dict = None,
    params_split: dict = None,
    params_fit_model: dict = None,
):
    """
    Run default end-to-end ML pipeline on a feature data set.

    Currently binary classification and regression in Spark and sklearn
    (on top of Pandas) is supported.

    Takes a dataframe, prepares it for machine learning, splits to train and
    test set, fits preprocessing pipeline on training data, fits model
    hyperparameters using given optimization technique, calculates various
    model properties, artifacts, and metrics and logs them to mlflow (if
    :param use_mlflow is specified). Please note that tracking URI and
    experiment should be set in MLflow in advance.

    This is just a wrapper. To achieve greater flexibility (e.g. custom
    train/test split or data wrangling), you can start from this function's
    implementation and/or provided examples and adjust the necessary parts
    according to your needs.

    Parameters starting with `params_` are passed into relevant functions.
    Some of their parameters are not supported (e.g. data since it will be
    supplied from previous steps inside of this function). In such a case,
    parameter will simply be ignored and warning will be written to logs.

    .. Note:: this function disables automatic tracking and only logs the
        final model so that the experiment is not polluted with exceeding
        amount of models with no data about them

    :param df: dataset containing features to be used for model training
    :param model_type: model type from MlModel
    :param use_mlflow: if set to True, log model, metrics, etc. to MLflow
    :param label_col: name of column to use as label/target values
    :param skip_cols: columns to be removed from consideration in
        preprocessing pipeline and model training
    :type skip_cols: list of strings
    :param params_get_cat_num_columns: parameters passed to
        get_categorical_and_numeric_cols
    :param params_fit_pipeline: parameters passed to fit_transformation_pipeline
    :param params_split: parameters passed to train_test_split
    :param params_fit_model: parameters passed to fit_supervised_model

    :return: transformed train data, transformed test data, model summary
    """
    # import pyspark.sql.functions as F

    # NOTE: synchronize any changes with relevant example notebook!!!

    # mutating collections that were defined as default params is an obscure Python bug
    if skip_cols is None:
        skip_cols = []

    if params_get_cat_num_columns is None:
        params_get_cat_num_columns = {}

    if params_fit_pipeline is None:
        params_fit_pipeline = {}

    if params_split is None:
        params_split = {}

    if params_fit_model is None:
        params_fit_model = {}

    # user input sanitation
    def ignore_param(param_dict, param, func):
        if param in param_dict:
            logging.warning(
                f"Passing '{param}' to '{func}' not supported in supervised_wrapper, ignoring it."
            )
            del param_dict[param]

    ignore_param(params_get_cat_num_columns, "df", "get_categorical_and_numeric_cols")
    ignore_param(params_fit_pipeline, "train_data", "fit_transformation_pipeline")
    ignore_param(params_fit_pipeline, "skip_cols", "fit_transformation_pipeline")
    ignore_param(params_split, "df", "train_test_split")
    ignore_param(params_fit_model, "model_type", "fit_supervised_model")
    ignore_param(params_fit_model, "train_data_transformed", "fit_supervised_model")

    if skip_cols is None:
        skip_cols = []

    spark = None  # provide some default value just in case

    if model_type.framework == "spark":
        framework = "spark"

        if not has_dependency("pyspark"):
            raise ValueError("Model type of framework 'spark' specified \
                              but 'pyspark' is not installed.")
        elif _SPARK_VERSION == 2:
            raise RuntimeError("Spark version 2 not supported in supervised_wrapper.")
        else:
            # get spark session, might be None if doesn't exist
            spark = pyspark.sql.SparkSession.getActiveSession()

        if has_dependency("pandas") and isinstance(df, pd.core.frame.DataFrame):
            logging.info("Model framework 'spark' but data provided as Pandas DF, \
                          casting to Spark DF.")
            df = spark.createDataFrame(df)

        df.cache()
    elif model_type.framework == "sklearn":
        framework = "sklearn"

        if not has_dependency("sklearn"):
            raise ValueError("Model type of framework 'sklearn' specified \
                              but 'sklearn' is not installed.")

        if has_dependency("pyspark") and isinstance(df, pyspark.sql.DataFrame):
            logging.info("Model framework 'sklearn' but data provided as Spark DF, \
                          casting to Pandas DF.")
            df = df.toPandas()
    else:
        raise ValueError(f"Model of framework '{model_type.framework}' \
                           is not supported in this function currently.")

    # TODO: what if "label" exists in columns?
    if framework == "spark":
        df = df.withColumnRenamed(label_col, "label")
    elif framework == "sklearn":
        df = df.rename(columns={label_col: "label"})

    params_split["df"] = df
    train_data, test_data = train_test_split(**params_split)

    if (params_fit_pipeline.get("cat_cols", None) is None
            and params_fit_pipeline.get("num_cols", None) is None):

        params_get_cat_num_columns["df"] = train_data
        params_get_cat_num_columns["skip_cols"] = skip_cols
        cat_cols, num_cols = get_categorical_and_numeric_cols(**params_get_cat_num_columns)
        params_fit_pipeline["cat_cols"] = cat_cols
        params_fit_pipeline["num_cols"] = num_cols
    else:
        # at least one is not None --> treat None as "no columns"
        if params_fit_pipeline.get("cat_cols", None) is None:
            params_fit_pipeline["cat_cols"] = []
        if params_fit_pipeline.get("num_cols", None) is None:
            params_fit_pipeline["num_cols"] = []

    params_fit_pipeline["train_data"] = train_data
    params_fit_pipeline["skip_cols"] = skip_cols + ["label"]
    pipeline = fit_transformation_pipeline(**params_fit_pipeline)

    train_data_transf, test_data_transf = apply_transformation_pipeline(
        pipeline,
        train_data,
        test_data,
    )

    # TODO: in case of Spark we probably need to cache *before* splitting
    # TODO: maybe just caching is not enough...
    if framework == "spark":
        train_data_transf.cache()
        test_data_transf.cache()

        _ = train_data_transf.count()
        _ = test_data_transf.count()

    if has_dependency("pyspark") and spark:
        # spark is None if there is no active session...

        # TODO: this is obviously databricks-specific, solve it (?)
        # disable MLlib automatic tracking temporarily
        track_mlflow_orig = spark.conf.get("spark.databricks.mlflow.trackMLlib.enabled", None)
        spark.conf.set("spark.databricks.mlflow.trackMLlib.enabled", "false")

    params_fit_model["model_type"] = model_type
    params_fit_model["train_data_transformed"] = train_data_transf
    model = fit_supervised_model(**params_fit_model)

    if has_dependency("pyspark") and spark:
        # spark is None if there is no active session...

        # set MLFlow settings back to the original state
        if track_mlflow_orig:
            spark.conf.set("spark.databricks.mlflow.trackMLlib.enabled", track_mlflow_orig)
        else:
            spark.conf.unset("spark.databricks.mlflow.trackMLlib.enabled")

    summary = get_model_summary(model, pipeline, test_data_transf)

    if use_mlflow:
        if not has_dependency("mlflow"):
            logging.error(
                "'use_mlflow' specified in 'supervised_wrapper' but mlflow is not installed"
            )
        else:
            with mlflow.start_run():
                log_model_summary(summary)

    return train_data_transf, test_data_transf, summary
