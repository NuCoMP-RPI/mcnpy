import metapy

import mcnpy.mixin
# All of the automatic wrappers.
from mcnpy.wrap import *
# All of the custom wrappers.
from ._deck import *
from .points import *
from .source import *
from .physics import *
from .materials import *
from .data import *
from .output import *
from .region import *
from .surfaces import *
from .tally import Tally
from .variance_reduction import *
from .geometry import *

# Custom classes that deviate from the parse tree.
from mcnpy.deck import *
from mcnpy.example import *
from mcnpy.mbody_decomp import *

# Translation
# Only import OpenMC if available.
try:
    import mcnpy.translate_to_openmc
except:
    pass
# Only import if SerPy is available.
try:
    import mcnpy.translate_mcnp_serpent
    import mcnpy.surface_converter
except:
    pass