# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FeaturizationConfig(Model):
    """FeaturizationConfig.

    :param mode: Possible values include: 'Off', 'Auto', 'Custom'
    :type mode: str or ~_restclient.models.FeaturizationMode
    :param _blocked_transformers:
    :type _blocked_transformers: list[str]
    :param _column_purposes:
    :type _column_purposes: object
    :param _transformer_params:
    :type _transformer_params: object
    :param _drop_columns:
    :type _drop_columns: list[str]
    :param blocked_transformers:
    :type blocked_transformers: list[str]
    :param column_purposes:
    :type column_purposes: object
    :param transformer_params:
    :type transformer_params: object
    """

    _attribute_map = {
        'mode': {'key': 'mode', 'type': 'FeaturizationMode'},
        '_blocked_transformers': {'key': '_blocked_transformers', 'type': '[str]'},
        '_column_purposes': {'key': '_column_purposes', 'type': 'object'},
        '_transformer_params': {'key': '_transformer_params', 'type': 'object'},
        '_drop_columns': {'key': '_drop_columns', 'type': '[str]'},
        'blocked_transformers': {'key': 'blocked_transformers', 'type': '[str]'},
        'column_purposes': {'key': 'column_purposes', 'type': 'object'},
        'transformer_params': {'key': 'transformer_params', 'type': 'object'},
    }

    def __init__(self, mode=None, _blocked_transformers=None, _column_purposes=None, _transformer_params=None, _drop_columns=None, blocked_transformers=None, column_purposes=None, transformer_params=None):
        super(FeaturizationConfig, self).__init__()
        self.mode = mode
        self._blocked_transformers = _blocked_transformers
        self._column_purposes = _column_purposes
        self._transformer_params = _transformer_params
        self._drop_columns = _drop_columns
        self.blocked_transformers = blocked_transformers
        self.column_purposes = column_purposes
        self.transformer_params = transformer_params
