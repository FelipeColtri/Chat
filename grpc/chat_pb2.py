# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\"3\n\x0eMessageRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"\"\n\x0eReceiveRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"4\n\x0fMessageResponse\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t2w\n\x0b\x43hatService\x12\x30\n\x0bSendMessage\x12\x0f.MessageRequest\x1a\x10.MessageResponse\x12\x36\n\x0fReceiveMessages\x12\x0f.ReceiveRequest\x1a\x10.MessageResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MESSAGEREQUEST']._serialized_start=14
  _globals['_MESSAGEREQUEST']._serialized_end=65
  _globals['_RECEIVEREQUEST']._serialized_start=67
  _globals['_RECEIVEREQUEST']._serialized_end=101
  _globals['_MESSAGERESPONSE']._serialized_start=103
  _globals['_MESSAGERESPONSE']._serialized_end=155
  _globals['_CHATSERVICE']._serialized_start=157
  _globals['_CHATSERVICE']._serialized_end=276
# @@protoc_insertion_point(module_scope)
