# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vod/business/vod_play.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from volcengine.vod.models.business import vod_common_pb2 as vod_dot_business_dot_vod__common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='vod/business/vod_play.proto',
  package='Volcengine.Vod.Models.Business',
  syntax='proto3',
  serialized_options=b'\n)com.volcengine.service.vod.model.businessB\007VodPlayP\001ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\240\001\001\330\001\001\302\002\000\312\002 Volc\\Service\\Vod\\Models\\Business\342\002#Volc\\Service\\Vod\\Models\\GPBMetadata',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bvod/business/vod_play.proto\x12\x1eVolcengine.Vod.Models.Business\x1a\x1dvod/business/vod_common.proto\"\x8e\x04\n\x10VodPlayInfoModel\x12H\n\x07Version\x18\n \x01(\x0e\x32\x37.Volcengine.Vod.Models.Business.VodPlayInfoModelVersion\x12\x0b\n\x03Vid\x18\x01 \x01(\t\x12\x0e\n\x06Status\x18\x02 \x01(\x05\x12\x11\n\tPosterUrl\x18\x03 \x01(\t\x12\x10\n\x08\x44uration\x18\x04 \x01(\x02\x12\x10\n\x08\x46ileType\x18\x05 \x01(\t\x12\x16\n\x0e\x45nableAdaptive\x18\x06 \x01(\x08\x12\x12\n\nTotalCount\x18\x07 \x01(\x05\x12\x45\n\x0c\x41\x64\x61ptiveInfo\x18\x08 \x01(\x0b\x32/.Volcengine.Vod.Models.Business.VodAdaptiveInfo\x12\x41\n\x0cPlayInfoList\x18\t \x03(\x0b\x32+.Volcengine.Vod.Models.Business.VodPlayInfo\x12\x43\n\rThumbInfoList\x18\x0b \x03(\x0b\x32,.Volcengine.Vod.Models.Business.VodThumbInfo\x12\x16\n\x0e\x42\x61rrageMaskUrl\x18\x0c \x01(\t\x12I\n\x10SubtitleInfoList\x18\r \x03(\x0b\x32/.Volcengine.Vod.Models.Business.VodSubtitleInfo\"\xd8\x01\n\x1cVodGetOriginalPlayInfoResult\x12\x10\n\x08\x46ileType\x18\x01 \x01(\t\x12\x10\n\x08\x44uration\x18\x02 \x01(\x02\x12\x0c\n\x04Size\x18\x03 \x01(\x01\x12\x0e\n\x06Height\x18\x04 \x01(\x05\x12\r\n\x05Width\x18\x05 \x01(\x05\x12\x0e\n\x06\x46ormat\x18\x06 \x01(\t\x12\r\n\x05\x43odec\x18\x07 \x01(\t\x12\x0f\n\x07\x42itrate\x18\x08 \x01(\x05\x12\x0b\n\x03Md5\x18\t \x01(\t\x12\x13\n\x0bMainPlayUrl\x18\n \x01(\t\x12\x15\n\rBackupPlayUrl\x18\x0b \x01(\t\"H\n\x19VodPrivateDrmPlayAuthInfo\x12\x12\n\nPlayAuthId\x18\x01 \x01(\t\x12\x17\n\x0fPlayAuthContent\x18\x02 \x01(\t\"u\n\x1eVodGetPrivateDrmPlayAuthResult\x12S\n\x10PlayAuthInfoList\x18\x01 \x03(\x0b\x32\x39.Volcengine.Vod.Models.Business.VodPrivateDrmPlayAuthInfo\"1\n\x1cVodGetHlsDecryptionKeyResult\x12\x11\n\tSecretKey\x18\x01 \x01(\t*\xd6\x01\n\x17VodPlayInfoModelVersion\x12$\n UndefinedVodPlayInfoModelVersion\x10\x00\x12%\n!InternalV1VodPlayInfoModelVersion\x10\x01\x12%\n!InternalV2VodPlayInfoModelVersion\x10\x02\x12%\n!InternalV3VodPlayInfoModelVersion\x10\x03\x12 \n\x1cToBV1VodPlayInfoModelVersion\x10\x04\x42\xcb\x01\n)com.volcengine.service.vod.model.businessB\x07VodPlayP\x01ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02 Volc\\Service\\Vod\\Models\\Business\xe2\x02#Volc\\Service\\Vod\\Models\\GPBMetadatab\x06proto3'
  ,
  dependencies=[vod_dot_business_dot_vod__common__pb2.DESCRIPTOR,])

