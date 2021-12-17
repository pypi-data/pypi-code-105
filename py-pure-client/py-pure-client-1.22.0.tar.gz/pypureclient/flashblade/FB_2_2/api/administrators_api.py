# coding: utf-8

"""
    FlashBlade REST API

    A lightweight client for FlashBlade REST API 2.2, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re

# python 2 and python 3 compatibility library
import six
from typing import List, Optional

from .. import models

class AdministratorsApi(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def api22_admins_api_tokens_delete_with_http_info(
        self,
        admin_ids=None,  # type: List[str]
        admin_names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """DELETE admins/api-tokens

        Deletes the API tokens of the specified administrators.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_api_tokens_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] admin_ids: A comma-separated list of admin IDs. If after filtering, there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with the `admin_names` query parameter.
        :param list[str] admin_names: A comma-separated list of admin names. If there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with `admin_ids` query parameter.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if admin_ids is not None:
            if not isinstance(admin_ids, list):
                admin_ids = [admin_ids]
        if admin_names is not None:
            if not isinstance(admin_names, list):
                admin_names = [admin_names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'admin_ids' in params:
            query_params.append(('admin_ids', params['admin_ids']))
            collection_formats['admin_ids'] = 'csv'
        if 'admin_names' in params:
            query_params.append(('admin_names', params['admin_names']))
            collection_formats['admin_names'] = 'csv'

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
            '/api/2.2/admins/api-tokens', 'DELETE',
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

    def api22_admins_api_tokens_get_with_http_info(
        self,
        admin_ids=None,  # type: List[str]
        admin_names=None,  # type: List[str]
        continuation_token=None,  # type: str
        expose_api_token=None,  # type: bool
        filter=None,  # type: str
        limit=None,  # type: int
        offset=None,  # type: int
        sort=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.AdminApiTokenGetResponse
        """GET admins/api-tokens

        Displays API tokens for the specified administrators.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_api_tokens_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] admin_ids: A comma-separated list of admin IDs. If after filtering, there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with the `admin_names` query parameter.
        :param list[str] admin_names: A comma-separated list of admin names. If there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with `admin_ids` query parameter.
        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool expose_api_token: If `true`, exposes the API token of the current user.
        :param str filter: Exclude resources that don't match the specified criteria.
        :param int limit: Limit the size of the response to the specified number of resources. A `limit` of `0` can be used to get the number of resources without getting all of the resources. It will be returned in the `total_item_count` field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request.
        :param int offset: The offset of the first resource to return from a collection.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). NOTE: If you provide a sort you will not get a `continuation_token` in the response.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: AdminApiTokenGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if admin_ids is not None:
            if not isinstance(admin_ids, list):
                admin_ids = [admin_ids]
        if admin_names is not None:
            if not isinstance(admin_names, list):
                admin_names = [admin_names]
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
            raise ValueError("Invalid value for parameter `limit` when calling `api22_admins_api_tokens_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api22_admins_api_tokens_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'admin_ids' in params:
            query_params.append(('admin_ids', params['admin_ids']))
            collection_formats['admin_ids'] = 'csv'
        if 'admin_names' in params:
            query_params.append(('admin_names', params['admin_names']))
            collection_formats['admin_names'] = 'csv'
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))
        if 'expose_api_token' in params:
            query_params.append(('expose_api_token', params['expose_api_token']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'

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
            '/api/2.2/admins/api-tokens', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AdminApiTokenGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api22_admins_api_tokens_post_with_http_info(
        self,
        admin_ids=None,  # type: List[str]
        admin_names=None,  # type: List[str]
        timeout=None,  # type: int
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.AdminApiTokenResponse
        """POST admins/api-tokens

        Creates API tokens for the specified administrators.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_api_tokens_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] admin_ids: A comma-separated list of admin IDs. If after filtering, there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with the `admin_names` query parameter.
        :param list[str] admin_names: A comma-separated list of admin names. If there is not at least one admin resource that matches each of the elements, then an error is returned. This cannot be provided together with `admin_ids` query parameter.
        :param int timeout: The duration of API token validity, in milliseconds.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: AdminApiTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if admin_ids is not None:
            if not isinstance(admin_ids, list):
                admin_ids = [admin_ids]
        if admin_names is not None:
            if not isinstance(admin_names, list):
                admin_names = [admin_names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'admin_ids' in params:
            query_params.append(('admin_ids', params['admin_ids']))
            collection_formats['admin_ids'] = 'csv'
        if 'admin_names' in params:
            query_params.append(('admin_names', params['admin_names']))
            collection_formats['admin_names'] = 'csv'
        if 'timeout' in params:
            query_params.append(('timeout', params['timeout']))

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
            '/api/2.2/admins/api-tokens', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AdminApiTokenResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api22_admins_cache_delete_with_http_info(
        self,
        ids=None,  # type: List[str]
        names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """DELETE admins/cache

        Delete cached administrator role information by name or ID.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_cache_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

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
            '/api/2.2/admins/cache', 'DELETE',
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

    def api22_admins_cache_get_with_http_info(
        self,
        continuation_token=None,  # type: str
        filter=None,  # type: str
        ids=None,  # type: List[str]
        limit=None,  # type: int
        names=None,  # type: List[str]
        offset=None,  # type: int
        refresh=None,  # type: bool
        sort=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.AdminCacheGetResponse
        """GET admins/cache

        List cached administrator information used to determine role based access control privileges.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_cache_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param str filter: Exclude resources that don't match the specified criteria.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param int limit: Limit the size of the response to the specified number of resources. A `limit` of `0` can be used to get the number of resources without getting all of the resources. It will be returned in the `total_item_count` field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request.
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param int offset: The offset of the first resource to return from a collection.
        :param bool refresh: Whether to refresh the user info from directory service. If not specified, defaults to `false`.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). NOTE: If you provide a sort you will not get a `continuation_token` in the response.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: AdminCacheGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        if names is not None:
            if not isinstance(names, list):
                names = [names]
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
            raise ValueError("Invalid value for parameter `limit` when calling `api22_admins_cache_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api22_admins_cache_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'refresh' in params:
            query_params.append(('refresh', params['refresh']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'

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
            '/api/2.2/admins/cache', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AdminCacheGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api22_admins_get_with_http_info(
        self,
        continuation_token=None,  # type: str
        expose_api_token=None,  # type: bool
        filter=None,  # type: str
        ids=None,  # type: List[str]
        limit=None,  # type: int
        names=None,  # type: List[str]
        offset=None,  # type: int
        sort=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.AdminGetResponse
        """GET admins

        List the administrator's attributes, including the API token and public key.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool expose_api_token: If `true`, exposes the API token of the current user.
        :param str filter: Exclude resources that don't match the specified criteria.
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param int limit: Limit the size of the response to the specified number of resources. A `limit` of `0` can be used to get the number of resources without getting all of the resources. It will be returned in the `total_item_count` field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request.
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param int offset: The offset of the first resource to return from a collection.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). NOTE: If you provide a sort you will not get a `continuation_token` in the response.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: AdminGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        if names is not None:
            if not isinstance(names, list):
                names = [names]
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
            raise ValueError("Invalid value for parameter `limit` when calling `api22_admins_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api22_admins_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))
        if 'expose_api_token' in params:
            query_params.append(('expose_api_token', params['expose_api_token']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'

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
            '/api/2.2/admins', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AdminGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api22_admins_patch_with_http_info(
        self,
        admin=None,  # type: models.AdminPatch
        ids=None,  # type: List[str]
        names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.AdminResponse
        """PATCH admins

        Modify the attributes of the administrator.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api22_admins_patch_with_http_info(admin, async_req=True)
        >>> result = thread.get()

        :param AdminPatch admin: (required)
        :param list[str] ids: A comma-separated list of resource IDs. If after filtering, there is not at least one resource that matches each of the elements of `ids`, then an error is returned. This cannot be provided together with the `name` or `names` query parameters.
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each of the elements of `names`, then an error is returned.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: AdminResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]
        # verify the required parameter 'admin' is set
        if admin is None:
            raise TypeError("Missing the required parameter `admin` when calling `api22_admins_patch`")

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'admin' in params:
            body_params = params['admin']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/2.2/admins', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AdminResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )
