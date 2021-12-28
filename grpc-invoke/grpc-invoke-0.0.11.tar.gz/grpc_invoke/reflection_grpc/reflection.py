"""
reflection base class, Please use the implement.
"""
from grpc_reflection.v1alpha.reflection_pb2 import ServerReflectionRequest


class Reflection(object):

    def __init__(self, channel):
        self._channel = channel

    @classmethod
    def call_reflection_method(cls, **kwargs):
        yield ServerReflectionRequest(**kwargs)

    def list_services(self):
        """
        get services exclude reflection
        :return:
        """
        raise NotImplementedError

    def list_services_and_methods(self):
        """
        get services and methods from server
        :return:
        """
        raise NotImplementedError

    def list_methods_by_service(self, symbol):
        """
        get method info by service
        :param symbol: service name
        :return:
        """
        raise NotImplementedError

    def get_file_descriptor(self, symbol):
        """
        get file descriptor with symbol from server
        :param symbol:
        :return:
        """
        raise NotImplementedError
