# -*- coding: utf-8 -*-
"""houses all the validations for the tool"""

from importlib import import_module
from .constants import Frameworks, ErrorMessages


def validate_frameworks(framework, type):
    if not framework in Frameworks.python:
        # throw error
        raise Exception(ErrorMessages.ValidateFrameworkError)
    else:
        if type not in Frameworks.python[framework]:
            # throw error
            raise Exception(ErrorMessages.ValidateFrameworkTypeError)


def validate_name(name):
    if name is None:
        raise Exception(ErrorMessages.BuildNameError)

    if not name.isidentifier():
        raise Exception(ErrorMessages.NotAValidDirectoryNameError)

    try:
        import_module(name)
    except:
        pass
    else:
        raise Exception(ErrorMessages.ExistingNameConflictError)
