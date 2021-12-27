from .base_internal import BaseInternal


class BaseRedisInternal(BaseInternal):
    expiration = 0
    key_template = 'object_id'
