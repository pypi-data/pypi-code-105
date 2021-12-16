# coding: utf-8

"""
    Klaviyo API

    Empowering creators to own their destiny  # noqa: E501

    OpenAPI spec version: 2021.11.26
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class MetricsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.warned = []

    def get_metrics(self, **kwargs):  # noqa: E501
        """Get Metrics Info  # noqa: E501

        Returns a list of all the metrics in your account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metrics(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: For pagination, which page of results to return. Default = 0
        :param int count: For pagination, the number of results to return. Default = 50 ; Max = 100
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_metrics_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_metrics_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_metrics_with_http_info(self, **kwargs):  # noqa: E501
        """Get Metrics Info  # noqa: E501

        Returns a list of all the metrics in your account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metrics_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: For pagination, which page of results to return. Default = 0
        :param int count: For pagination, the number of results to return. Default = 50 ; Max = 100
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['page', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_metrics" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/metrics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse200',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def metric_export(self, metric_id, **kwargs):  # noqa: E501
        """Query Event Data  # noqa: E501

        Exports event data from Klaviyo, optionally filtering and segmenting on available event properties. To ensure a correct response, enter parameters in the curl request as they are ordered below:  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metric_export(metric_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str metric_id: (required)
        :param str start_date:  Beginning of timeframe to pull event data for. The default value is 1 month ago. Can also accept a 10-digit UNIX timestamp. When sending a `start_date`, you must also send an `end_date`  Ex: `1610524800` OR `2021-01-13` 
        :param str end_date:  End of timeframe to pull event data for. The default is the current day, or 1 month from start_date, whichever is sooner. Can also accept a 10-digit UNIX timestamp. When sending an `end_date`, you must also send a `start_date`. Must be *at most* 31 days after `start_date`  Ex: `1612080000` OR `2021-01-31` 
        :param str unit: Granularity to bucket data points into - one of `day`, `week`, or `month`. Defaults to `day`.
        :param str measurement:  Type of metric to fetch - one of `unique`, `count`, `value`, or `sum`. Defaults to `count`. For `sum` a property name to operate on must be supplied as a JSON-encoded list like `[\"sum\",\"ItemCount\"]` 
        :param str where: Optional, JSON-encoded list. Conditions to use to filter the set of events. A max of 1 condition can be given. `where` and `by` parameters cannot be specified at the same time.  ex: `[[\"$attributed_flow\",\"=\",\"FLOW_ID\"]]` 
        :param str by: The name of a property to segment the event data on. `where` and `by` parameters cannot be specified at the same time. Cannot be used alongside `where` parameter.
        :param int count: Maximum number of segments to return. Default = 25, **MAX = 1000**
        :return: MetricExport
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.metric_export_with_http_info(metric_id, **kwargs)  # noqa: E501
        else:
            (data) = self.metric_export_with_http_info(metric_id, **kwargs)  # noqa: E501
            return data

    def metric_export_with_http_info(self, metric_id, **kwargs):  # noqa: E501
        """Query Event Data  # noqa: E501

        Exports event data from Klaviyo, optionally filtering and segmenting on available event properties. To ensure a correct response, enter parameters in the curl request as they are ordered below:  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metric_export_with_http_info(metric_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str metric_id: (required)
        :param str start_date:  Beginning of timeframe to pull event data for. The default value is 1 month ago. Can also accept a 10-digit UNIX timestamp. When sending a `start_date`, you must also send an `end_date`  Ex: `1610524800` OR `2021-01-13` 
        :param str end_date:  End of timeframe to pull event data for. The default is the current day, or 1 month from start_date, whichever is sooner. Can also accept a 10-digit UNIX timestamp. When sending an `end_date`, you must also send a `start_date`. Must be *at most* 31 days after `start_date`  Ex: `1612080000` OR `2021-01-31` 
        :param str unit: Granularity to bucket data points into - one of `day`, `week`, or `month`. Defaults to `day`.
        :param str measurement:  Type of metric to fetch - one of `unique`, `count`, `value`, or `sum`. Defaults to `count`. For `sum` a property name to operate on must be supplied as a JSON-encoded list like `[\"sum\",\"ItemCount\"]` 
        :param str where: Optional, JSON-encoded list. Conditions to use to filter the set of events. A max of 1 condition can be given. `where` and `by` parameters cannot be specified at the same time.  ex: `[[\"$attributed_flow\",\"=\",\"FLOW_ID\"]]` 
        :param str by: The name of a property to segment the event data on. `where` and `by` parameters cannot be specified at the same time. Cannot be used alongside `where` parameter.
        :param int count: Maximum number of segments to return. Default = 25, **MAX = 1000**
        :return: MetricExport
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['metric_id', 'start_date', 'end_date', 'unit', 'measurement', 'where', 'by', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method metric_export" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'metric_id' is set
        if ('metric_id' not in params or
                params['metric_id'] is None):
            raise ValueError("Missing the required parameter `metric_id` when calling `metric_export`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'metric_id' in params:
            path_params['metric_id'] = params['metric_id']  # noqa: E501

        query_params = []
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501
        if 'unit' in params:
            query_params.append(('unit', params['unit']))  # noqa: E501
        if 'measurement' in params:
            query_params.append(('measurement', params['measurement']))  # noqa: E501
        if 'where' in params:
            query_params.append(('where', params['where']))  # noqa: E501
        if 'by' in params:
            query_params.append(('by', params['by']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/metric/{metric_id}/export', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MetricExport',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def metric_timeline(self, metric_id, **kwargs):  # noqa: E501
        """Get Events for a Specific Metric  # noqa: E501

        Returns a batched timeline for one specific metric.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metric_timeline(metric_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str metric_id: (required)
        :param str since: Either a 10-digit Unix timestamp (UTC) to use as starting datetime, OR a pagination token obtained from the `next` attribute of a prior API call. For backwards compatibility, UUIDs will continue to be supported for a limited time. Defaults to current time.
        :param int count: Number of events to return in a batch. Max = 100
        :param str sort: Sort order to apply to timeline, either descending or ascending. Valid values are `desc` or `asc`. Defaults to `desc`. Always descending when `since` is not sent, as `since` defaults to current time.
        :return: MetricTimeline
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.metric_timeline_with_http_info(metric_id, **kwargs)  # noqa: E501
        else:
            (data) = self.metric_timeline_with_http_info(metric_id, **kwargs)  # noqa: E501
            return data

    def metric_timeline_with_http_info(self, metric_id, **kwargs):  # noqa: E501
        """Get Events for a Specific Metric  # noqa: E501

        Returns a batched timeline for one specific metric.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metric_timeline_with_http_info(metric_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str metric_id: (required)
        :param str since: Either a 10-digit Unix timestamp (UTC) to use as starting datetime, OR a pagination token obtained from the `next` attribute of a prior API call. For backwards compatibility, UUIDs will continue to be supported for a limited time. Defaults to current time.
        :param int count: Number of events to return in a batch. Max = 100
        :param str sort: Sort order to apply to timeline, either descending or ascending. Valid values are `desc` or `asc`. Defaults to `desc`. Always descending when `since` is not sent, as `since` defaults to current time.
        :return: MetricTimeline
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['metric_id', 'since', 'count', 'sort']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method metric_timeline" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'metric_id' is set
        if ('metric_id' not in params or
                params['metric_id'] is None):
            raise ValueError("Missing the required parameter `metric_id` when calling `metric_timeline`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'metric_id' in params:
            path_params['metric_id'] = params['metric_id']  # noqa: E501

        query_params = []
        if 'since' in params:
            query_params.append(('since', params['since']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/metric/{metric_id}/timeline', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MetricTimeline',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def metrics_timeline(self, **kwargs):  # noqa: E501
        """Get Events for All Metrics  # noqa: E501

        Returns a batched timeline of all events in your account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics_timeline(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str since: Either a 10-digit Unix timestamp (UTC) to use as starting datetime, OR a pagination token obtained from the next attribute of a prior API call. For backwards compatibility, UUIDs will continue to be supported for a limited time. Defaults to current time.
        :param int count: Number of events to return in a batch. Default = 50, Max = 100
        :param str sort: Sort order to apply to timeline, either descending or ascending. Valid values are `desc` or `asc`. Defaults to `desc`. Always descending when `since` is not sent, as `since` defaults to current time.
        :return: MetricTimeline
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.metrics_timeline_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.metrics_timeline_with_http_info(**kwargs)  # noqa: E501
            return data

    def metrics_timeline_with_http_info(self, **kwargs):  # noqa: E501
        """Get Events for All Metrics  # noqa: E501

        Returns a batched timeline of all events in your account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics_timeline_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str since: Either a 10-digit Unix timestamp (UTC) to use as starting datetime, OR a pagination token obtained from the next attribute of a prior API call. For backwards compatibility, UUIDs will continue to be supported for a limited time. Defaults to current time.
        :param int count: Number of events to return in a batch. Default = 50, Max = 100
        :param str sort: Sort order to apply to timeline, either descending or ascending. Valid values are `desc` or `asc`. Defaults to `desc`. Always descending when `since` is not sent, as `since` defaults to current time.
        :return: MetricTimeline
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['since', 'count', 'sort']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method metrics_timeline" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'since' in params:
            query_params.append(('since', params['since']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/metrics/timeline', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MetricTimeline',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
