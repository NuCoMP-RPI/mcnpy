from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class TerminationSetting(ABC):
    """
    """

class HistoryCutoff(HistoryCutoffBase, TerminationSetting):
    __doc__ = """NPS
    """
    __doc__ += HistoryCutoffBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PrecisionCutoff(PrecisionCutoffBase, TerminationSetting):
    __doc__ = """STOP
    """
    __doc__ += PrecisionCutoffBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CpuTimeCutoff(CpuTimeCutoffBase, TerminationSetting):
    __doc__ = """CTME
    """
    __doc__ += CpuTimeCutoffBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override