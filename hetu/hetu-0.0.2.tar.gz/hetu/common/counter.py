import requests
import functools


class HetuCounter:
    def __init__(self, url=''):
        self.url = url if url else 'http://47.110.94.96:5000/hetu/api/counter'
        self.token = 'eHVlbGFuZ3l1bg=='
        self.req_count()

    def req_count(self):
        requests.get(url=self.url)
        return 1


def func_count(url=None, module_id=None, func=None):
    url = url if url else 'http://47.110.94.96:5000/hetu/api/counter/func'
    requests.get(url=url, params={'module_id': module_id, 'func': func})


def func_counter(*_args, **_kwargs):
    def make_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            url = kwargs.get('url') if kwargs.get('url') else 'http://47.110.94.96:5000/hetu/api/counter/func'
            requests.get(url=url, params={'module_id': _kwargs.get('module_id'), 'func': func_name})
            return func(*args, **kwargs)
        return wrapper
    return make_decorator
