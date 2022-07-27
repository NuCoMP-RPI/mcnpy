from mcnpy import SourceSetting, PhysicsSetting
from abc import ABC
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MiscSetting(ABC):
    """
    """

class Random(RandomBase, MiscSetting):
    __doc__ = RandomBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Debug(DebugBase, MiscSetting):
    __doc__ = DebugBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class LostParticles(LostParticlesBase, MiscSetting):
    __doc__ = LostParticlesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class IntegerArray(IntegerArrayBase, MiscSetting):
    __doc__ = IntegerArrayBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class FloatArray(FloatArrayBase, MiscSetting):
    __doc__ = FloatArrayBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Files(FilesBase, MiscSetting):
    __doc__ = FilesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

    class File(FileBase):
        __doc__ = FileBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class ReadFile(ReadFileBase, MiscSetting):
    __doc__ = ReadFileBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Vertical(ABC):
    """
    """
    class Cell(VerticalCellBase, MiscSetting):
        __doc__ = VerticalCellBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

        class Entry(VerticalCellEntryBase):
            __doc__ = VerticalCellEntryBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Keyword(CellKeywordBase):
            __doc__ = CellKeywordBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Value(VerticalCellValueBase):
            __doc__ = VerticalCellValueBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class Surface(VerticalSurfaceBase, MiscSetting):
        __doc__ = VerticalSurfaceBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

        class Entry(VerticalSurfaceEntryBase):
            __doc__ = VerticalSurfaceEntryBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class Source(ABC):
        """
        """
        class Distribution(VerticalSourceDistributionBase, SourceSetting):
            __doc__ = VerticalSourceDistributionBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        class Options(VerticalSourceOptionsBase):
            __doc__ = VerticalSourceOptionsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Values(VerticalSourceValuesBase):
            __doc__ = VerticalSourceValuesBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Mode(VerticalModeBase, PhysicsSetting):
            """
            """
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

class TerminationSetting(ABC):
    """
    """
class Cutoff(ABC):
    """
    """
    class History(HistoryCutoffBase, TerminationSetting):
        __doc__ = """NPS
        """
        __doc__ += HistoryCutoffBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Precision(PrecisionCutoffBase, TerminationSetting):
        __doc__ = """STOP
        """
        __doc__ += PrecisionCutoffBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class CpuTime(CpuTimeCutoffBase, TerminationSetting):
        __doc__ = """CTME
        """
        __doc__ += CpuTimeCutoffBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class Continue(ABC):
    class DontPrintTallies(ContDontPrintTalliesBase):
        __doc__ = ContDontPrintTalliesBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class EmbeddedGeometry(ContEmbeddedGeometryBase):
        __doc__ = ContEmbeddedGeometryBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class TallyPrint(ContTallyPrintBase):
        __doc__ = ContTallyPrintBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override

subclass_overrides(Vertical, ignore=[Vertical.Source])
subclass_overrides(Vertical.Source)
subclass_overrides(Cutoff)
subclass_overrides(Continue)
subclass_overrides(Files)