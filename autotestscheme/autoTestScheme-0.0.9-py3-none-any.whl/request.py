import os
import sys
import allure
import copy
import time
import inspect
import requests

from urllib.parse import urlencode

from .common import config, constant, logger


class requestBase(object):


    def __init__(self):
        self.setup_hook_list = []
        self.teardown_hook_list = []
        self.logger = logger
        self.api_data = {}
        self.session = requests.Session()
        self.agreement = 'http'  # 协议
        self.base_url = None # 域名
        self.subdomain = None # 子域名
        self.catch_response = False # locust的时候使用
        self.kwargs = {} # request配置文件内的参数

    def set_session(self, client):
        self.session = client

    def read_api_folder(self, *folder_name):
        if isinstance(folder_name, tuple) is False:
            folder_name = (folder_name,)
        folder = os.path.join(constant.BASE_DIR, *folder_name)
        for root, dirs, files in os.walk(folder):
            for name in files:
                _path = os.path.join(root, name)
                if name.endswith('.json') is True:
                    _data = config.Json(_path).get_object()
                    if _data.get('id') is not None:
                        self.register_api(_data)

    def register_api(self, _data):
        _id = _data.get('id')
        if _id in list(self.api_data.keys()):
            self.logger.error("api({})重复注册".format(_id))
        self.api_data[_id] = _data

    def get_api(self, api_id):
        if api_id in list(self.api_data.keys()):
            return self.api_data[api_id]
        assert False, "api({})未注册".format(api_id)

    def register_setup_hook(self, hook):
        self.setup_hook_list.append(hook)

    def register_teardown_hook(self, hook):
        self.teardown_hook_list.append(hook)

    def get_url(self, path):
        '''
            获取网址
        '''
        if self.subdomain is None:
            base_url = self.base_url
        else:
            base_url = self.subdomain + '.' + self.base_url
        url = '{}://{}{}'.format(self.agreement, base_url, path)
        return url

    def send(self, api_id, params={}, json={}, data={}, timeout=None, title=None, is_json=True):
        request = self.get_api(api_id)
        request['params'] = params
        request['json'] = json
        request['data'] = data
        if timeout is not None:
            request['timeout'] = timeout
        if title is not None:
            request['title'] = title
        response = self._excute(request)
        if is_json is True:
            return response.json()
        return response

    def execute(self, request):
        """
            发送请求
        """
        for hook in self.setup_hook_list:
            self.excute_kwargs(hook, request)
        request['title'] = request.get('title') if request.get('title') is not None else request.get('path')
        with allure.step(request['title']):
            self.logger.debug('发送请求：{}'.format(request['title']))
            response = self._excute(request)
            for hook in self.teardown_hook_list:
                self.excute_kwargs(hook, request)
            return response

    def excute_kwargs(self, hook, request):
        kwarg = {}
        kwargs = {'request': request, 'session': self.session, 'kwargs': self.kwargs}
        for i in inspect.getfullargspec(hook).args:
            if i in ['self', 'cls']:
                continue
            kwarg[i] = kwargs[i]
        hook(**kwarg)

    def _excute(self, request):
        current_time = time.time()
        new_request = copy.deepcopy(request)
        new_request['url'] = self.get_url(new_request.get('path'))
        if 'path' in new_request:
            del new_request['path']
        new_request['verify'] = False
        if self.catch_response is True:
            new_request['url'] = new_request['url'] + '?' + urlencode(new_request['params'])
            new_request['name'] = new_request['title']
            del new_request['params']
            new_request['catch_response'] = True
        for i in ['id', 'title']:
            if i in new_request:
                del new_request[i]
        result = self.session.request(**new_request)
        response = result.text.replace('\n', '').replace('\r', '').replace('  ', '')
        self.logger.debug('请求参数：method：{}，url：{}, \nparams:{}, headers:{}, \ndata:{}, json:{},'
                          '\n返回：{},时间:{}'.format(new_request.get('method'), new_request.get('url'), new_request.get('params'),
                                                 new_request.get('headers'), new_request.get('data'), new_request.get('json'),
                                                 response, time.time() - current_time))
        if self.catch_response is True:
            return result
        return result

    def qs_parse(self, data):
        for key in list(data.keys()):
            value = data[key]
            if type(value) == dict:
                del data[key]
                for _key in list(value.keys()):
                    data[key + '[' + _key + ']'] = value[_key]
            elif type(value) == list:
                del data[key]
                for _key in range(len(value)):
                    data[key + '[' + str(_key) + ']'] = value[_key]
