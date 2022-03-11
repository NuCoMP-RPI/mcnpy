from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class OutputSetting(ABC):
    """
    """

class Print(PrintBase, OutputSetting):
    """PRINT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DontPrintTallies(DontPrintTalliesBase, OutputSetting):
    """TALNP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PrintDump(PrintDumpBase, OutputSetting):
    """PRDMP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ParticleTrack(ParticleTrackBase, OutputSetting):
    """PTRAC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CreateLahet(CreateLahetBase, OutputSetting):
    """HISTP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class InteractivePlot(InteractivePlotBase, OutputSetting):
    """MPLOT
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