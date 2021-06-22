"""
### `mcnpy` - The MCNP API from NuCoMP
  Read, write, and edit MCNP decks like a pro.
"""
import atexit
from .java_server import Server
server = Server()
from .gateway import gateway
# All of the automatic wrappers.
from .wrap import *
# All of the custom wrappers.
from .override import *

# Custom classes that deviate from the parse tree.
from .universe import UniverseList
from .lattice import Lattice
from .input_deck import InputDeck
from mcnpy import example

def kill_gateway():
    """Kills the Py4j gateway and the MCNP Gateway Server.
      Should be called at the end of your Python script to
      avoid leaving a Java process running.
    """
    gateway.shutdown()
    server.kill()

atexit.register(kill_gateway)