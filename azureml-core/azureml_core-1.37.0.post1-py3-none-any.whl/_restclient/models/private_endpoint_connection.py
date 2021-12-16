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


class PrivateEndpointConnection(Model):
    """The Private Endpoint Connection resource.

    :param private_endpoint: The resource of private end point.
    :type private_endpoint: ~_restclient.models.PrivateEndpoint
    :param private_link_service_connection_state: A collection of information
     about the state of the connection between service consumer and provider.
    :type private_link_service_connection_state:
     ~_restclient.models.PrivateLinkServiceConnectionState
    :param provisioning_state: The provisioning state of the private endpoint
     connection resource. Possible values include: 'Succeeded', 'Creating',
     'Deleting', 'Failed'
    :type provisioning_state: str or
     ~_restclient.models.PrivateEndpointConnectionProvisioningState
    """

    _validation = {
        'private_link_service_connection_state': {'required': True},
    }

    _attribute_map = {
        'private_endpoint': {'key': 'properties.privateEndpoint', 'type': 'PrivateEndpoint'},
        'private_link_service_connection_state': {'key': 'properties.privateLinkServiceConnectionState', 'type': 'PrivateLinkServiceConnectionState'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
    }

    def __init__(self, private_link_service_connection_state, private_endpoint=None, provisioning_state=None):
        super(PrivateEndpointConnection, self).__init__()
        self.private_endpoint = private_endpoint
        self.private_link_service_connection_state = private_link_service_connection_state
        self.provisioning_state = provisioning_state
