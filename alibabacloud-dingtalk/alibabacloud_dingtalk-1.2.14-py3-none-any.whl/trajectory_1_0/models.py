# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List


class QueryAppActiveUsersHeaders(TeaModel):
    def __init__(
        self,
        common_headers: Dict[str, str] = None,
        x_acs_dingtalk_access_token: str = None,
    ):
        self.common_headers = common_headers
        self.x_acs_dingtalk_access_token = x_acs_dingtalk_access_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.common_headers is not None:
            result['commonHeaders'] = self.common_headers
        if self.x_acs_dingtalk_access_token is not None:
            result['x-acs-dingtalk-access-token'] = self.x_acs_dingtalk_access_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('commonHeaders') is not None:
            self.common_headers = m.get('commonHeaders')
        if m.get('x-acs-dingtalk-access-token') is not None:
            self.x_acs_dingtalk_access_token = m.get('x-acs-dingtalk-access-token')
        return self


class QueryAppActiveUsersRequest(TeaModel):
    def __init__(
        self,
        need_position_info: bool = None,
        next_token: int = None,
        max_results: int = None,
    ):
        # 是否需要返回位置信息
        self.need_position_info = need_position_info
        # 标记当前开始读取的位置，置空表示从头开始
        self.next_token = next_token
        # 本次读取的最大数据记录数量
        self.max_results = max_results

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.need_position_info is not None:
            result['needPositionInfo'] = self.need_position_info
        if self.next_token is not None:
            result['nextToken'] = self.next_token
        if self.max_results is not None:
            result['maxResults'] = self.max_results
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('needPositionInfo') is not None:
            self.need_position_info = m.get('needPositionInfo')
        if m.get('nextToken') is not None:
            self.next_token = m.get('nextToken')
        if m.get('maxResults') is not None:
            self.max_results = m.get('maxResults')
        return self


