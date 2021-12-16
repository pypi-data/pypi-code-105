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


class SavedDataset(Model):
    """SavedDataset.

    :param id:
    :type id: str
    :param dataset_type:
    :type dataset_type: str
    :param properties:
    :type properties: dict[str, object]
    :param dataflow_json:
    :type dataflow_json: str
    :param data_changed:
    :type data_changed: bool
    :param data_path:
    :type data_path: ~_restclient.models.DatasetPath
    :param telemetry_info:
    :type telemetry_info: dict[str, str]
    :param data_expiry_time:
    :type data_expiry_time: datetime
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'dataset_type': {'key': 'datasetType', 'type': 'str'},
        'properties': {'key': 'properties', 'type': '{object}'},
        'dataflow_json': {'key': 'dataflowJson', 'type': 'str'},
        'data_changed': {'key': 'dataChanged', 'type': 'bool'},
        'data_path': {'key': 'dataPath', 'type': 'DatasetPath'},
        'telemetry_info': {'key': 'telemetryInfo', 'type': '{str}'},
        'data_expiry_time': {'key': 'dataExpiryTime', 'type': 'iso-8601'},
    }

    def __init__(self, id=None, dataset_type=None, properties=None, dataflow_json=None, data_changed=None, data_path=None, telemetry_info=None, data_expiry_time=None):
        super(SavedDataset, self).__init__()
        self.id = id
        self.dataset_type = dataset_type
        self.properties = properties
        self.dataflow_json = dataflow_json
        self.data_changed = data_changed
        self.data_path = data_path
        self.telemetry_info = telemetry_info
        self.data_expiry_time = data_expiry_time
