# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.7
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re

# python 2 and python 3 compatibility library
import six
from typing import List, Optional

from .. import models

class RemoteProtectionGroupSnapshotsApi(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def api27_remote_protection_group_snapshots_delete_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        names=None,  # type: List[str]
        on=None,  # type: str
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> None
        """Delete a remote protection group snapshot

        Deletes a remote protection group snapshot that has been destroyed and is pending eradication. Eradicated remote protection group snapshots cannot be recovered. Remote protection group snapshots are destroyed using the `PATCH` method. The `names` parameter represents the name of the protection group snapshot. The `on` parameter represents the name of the offload target. The `names` and `on` parameters are required and must be used together.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api27_remote_protection_group_snapshots_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`, `/login`, and `/logout`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param list[str] names: Performs the operation on the unique name specified. Enter multiple names in comma-separated format. For example, `name01,name02`.
        :param str on: Performs the operation on the target name specified. For example, `targetName01`.
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
        if 'on' in params:
            query_params.append(('on', params['on']))

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

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
        auth_settings = []

        return self.api_client.call_api(
            '/api/2.7/remote-protection-group-snapshots', 'DELETE',
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

    def api27_remote_protection_group_snapshots_get_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        destroyed=None,  # type: bool
        filter=None,  # type: str
        limit=None,  # type: int
        names=None,  # type: List[str]
        offset=None,  # type: int
        on=None,  # type: List[str]
        sort=None,  # type: List[str]
        source_names=None,  # type: List[str]
        total_item_count=None,  # type: bool
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.RemoteProtectionGroupSnapshotGetResponse
        """List remote protection group snapshots

        Displays a list of remote protection group snapshots.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api27_remote_protection_group_snapshots_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`, `/login`, and `/logout`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param bool destroyed: If set to `true`, lists only destroyed objects that are in the eradication pending state. If set to `false`, lists only objects that are not destroyed. For destroyed objects, the time remaining is displayed in milliseconds.
        :param str filter: Narrows down the results to only the response objects that satisfy the filter criteria.
        :param int limit: Limits the size of the response to the specified number of objects on each page. To return the total number of resources, set `limit=0`. The total number of resources is returned as a `total_item_count` value. If the page size requested is larger than the system maximum limit, the server returns the maximum limit, disregarding the requested page size.
        :param list[str] names: Performs the operation on the unique name specified. Enter multiple names in comma-separated format. For example, `name01,name02`.
        :param int offset: The starting position based on the results of the query in relation to the full set of response objects returned.
        :param list[str] on: Performs the operation on the target name specified. Enter multiple target names in comma-separated format. For example, `targetName01,targetName02`.
        :param list[str] sort: Returns the response objects in the order specified. Set `sort` to the name in the response by which to sort. Sorting can be performed on any of the names in the response, and the objects can be sorted in ascending or descending order. By default, the response objects are sorted in ascending order. To sort in descending order, append the minus sign (`-`) to the name. A single request can be sorted on multiple objects. For example, you can sort all volumes from largest to smallest volume size, and then sort volumes of the same size in ascending order by volume name. To sort on multiple names, list the names as comma-separated values.
        :param list[str] source_names: Performs the operation on the source name specified. Enter multiple source names in comma-separated format. For example, `name01,name02`.
        :param bool total_item_count: If set to `true`, the `total_item_count` matching the specified query parameters is calculated and returned in the response. If set to `false`, the `total_item_count` is `null` in the response. This may speed up queries where the `total_item_count` is large. If not specified, defaults to `false`.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: RemoteProtectionGroupSnapshotGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if on is not None:
            if not isinstance(on, list):
                on = [on]
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
        if source_names is not None:
            if not isinstance(source_names, list):
                source_names = [source_names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        if 'limit' in params and params['limit'] < 1:
            raise ValueError("Invalid value for parameter `limit` when calling `api27_remote_protection_group_snapshots_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api27_remote_protection_group_snapshots_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'destroyed' in params:
            query_params.append(('destroyed', params['destroyed']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'on' in params:
            query_params.append(('on', params['on']))
            collection_formats['on'] = 'csv'
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'
        if 'source_names' in params:
            query_params.append(('source_names', params['source_names']))
            collection_formats['source_names'] = 'csv'
        if 'total_item_count' in params:
            query_params.append(('total_item_count', params['total_item_count']))

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

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
        auth_settings = []

        return self.api_client.call_api(
            '/api/2.7/remote-protection-group-snapshots', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemoteProtectionGroupSnapshotGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api27_remote_protection_group_snapshots_patch_with_http_info(
        self,
        remote_protection_group_snapshot=None,  # type: models.DestroyedPatchPost
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        names=None,  # type: List[str]
        on=None,  # type: str
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.RemoteProtectionGroupSnapshotResponse
        """Modify a remote protection group snapshot

        Modifies a remote protection group snapshot, removing it from the offload target and destroying the snapshot. The `on` parameter represents the name of the offload target. The `ids` or `names` parameter and the `on` parameter are required and must be used together.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api27_remote_protection_group_snapshots_patch_with_http_info(remote_protection_group_snapshot, async_req=True)
        >>> result = thread.get()

        :param DestroyedPatchPost remote_protection_group_snapshot: (required)
        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`, `/login`, and `/logout`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param list[str] names: Performs the operation on the unique name specified. Enter multiple names in comma-separated format. For example, `name01,name02`.
        :param str on: Performs the operation on the target name specified. For example, `targetName01`.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: RemoteProtectionGroupSnapshotResponse
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
        # verify the required parameter 'remote_protection_group_snapshot' is set
        if remote_protection_group_snapshot is None:
            raise TypeError("Missing the required parameter `remote_protection_group_snapshot` when calling `api27_remote_protection_group_snapshots_patch`")

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'on' in params:
            query_params.append(('on', params['on']))

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

        form_params = []
        local_var_files = {}

        body_params = None
        if 'remote_protection_group_snapshot' in params:
            body_params = params['remote_protection_group_snapshot']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(
            '/api/2.7/remote-protection-group-snapshots', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemoteProtectionGroupSnapshotResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api27_remote_protection_group_snapshots_post_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        apply_retention=None,  # type: bool
        convert_source_to_baseline=None,  # type: bool
        for_replication=None,  # type: bool
        names=None,  # type: List[str]
        replicate=None,  # type: bool
        replicate_now=None,  # type: bool
        source_names=None,  # type: List[str]
        on=None,  # type: str
        remote_protection_group_snapshot=None,  # type: models.RemoteProtectionGroupSnapshotPost
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.RemoteProtectionGroupSnapshotResponse
        """Create remote protection group snapshot

        Creates remote protection group snapshots.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api27_remote_protection_group_snapshots_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`, `/login`, and `/logout`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param bool apply_retention: If `true`, applies the local and remote retention policy to the snapshots.
        :param bool convert_source_to_baseline: Set to `true` to have the snapshot be eradicated when it is no longer baseline on source.
        :param bool for_replication: If `true`, destroys and eradicates the snapshot after 1 hour.
        :param list[str] names: Performs the operation on the unique name specified. Enter multiple names in comma-separated format. For example, `name01,name02`.
        :param bool replicate: If set to `true`, queues up and begins replicating to each allowed target after all earlier replication sessions for the same protection group have been completed to that target. The `replicate` and `replicate_now` parameters cannot be used together.
        :param bool replicate_now: If set to `true`, replicates the snapshots to each allowed target. The `replicate` and `replicate_now` parameters cannot be used together.
        :param list[str] source_names: Performs the operation on the source name specified. Enter multiple source names in comma-separated format. For example, `name01,name02`.
        :param str on: Performs the operation on the target name specified. For example, `targetName01`.
        :param RemoteProtectionGroupSnapshotPost remote_protection_group_snapshot:
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: RemoteProtectionGroupSnapshotResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        if source_names is not None:
            if not isinstance(source_names, list):
                source_names = [source_names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        collection_formats = {}
        path_params = {}

        query_params = []
        if 'apply_retention' in params:
            query_params.append(('apply_retention', params['apply_retention']))
        if 'convert_source_to_baseline' in params:
            query_params.append(('convert_source_to_baseline', params['convert_source_to_baseline']))
        if 'for_replication' in params:
            query_params.append(('for_replication', params['for_replication']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'replicate' in params:
            query_params.append(('replicate', params['replicate']))
        if 'replicate_now' in params:
            query_params.append(('replicate_now', params['replicate_now']))
        if 'source_names' in params:
            query_params.append(('source_names', params['source_names']))
            collection_formats['source_names'] = 'csv'
        if 'on' in params:
            query_params.append(('on', params['on']))

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

        form_params = []
        local_var_files = {}

        body_params = None
        if 'remote_protection_group_snapshot' in params:
            body_params = params['remote_protection_group_snapshot']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(
            '/api/2.7/remote-protection-group-snapshots', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemoteProtectionGroupSnapshotResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api27_remote_protection_group_snapshots_transfer_get_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        destroyed=None,  # type: bool
        filter=None,  # type: str
        limit=None,  # type: int
        offset=None,  # type: int
        on=None,  # type: List[str]
        sort=None,  # type: List[str]
        source_names=None,  # type: List[str]
        total_item_count=None,  # type: bool
        total_only=None,  # type: bool
        names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.RemoteProtectionGroupSnapshotTransferGetResponse
        """List remote protection groups with transfer statistics

        Returns a list of remote protection groups and their transfer statistics.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api27_remote_protection_group_snapshots_transfer_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`, `/login`, and `/logout`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param bool destroyed: If set to `true`, lists only destroyed objects that are in the eradication pending state. If set to `false`, lists only objects that are not destroyed. For destroyed objects, the time remaining is displayed in milliseconds.
        :param str filter: Narrows down the results to only the response objects that satisfy the filter criteria.
        :param int limit: Limits the size of the response to the specified number of objects on each page. To return the total number of resources, set `limit=0`. The total number of resources is returned as a `total_item_count` value. If the page size requested is larger than the system maximum limit, the server returns the maximum limit, disregarding the requested page size.
        :param int offset: The starting position based on the results of the query in relation to the full set of response objects returned.
        :param list[str] on: Performs the operation on the target name specified. Enter multiple target names in comma-separated format. For example, `targetName01,targetName02`.
        :param list[str] sort: Returns the response objects in the order specified. Set `sort` to the name in the response by which to sort. Sorting can be performed on any of the names in the response, and the objects can be sorted in ascending or descending order. By default, the response objects are sorted in ascending order. To sort in descending order, append the minus sign (`-`) to the name. A single request can be sorted on multiple objects. For example, you can sort all volumes from largest to smallest volume size, and then sort volumes of the same size in ascending order by volume name. To sort on multiple names, list the names as comma-separated values.
        :param list[str] source_names: Performs the operation on the source name specified. Enter multiple source names in comma-separated format. For example, `name01,name02`.
        :param bool total_item_count: If set to `true`, the `total_item_count` matching the specified query parameters is calculated and returned in the response. If set to `false`, the `total_item_count` is `null` in the response. This may speed up queries where the `total_item_count` is large. If not specified, defaults to `false`.
        :param bool total_only: If set to `true`, returns the aggregate value of all items after filtering. Where it makes more sense, the average value is displayed instead. The values are displayed for each name where meaningful. If `total_only=true`, the `items` list will be empty.
        :param list[str] names: Performs the operation on the unique name specified. Enter multiple names in comma-separated format. For example, `name01,name02`.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: RemoteProtectionGroupSnapshotTransferGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        if on is not None:
            if not isinstance(on, list):
                on = [on]
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
        if source_names is not None:
            if not isinstance(source_names, list):
                source_names = [source_names]
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        if 'limit' in params and params['limit'] < 1:
            raise ValueError("Invalid value for parameter `limit` when calling `api27_remote_protection_group_snapshots_transfer_get`, must be a value greater than or equal to `1`")
        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api27_remote_protection_group_snapshots_transfer_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'destroyed' in params:
            query_params.append(('destroyed', params['destroyed']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'on' in params:
            query_params.append(('on', params['on']))
            collection_formats['on'] = 'csv'
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'
        if 'source_names' in params:
            query_params.append(('source_names', params['source_names']))
            collection_formats['source_names'] = 'csv'
        if 'total_item_count' in params:
            query_params.append(('total_item_count', params['total_item_count']))
        if 'total_only' in params:
            query_params.append(('total_only', params['total_only']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

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
        auth_settings = []

        return self.api_client.call_api(
            '/api/2.7/remote-protection-group-snapshots/transfer', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemoteProtectionGroupSnapshotTransferGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )
