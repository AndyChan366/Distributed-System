# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.rpc_package_pb2 as rpc__package__pb2


class DatastoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.put = channel.unary_unary(
                '/rpc_package.Datastore/put',
                request_serializer=rpc__package__pb2.Request.SerializeToString,
                response_deserializer=rpc__package__pb2.Response.FromString,
                )
        self.get = channel.unary_unary(
                '/rpc_package.Datastore/get',
                request_serializer=rpc__package__pb2.Request.SerializeToString,
                response_deserializer=rpc__package__pb2.Response.FromString,
                )
        self.delete = channel.unary_unary(
                '/rpc_package.Datastore/delete',
                request_serializer=rpc__package__pb2.Request.SerializeToString,
                response_deserializer=rpc__package__pb2.Response.FromString,
                )
        self.receive = channel.unary_unary(
                '/rpc_package.Datastore/receive',
                request_serializer=rpc__package__pb2.BackUp.SerializeToString,
                response_deserializer=rpc__package__pb2.Response.FromString,
                )
        self.transform = channel.unary_unary(
                '/rpc_package.Datastore/transform',
                request_serializer=rpc__package__pb2.TransFrom.SerializeToString,
                response_deserializer=rpc__package__pb2.Response.FromString,
                )


class DatastoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def receive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def transform(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatastoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'put': grpc.unary_unary_rpc_method_handler(
                    servicer.put,
                    request_deserializer=rpc__package__pb2.Request.FromString,
                    response_serializer=rpc__package__pb2.Response.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=rpc__package__pb2.Request.FromString,
                    response_serializer=rpc__package__pb2.Response.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=rpc__package__pb2.Request.FromString,
                    response_serializer=rpc__package__pb2.Response.SerializeToString,
            ),
            'receive': grpc.unary_unary_rpc_method_handler(
                    servicer.receive,
                    request_deserializer=rpc__package__pb2.BackUp.FromString,
                    response_serializer=rpc__package__pb2.Response.SerializeToString,
            ),
            'transform': grpc.unary_unary_rpc_method_handler(
                    servicer.transform,
                    request_deserializer=rpc__package__pb2.TransFrom.FromString,
                    response_serializer=rpc__package__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc_package.Datastore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Datastore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Datastore/put',
            rpc__package__pb2.Request.SerializeToString,
            rpc__package__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Datastore/get',
            rpc__package__pb2.Request.SerializeToString,
            rpc__package__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Datastore/delete',
            rpc__package__pb2.Request.SerializeToString,
            rpc__package__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def receive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Datastore/receive',
            rpc__package__pb2.BackUp.SerializeToString,
            rpc__package__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def transform(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Datastore/transform',
            rpc__package__pb2.TransFrom.SerializeToString,
            rpc__package__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class SlaveStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add_slave_setting = channel.unary_unary(
                '/rpc_package.Slave/add_slave_setting',
                request_serializer=rpc__package__pb2.SlaveInformation.SerializeToString,
                response_deserializer=rpc__package__pb2.SlaveCode.FromString,
                )


class SlaveServicer(object):
    """Missing associated documentation comment in .proto file."""

    def add_slave_setting(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SlaveServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'add_slave_setting': grpc.unary_unary_rpc_method_handler(
                    servicer.add_slave_setting,
                    request_deserializer=rpc__package__pb2.SlaveInformation.FromString,
                    response_serializer=rpc__package__pb2.SlaveCode.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc_package.Slave', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Slave(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def add_slave_setting(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc_package.Slave/add_slave_setting',
            rpc__package__pb2.SlaveInformation.SerializeToString,
            rpc__package__pb2.SlaveCode.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
