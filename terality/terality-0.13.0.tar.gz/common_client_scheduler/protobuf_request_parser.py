from common_client_scheduler.protobuf.generated.client_scheduler_messages_pb2 import (
    ProtobufRequestProto,
)
from common_client_scheduler.requests import (
    ProtobufRequest,
)
from common_client_scheduler.requests import CreateUserRequest, FollowUpRequest
from common_client_scheduler import (
    ImportFromCloudRequest,
    ExportToCloudRequest,
    PandasFunctionRequest,
)
from terality_serde.protobuf_helpers import ProtobufParser


class ProtobufRequestParser(ProtobufParser):
    protobuf_class = ProtobufRequestProto

    @classmethod
    def to_protobuf_message(cls, request: ProtobufRequest) -> ProtobufRequestProto:
        proto = ProtobufRequestProto()
        if isinstance(request, CreateUserRequest):
            proto.create_user_request.MergeFrom(request.proto)
        if isinstance(request, ImportFromCloudRequest):
            proto.import_from_cloud_request.MergeFrom(request.proto)
        if isinstance(request, ExportToCloudRequest):
            proto.export_to_cloud_request.MergeFrom(request.proto)
        if isinstance(request, PandasFunctionRequest):
            proto.pandas_function_request.MergeFrom(request.proto)
        if isinstance(request, FollowUpRequest):
            proto.follow_up_request.MergeFrom(request.proto)

        return proto

    @classmethod
    def to_terality_class(cls, proto: ProtobufRequestProto) -> ProtobufRequest:
        request_type = proto.WhichOneof("request")

        if request_type == "create_user_request":
            return CreateUserRequest.from_proto(proto.create_user_request)
        if request_type == "import_from_cloud_request":
            return ImportFromCloudRequest.from_proto(proto.import_from_cloud_request)
        if request_type == "export_to_cloud_request":
            return ExportToCloudRequest.from_proto(proto.export_to_cloud_request)
        if request_type == "pandas_function_request":
            return PandasFunctionRequest.from_proto(proto.pandas_function_request)
        if request_type == "follow_up_request":
            return FollowUpRequest.from_proto(proto.follow_up_request)

        raise ValueError(f"Could not infer ProtobufRequest type from proto={proto}")
