import py4j.java_gateway
from py4j.java_gateway import JavaGateway #, CallbackServerParameters

"""_params = CallbackServerParameters(daemonize=True)
gateway = JavaGateway(auto_field=True, auto_convert=True, eager_load=True,
                      start_callback_server=True,
                      callback_server_parameters=_params)"""
gateway = JavaGateway(auto_field=True, auto_convert=True, eager_load=True)
#gateway.entry_point.setup()

def is_instance_of(java_object, java_class, gateway=gateway):
    return py4j.java_gateway.is_instance_of(gateway, java_object, java_class)

def copy(object):
    return gateway.copier.copy(object._e_object)