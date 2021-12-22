################################################################################
# NOTE: this module is being deprecated, do not add new functionality
################################################################################

from ._online_marketing import url_to_adform_format  # noqa: F401


__all__ = [  # TODO: remove this, needed for documentation build currently...
    "url_to_adform_format",
]

__import__("logging").warning(
    "Module 'online_marketing' is being deprecated and will be removed in a future release."
)
