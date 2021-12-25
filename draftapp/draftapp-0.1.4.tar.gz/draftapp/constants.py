# -*- coding: utf-8 -*-
"""SetApp constants module"""


class Frameworks:
    """Frameworks and Types constants"""

    python = {"flask": ["basic", "advanced"]}


class ErrorMessages:
    """Messages for errors thrown"""

    ValidateFrameworkError = (
        "Invalid framework. Kindly see --help for supported frameworks"
    )
    ValidateFrameworkTypeError = (
        "Invalid framework type. See --help for supported framework types"
    )
    BuildNameError = "Please provide an app name to build the project with. Kindly see --help for more details"
    NotAValidDirectoryNameError = (
        "Please provide a valid directory name with a valid identifier"
    )
    ExistingNameConflictError = "The provided app name conflicts with an existing python module and cannot be used.Please try another name"
    FileAlreadyExistsError = "A directory with the name specified already exists in the current working directory. Kindly provide a different name / path"
    OSErrorThrown = "OS error thrown !"


class TemplateFileContentReplace:
    filenames = [
        "Makefile",
        "setup.py",
        "env.py",
        "project_name-cli",
        "Dockerfile",
        "config.py",
        "log.py",
        "conftest.py",
        "test_views.py",
        ".coveragerc",
        "deployment.yaml",
        "configmap.yaml"
    ]