_VODPLAYINFOMODELVERSION = _descriptor.EnumDescriptor(
  name='VodPlayInfoModelVersion',
  full_name='Volcengine.Vod.Models.Business.VodPlayInfoModelVersion',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UndefinedVodPlayInfoModelVersion', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='InternalV1VodPlayInfoModelVersion', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='InternalV2VodPlayInfoModelVersion', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='InternalV3VodPlayInfoModelVersion', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ToBV1VodPlayInfoModelVersion', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1087,
  serialized_end=1301,
)
_sym_db.RegisterEnumDescriptor(_VODPLAYINFOMODELVERSION)

VodPlayInfoModelVersion = enum_type_wrapper.EnumTypeWrapper(_VODPLAYINFOMODELVERSION)
UndefinedVodPlayInfoModelVersion = 0
InternalV1VodPlayInfoModelVersion = 1
InternalV2VodPlayInfoModelVersion = 2
InternalV3VodPlayInfoModelVersion = 3
ToBV1VodPlayInfoModelVersion = 4



_VODPLAYINFOMODEL = _descriptor.Descriptor(
  name='VodPlayInfoModel',
  full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Version', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.Version', index=0,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Vid', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.Vid', index=1,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Status', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.Status', index=2,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PosterUrl', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.PosterUrl', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Duration', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.Duration', index=4,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='FileType', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.FileType', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='EnableAdaptive', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.EnableAdaptive', index=6,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='TotalCount', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.TotalCount', index=7,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AdaptiveInfo', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.AdaptiveInfo', index=8,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PlayInfoList', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.PlayInfoList', index=9,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ThumbInfoList', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.ThumbInfoList', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='BarrageMaskUrl', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.BarrageMaskUrl', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SubtitleInfoList', full_name='Volcengine.Vod.Models.Business.VodPlayInfoModel.SubtitleInfoList', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=621,
)


_VODGETORIGINALPLAYINFORESULT = _descriptor.Descriptor(
  name='VodGetOriginalPlayInfoResult',
  full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='FileType', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.FileType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Duration', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Duration', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Size', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Size', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Height', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Height', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Width', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Width', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Format', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Format', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Codec', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Codec', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Bitrate', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Bitrate', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Md5', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.Md5', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='MainPlayUrl', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.MainPlayUrl', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='BackupPlayUrl', full_name='Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult.BackupPlayUrl', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=624,
  serialized_end=840,
)


_VODPRIVATEDRMPLAYAUTHINFO = _descriptor.Descriptor(
  name='VodPrivateDrmPlayAuthInfo',
  full_name='Volcengine.Vod.Models.Business.VodPrivateDrmPlayAuthInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='PlayAuthId', full_name='Volcengine.Vod.Models.Business.VodPrivateDrmPlayAuthInfo.PlayAuthId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PlayAuthContent', full_name='Volcengine.Vod.Models.Business.VodPrivateDrmPlayAuthInfo.PlayAuthContent', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=842,
  serialized_end=914,
)


_VODGETPRIVATEDRMPLAYAUTHRESULT = _descriptor.Descriptor(
  name='VodGetPrivateDrmPlayAuthResult',
  full_name='Volcengine.Vod.Models.Business.VodGetPrivateDrmPlayAuthResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='PlayAuthInfoList', full_name='Volcengine.Vod.Models.Business.VodGetPrivateDrmPlayAuthResult.PlayAuthInfoList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=916,
  serialized_end=1033,
)


_VODGETHLSDECRYPTIONKEYRESULT = _descriptor.Descriptor(
  name='VodGetHlsDecryptionKeyResult',
  full_name='Volcengine.Vod.Models.Business.VodGetHlsDecryptionKeyResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='SecretKey', full_name='Volcengine.Vod.Models.Business.VodGetHlsDecryptionKeyResult.SecretKey', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1035,
  serialized_end=1084,
)