class QueryAppActiveUsersResponseBodyList(TeaModel):
    def __init__(
        self,
        start_time: int = None,
        app_trace_id: str = None,
        longitude: float = None,
        latitude: float = None,
        report_time: int = None,
        user_id: str = None,
    ):
        # 轨迹采集开启时间
        self.start_time = start_time
        # 应用轨迹ID
        self.app_trace_id = app_trace_id
        # 经度
        self.longitude = longitude
        # 纬度
        self.latitude = latitude
        # 该位置采集时间
        self.report_time = report_time
        # 员工Id
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.app_trace_id is not None:
            result['appTraceId'] = self.app_trace_id
        if self.longitude is not None:
            result['longitude'] = self.longitude
        if self.latitude is not None:
            result['latitude'] = self.latitude
        if self.report_time is not None:
            result['reportTime'] = self.report_time
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('appTraceId') is not None:
            self.app_trace_id = m.get('appTraceId')
        if m.get('longitude') is not None:
            self.longitude = m.get('longitude')
        if m.get('latitude') is not None:
            self.latitude = m.get('latitude')
        if m.get('reportTime') is not None:
            self.report_time = m.get('reportTime')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class QueryAppActiveUsersResponseBody(TeaModel):
    def __init__(
        self,
        has_more: bool = None,
        total_count: int = None,
        list: List[QueryAppActiveUsersResponseBodyList] = None,
        next_token: int = None,
    ):
        # 是否存在更多数据需要获取
        self.has_more = has_more
        # 总数
        self.total_count = total_count
        # 数据集合
        self.list = list
        # 下一次获取开始位置
        self.next_token = next_token

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.has_more is not None:
            result['hasMore'] = self.has_more
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        result['list'] = []
        if self.list is not None:
            for k in self.list:
                result['list'].append(k.to_map() if k else None)
        if self.next_token is not None:
            result['nextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('hasMore') is not None:
            self.has_more = m.get('hasMore')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        self.list = []
        if m.get('list') is not None:
            for k in m.get('list'):
                temp_model = QueryAppActiveUsersResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('nextToken') is not None:
            self.next_token = m.get('nextToken')
        return self


class QueryAppActiveUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: QueryAppActiveUsersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = QueryAppActiveUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class QueryCollectingTraceTaskHeaders(TeaModel):
    def __init__(
        self,
        common_headers: Dict[str, str] = None,
        x_acs_dingtalk_access_token: str = None,
    ):
        self.common_headers = common_headers
        self.x_acs_dingtalk_access_token = x_acs_dingtalk_access_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.common_headers is not None:
            result['commonHeaders'] = self.common_headers
        if self.x_acs_dingtalk_access_token is not None:
            result['x-acs-dingtalk-access-token'] = self.x_acs_dingtalk_access_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('commonHeaders') is not None:
            self.common_headers = m.get('commonHeaders')
        if m.get('x-acs-dingtalk-access-token') is not None:
            self.x_acs_dingtalk_access_token = m.get('x-acs-dingtalk-access-token')
        return self


class QueryCollectingTraceTaskRequest(TeaModel):
    def __init__(
        self,
        user_ids: List[str] = None,
        ding_isv_org_id: int = None,
        ding_token_grant_type: int = None,
        ding_client_id: str = None,
        ding_org_id: int = None,
        ding_oauth_app_id: int = None,
    ):
        # 员工用户ID列表
        self.user_ids = user_ids
        # isvOrgId
        self.ding_isv_org_id = ding_isv_org_id
        # tokenGrantType
        self.ding_token_grant_type = ding_token_grant_type
        # appKey
        self.ding_client_id = ding_client_id
        # orgId
        self.ding_org_id = ding_org_id
        # oauthAppId
        self.ding_oauth_app_id = ding_oauth_app_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.user_ids is not None:
            result['userIds'] = self.user_ids
        if self.ding_isv_org_id is not None:
            result['dingIsvOrgId'] = self.ding_isv_org_id
        if self.ding_token_grant_type is not None:
            result['dingTokenGrantType'] = self.ding_token_grant_type
        if self.ding_client_id is not None:
            result['dingClientId'] = self.ding_client_id
        if self.ding_org_id is not None:
            result['dingOrgId'] = self.ding_org_id
        if self.ding_oauth_app_id is not None:
            result['dingOauthAppId'] = self.ding_oauth_app_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('userIds') is not None:
            self.user_ids = m.get('userIds')
        if m.get('dingIsvOrgId') is not None:
            self.ding_isv_org_id = m.get('dingIsvOrgId')
        if m.get('dingTokenGrantType') is not None:
            self.ding_token_grant_type = m.get('dingTokenGrantType')
        if m.get('dingClientId') is not None:
            self.ding_client_id = m.get('dingClientId')
        if m.get('dingOrgId') is not None:
            self.ding_org_id = m.get('dingOrgId')
        if m.get('dingOauthAppId') is not None:
            self.ding_oauth_app_id = m.get('dingOauthAppId')
        return self


class QueryCollectingTraceTaskResponseBodyList(TeaModel):
    def __init__(
        self,
        app_trace_id: str = None,
        user_id: str = None,
        geo_report_status: int = None,
        geo_report_period: int = None,
        geo_collect_period: int = None,
        report_start_time: int = None,
        report_end_time: int = None,
    ):
        # 应用轨迹ID
        self.app_trace_id = app_trace_id
        # 组织下员工Id
        self.user_id = user_id
        self.geo_report_status = geo_report_status
        self.geo_report_period = geo_report_period
        self.geo_collect_period = geo_collect_period
        self.report_start_time = report_start_time
        self.report_end_time = report_end_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_trace_id is not None:
            result['appTraceId'] = self.app_trace_id
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.geo_report_status is not None:
            result['geoReportStatus'] = self.geo_report_status
        if self.geo_report_period is not None:
            result['geoReportPeriod'] = self.geo_report_period
        if self.geo_collect_period is not None:
            result['geoCollectPeriod'] = self.geo_collect_period
        if self.report_start_time is not None:
            result['reportStartTime'] = self.report_start_time
        if self.report_end_time is not None:
            result['reportEndTime'] = self.report_end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('appTraceId') is not None:
            self.app_trace_id = m.get('appTraceId')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('geoReportStatus') is not None:
            self.geo_report_status = m.get('geoReportStatus')
        if m.get('geoReportPeriod') is not None:
            self.geo_report_period = m.get('geoReportPeriod')
        if m.get('geoCollectPeriod') is not None:
            self.geo_collect_period = m.get('geoCollectPeriod')
        if m.get('reportStartTime') is not None:
            self.report_start_time = m.get('reportStartTime')
        if m.get('reportEndTime') is not None:
            self.report_end_time = m.get('reportEndTime')
        return self


class QueryCollectingTraceTaskResponseBody(TeaModel):
    def __init__(
        self,
        list: List[QueryCollectingTraceTaskResponseBodyList] = None,
    ):
        # result
        self.list = list

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['list'] = []
        if self.list is not None:
            for k in self.list:
                result['list'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('list') is not None:
            for k in m.get('list'):
                temp_model = QueryCollectingTraceTaskResponseBodyList()
                self.list.append(temp_model.from_map(k))
        return self


class QueryCollectingTraceTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: QueryCollectingTraceTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = QueryCollectingTraceTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class QueryPageTraceDataHeaders(TeaModel):
    def __init__(
        self,
        common_headers: Dict[str, str] = None,
        x_acs_dingtalk_access_token: str = None,
    ):
        self.common_headers = common_headers
        self.x_acs_dingtalk_access_token = x_acs_dingtalk_access_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.common_headers is not None:
            result['commonHeaders'] = self.common_headers
        if self.x_acs_dingtalk_access_token is not None:
            result['x-acs-dingtalk-access-token'] = self.x_acs_dingtalk_access_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('commonHeaders') is not None:
            self.common_headers = m.get('commonHeaders')
        if m.get('x-acs-dingtalk-access-token') is not None:
            self.x_acs_dingtalk_access_token = m.get('x-acs-dingtalk-access-token')
        return self


class QueryPageTraceDataRequest(TeaModel):
    def __init__(
        self,
        trace_id: str = None,
        next_token: int = None,
        max_results: int = None,
        start_time: int = None,
        end_time: int = None,
        staff_id: str = None,
    ):
        # traceId
        self.trace_id = trace_id
        # 起始位置
        self.next_token = next_token
        # 查询数量
        self.max_results = max_results
        # 开始时间
        self.start_time = start_time
        # 终止时间
        self.end_time = end_time
        # 员工ID
        self.staff_id = staff_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.trace_id is not None:
            result['traceId'] = self.trace_id
        if self.next_token is not None:
            result['nextToken'] = self.next_token
        if self.max_results is not None:
            result['maxResults'] = self.max_results
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.staff_id is not None:
            result['staffId'] = self.staff_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('traceId') is not None:
            self.trace_id = m.get('traceId')
        if m.get('nextToken') is not None:
            self.next_token = m.get('nextToken')
        if m.get('maxResults') is not None:
            self.max_results = m.get('maxResults')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('staffId') is not None:
            self.staff_id = m.get('staffId')
        return self


class QueryPageTraceDataResponseBodyListCoordinates(TeaModel):
    def __init__(
        self,
        longitude: float = None,
        latitude: float = None,
    ):
        # 经度
        self.longitude = longitude
        # 纬度
        self.latitude = latitude

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.longitude is not None:
            result['longitude'] = self.longitude
        if self.latitude is not None:
            result['latitude'] = self.latitude
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('longitude') is not None:
            self.longitude = m.get('longitude')
        if m.get('latitude') is not None:
            self.latitude = m.get('latitude')
        return self


class QueryPageTraceDataResponseBodyList(TeaModel):
    def __init__(
        self,
        coordinates: QueryPageTraceDataResponseBodyListCoordinates = None,
        gmt_location: int = None,
        gmt_upload: int = None,
    ):
        # 经纬度
        self.coordinates = coordinates
        # 定位时间
        self.gmt_location = gmt_location
        # 上报时间
        self.gmt_upload = gmt_upload

    def validate(self):
        if self.coordinates:
            self.coordinates.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.coordinates is not None:
            result['coordinates'] = self.coordinates.to_map()
        if self.gmt_location is not None:
            result['gmtLocation'] = self.gmt_location
        if self.gmt_upload is not None:
            result['gmtUpload'] = self.gmt_upload
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('coordinates') is not None:
            temp_model = QueryPageTraceDataResponseBodyListCoordinates()
            self.coordinates = temp_model.from_map(m['coordinates'])
        if m.get('gmtLocation') is not None:
            self.gmt_location = m.get('gmtLocation')
        if m.get('gmtUpload') is not None:
            self.gmt_upload = m.get('gmtUpload')
        return self


class QueryPageTraceDataResponseBody(TeaModel):
    def __init__(
        self,
        list: List[QueryPageTraceDataResponseBodyList] = None,
        has_more: bool = None,
        next_token: int = None,
    ):
        # 轨迹点列表
        self.list = list
        # 是否结束
        self.has_more = has_more
        # 下一个开始位置
        self.next_token = next_token

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['list'] = []
        if self.list is not None:
            for k in self.list:
                result['list'].append(k.to_map() if k else None)
        if self.has_more is not None:
            result['hasMore'] = self.has_more
        if self.next_token is not None:
            result['nextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('list') is not None:
            for k in m.get('list'):
                temp_model = QueryPageTraceDataResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('hasMore') is not None:
            self.has_more = m.get('hasMore')
        if m.get('nextToken') is not None:
            self.next_token = m.get('nextToken')
        return self


class QueryPageTraceDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: QueryPageTraceDataResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = QueryPageTraceDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


