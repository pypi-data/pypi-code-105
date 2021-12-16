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


class CachePolicy(Model):
    """CachePolicy.

    :param ttl:
    :type ttl: ~_restclient.models.TimeToLive
    :param high_water_mark:
    :type high_water_mark: int
    :param low_water_mark:
    :type low_water_mark: int
    :param total_capacity_in_gb:
    :type total_capacity_in_gb: long
    :param default_replica_number:
    :type default_replica_number: int
    :param data_management_compute_name:
    :type data_management_compute_name: str
    :param data_hydration_external_resources:
    :type data_hydration_external_resources:
     ~_restclient.models.DataHydrationExternalResources
    """

    _attribute_map = {
        'ttl': {'key': 'ttl', 'type': 'TimeToLive'},
        'high_water_mark': {'key': 'highWaterMark', 'type': 'int'},
        'low_water_mark': {'key': 'lowWaterMark', 'type': 'int'},
        'total_capacity_in_gb': {'key': 'totalCapacityInGb', 'type': 'long'},
        'default_replica_number': {'key': 'defaultReplicaNumber', 'type': 'int'},
        'data_management_compute_name': {'key': 'dataManagementComputeName', 'type': 'str'},
        'data_hydration_external_resources': {'key': 'dataHydrationExternalResources', 'type': 'DataHydrationExternalResources'},
    }

    def __init__(self, ttl=None, high_water_mark=None, low_water_mark=None, total_capacity_in_gb=None, default_replica_number=None, data_management_compute_name=None, data_hydration_external_resources=None):
        super(CachePolicy, self).__init__()
        self.ttl = ttl
        self.high_water_mark = high_water_mark
        self.low_water_mark = low_water_mark
        self.total_capacity_in_gb = total_capacity_in_gb
        self.default_replica_number = default_replica_number
        self.data_management_compute_name = data_management_compute_name
        self.data_hydration_external_resources = data_hydration_external_resources
