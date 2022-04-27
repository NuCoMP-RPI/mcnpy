from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class OutputSetting(ABC):
    """
    """

class Print(PrintBase, OutputSetting):
    __doc__ = PrintBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DontPrintTallies(DontPrintTalliesBase, OutputSetting):
    __doc__ = DontPrintTalliesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PrintDump(PrintDumpBase, OutputSetting):
    __doc__ = PrintDumpBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ParticleTrack(ParticleTrackBase, OutputSetting):
    __doc__ = ParticleTrackBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CreateLahet(CreateLahetBase, OutputSetting):
    __doc__ = CreateLahetBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class InteractivePlot(InteractivePlotBase, OutputSetting):
    __doc__ = InteractivePlotBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Events(EventsBase):
    __doc__ = EventsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ParticleTrackFilter(ParticleTrackFilterBase):
    __doc__ = ParticleTrackFilterBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ParticleTrackTally(ParticleTrackTallyBase):
    __doc__ = ParticleTrackTallyBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override