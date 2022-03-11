from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class TerminationSetting(ABC):
    """
    """

class HistoryCutoff(HistoryCutoffBase, TerminationSetting):
    """NPS
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PrecisionCutoff(PrecisionCutoffBase, TerminationSetting):
    """STOP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CpuTimeCutoff(CpuTimeCutoffBase, TerminationSetting):
    """CTME
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override