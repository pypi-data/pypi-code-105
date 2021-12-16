# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='msg.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\tmsg.proto\"(\n\x06Status\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\x08\"\x8d\x01\n\x0bMessageData\x12\x10\n\x08identity\x18\x01 \x01(\t\x12\x0e\n\x06msg_id\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontrol\x18\x03 \x01(\t\x12\x0f\n\x07\x63ommand\x18\x04 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x05 \x01(\t\x12\x0c\n\x04info\x18\x06 \x01(\t\x12\x0e\n\x06stderr\x18\x07 \x01(\t\x12\x0e\n\x06stdout\x18\x08 \x01(\t\"]\n\x0fMessageResponse\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x08\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x0c.MessageData\"3\n\x11GetMessageRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"O\n\x11PutMessageRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x0c.MessageData\"Y\n\x0bJobResponse\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x08\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x0c.MessageData\"/\n\rGetJobRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"K\n\rPutJobRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x0c.MessageData\".\n\x0c\x43heckRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"A\n\rCheckResponse\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x10\n\x08has_data\x18\x03 \x01(\x08\"/\n\x0c\x42\x61sicRequest\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x0f\n\x07verbose\x18\x02 \x01(\x08\x32\xbb\x02\n\x0eMessageService\x12\x32\n\nGetMessage\x12\x12.GetMessageRequest\x1a\x10.MessageResponse\x12)\n\nPutMessage\x12\x12.PutMessageRequest\x1a\x07.Status\x12-\n\x0cMessageCheck\x12\r.CheckRequest\x1a\x0e.CheckResponse\x12&\n\x06GetJob\x12\x0e.GetJobRequest\x1a\x0c.JobResponse\x12!\n\x06PutJob\x12\x0e.PutJobRequest\x1a\x07.Status\x12)\n\x08JobCheck\x12\r.CheckRequest\x1a\x0e.CheckResponse\x12%\n\x0bPurgeQueues\x12\r.BasicRequest\x1a\x07.Statusb\x06proto3')
)




_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='Status.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='Status.result', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=13,
  serialized_end=53,
)


_MESSAGEDATA = _descriptor.Descriptor(
  name='MessageData',
  full_name='MessageData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='identity', full_name='MessageData.identity', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msg_id', full_name='MessageData.msg_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control', full_name='MessageData.control', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='command', full_name='MessageData.command', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='MessageData.data', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info', full_name='MessageData.info', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stderr', full_name='MessageData.stderr', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stdout', full_name='MessageData.stdout', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=56,
  serialized_end=197,
)


_MESSAGERESPONSE = _descriptor.Descriptor(
  name='MessageResponse',
  full_name='MessageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='MessageResponse.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='MessageResponse.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='MessageResponse.target', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='MessageResponse.data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=199,
  serialized_end=292,
)


_GETMESSAGEREQUEST = _descriptor.Descriptor(
  name='GetMessageRequest',
  full_name='GetMessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='GetMessageRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='GetMessageRequest.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=294,
  serialized_end=345,
)


_PUTMESSAGEREQUEST = _descriptor.Descriptor(
  name='PutMessageRequest',
  full_name='PutMessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='PutMessageRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='PutMessageRequest.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='PutMessageRequest.data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=347,
  serialized_end=426,
)


_JOBRESPONSE = _descriptor.Descriptor(
  name='JobResponse',
  full_name='JobResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='JobResponse.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='JobResponse.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='JobResponse.target', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='JobResponse.data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=428,
  serialized_end=517,
)


_GETJOBREQUEST = _descriptor.Descriptor(
  name='GetJobRequest',
  full_name='GetJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='GetJobRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='GetJobRequest.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=519,
  serialized_end=566,
)


_PUTJOBREQUEST = _descriptor.Descriptor(
  name='PutJobRequest',
  full_name='PutJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='PutJobRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='PutJobRequest.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='PutJobRequest.data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=568,
  serialized_end=643,
)


_CHECKREQUEST = _descriptor.Descriptor(
  name='CheckRequest',
  full_name='CheckRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='CheckRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='CheckRequest.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=645,
  serialized_end=691,
)


_CHECKRESPONSE = _descriptor.Descriptor(
  name='CheckResponse',
  full_name='CheckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='CheckResponse.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='CheckResponse.target', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_data', full_name='CheckResponse.has_data', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=693,
  serialized_end=758,
)


_BASICREQUEST = _descriptor.Descriptor(
  name='BasicRequest',
  full_name='BasicRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='BasicRequest.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verbose', full_name='BasicRequest.verbose', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=760,
  serialized_end=807,
)

