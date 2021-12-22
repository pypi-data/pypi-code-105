
from ._utils import experimental  # noqa: F401
from ._utils import has_dependency  # noqa: F401
from ._utils import requires  # noqa: F401
from ._utils import current_dbx_notebook_path  # noqa: F401


_ERR_SPLIT_COL_AND_NOT_COL_BASED = \
        "train_test_split called with split_col but split_type is not column_based"
# TODO: in some places it can be Spark DF, Pandas DF, or list[PD_DF] / tuple[PD_DF]...
# TODO: add formatting option {df_type}, add note about potential missing dependencies
_ERR_INVALID_DF_TYPE = \
        "dataframe type must be either pandas or pyspark"


__all__ = [  # TODO: remove this, needed for documentation build currently...
    # "copy_docstring_from",
    "current_dbx_notebook_path",
    # "experimental",
    # "has_dependency",
    # "requires",
]
