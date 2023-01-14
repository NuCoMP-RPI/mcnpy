from mcnpy import SourceSetting, PhysicsSetting
from abc import ABC
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MiscSetting(ABC):
    """
    """

class Random(RandomBase, MiscSetting):
    """
    A representation of the model object `Random`.
    
    Parameters
    ----------
    generator : str
        Generator for `Random`.
    seed : mcnpy.long
        Seed for `Random`.
    stride : int
        Stride for `Random`.
    start_at_history : int
        StartAtHistory for `Random`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Debug(DebugBase, MiscSetting):
    """
    A representation of the model object `Debug`.
    
    Parameters
    ----------
    x1 : float
        X1 for `Debug`.
    x2 : float
        X2 for `Debug`.
    x3 : float
        X3 for `Debug`.
    x4 : float
        X4 for `Debug`.
    x5 : float
        X5 for `Debug`.
    x6 : float
        X6 for `Debug`.
    x7 : float
        X7 for `Debug`.
    x8 : float
        X8 for `Debug`.
    x9 : float
        X9 for `Debug`.
    x10 : float
        X10 for `Debug`.
    x11 : float
        X11 for `Debug`.
    x12 : float
        X12 for `Debug`.
    x13 : float
        X13 for `Debug`.
    x14 : float
        X14 for `Debug`.
    x15 : float
        X15 for `Debug`.
    x16 : float
        X16 for `Debug`.
    x17 : float
        X17 for `Debug`.
    x18 : float
        X18 for `Debug`.
    x19 : float
        X19 for `Debug`.
    x23 : float
        X23 for `Debug`.
    x24 : float
        X24 for `Debug`.
    x27 : float
        X27 for `Debug`.
    x28 : str
        X28 for `Debug`.
    x32 : float
        X32 for `Debug`.
    x33 : float
        X33 for `Debug`.
    x34 : float
        X34 for `Debug`.
    x35 : float
        X35 for `Debug`.
    x36 : float
        X36 for `Debug`.
    x37 : float
        X37 for `Debug`.
    x38 : float
        X38 for `Debug`.
    x39 : float
        X39 for `Debug`.
    x40 : str
        X40 for `Debug`.
    x41 : str
        X41 for `Debug`.
    x42 : float
        X42 for `Debug`.
    x43 : float
        X43 for `Debug`.
    x44 : float
        X44 for `Debug`.
    x45 : float
        X45 for `Debug`.
    x46 : float
        X46 for `Debug`.
    x47 : float
        X47 for `Debug`.
    x48 : float
        X48 for `Debug`.
    x49 : float
        X49 for `Debug`.
    x50 : float
        X50 for `Debug`.
    x51 : str
        X51 for `Debug`.
    x52 : str
        X52 for `Debug`.
    x53 : float
        X53 for `Debug`.
    x54 : float
        X54 for `Debug`.
    x55 : float
        X55 for `Debug`.
    x60 : float
        X60 for `Debug`.
    x61 : float
        X61 for `Debug`.
    x62 : float
        X62 for `Debug`.
    x64 : float
        X64 for `Debug`.
    x65 : float
        X65 for `Debug`.
    x66 : float
        X66 for `Debug`.
    x67 : float
        X67 for `Debug`.
    x69 : str
        X69 for `Debug`.
    x70 : float
        X70 for `Debug`.
    x71 : float
        X71 for `Debug`.
    x72 : float
        X72 for `Debug`.
    x75 : str
        X75 for `Debug`.
    x76 : str
        X76 for `Debug`.
    x77 : float
        X77 for `Debug`.
    x78 : str
        X78 for `Debug`.
    x79 : str
        X79 for `Debug`.
    x81 : str
        X81 for `Debug`.
    x82 : str
        X82 for `Debug`.
    x83 : str
        X83 for `Debug`.
    x84 : str
        X84 for `Debug`.
    x85 : str
        X85 for `Debug`.
    x86 : str
        X86 for `Debug`.
    x87 : str
        X87 for `Debug`.
    x88 : str
        X88 for `Debug`.
    x89 : str
        X89 for `Debug`.
    x90 : float
        X90 for `Debug`.
    x91 : float
        X91 for `Debug`.
    x92 : float
        X92 for `Debug`.
    x100 : float
        X100 for `Debug`.
    j_x1 : str
        J_x1 for `Debug`.
    j_x2 : str
        J_x2 for `Debug`.
    j_x3 : str
        J_x3 for `Debug`.
    j_x4 : str
        J_x4 for `Debug`.
    j_x5 : str
        J_x5 for `Debug`.
    j_x6 : str
        J_x6 for `Debug`.
    j_x7 : str
        J_x7 for `Debug`.
    j_x8 : str
        J_x8 for `Debug`.
    j_x9 : str
        J_x9 for `Debug`.
    j_x10 : str
        J_x10 for `Debug`.
    j_x11 : str
        J_x11 for `Debug`.
    j_x12 : str
        J_x12 for `Debug`.
    j_x13 : str
        J_x13 for `Debug`.
    j_x14 : str
        J_x14 for `Debug`.
    j_x15 : str
        J_x15 for `Debug`.
    j_x16 : str
        J_x16 for `Debug`.
    j_x17 : str
        J_x17 for `Debug`.
    j_x18 : str
        J_x18 for `Debug`.
    j_x19 : str
        J_x19 for `Debug`.
    j_x23 : str
        J_x23 for `Debug`.
    j_x24 : str
        J_x24 for `Debug`.
    j_x27 : str
        J_x27 for `Debug`.
    j_x32 : str
        J_x32 for `Debug`.
    j_x33 : str
        J_x33 for `Debug`.
    j_x34 : str
        J_x34 for `Debug`.
    j_x35 : str
        J_x35 for `Debug`.
    j_x36 : str
        J_x36 for `Debug`.
    j_x37 : str
        J_x37 for `Debug`.
    j_x38 : str
        J_x38 for `Debug`.
    j_x39 : str
        J_x39 for `Debug`.
    j_x42 : str
        J_x42 for `Debug`.
    j_x43 : str
        J_x43 for `Debug`.
    j_x44 : str
        J_x44 for `Debug`.
    j_x45 : str
        J_x45 for `Debug`.
    j_x46 : str
        J_x46 for `Debug`.
    j_x47 : str
        J_x47 for `Debug`.
    j_x48 : str
        J_x48 for `Debug`.
    j_x49 : str
        J_x49 for `Debug`.
    j_x50 : str
        J_x50 for `Debug`.
    j_x53 : str
        J_x53 for `Debug`.
    j_x54 : str
        J_x54 for `Debug`.
    j_x55 : str
        J_x55 for `Debug`.
    j_x60 : str
        J_x60 for `Debug`.
    j_x61 : str
        J_x61 for `Debug`.
    j_x62 : str
        J_x62 for `Debug`.
    j_x63 : str
        J_x63 for `Debug`.
    j_x64 : str
        J_x64 for `Debug`.
    j_x65 : str
        J_x65 for `Debug`.
    j_x66 : str
        J_x66 for `Debug`.
    j_x67 : str
        J_x67 for `Debug`.
    j_x68 : str
        J_x68 for `Debug`.
    j_x70 : str
        J_x70 for `Debug`.
    j_x71 : str
        J_x71 for `Debug`.
    j_x72 : str
        J_x72 for `Debug`.
    j_x77 : str
        J_x77 for `Debug`.
    j_x90 : str
        J_x90 for `Debug`.
    j_x91 : str
        J_x91 for `Debug`.
    j_x92 : str
        J_x92 for `Debug`.
    j_x100 : str
        J_x100 for `Debug`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class LostParticles(LostParticlesBase, MiscSetting):
    """
    A representation of the model object `LostParticles`.
    
    Parameters
    ----------
    max_lost : int
        MaxLost for `LostParticles`.
    max_debug_prints : int
        MaxDebugPrints for `LostParticles`.
    j_max_lost : str
        J_maxLost for `LostParticles`.
    j_max_debug_prints : str
        J_maxDebugPrints for `LostParticles`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class IntegerArray(IntegerArrayBase, MiscSetting):
    """
    A representation of the model object `intArray`.
    
    Parameters
    ----------
    integers : iterable of str
        ints for `intArray`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class FloatArray(FloatArrayBase, MiscSetting):
    """
    A representation of the model object `FloatArray`.
    
    Parameters
    ----------
    floats : iterable of float
        Floats for `FloatArray`.
    jump : iterable of str
        Jump for `FloatArray`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Files(FilesBase, MiscSetting):
    """
    A representation of the model object `Files`.
    
    Parameters
    ----------
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

    class File(FileBase):
        """
        A representation of the model object `Files.File`.
        
        Parameters
        ----------
        name : int
            Name for `Files.File`.
        filename : int
            Filename for `Files.File`.
        access : mcnpy.Files.FileAccess
            Access for `Files.File`.
        format : mcnpy.Files.FileFormat
            Format for `Files.File`.
        record_length : int
            RecordLength for `Files.File`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class ReadFile(ReadFileBase, MiscSetting):
    """
    A representation of the model object `ReadFile`.
    
    Parameters
    ----------
    file : str
        File for `ReadFile`.
    password_decode : str
        Password_decode for `ReadFile`.
    password_encode : str
        Password_encode for `ReadFile`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Vertical(ABC):
    """
    """
    class Cell(VerticalCellBase, MiscSetting):
        """
        A representation of the model object `Vertical.Cell`.
        
        Parameters
        ----------
        cell_keywords : iterable of mcnpy.Vertical.Cell.Keyword
            CellKeywords for `Vertical.Cell`.
        parameters : iterable of mcnpy.Vertical.CellEntry
            Parameters for `Vertical.Cell`.
        jump : iterable of str
            Jump for `Vertical.Cell`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

        class Entry(VerticalCellEntryBase):
            """
            A representation of the model object `Vertical.Cell.Entry`.
            
            Parameters
            ----------
            i_d : mcnpy.Cell
                ID for `Vertical.Cell.Entry`.
            parameters : iterable of mcnpy.Vertical.CellValue
                Parameters for `Vertical.Cell.Entry`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Keyword(CellKeywordBase):
            """
            A representation of the model object `Vertical.Cell.Keyword`.
            
            Parameters
            ----------
            vol : str
                Vol for `Vertical.Cell.Keyword`.
            pwt : str
                Pwt for `Vertical.Cell.Keyword`.
            nonu : str
                Nonu for `Vertical.Cell.Keyword`.
            tmp : str
                Tmp for `Vertical.Cell.Keyword`.
            tmp_i_d : int
                TmpID for `Vertical.Cell.Keyword`.
            u : str
                U for `Vertical.Cell.Keyword`.
            lat : str
                Lat for `Vertical.Cell.Keyword`.
            trcl : str
                Trcl for `Vertical.Cell.Keyword`.
            cosy : str
                Cosy for `Vertical.Cell.Keyword`.
            bflcl : str
                Bflcl for `Vertical.Cell.Keyword`.
            mat : str
                Mat for `Vertical.Cell.Keyword`.
            rho : str
                Rho for `Vertical.Cell.Keyword`.
            unit : mcnpy.AngleUnit
                Unit for `Vertical.Cell.Keyword`.
            fill : str
                Fill for `Vertical.Cell.Keyword`.
            imp : str
                Imp for `Vertical.Cell.Keyword`.
            ext : str
                Ext for `Vertical.Cell.Keyword`.
            fcl : str
                Fcl for `Vertical.Cell.Keyword`.
            wwn : str
                Wwn for `Vertical.Cell.Keyword`.
            wwn_i_d : int
                WwnID for `Vertical.Cell.Keyword`.
            dxc : str
                Dxc for `Vertical.Cell.Keyword`.
            pd : str
                Pd for `Vertical.Cell.Keyword`.
            tally : mcnpy.Tally
                Tally for `Vertical.Cell.Keyword`.
            elept : str
                Elept for `Vertical.Cell.Keyword`.
            unc : str
                Unc for `Vertical.Cell.Keyword`.
            particles : iterable of mcnpy.Particle
                Particles for `Vertical.Cell.Keyword`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Value(VerticalCellValueBase):
            """
            A representation of the model object `Vertical.Cell.Value`.
            
            Parameters
            ----------
            value : float
                Value for `Vertical.Cell.Value`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class Surface(VerticalSurfaceBase, MiscSetting):
        """
        A representation of the model object `Vertical.Surface`.
        
        Parameters
        ----------
        areas : iterable of mcnpy.Vertical.SurfaceEntry
            Areas for `Vertical.Surface`.
        jump : iterable of str
            Jump for `Vertical.Surface`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

        class Entry(VerticalSurfaceEntryBase):
            """
            A representation of the model object `Vertical.Surface.Entry`.
            
            Parameters
            ----------
            id : mcnpy.Surface
                Id for `Vertical.Surface.Entry`.
            area : iterable of float
                Area for `Vertical.Surface.Entry`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class Source(ABC):
        """
        """
        class Distribution(VerticalSourceDistributionBase, SourceSetting):
            """
            A representation of the model object `Vertical.Source.Distribution`.
            
            Parameters
            ----------
            src_keywords : iterable of mcnpy.SourceID
                SrcKeywords for `Vertical.Source.Distribution`.
            options : iterable of mcnpy.Vertical.Source.Options
                Options for `Vertical.Source.Distribution`.
            jump : iterable of str
                Jump for `Vertical.Source.Distribution`.
            parameters : iterable of mcnpy.Vertical.Source.Values
                Parameters for `Vertical.Source.Distribution`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        class Options(VerticalSourceOptionsBase):
            """
            A representation of the model object `Vertical.Source.Options`.
            
            Parameters
            ----------
            options : iterable of mcnpy.VerticalSrcOptions
                Options for `Vertical.Source.Options`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Values(VerticalSourceValuesBase):
            """
            A representation of the model object `Vertical.Source.Values`.
            
            Parameters
            ----------
            parameters : iterable of float
                Parameters for `Vertical.Source.Values`.
            
            """

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
        """
        NPS
        A representation of the model object `Cutoff.History`.
        
        Parameters
        ----------
        histories : float
            Histories for `Cutoff.History`.
        pixel_histories : float
            PixelHistories for `Cutoff.History`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Precision(PrecisionCutoffBase, TerminationSetting):
        __doc__ = """STOP
        """
        """
        STOP
        A representation of the model object `Cutoff.Precision`.
        
        Parameters
        ----------
        history_cutoff : mcnpy.Cutoff.History
            HistoryCutoff for `Cutoff.Precision`.
        cpu_cutoff_time : float
            CpuCutoffTime for `Cutoff.Precision`.
        tallies : iterable of mcnpy.Tally
            Tallies for `Cutoff.Precision`.
        precisions : iterable of float
            Precisions for `Cutoff.Precision`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class CpuTime(CpuTimeCutoffBase, TerminationSetting):
        __doc__ = """CTME
        """
        """
        CTME
        A representation of the model object `Cutoff.CpuTime`.
        
        Parameters
        ----------
        minutes : float
            Minutes for `Cutoff.CpuTime`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class Continue(ABC):
    class DontPrintTallies(ContDontPrintTalliesBase):
        """
        A representation of the model object `Continue.DontPrintTallies`.
        
        Parameters
        ----------
        dont_print : iterable of int
            DontPrint for `Continue.DontPrintTallies`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class EmbeddedGeometry(ContEmbeddedGeometryBase):
        """
        A representation of the model object `Continue.EmbeddedGeometry`.
        
        Parameters
        ----------
        name : int
            Name for `Continue.EmbeddedGeometry`.
        background : int
            Background for `Continue.EmbeddedGeometry`.
        sign : iterable of str
            Sign for `Continue.EmbeddedGeometry`.
        materials : iterable of int
            Materials for `Continue.EmbeddedGeometry`.
        cells : iterable of int
            Cells for `Continue.EmbeddedGeometry`.
        mesh_format : mcnpy.Embedded.GeometryMeshFormat
            MeshFormat for `Continue.EmbeddedGeometry`.
        mesh : str
            Mesh for `Continue.EmbeddedGeometry`.
        eeout : str
            Eeout for `Continue.EmbeddedGeometry`.
        eeout_res : str
            EeoutRes for `Continue.EmbeddedGeometry`.
        calculate_volumes : mcnpy.YesNo
            CalculateVolumes for `Continue.EmbeddedGeometry`.
        debug : mcnpy.Embedded.GeometryDebug
            Debug for `Continue.EmbeddedGeometry`.
        filetype : mcnpy.Embedded.GeometryFiletype
            Filetype for `Continue.EmbeddedGeometry`.
        gmv_file : str
            GmvFile for `Continue.EmbeddedGeometry`.
        length_conversion_factor : float
            LengthConversionFactor for `Continue.EmbeddedGeometry`.
        mcnpum_file : str
            McnpumFile for `Continue.EmbeddedGeometry`.
        overlap_all : mcnpy.Embedded.GeometryOverlap
            OverlapAll for `Continue.EmbeddedGeometry`.
        overlap_cell : iterable of mcnpy.Embedded.GeometryOverlap
            OverlapCell for `Continue.EmbeddedGeometry`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class TallyPrint(ContTallyPrintBase):
        """
        A representation of the model object `Continue.TallyPrint`.
        
        Parameters
        ----------
        tally : int
            Tally for `Continue.TallyPrint`.
        order : iterable of mcnpy.TallyQuantity
            Order for `Continue.TallyPrint`.
        
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

subclass_overrides(Vertical, ignore=[Vertical.Source])
subclass_overrides(Vertical.Source)
subclass_overrides(Cutoff)
subclass_overrides(Continue)
subclass_overrides(Files)