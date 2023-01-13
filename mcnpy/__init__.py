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
from .enum_keywords import *

# Custom classes that deviate from the parse tree.
from mcnpy.deck import *
from mcnpy.example import *
from mcnpy.mbody_decomp import *

# Translation
# Only import OpenMC if available.
try:
    import mcnpy.translate_mcnp_openmc
    import mcnp.surface_converter_openmc
except ModuleNotFoundError:
    pass
# Only import if SerPy is available.
try:
    import mcnpy.translate_mcnp_serpent
    import mcnpy.surface_converter_serpent
except ModuleNotFoundError:
    pass