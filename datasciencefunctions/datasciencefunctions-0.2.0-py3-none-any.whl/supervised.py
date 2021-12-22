from ._supervised import supervised_wrapper  # noqa: F401
from ._supervised import fit_supervised_model  # noqa: F401
from ._supervised import get_model_metrics  # noqa: F401
from ._supervised import get_model_metrics_sklearn  # noqa: F401
from ._supervised import get_model_metrics_spark  # noqa: F401
from ._supervised import get_spark_glm_summary  # noqa: F401
from ._supervised import get_model_properties  # noqa: F401
from ._supervised import get_model_properties_sklearn  # noqa: F401
from ._supervised import get_model_properties_spark  # noqa: F401
from ._supervised import get_model_summary  # noqa: F401
from ._supervised import get_model_summary_sklearn  # noqa: F401
from ._supervised import get_model_summary_spark  # noqa: F401
from ._supervised import get_summary_layout  # noqa: F401
from ._supervised import index_to_feature_mapper_spark  # noqa: F401
from ._supervised import lift_curve  # noqa: F401
from ._supervised import lift_curve_pandas  # noqa: F401
from ._supervised import lift_curve_spark  # noqa: F401
from ._supervised import log_model_summary  # noqa: F401
from ._supervised import merge_summaries  # noqa: F401


__all__ = [  # TODO: remove this, needed for documentation build currently...
    "supervised_wrapper",
    "fit_supervised_model",
    "get_model_metrics",
    "get_model_metrics_sklearn",
    "get_model_metrics_spark",
    "get_model_properties",
    "get_model_properties_sklearn",
    "get_model_properties_spark",
    "get_model_summary",
    "get_model_summary_sklearn",
    "get_model_summary_spark",
    "get_spark_glm_summary",
    "get_summary_layout",
    "index_to_feature_mapper_spark",
    "lift_curve",
    "lift_curve_pandas",
    "lift_curve_spark",
    "log_model_summary",
    "merge_summaries",
]


# NOTE: (in the future move more general functions (summary and its manipulations,
# functions that work on more than classification/regression) elsewhere
