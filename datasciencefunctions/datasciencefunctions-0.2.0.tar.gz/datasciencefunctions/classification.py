
################################################################################
# NOTE: this module is being deprecated, do not add new functionality
################################################################################

from .supervised import *  # noqa F401, F403 INTENTIONAL - exact copy of 'supervised'
from ._classification import do_datasciencing  # noqa: F401
from ._classification import fit_classification_model  # noqa: F401


__import__("logging").warning(
    "Module 'classification' has been renamed to 'supervised', consider migrating "
    + " to the new name. Old name will stop working in a future release."
)
