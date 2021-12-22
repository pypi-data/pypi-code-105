import copy
import functools
import importlib
import logging
import os


# IDEA: remove some functions from external documentation? (should requires and
#       experimental be available to end-users?
# IDEA: provide context manager to disable MLflow automatic tracking
#   - not so easy...
#   - somehow disable MLflow?
#   - create dummy "/dev/null" run and log into it?
# def disable_mlflow_automatic_tracking():
#     pass


# lookups to be used with has_dependency, procees with caution
_VALID_IMPORTS_LOOKUP = set()
_INVALID_IMPORTS_LOOKUP = set()

# NOTE: Some decorators change docstrings, make sure to use them in correct
# order. For example `requires` adds a note to docstring while
# `copy_docstring_from` overrides docstring. If you use `copy_docstring_from`
# *after* `required`, you will have effectively negated the effect on docstring.


def current_dbx_notebook_path(dbutils):
    """
    Get full path of current Databricks notebook.

    :param dbutils: Databricks Utils handler, accessible as ``dbutils``
    :type dbutils: DBUtils

    :return: path of current notebook
    :rtype: str
    """

    return (
        dbutils
        .entry_point
        .getDbutils()
        .notebook()
        .getContext()
        .notebookPath()
        .get()
    )


# TODO: copy docstring in full at runtime but only a
# "see..." at documentation build time
def copy_docstring_from(other_func):
    """
    Decorate function to set its docstring to that of other function.

    :param other_func: function to copy the docstring from
    """

    # IDEA: add parameter to do an append (take the docstring of `func` and merge it into
    # `other_func`s docstring

    # TODO: tests ... basic value, edge cases (Nones on either side)

    if os.environ.get("SPHINX_RUNNING", None) == "true":  # set in docs/source/conf.py
        # for building documentation, we don't need to really copy the
        # docstring and it would look weird having the same text several times
        def decorator(func):
            func.__doc__ = (
                f"Specialized implementation, see documentation of `{other_func.__name__}`."
            )
            return func
    else:
        # not building documentation, actually copy the docstring
        def decorator(func):
            # TODO: is copy.deepcopy enough? (didn't work properly for strings somewhere...)
            func.__doc__ = copy.deepcopy(other_func.__doc__)
            return func

    return decorator


def experimental(func):
    """
    Decorate function as experimental.

    Annotates the function as experimental for documentation purposes and produces logging
    output when the function is used.

    :param func: function to decorate
    """
    disclaimer = "    .. Note:: this function is experimental and may be "\
        "changed or removed without prior notice\n\n"
    if func.__doc__:
        func.__doc__ = disclaimer + func.__doc__
    else:
        func.__doc__ = disclaimer

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning(f"function {func.__name__} is experimental")
        return func(*args, **kwargs)
    return wrapper


def deprecated(comment: str = None):
    """
    Decorate function as deprecated.

    Annotates the function as experimental for documentation purposes and produces logging
    output when the function is used.

    :param comment: optional comment to be appended to docstring and log output
    """
    def outer_wrapper(func):
        disclaimer = (
            "    .. Note:: this function is deprecated and "
            + " will be removed in a future release"
            + (". " + comment if comment else "")
            + "\n\n"
        )
        if func.__doc__:
            func.__doc__ = disclaimer + func.__doc__
        else:
            func.__doc__ = disclaimer

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.warning(
                f"Function {func.__name__} is deprecated."
                + (" " + comment if comment else "")
            )
            return func(*args, **kwargs)
        return wrapper

    return outer_wrapper


def has_dependency(module_name: str) -> bool:
    """
    Check whether module can be imported.

    Uses lookups so that we do not try to repeatedly import a module that isn't available.

    :param module_name: name of module to check
    """
    if module_name in _VALID_IMPORTS_LOOKUP:
        return True
    elif module_name in _INVALID_IMPORTS_LOOKUP:
        return False
    else:
        try:
            importlib.import_module(module_name)
            # managed to import, it's valid
            _VALID_IMPORTS_LOOKUP.add(module_name)
            return True
        except ImportError as e:  # noqa: F841
            _INVALID_IMPORTS_LOOKUP.add(module_name)
            return False


# init lookups with some modules that are likely to be checked anyways
for name in ["pandas", "pyspark", "sklearn", "hyperopt"]:
    _ = has_dependency(name)


# IDEA: test flag, if set, do additional checks at import time? (module_names has
# [A-Za-z_] values etc.
def requires(*module_names, strict=True):
    """
    Decorate function giving it runtime check for required external modules.

    This library is designed to work with several frameworks but to be able to work
    when some of them aren't present. To do this, no external dependencies are needed
    during installation or import time. If a function needs access to external libraries,
    use this decorator to provide a runtime check and also to annotate it for
    documentation purposes. Wording of annotation depends on :param strict.

    Note that if :param strict is set as True, an ImportError will be raised *at runtime*
    if some dependencies are not met.

    :param module_names: modules required by given function
    :type module_names: list of str
    :param strict: treat dependencies as strictly required or optional
    :type strict: bool
    """

    # IDEA: it might be better to just check at function definition time and if imports
    # are missing, wrap it with "raise exception" otherwise return it unchanged

    def outer_wrapper(func):
        if strict:
            disclaimer = (
                "    .. Note:: This function requires the following packages: "
                + ", ".join(module_names)
                + "\n\n"
            )
        else:
            disclaimer = (
                "    .. Note:: This function has the following packages as "
                + "optional dependencies: "
                + ", ".join(module_names)
                + "\n\n"
            )

        if func.__doc__:
            func.__doc__ = disclaimer + func.__doc__
        else:
            func.__doc__ = disclaimer

        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            for import_name in module_names:
                if not has_dependency(import_name):
                    if strict:
                        error_message = f"function {func.__name__} requires " \
                                f"'{import_name}' which is not installed"
                        logging.error(error_message)
                        raise ImportError(error_message)
                    else:
                        error_message = (
                            f"function {func.__name__} is missing optional dependency "
                            + f"{import_name}"
                        )
                        logging.warning(error_message)
            return func(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper


@requires("pyspark")
def _get_active_spark_session():
    from pyspark.sql import SparkSession

    try:
        return SparkSession.getActiveSession()  # Spark 3.0+ only
    except Exception:
        return SparkSession._instantiatedSession