_VODPLAYINFOMODEL.fields_by_name['Version'].enum_type = _VODPLAYINFOMODELVERSION
_VODPLAYINFOMODEL.fields_by_name['AdaptiveInfo'].message_type = vod_dot_business_dot_vod__common__pb2._VODADAPTIVEINFO
_VODPLAYINFOMODEL.fields_by_name['PlayInfoList'].message_type = vod_dot_business_dot_vod__common__pb2._VODPLAYINFO
_VODPLAYINFOMODEL.fields_by_name['ThumbInfoList'].message_type = vod_dot_business_dot_vod__common__pb2._VODTHUMBINFO
_VODPLAYINFOMODEL.fields_by_name['SubtitleInfoList'].message_type = vod_dot_business_dot_vod__common__pb2._VODSUBTITLEINFO
_VODGETPRIVATEDRMPLAYAUTHRESULT.fields_by_name['PlayAuthInfoList'].message_type = _VODPRIVATEDRMPLAYAUTHINFO
DESCRIPTOR.message_types_by_name['VodPlayInfoModel'] = _VODPLAYINFOMODEL
DESCRIPTOR.message_types_by_name['VodGetOriginalPlayInfoResult'] = _VODGETORIGINALPLAYINFORESULT
DESCRIPTOR.message_types_by_name['VodPrivateDrmPlayAuthInfo'] = _VODPRIVATEDRMPLAYAUTHINFO
DESCRIPTOR.message_types_by_name['VodGetPrivateDrmPlayAuthResult'] = _VODGETPRIVATEDRMPLAYAUTHRESULT
DESCRIPTOR.message_types_by_name['VodGetHlsDecryptionKeyResult'] = _VODGETHLSDECRYPTIONKEYRESULT
DESCRIPTOR.enum_types_by_name['VodPlayInfoModelVersion'] = _VODPLAYINFOMODELVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VodPlayInfoModel = _reflection.GeneratedProtocolMessageType('VodPlayInfoModel', (_message.Message,), {
  'DESCRIPTOR' : _VODPLAYINFOMODEL,
  '__module__' : 'vod.business.vod_play_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodPlayInfoModel)
  })
_sym_db.RegisterMessage(VodPlayInfoModel)

VodGetOriginalPlayInfoResult = _reflection.GeneratedProtocolMessageType('VodGetOriginalPlayInfoResult', (_message.Message,), {
  'DESCRIPTOR' : _VODGETORIGINALPLAYINFORESULT,
  '__module__' : 'vod.business.vod_play_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodGetOriginalPlayInfoResult)
  })
_sym_db.RegisterMessage(VodGetOriginalPlayInfoResult)

VodPrivateDrmPlayAuthInfo = _reflection.GeneratedProtocolMessageType('VodPrivateDrmPlayAuthInfo', (_message.Message,), {
  'DESCRIPTOR' : _VODPRIVATEDRMPLAYAUTHINFO,
  '__module__' : 'vod.business.vod_play_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodPrivateDrmPlayAuthInfo)
  })
_sym_db.RegisterMessage(VodPrivateDrmPlayAuthInfo)

VodGetPrivateDrmPlayAuthResult = _reflection.GeneratedProtocolMessageType('VodGetPrivateDrmPlayAuthResult', (_message.Message,), {
  'DESCRIPTOR' : _VODGETPRIVATEDRMPLAYAUTHRESULT,
  '__module__' : 'vod.business.vod_play_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodGetPrivateDrmPlayAuthResult)
  })
_sym_db.RegisterMessage(VodGetPrivateDrmPlayAuthResult)

VodGetHlsDecryptionKeyResult = _reflection.GeneratedProtocolMessageType('VodGetHlsDecryptionKeyResult', (_message.Message,), {
  'DESCRIPTOR' : _VODGETHLSDECRYPTIONKEYRESULT,
  '__module__' : 'vod.business.vod_play_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodGetHlsDecryptionKeyResult)
  })
_sym_db.RegisterMessage(VodGetHlsDecryptionKeyResult)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
