from abc import ABC
from mcnpy.wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class OutputSetting(ABC):
    """
    """

class Print(PrintBase, OutputSetting):
    """
    A representation of the model object `Print`.
    
    Parameters
    ----------
    tables : iterable of int
        Tables for `Print`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DontPrintTallies(DontPrintTalliesBase, OutputSetting):
    """
    A representation of the model object `DontPrintTallies`.
    
    Parameters
    ----------
    dont_print : iterable of mcnpy.Tally
        DontPrint for `DontPrintTallies`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PrintDump(PrintDumpBase, OutputSetting):
    """
    A representation of the model object `PrintDump`.
    
    Parameters
    ----------
    increment_tallies : float
        IncrementTallies for `PrintDump`.
    increment_runtape : float
        IncrementRuntape for `PrintDump`.
    print_mctal : float
        PrintMctal for `PrintDump`.
    max_dumps_runtape : float
        MaxDumpsRuntape for `PrintDump`.
    print_tally_chart : float
        PrintTallyChart for `PrintDump`.
    j_increment_tallies : str
        J_incrementTallies for `PrintDump`.
    j_increment_runtape : str
        J_incrementRuntape for `PrintDump`.
    j_print_mctal : str
        J_printMctal for `PrintDump`.
    j_max_dumps_runtape : str
        J_maxDumpsRuntape for `PrintDump`.
    j_print_chart_tally : str
        J_printChartTally for `PrintDump`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ParticleTrack(ParticleTrackBase, OutputSetting):
    """
    A representation of the model object `ParticleTrack`.
    
    Parameters
    ----------
    buffer : float
        Buffer for `ParticleTrack`.
    format : mcnpy.ParticleTrackFormat
        Format for `ParticleTrack`.
    max_tracks : int
        MaxTracks for `ParticleTrack`.
    max_events_per_history : int
        MaxEventsPerHistory for `ParticleTrack`.
    write : mcnpy.ParticleTrackWrite
        Write for `ParticleTrack`.
    print_zero_tallies : mcnpy.Boolean
        PrintZeroTallies for `ParticleTrack`.
    event : iterable of mcnpy.Events
        Event for `ParticleTrack`.
    filters : iterable of mcnpy.ParticleTrackFilter
        Filters for `ParticleTrack`.
    particles : iterable of mcnpy.Particle
        Particles for `ParticleTrack`.
    histories : iterable of int
        Histories for `ParticleTrack`.
    cells : iterable of mcnpy.Cell
        Cells for `ParticleTrack`.
    surfaces : iterable of mcnpy.Surface
        Surfaces for `ParticleTrack`.
    tallies : iterable of mcnpy.ParticleTrackTally
        Tallies for `ParticleTrack`.
    tally_cutoffs : iterable of mcnpy.ParticleTrack.Values
        TallyCutoffs for `ParticleTrack`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class Values(ValuesBase):
        """
        A representation of the model object `ParticleTrack.Values`.
        
        Parameters
        ----------
        value : float
            Value for `ParticleTrack.Values`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class CreateLahet(CreateLahetBase, OutputSetting):
    """
    A representation of the model object `CreateLahet`.
    
    Parameters
    ----------
    max_words_per_file : int
        MaxWordsPerFile for `CreateLahet`.
    cells : iterable of mcnpy.Cell
        Cells for `CreateLahet`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class InteractivePlot(InteractivePlotBase, OutputSetting):
    """
    A representation of the model object `InteractivePlot`.
    
    Parameters
    ----------
    output_device_type : int
        OutputDeviceType for `InteractivePlot`.
    send_plots : str
        SendPlots for `InteractivePlot`.
    interval_of_cells : float
        IntervalOfCells for `InteractivePlot`.
    pause_time : float
        PauseTime for `InteractivePlot`.
    filename : int
        Filename for `InteractivePlot`.
    print_type_param : int
        PrintTypeParam for `InteractivePlot`.
    current_runtpe_file : int
        CurrentRuntpeFile for `InteractivePlot`.
    tally_data_file : str
        TallyDataFile for `InteractivePlot`.
    m_c_t_a_lfile : str
        MCTALfile for `InteractivePlot`.
    tally : mcnpy.Tally
        Tally for `InteractivePlot`.
    pert_num : int
        PertNum for `InteractivePlot`.
    a_param : mcnpy.Axis
        AParam for `InteractivePlot`.
    f_param : float
        FParam for `InteractivePlot`.
    s_param : float
        SParam for `InteractivePlot`.
    command : mcnpy.ParameterCommand
        Command for `InteractivePlot`.
    title_toggle : int
        TitleToggle for `InteractivePlot`.
    line : str
        Line for `InteractivePlot`.
    x_location : float
        XLocation for `InteractivePlot`.
    y_location : float
        YLocation for `InteractivePlot`.
    subtitle : str
        Subtitle for `InteractivePlot`.
    xtitle : str
        Xtitle for `InteractivePlot`.
    ytitle : str
        Ytitle for `InteractivePlot`.
    ztitle : str
        Ztitle for `InteractivePlot`.
    label : str
        Label for `InteractivePlot`.
    x_variable : float
        XVariable for `InteractivePlot`.
    y_variable : float
        YVariable for `InteractivePlot`.
    num_bins : int
        NumBins for `InteractivePlot`.
    var : mcnpy.FixedVariable
        Var for `InteractivePlot`.
    bin_num : int
        BinNum for `InteractivePlot`.
    setvar : iterable of mcnpy.FixedVariable
        Setvar for `InteractivePlot`.
    allowed_value : mcnpy.TallyFluctuationList
        AllowedValue for `InteractivePlot`.
    keff_val : int
        KeffVal for `InteractivePlot`.
    material_num : mcnpy.Material
        MaterialNum for `InteractivePlot`.
    reaction_num : mcnpy.Material
        ReactionNum for `InteractivePlot`.
    part_type : mcnpy.Particle
        PartType for `InteractivePlot`.
    xmin : float
        Xmin for `InteractivePlot`.
    xmax : float
        Xmax for `InteractivePlot`.
    xsteps : int
        Xsteps for `InteractivePlot`.
    ymin : float
        Ymin for `InteractivePlot`.
    ymax : float
        Ymax for `InteractivePlot`.
    ysteps : int
        Ysteps for `InteractivePlot`.
    scales_val : int
        ScalesVal for `InteractivePlot`.
    splines_of_tension : float
        SplinesOfTension for `InteractivePlot`.
    thickness : float
        Thickness for `InteractivePlot`.
    legend_vals : iterable of float
        LegendVals for `InteractivePlot`.
    cmin : float
        Cmin for `InteractivePlot`.
    cmax : float
        Cmax for `InteractivePlot`.
    csteps : int
        Csteps for `InteractivePlot`.
    wash_param : mcnpy.EBoolean
        WashParam for `InteractivePlot`.
    mesh_tally : mcnpy.Tally
        MeshTally for `InteractivePlot`.
    rel_error : mcnpy.Tally
        RelError for `InteractivePlot`.
    tally_results : iterable of mcnpy.LogLin
        TallyResults for `InteractivePlot`.
    energy_bin_tally : mcnpy.Tally
        EnergyBinTally for `InteractivePlot`.
    time_bin_tally : mcnpy.Tally
        TimeBinTally for `InteractivePlot`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Events(EventsBase):
    """
    A representation of the model object `Events`.
    
    Parameters
    ----------
    event : mcnpy.ParticleTrackEvent
        Event for `Events`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ParticleTrackFilter(ParticleTrackFilterBase):
    """
    A representation of the model object `ParticleTrackFilter`.
    
    Parameters
    ----------
    bounds : iterable of float
        Bounds for `ParticleTrackFilter`.
    quantity : mcnpy.ParticleTrackFilterQuantity
        Quantity for `ParticleTrackFilter`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ParticleTrackTally(ParticleTrackTallyBase):
    """
    A representation of the model object `ParticleTrackTally`.
    
    Parameters
    ----------
    cutoff_multiplier : mcnpy.Boolean
        CutoffMultiplier for `ParticleTrackTally`.
    tally : mcnpy.Tally
        Tally for `ParticleTrackTally`.
    
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

subclass_overrides(ParticleTrack)