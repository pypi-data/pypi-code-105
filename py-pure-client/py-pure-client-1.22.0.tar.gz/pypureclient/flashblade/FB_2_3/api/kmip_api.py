# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.3, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re

# python 2 and python 3 compatibility library
import six
from typing import List, Optional

from .. import models

class KMIPApi(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def api23_kmip_delete_with_http_info(
        self,
        names=None,  # type: List[str]
        ids=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Delete a KMIP server configuration

        Deletes a KMIP server configuration. A server can only be deleted when not in use by the array.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api23_kmip_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.3/kmip', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api23_kmip_get_with_http_info(
        self,
        names=None,  # type: List[str]
        ids=None,  # type: List[str]
        filter=None,  # type: str
        limit=None,  # type: int
        offset=None,  # type: int
        sort=None,  # type: List[str]
        continuation_token=None,  # type: str
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.KmipServerResponse
        """List KMIP server configurations

        Displays a list of KMIP server configurations.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api23_kmip_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param str filter: Exclude resources that don't match the specified criteria.
        :param int limit: Limit the size of the response to the specified number of resources. A `limit` of `0` can be used to get the number of resources without getting all of the resources. It will be returned in the `total_item_count` field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request.
        :param int offset: The offset of the first resource to return from a collection.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). NOTE: If you provide a sort you will not get a `continuation_token` in the response.
        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: KmipServerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        if 'limit' in params and params['limit'] < 1:
            raise ValueError("Invalid value for parameter `limit` when calling `api23_kmip_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api23_kmip_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.3/kmip', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='KmipServerResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api23_kmip_patch_with_http_info(
        self,
        kmip_server=None,  # type: models.KmipServer
        names=None,  # type: List[str]
        ids=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.KmipServerResponse
        """Modify a KMIP server configuration

        Modifies KMIP server properties - URI, certificate, certificate group.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api23_kmip_patch_with_http_info(kmip_server, async_req=True)
        >>> result = thread.get()

        :param KmipServer kmip_server: (required)
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: KmipServerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]
        # verify the required parameter 'kmip_server' is set
        if kmip_server is None:
            raise TypeError("Missing the required parameter `kmip_server` when calling `api23_kmip_patch`")

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'kmip_server' in params:
            body_params = params['kmip_server']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.3/kmip', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='KmipServerResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api23_kmip_post_with_http_info(
        self,
        kmip_server=None,  # type: models.KmipServer
        names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.KmipServerResponse
        """Create a KMIP server configuration

        Creates a KMIP server configuration.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api23_kmip_post_with_http_info(kmip_server, async_req=True)
        >>> result = thread.get()

        :param KmipServer kmip_server: (required)
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: KmipServerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]
        # verify the required parameter 'kmip_server' is set
        if kmip_server is None:
            raise TypeError("Missing the required parameter `kmip_server` when calling `api23_kmip_post`")

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'kmip_server' in params:
            body_params = params['kmip_server']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.3/kmip', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='KmipServerResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api23_kmip_test_get_with_http_info(
        self,
        names=None,  # type: List[str]
        ids=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.TestResultResponse
        """Displays KMIP server test results

        Displays a detailed result of of KMIP server test.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api23_kmip_test_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: TestResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.3/kmip/test', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TestResultResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )
