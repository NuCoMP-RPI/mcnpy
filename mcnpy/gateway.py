import py4j.java_gateway
from py4j.java_gateway import JavaGateway #, CallbackServerParameters
#import time
#from inspect import getsourcefile
#from os.path import abspath, dirname, getmtime, join

#MCNPY_PATH = abspath(dirname(getsourcefile(lambda:0)))

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

def get_documentation(e_class):
    """Retrieve metamodel annotations."""
    return gateway.getDocs(e_class)

def print_deck(deck):
    return gateway.printDeck(deck)

def load_file(filename):
    return gateway.load_file(filename)

def deck_resource(deck):
    return gateway.deckResource(deck.__copy__(), 'deck.mcnp')

"""def add_adapter(object):
    gateway.addAdapter(object._e_object)"""

"""def java_modified():
    mod_time = getmtime(join(MCNPY_PATH, 'lib', 'gov.lanl.mcnp-1.0.0-SNAPSHOT.jar'))

    try:
        with open(join(MCNPY_PATH, 'last_java_update'), 'r') as file:
            last_update = file.read()
    except:
        last_update = None

    if str(mod_time) != last_update:
        with open(join(MCNPY_PATH, 'last_java_update'), 'w') as file:
            file.write(str(mod_time))
            return True
    else:
        return False

JAVA_MODIFIED = java_modified()"""