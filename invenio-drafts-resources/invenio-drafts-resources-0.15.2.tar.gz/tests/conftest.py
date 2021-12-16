# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask_principal import Identity, Need, UserNeed
from invenio_app.factory import create_api as _create_api
from invenio_records_resources.services.files import FileService
from mock_module.service import DraftFileServiceConfig, FileServiceConfig

pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {
        'invenio_db.model': [
            'mock_module = mock_module.models',
        ],
        'invenio_jsonschemas.schemas': [
            'mock_module = mock_module.jsonschemas',
        ],
        'invenio_search.mappings': [
            'draftsresources = mock_module.mappings',
        ]
    }


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_api


@pytest.fixture()
def input_data():
    """Input data (as coming from the view layer).

    Most tests don't care about files, so files are disabled in the fixture.
    """
    return {
        'metadata': {
            'title': 'Test'
        },
        'files': {
            'enabled': False
        }
    }


@pytest.fixture(scope="module")
def file_service():
    """File service fixture."""
    return FileService(FileServiceConfig)


@pytest.fixture(scope="module")
def draft_file_service():
    """File service fixture."""
    return FileService(DraftFileServiceConfig)


@pytest.fixture()
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(Need(method='system_role', value='any_user'))
    return i
