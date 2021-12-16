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


class CreateDatacacheStoreRequest(Model):
    """CreateDatacacheStoreRequest.

    :param datacache_store_name:
    :type datacache_store_name: str
    :param datastore_names:
    :type datastore_names: list[str]
    :param datacache_store_policy:
    :type datacache_store_policy:
     ~_restclient.models.DatacacheStorePolicyInput
    """

    _attribute_map = {
        'datacache_store_name': {'key': 'datacacheStoreName', 'type': 'str'},
        'datastore_names': {'key': 'datastoreNames', 'type': '[str]'},
        'datacache_store_policy': {'key': 'datacacheStorePolicy', 'type': 'DatacacheStorePolicyInput'},
    }

    def __init__(self, datacache_store_name=None, datastore_names=None, datacache_store_policy=None):
        super(CreateDatacacheStoreRequest, self).__init__()
        self.datacache_store_name = datacache_store_name
        self.datastore_names = datastore_names
        self.datacache_store_policy = datacache_store_policy
