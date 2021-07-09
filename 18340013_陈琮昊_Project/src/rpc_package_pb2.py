# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc_package.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rpc_package.proto',
  package='rpc_package',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11rpc_package.proto\x12\x0brpc_package\"%\n\x07Request\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"*\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"&\n\x06\x42\x61\x63kUp\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\x0e\n\x06values\x18\x02 \x03(\t\"I\n\tTransFrom\x12\r\n\x05start\x18\x01 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x03\x12\x0e\n\x06\x61im_ip\x18\x03 \x01(\t\x12\x10\n\x08\x61im_port\x18\x04 \x01(\t\",\n\x10SlaveInformation\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x1c\n\tSlaveCode\x12\x0f\n\x07message\x18\x01 \x01(\t2\xa7\x02\n\tDatastore\x12\x34\n\x03put\x12\x14.rpc_package.Request\x1a\x15.rpc_package.Response\"\x00\x12\x34\n\x03get\x12\x14.rpc_package.Request\x1a\x15.rpc_package.Response\"\x00\x12\x37\n\x06\x64\x65lete\x12\x14.rpc_package.Request\x1a\x15.rpc_package.Response\"\x00\x12\x37\n\x07receive\x12\x13.rpc_package.BackUp\x1a\x15.rpc_package.Response\"\x00\x12<\n\ttransform\x12\x16.rpc_package.TransFrom\x1a\x15.rpc_package.Response\"\x00\x32U\n\x05Slave\x12L\n\x11\x61\x64\x64_slave_setting\x12\x1d.rpc_package.SlaveInformation\x1a\x16.rpc_package.SlaveCode\"\x00\x62\x06proto3'
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='rpc_package.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='rpc_package.Request.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='rpc_package.Request.value', index=1,
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
  serialized_start=34,
  serialized_end=71,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='rpc_package.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='rpc_package.Response.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='rpc_package.Response.value', index=1,
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
  serialized_start=73,
  serialized_end=115,
)


_BACKUP = _descriptor.Descriptor(
  name='BackUp',
  full_name='rpc_package.BackUp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='keys', full_name='rpc_package.BackUp.keys', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='values', full_name='rpc_package.BackUp.values', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=117,
  serialized_end=155,
)


_TRANSFROM = _descriptor.Descriptor(
  name='TransFrom',
  full_name='rpc_package.TransFrom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='rpc_package.TransFrom.start', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='rpc_package.TransFrom.end', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aim_ip', full_name='rpc_package.TransFrom.aim_ip', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aim_port', full_name='rpc_package.TransFrom.aim_port', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=157,
  serialized_end=230,
)


_SLAVEINFORMATION = _descriptor.Descriptor(
  name='SlaveInformation',
  full_name='rpc_package.SlaveInformation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='rpc_package.SlaveInformation.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='rpc_package.SlaveInformation.port', index=1,
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
  serialized_start=232,
  serialized_end=276,
)


_SLAVECODE = _descriptor.Descriptor(
  name='SlaveCode',
  full_name='rpc_package.SlaveCode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='rpc_package.SlaveCode.message', index=0,
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
  serialized_start=278,
  serialized_end=306,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['BackUp'] = _BACKUP
DESCRIPTOR.message_types_by_name['TransFrom'] = _TRANSFROM
DESCRIPTOR.message_types_by_name['SlaveInformation'] = _SLAVEINFORMATION
DESCRIPTOR.message_types_by_name['SlaveCode'] = _SLAVECODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.Request)
  })
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.Response)
  })
_sym_db.RegisterMessage(Response)

BackUp = _reflection.GeneratedProtocolMessageType('BackUp', (_message.Message,), {
  'DESCRIPTOR' : _BACKUP,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.BackUp)
  })
_sym_db.RegisterMessage(BackUp)

TransFrom = _reflection.GeneratedProtocolMessageType('TransFrom', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFROM,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.TransFrom)
  })
_sym_db.RegisterMessage(TransFrom)

SlaveInformation = _reflection.GeneratedProtocolMessageType('SlaveInformation', (_message.Message,), {
  'DESCRIPTOR' : _SLAVEINFORMATION,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.SlaveInformation)
  })
_sym_db.RegisterMessage(SlaveInformation)

SlaveCode = _reflection.GeneratedProtocolMessageType('SlaveCode', (_message.Message,), {
  'DESCRIPTOR' : _SLAVECODE,
  '__module__' : 'rpc_package_pb2'
  # @@protoc_insertion_point(class_scope:rpc_package.SlaveCode)
  })
_sym_db.RegisterMessage(SlaveCode)



_DATASTORE = _descriptor.ServiceDescriptor(
  name='Datastore',
  full_name='rpc_package.Datastore',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=309,
  serialized_end=604,
  methods=[
  _descriptor.MethodDescriptor(
    name='put',
    full_name='rpc_package.Datastore.put',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get',
    full_name='rpc_package.Datastore.get',
    index=1,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='rpc_package.Datastore.delete',
    index=2,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='receive',
    full_name='rpc_package.Datastore.receive',
    index=3,
    containing_service=None,
    input_type=_BACKUP,
    output_type=_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='transform',
    full_name='rpc_package.Datastore.transform',
    index=4,
    containing_service=None,
    input_type=_TRANSFROM,
    output_type=_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DATASTORE)

DESCRIPTOR.services_by_name['Datastore'] = _DATASTORE


_SLAVE = _descriptor.ServiceDescriptor(
  name='Slave',
  full_name='rpc_package.Slave',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=606,
  serialized_end=691,
  methods=[
  _descriptor.MethodDescriptor(
    name='add_slave_setting',
    full_name='rpc_package.Slave.add_slave_setting',
    index=0,
    containing_service=None,
    input_type=_SLAVEINFORMATION,
    output_type=_SLAVECODE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SLAVE)

DESCRIPTOR.services_by_name['Slave'] = _SLAVE

# @@protoc_insertion_point(module_scope)
