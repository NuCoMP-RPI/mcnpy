from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MiscSetting(ABC):
    """
    """

class Random(RandomBase, MiscSetting):
    """RAND
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Debug(DebugBase, MiscSetting):
    """DBCN
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class LostParticles(LostParticlesBase, MiscSetting):
    """LOST
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class IntegerArray(IntegerArrayBase, MiscSetting):
    """IDUM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class FloatArray(FloatArrayBase, MiscSetting):
    """RDUM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Files(FilesBase, MiscSetting):
    """FILES
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ReadFile(ReadFileBase, MiscSetting):
    """READ
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalCell(VerticalCellBase, MiscSetting):
    """#
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalSurface(VerticalSurfaceBase, MiscSetting):
    """# ARA
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override