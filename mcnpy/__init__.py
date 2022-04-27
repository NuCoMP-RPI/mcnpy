import atexit
from time import sleep
from mcnpy.java_server import Server
server = Server()

# This accomodates the brief delay for the server to start running.
running = False
sleep_time = 0.0
while running is False:
    try:
        from mcnpy.gateway import gateway
        running = True
        # sleep_time will be 0.0 if the server is already running.
        # An alternate message prints in that case.
        if sleep_time > 0.0:
            print('MCNP Gateway Server Started')
    except:
        # Change wait time if necessary.
        wait = 0.01
        sleep(wait)
        sleep_time += wait
        # TODO: Figure out a realistic upper limit for the wait.
        if sleep_time == 5.0:
            break

# TODO: Remove when we're confident about stable startup.
print('I slept for: ' + str(sleep_time) + ' seconds!')

"""try:
    from mcnpy.gateway import gateway
    running = True
except:
    server.kill()
    running = False
if running is False:
    raise Exception('Error reaching Java Gateway.\n Try increasing the startup '
                    + 'delay by editing ".../mcnpy/server_delay".')"""

# All of the automatic wrappers.
from mcnpy.wrap import *
# All of the custom wrappers.
from mcnpy.override import *

# Custom classes that deviate from the parse tree.
from mcnpy.deck import *
from mcnpy.example import *
from mcnpy.lattice import *
from mcnpy.mbody_decomp import *
from mcnpy.universe import UniverseList

#from mcnpy import material_helper

def _kill_gateway():
    """Kills the Py4j gateway and the MCNP Gateway Server. Automatically called upon exit after importing module.
    """

    # Shutdown gateway if server started via popen.
    # This will leave an externally started server running.
    if server.pid is None:
        gateway.shutdown()
    # Try to kill the server.
    try:
        server.kill()
    # Exception occurs is an externally started server is killed before exiting
    # the Python script.
    except:
        # Since the server is already killed, we just shutdown the gateway.
        gateway.shutdown()
        print('MCNP Gateway Server Killed Externally')

atexit.register(_kill_gateway)