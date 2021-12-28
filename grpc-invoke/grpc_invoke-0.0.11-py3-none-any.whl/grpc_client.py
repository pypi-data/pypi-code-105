"""
grpc client for python is a tool inspired by grpcurl
you can use it as python package to realize what you want to do instead of using "grpcurl.exe -args"
thanks for grpcurl, I have read the source code of grpcurl to help me
"""

__author__ = "woody"

import json
import traceback

import google.protobuf.descriptor as _descriptor
import grpc
from google.protobuf import json_format
from google.protobuf.json_format import Parse, ParseError
from google.protobuf.message_factory import MessageFactory

from gexceptions.MethodException import MethodException
from gexceptions.ParamsException import ParamsException
from gexceptions.ServiceException import ServiceException
from reflection_grpc.reflection_stub import ReflectionStub


class GrpcClient(object):
    """
    python grpc client inspired by grpcurl

    usage:
    with GrpcClient("ip:port", "service", "method") as client:
        resp = client.invoke({"a": b})  # params is a dict in python
        # response is formatted json string
        print(resp)
    """
    stub = None
    _channel = None
    _factory = MessageFactory()

    def __init__(self, address: str, iface: str, method: str):
        """
        :param address:  examples: host:port
        :param iface: iface is service name
        :param method: method is what method you want to call
        """
        self.address = address
        self.iface = iface
        self.method = method
        self._channel = grpc.insecure_channel(self.address)
        self._reflection_stub = ReflectionStub(self._channel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._channel is not None:
            self._channel.close()

    @classmethod
    def _convert_metadata(cls, header):
        """
        convert metadata
        :param header:
        :return:
        """
        if header is None:
            return None
        ans = []
        for k, v in header.items():
            if not isinstance(k, str):
                k = str(k)
            if not isinstance(v, str):
                v = str(v)
            data = (k.encode(), v.encode())
            ans.append(data)
        return ans

    def invoke(self, data=None, header=None, origin=False):
        """
        core method for call grpc service
        when the return value has utf-8 string like chinese/japanese, you should deal with it yourself
        :param data: data is dictionary in python, so the method support json data
        :param header: key-value header
        :param origin: if false, you can get a json value, otherwise an original response
        :return:
        """
        msg, req_type, resp_type = self.get_args_and_response(data)
        rpc_client = self.client(req_type, resp_type)
        metadata = self._convert_metadata(header)
        response = rpc_client(msg, metadata=metadata)
        if origin:
            return response
        return json_format.MessageToJson(response)

    def client(self, request_type, response_type):
        return self._channel.unary_unary(
            f'/{self.iface}/{self.method}',
            request_serializer=getattr(request_type, "SerializeToString"),
            response_deserializer=getattr(response_type, "FromString")
        )

    @classmethod
    def get_in_out_type(cls, request_type, response_type, descriptor):
        req_type, resp_type = None, None
        for m in descriptor.message_type:
            if req_type is None and request_type.endswith(m.name):
                desc = _descriptor.MakeDescriptor(m)
                request_cls = cls._factory.GetPrototype(desc)
                req_type = request_cls()
                continue
            if resp_type is None and response_type.endswith(m.name):
                desc = _descriptor.MakeDescriptor(m)
                response_cls = cls._factory.GetPrototype(desc)
                resp_type = response_cls()
        return req_type, resp_type

    def get_args_and_response(self, params):
        """
        get request and response descriptor according to file descriptor
        :param params:
        :return:
        """
        try:
            methods = self._reflection_stub.list_methods_by_service(self.iface)
            desc = self._reflection_stub.get_file_descriptor(self.iface)
            for m in methods:
                if m.name.lower() == self.method.lower():
                    # match method
                    request_type, response_type = self.get_in_out_type(m.input_type, m.output_type, desc)
                    if request_type is None:
                        raise ParamsException(f"get method: {self.method} input type error")
                    if response_type is None:
                        raise ParamsException(f"get method: {self.method} out type error")
                    msg = Parse(json.dumps(params, ensure_ascii=False), request_type)
                    return msg, request_type, response_type
            raise MethodException(f"{self.method} doesn't exist in {self.iface}")
        except ServiceException or MethodException or ParamsException:
            raise
        except ParseError as e:
            raise ParamsException(f"params validate failed, Please check! {str(e)}")
        except Exception as e:
            traceback.print_exc()
            raise ParamsException(f"unknown error: {e}")


if __name__ == "__main__":
    with GrpcClient("localhost:50052", "Hello", "Kujiji") as client:
        resp = client.invoke({"hehe": "hello"}, {"name": "lixiaoyao"})
        print(resp)
