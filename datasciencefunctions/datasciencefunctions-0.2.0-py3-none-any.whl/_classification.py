
################################################################################
#  NOTE: this module is being deprecated, do not add new functionality
################################################################################

from ._supervised import supervised_wrapper
from ._supervised import fit_supervised_model
from ._utils import deprecated


@deprecated(comment="Use 'supervised_wrapper' from 'supervised' instead.")
def do_datasciencing(*args, **kwargs):
    supervised_wrapper(*args, **kwargs)


@deprecated(comment="Use 'fit_supervised_model' from 'supervised' instead.")
def fit_classification_model(*args, **kwargs):
    fit_supervised_model(*args, **kwargs)
