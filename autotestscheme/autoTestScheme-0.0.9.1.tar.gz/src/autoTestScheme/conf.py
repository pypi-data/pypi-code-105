from dynaconf import Dynaconf
from .common import constant, common
from .common import logger
from .common.sql import MySql
from .request import requestBase
from rediscluster import RedisCluster
from redis import StrictRedis
import os, copy


class BaseDynaconf(Dynaconf):

    _session_list = {}
    _redis_list = {}
    _mysql_list = {}

    def __getattr__(self, item: str):
        try:
            result = super().__getattr__(item)
        except Exception as e:
            if item.startswith("request") or item.startswith("sql") or item.startswith("redis"):
                response = requestBase()
                response.is_exists = False
                return response
            else:
                raise e
        if item.startswith("redis"):
            return self.get_redis(item, result)
        elif item.startswith("request"):
            return self.get_session(item, result)
        elif item.startswith("sql"):
            return self.get_sql(item, result)
        return result

    def get_redis(self, item, config):
        if item not in self._session_list:
            new_config = copy.deepcopy(config)
            is_colony = new_config.get('is_colony', True)
            if 'is_colony' in new_config:
                del new_config['is_colony']
            if is_colony is True:
                if 'db' in new_config:
                    del new_config['db']
                return RedisCluster(**new_config)
            self._redis_list[item] = StrictRedis(**new_config)
        return self._redis_list[item]

    def get_session(self, item, config) -> requestBase:
        if item not in self._session_list:
            request = requestBase()
            request.is_exists = False
            if config.get("base_url", None) is not None:
                request.base_url = config['base_url']
                request.subdomain = config.get('subdomain', 'www')
                request.agreement = config.get('agreement', 'https')
                request.kwargs = config
                for i in config.get('api', []):
                    request.read_api_folder(*i)
                request.is_exists = True
            else:
                logger.error("{} 注册request失败, 配置信息:{}".format(item, config))
            self._session_list[item] = request
        return self._session_list[item]

    def get_sql(self, item, config) -> requestBase:
        if item not in self._session_list:
            sql = MySql()
            sql.connect(config)
            self._mysql_list[item] = sql
        return self._mysql_list[item]


default_settings = {'name': '未定义的name', 'test_tags': [], 'test_case': 'all', 'is_debug': False, 'process_num': 1,
                    'tag_list': {'all': '其他'}, 'is_locust': False}
settings = BaseDynaconf(envvar_prefix=False, merge_enabled=True, environments=True, load_dotenv=True,
                    env_switcher="ENV", root_path=constant.CONFIG_FOLDER, includes=['*.toml'])
if settings.exists('run'):
    settings.set('run', {})
for key, value in default_settings.items():
    if key not in settings.run:
        setattr(settings.run, key, value)
