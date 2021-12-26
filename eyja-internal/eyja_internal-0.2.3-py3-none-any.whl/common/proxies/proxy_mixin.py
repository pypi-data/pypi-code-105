from .target_getter import TargetGetterProxy


class ProxyMixin:
    @classmethod
    def class_proxy_target(cls, target):
        return TargetGetterProxy(cls, target)

    def self_proxy_target(self, target):
        return TargetGetterProxy(self, target)
 