_MESSAGERESPONSE.fields_by_name['data'].message_type = _MESSAGEDATA
_PUTMESSAGEREQUEST.fields_by_name['data'].message_type = _MESSAGEDATA
_JOBRESPONSE.fields_by_name['data'].message_type = _MESSAGEDATA
_PUTJOBREQUEST.fields_by_name['data'].message_type = _MESSAGEDATA
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['MessageData'] = _MESSAGEDATA
DESCRIPTOR.message_types_by_name['MessageResponse'] = _MESSAGERESPONSE
DESCRIPTOR.message_types_by_name['GetMessageRequest'] = _GETMESSAGEREQUEST
DESCRIPTOR.message_types_by_name['PutMessageRequest'] = _PUTMESSAGEREQUEST
DESCRIPTOR.message_types_by_name['JobResponse'] = _JOBRESPONSE
DESCRIPTOR.message_types_by_name['GetJobRequest'] = _GETJOBREQUEST
DESCRIPTOR.message_types_by_name['PutJobRequest'] = _PUTJOBREQUEST
DESCRIPTOR.message_types_by_name['CheckRequest'] = _CHECKREQUEST
DESCRIPTOR.message_types_by_name['CheckResponse'] = _CHECKRESPONSE
DESCRIPTOR.message_types_by_name['BasicRequest'] = _BASICREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:Status)
  })
_sym_db.RegisterMessage(Status)

MessageData = _reflection.GeneratedProtocolMessageType('MessageData', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEDATA,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:MessageData)
  })
_sym_db.RegisterMessage(MessageData)

MessageResponse = _reflection.GeneratedProtocolMessageType('MessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGERESPONSE,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:MessageResponse)
  })
_sym_db.RegisterMessage(MessageResponse)

GetMessageRequest = _reflection.GeneratedProtocolMessageType('GetMessageRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMESSAGEREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:GetMessageRequest)
  })
_sym_db.RegisterMessage(GetMessageRequest)

PutMessageRequest = _reflection.GeneratedProtocolMessageType('PutMessageRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUTMESSAGEREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:PutMessageRequest)
  })
_sym_db.RegisterMessage(PutMessageRequest)

JobResponse = _reflection.GeneratedProtocolMessageType('JobResponse', (_message.Message,), {
  'DESCRIPTOR' : _JOBRESPONSE,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:JobResponse)
  })
_sym_db.RegisterMessage(JobResponse)

GetJobRequest = _reflection.GeneratedProtocolMessageType('GetJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETJOBREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:GetJobRequest)
  })
_sym_db.RegisterMessage(GetJobRequest)

PutJobRequest = _reflection.GeneratedProtocolMessageType('PutJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUTJOBREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:PutJobRequest)
  })
_sym_db.RegisterMessage(PutJobRequest)

CheckRequest = _reflection.GeneratedProtocolMessageType('CheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHECKREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:CheckRequest)
  })
_sym_db.RegisterMessage(CheckRequest)

CheckResponse = _reflection.GeneratedProtocolMessageType('CheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHECKRESPONSE,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:CheckResponse)
  })
_sym_db.RegisterMessage(CheckResponse)

BasicRequest = _reflection.GeneratedProtocolMessageType('BasicRequest', (_message.Message,), {
  'DESCRIPTOR' : _BASICREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:BasicRequest)
  })
_sym_db.RegisterMessage(BasicRequest)



_MESSAGESERVICE = _descriptor.ServiceDescriptor(
  name='MessageService',
  full_name='MessageService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=810,
  serialized_end=1125,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetMessage',
    full_name='MessageService.GetMessage',
    index=0,
    containing_service=None,
    input_type=_GETMESSAGEREQUEST,
    output_type=_MESSAGERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PutMessage',
    full_name='MessageService.PutMessage',
    index=1,
    containing_service=None,
    input_type=_PUTMESSAGEREQUEST,
    output_type=_STATUS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='MessageCheck',
    full_name='MessageService.MessageCheck',
    index=2,
    containing_service=None,
    input_type=_CHECKREQUEST,
    output_type=_CHECKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetJob',
    full_name='MessageService.GetJob',
    index=3,
    containing_service=None,
    input_type=_GETJOBREQUEST,
    output_type=_JOBRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PutJob',
    full_name='MessageService.PutJob',
    index=4,
    containing_service=None,
    input_type=_PUTJOBREQUEST,
    output_type=_STATUS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='JobCheck',
    full_name='MessageService.JobCheck',
    index=5,
    containing_service=None,
    input_type=_CHECKREQUEST,
    output_type=_CHECKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PurgeQueues',
    full_name='MessageService.PurgeQueues',
    index=6,
    containing_service=None,
    input_type=_BASICREQUEST,
    output_type=_STATUS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MESSAGESERVICE)

DESCRIPTOR.services_by_name['MessageService'] = _MESSAGESERVICE

# @@protoc_insertion_point(module_scope)
