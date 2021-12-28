from collections import defaultdict

from google.protobuf.descriptor_pb2 import FileDescriptorProto
from grpc_reflection.v1alpha.reflection_pb2_grpc import ServerReflectionStub

from ..gexceptions.ServiceException import ServiceException
from .descriptor_cache import file_cache
from .reflection import Reflection


class ReflectionStub(Reflection):
    REFLECT_SERVICE = "grpc.reflection."

    def __init__(self, channel):
        super().__init__(channel)
        self._reflection_stub = ServerReflectionStub(self._channel)

    def invoke(self, request):
        return self._reflection_stub.ServerReflectionInfo(request)

    def list_services(self):
        """
        call reflection service
        :return:
        """
        try:
            req = self.call_reflection_method(list_services='')
            response = self._reflection_stub.ServerReflectionInfo(req)
            for r in response:
                return [x.name for x in r.list_services_response.service if not x.name.startswith(self.REFLECT_SERVICE)]
            return list()
        except Exception as e:
            raise ServiceException(f"get service list error: {e}")

    def get_descriptor(self, service):
        descriptor = file_cache.get_descriptor(service)
        if descriptor is None:
            descriptor = self.get_file_descriptor(service)
            file_cache.set_descriptor(service, descriptor)
        return descriptor

    def list_services_and_methods(self):
        services = self.list_services()
        ans = defaultdict(list)
        for srv in services:
            descriptor = self.get_descriptor(srv)
            # 解析完成以后
            srv = list(descriptor.service)
            if len(srv) == 0:
                raise ServiceException(f"get service [{srv}] info failed!")
            md = srv[0].method
            for m in md:
                ans[srv].append(m.name)
        return ans

    def list_methods_by_service(self, symbol):
        descriptor = self.get_descriptor(symbol)
        ans = list()
        for srv in descriptor.service:
            if srv.name == symbol:
                for m in srv.method:
                    ans.append(m)
        return ans

    def get_file_descriptor(self, symbol):
        """
        call reflection server to get methods list via symbol(service)
        :param symbol:
        :return:
        """
        request = self.call_reflection_method(file_containing_symbol=symbol)
        resp = self._reflection_stub.ServerReflectionInfo(request)
        for r in resp:
            data = r.file_descriptor_response.file_descriptor_proto[0]
            descriptor = FileDescriptorProto()
            descriptor.ParseFromString(data)
            return descriptor
