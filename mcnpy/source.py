from abc import ABC
from enum import Enum
from .wrap import wrappers, overrides, subclass_overrides
from metapy.zaid_helper import element_to_zaid, zaid_to_element
from .points import Point
import mcnpy

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

PARTICLE = {
    'COSMIC' : 'CR',
    'COSMIC_PROTONS' : 'C1001',
	'COSMIC_ALPHAS' : 'C2004',
	'BACKGROUND' : 'BG',
	'BACKGROUND_NEUTRONS' : 'BN',
	'BACKGROUND_PHOTONS' : 'BP',
	'SPONTANEOUS_FISSION' : 'SF',
	'SPONTAENOUS_PHOTON' : 'SP',
	'COSMIC_NITROGEN' : 'C7014',
	'COSMIC_SILICON' : 'C14028',
	'COSMIC_IRON' : 'C26056',
	'NEUTRON' : 'N',
	'ANTI_NEUTRON' : 'Q',
	'PHOTON' : 'P',
	'ELECTRON ' : 'E',
	'POSITRON' : 'F',
	'NEGATIVE_MUON' : '|',
	'POSITIVE_MUON' : '!',
	'ELECTRON_NEUTRINO' : 'U',
	'ANTI_ELECTRON_NEUTRINO' : '<',
	'MUON_NEUTRINO' : 'V',
	'ANTI_MUON_NEUTRINO' : '>',
	'PROTON' : 'H',
	'ANTI_PROTON' : 'G',
	'LAMBDA_BARYON' : 'L',
	'ANTI_LAMBDA_BARYON' : 'B',
	'POSITIVE_SIGMA_BARYON' : '+',
	'ANTI_POSITIVE_SIGMA_BARYON' : '_',
	'NEGATIVE_SIGMA_BARYON' : '-',
	'ANTI_NEGATIVE_SIGMA_BARYON' : '~',
	'XI_BARYON' : 'X',
	'ANTI_NEUTRAL_XI_BARYON' : 'C',
	'NEGATIVE_XI_BARYON' : 'Y',
	'POSITIVE_XI_BARYON' : 'W',
	'OMEGA_BARYON' : 'O',
	'ANTI_OMEGA_BARYON' : '@',
	'POSITIVE_PION' : '/',
	'NEGATIVE_PION' : '*',
	'NEUTRAL_PION' : 'Z',
	'POSITIVE_KAON' : 'K',
	'NEGATIVE_KAON' : '?',
	'KAON_SHORT' : '%',
	'KAON_LONG' : '^',
	'DEUTERON' : 'D',
	'TRITION' : 'T',
	'HELION' : 'S',
	'ALPHA' : 'A',
	'HEAVY_IONS' : '#'
}

class SourceSetting(ABC):
    """
    """
    
class CriticalitySource(CriticalitySourceBase, SourceSetting):
    """
    A representation of the model object `CriticalitySource`.
    
    Parameters
    ----------
    histories : float
        Histories for `CriticalitySource`.
    j_histories : str
        J_histories for `CriticalitySource`.
    keff_guess : float
        KeffGuess for `CriticalitySource`.
    j_keff_guess : str
        J_keffGuess for `CriticalitySource`.
    skip_cycles : float
        SkipCycles for `CriticalitySource`.
    j_skip_cycles : str
        J_skipCycles for `CriticalitySource`.
    cycles : float
        Cycles for `CriticalitySource`.
    j_cycles : str
        J_cycles for `CriticalitySource`.
    source_point_count : int
        SourcePointCount for `CriticalitySource`.
    j_source_point_count : str
        J_sourcePointCount for `CriticalitySource`.
    normalize_tallies : str
        NormalizeTallies for `CriticalitySource`.
    j_normalize_tallies : str
        J_normalizeTallies for `CriticalitySource`.
    max_cycles : int
        MaxCycles for `CriticalitySource`.
    j_max_cycles : str
        J_maxCycles for `CriticalitySource`.
    average_by_cycles : str
        AverageByCycles for `CriticalitySource`.
    j_average_by_cycles : str
        J_averageByCycles for `CriticalitySource`.
    
    """

    def _init(self, **kwargs):
        """KCODE
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'KCODE\n'
        string += 'Histories: ' + str(self.histories) + '\n'
        string += 'Guess: ' + str(self.keff_guess) + '\n'
        string += 'Skip Cycles: ' + str(self.skip_cycles) + '\n'
        string += 'Total Cycles: ' + str(self.cycles) + '\n'
        string += 'Source Points: ' + str(self.source_point_count) + '\n'
        string += 'Normalize: ' + str(self.normalize_tallies) + '\n'
        string += 'Max Cycles: ' + str(self.max_cycles) + '\n'
        string += 'Averaged: ' + str(self.average_by_cycles) + '\n'

        return string

    def __repr__(self) -> str:
        return str(self)

class CriticalitySourcePoints(CriticalitySourcePointsBase, SourceSetting):
    """
    A representation of the model object `CriticalitySourcePoints`.
    
    Parameters
    ----------
    points : iterable of mcnpy.Point
        Points for `CriticalitySourcePoints`.
    
    """
    
    def _init(self, points):
        self.points = []
        for p in points:
            if isinstance(p, Point) is False:
                p = Point.aspoint(p)
            self.points.append(p)

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return str(self)

class CriticalityOptions(CriticalityOptionsBase, SourceSetting):
    """
    A representation of the model object `CriticalityOptions`.
    
    Parameters
    ----------
    outer_cycles : int
        OuterCycles for `CriticalityOptions`.
    kinetics : mcnpy.YesNo
        Kinetics for `CriticalityOptions`.
    precursor : mcnpy.YesNo
        Precursor for `CriticalityOptions`.
    sensitivity_profile : mcnpy.CriticalityOptionsSensitivityProfile
        SensitivityProfile for `CriticalityOptions`.
    fmat : mcnpy.YesNo
        Fmat for `CriticalityOptions`.
    fmat_skip : int
        Fmat_skip for `CriticalityOptions`.
    fmat_ncyc : int
        Fmat_ncyc for `CriticalityOptions`.
    fmat_space : int
        Fmat_space for `CriticalityOptions`.
    fmat_accel : mcnpy.YesNo
        Fmat_accel for `CriticalityOptions`.
    fmat_reduce : mcnpy.YesNo
        Fmat_reduce for `CriticalityOptions`.
    fmat_nx : int
        Fmat_nx for `CriticalityOptions`.
    fmat_ny : int
        Fmat_ny for `CriticalityOptions`.
    fmat_nz : int
        Fmat_nz for `CriticalityOptions`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
        
#TODO: Better distribution support
class Source(SourceBase, SourceSetting):
    """
    A representation of the model object `Source`.
    
    Parameters
    ----------
    dependent_cel : mcnpy.DependentDistributionPos
        DependentCel for `Source`.
    cells : iterable of mcnpy.SourceCell
        Cells for `Source`.
    dependent_sur : mcnpy.DependentDistributionPos
        DependentSur for `Source`.
    surface : mcnpy.Tally.Bin.UnarySurfaceBin
        Surface for `Source`.
    surfaces : mcnpy.Distributions
        Surfaces for `Source`.
    dependent_erg : mcnpy.DependentDistribution
        DependentErg for `Source`.
    energy : float
        Energy for `Source`.
    energies : mcnpy.Distributions
        Energies for `Source`.
    dependent_tme : mcnpy.DependentDistribution
        DependentTme for `Source`.
    time : float
        Time for `Source`.
    times : mcnpy.Distributions
        Times for `Source`.
    dependent_dir : mcnpy.DependentDistribution
        DependentDir for `Source`.
    cosine : float
        Cosine for `Source`.
    cosines : mcnpy.Distributions
        Cosines for `Source`.
    dependent_vec : mcnpy.DependentDistribution
        DependentVec for `Source`.
    vector : mcnpy.Point
        Vector for `Source`.
    vectors : mcnpy.Distributions
        Vectors for `Source`.
    dependent_nrm : mcnpy.DependentDistribution
        DependentNrm for `Source`.
    direction : float
        Direction for `Source`.
    directions : mcnpy.Distributions
        Directions for `Source`.
    dependent_pos : mcnpy.DependentDistributionPos
        DependentPos for `Source`.
    position : mcnpy.Point
        Position for `Source`.
    points : mcnpy.Distributions
        Points for `Source`.
    volumer : str
        Volumer for `Source`.
    dependent_rad : mcnpy.DependentDistributionPos
        DependentRad for `Source`.
    radial_distance : float
        RadialDistance for `Source`.
    radial_distances : mcnpy.Distributions
        RadialDistances for `Source`.
    dependent_ext : mcnpy.DependentDistributionPos
        DependentExt for `Source`.
    extent : float
        Extent for `Source`.
    extents : mcnpy.Distributions
        Extents for `Source`.
    dependent_axs : mcnpy.DependentDistributionPos
        DependentAxs for `Source`.
    axis : mcnpy.Point
        Axis for `Source`.
    axes : mcnpy.Distributions
        Axes for `Source`.
    dependent_x : mcnpy.DependentDistributionPos
        DependentX for `Source`.
    x_coord : float
        XCoord for `Source`.
    x_coords : mcnpy.Distributions
        XCoords for `Source`.
    dependent_y : mcnpy.DependentDistributionPos
        DependentY for `Source`.
    y_coord : float
        YCoord for `Source`.
    y_coords : mcnpy.Distributions
        YCoords for `Source`.
    dependent_z : mcnpy.DependentDistributionPos
        DependentZ for `Source`.
    z_coord : float
        ZCoord for `Source`.
    z_coords : mcnpy.Distributions
        ZCoords for `Source`.
    dependent_ccc : mcnpy.DependentDistributionPos
        DependentCcc for `Source`.
    cookie_cutter_cell : mcnpy.Cell
        CookieCutterCell for `Source`.
    cookie_cutter_cells : mcnpy.Distributions
        CookieCutterCells for `Source`.
    dependent_ara : mcnpy.DependentDistribution
        DependentAra for `Source`.
    area : float
        Area for `Source`.
    areas : mcnpy.Distributions
        Areas for `Source`.
    dependent_wgt : mcnpy.DependentDistribution
        DependentWgt for `Source`.
    weight : float
        Weight for `Source`.
    weights : mcnpy.Distributions
        Weights for `Source`.
    dependent_tr : mcnpy.DependentDistribution
        DependentTr for `Source`.
    transformation : mcnpy.Transformation
        Transformation for `Source`.
    transformations : mcnpy.Distributions
        Transformations for `Source`.
    dependent_eff : mcnpy.DependentDistribution
        DependentEff for `Source`.
    rejection_efficiency : float
        RejectionEfficiency for `Source`.
    rejection_efficiencies : mcnpy.Distributions
        RejectionEfficiencies for `Source`.
    dependent_par : mcnpy.DependentDistribution
        DependentPar for `Source`.
    particles : mcnpy.Distributions
        Particles for `Source`.
    normalize : mcnpy.Boolean
        Normalize for `Source`.
    particle : mcnpy.SourceParticle
        Particle for `Source`.
    month : int
        Month for `Source`.
    day : int
        Day for `Source`.
    year : int
        Year for `Source`.
    lattitude : float
        Lattitude for `Source`.
    longitude : float
        Longitude for `Source`.
    altitude : float
        Altitude for `Source`.
    x_beam_emittance : float
        XBeamEmittance for `Source`.
    y_beam_emittance : float
        YBeamEmittance for `Source`.
    beam_distance : float
        BeamDistance for `Source`.
    x_beam_aperature : float
        XBeamAperature for `Source`.
    y_beam_aperature : float
        YBeamAperature for `Source`.
    u : float
        U for `Source`.
    
    """

    def _init(self, **kwargs):
        for k in kwargs:
            if k.lower() == 'loc':
                self.lattitude = kwargs[k][0]
                self.longitude = kwargs[k][1]
                self.altitude = kwargs[k][2]
            elif k.lower() == 'ara':
                self.area = kwargs[k]
            elif k.lower() == 'axs':
                if isinstance(kwargs[k], Point):
                    self.axis = kwargs[k]
                else:
                    #self.axis = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.axis = Point.aspoint(kwargs[k])
            elif k.lower() == 'bem':
                self.x_beam_emittance = kwargs[k][0]
                self.y_beam_emittance = kwargs[k][1]
                self.beam_distance = kwargs[k][2]
            elif k.lower() == 'cel':
                self.cells = kwargs[k]
            elif k.lower() == 'ccc':
                self.cookie_cutter_cell = kwargs[k]
            elif k.lower() == 'dir':
                self.cosine = kwargs[k]
            elif k.lower() == 'dat':
                self.month = kwargs[k][0]
                self.day = kwargs[k][1]
                self.year = kwargs[k][2]
            elif k.lower() == 'nrm':
                self.direction = kwargs[k]
            elif k.lower() == 'erg':
                self.energy = kwargs[k]
            elif k.lower() == 'ext':
                self.extent = kwargs[k]
            elif k.lower() == 'par':
                self.particle = SourceParticle(kwargs[k])
            elif k.lower() == 'pos':
                if isinstance(kwargs[k], Point):
                    self.position = kwargs[k]
                else:
                    #self.position = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.position = Point.aspoint(kwargs[k])
            elif k.lower() == 'rad':
                self.radial_distance = kwargs[k]
            elif k.lower() == 'eff':
                self.rejection_efficiency = kwargs[k]
            elif k.lower() == 'sur':
                self.surface = kwargs[k]
            elif k.lower() == 'tme':
                self.time = kwargs[k]
            elif k.lower() == 'tr':
                self.transformation = kwargs[k]
            elif k.lower() == 'bap':
                self.x_beam_aperature = kwargs[k][0]
                self.y_beam_aperature = kwargs[k][1]
                self.u = kwargs[k][2]
            elif k.lower() == 'vec':
                if isinstance(kwargs[k], Point):
                    self.vector = kwargs[k]
                else:
                    #self.vector = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.vector = Point.aspoint(kwargs[k])
            elif k.lower() == 'wgt':
                self.weight = kwargs[k]
            elif k.lower() == 'x':
                self.x_coord = kwargs[k]
            elif k.lower() == 'y':
                self.y_coord = kwargs[k]
            elif k.lower() == 'z':
                self.z_coord = kwargs[k]
            elif k.lower() == 'normalize':
                self.normal = kwargs[k]
            else:
                setattr(self, k.lower(), kwargs[k])

        """def __str__(self):
            string = 

            return string

        def __repr__(self):
            return str(self)"""

class SourceParticle(SourceParticleBase):
    """
    A representation of the model object `SourceParticle`.
    
    Parameters
    ----------
    particle : mcnpy.SourceParticleCategory
        Particle for `SourceParticle`.
    ion : str
        Ion for `SourceParticle`.
    
    """
    
    def _init(self, par):
        """
        """
        # For when an enum is used.
        if str(par).upper() in PARTICLE.keys() or str(par).upper() in PARTICLE.values():
            self.particle = par
        # For when a ZAID is used.
        else:
            self.ion = int(element_to_zaid(str(par)))

    @property
    def particle(self):
        return self._e_object.getParticle()

    @particle.setter
    def particle(self, par):
        ePackage = mcnpy.wrap.package
        if isinstance(par, Enum):
            self._e_object.setParticle(par)
            self.ion = None
        elif isinstance(par, str):
            if par.upper() in PARTICLE or par.upper() in PARTICLE.values():
                self._e_object.setParticle(par)
                self._e_object.eUnset(ePackage.SOURCE_PARTICLE__ION)
        else:
            self._e_object.eUnset(ePackage.SOURCE_PARTICLE__PARTICLE)
            self._e_object.setIon(int(element_to_zaid(str(par))))

    @property
    def ion(self):
        return self._e_object.getIon()

    @ion.setter
    def ion(self, par):
        ePackage = mcnpy.wrap.package
        self._e_object.setIon(int(element_to_zaid(str(par))))
        self._e_object.eUnset(ePackage.SOURCE_PARTICLE__PARTICLE)

    def __str__(self):
        if self.ion is not None:
            string = zaid_to_element(self.ion)
        elif self.particle is not None:
            string = str(self.particle)
        else:
            string = ''
        
        return string

    def __repr__(self):
            return str(self)

class SourceInfo(SourceInfoBase, SourceSetting):
    """
    A representation of the model object `SourceInfo`.
    
    Parameters
    ----------
    name : int
        Name for `SourceInfo`.
    option : mcnpy.SourceInfoOption
        Option for `SourceInfo`.
    values : iterable of float
        Values for `SourceInfo`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    
    class Cells(SourceInfoCellsBase, SourceSetting):
        """
        A representation of the model object `SourceInfo.Cells`.
        
        Parameters
        ----------
        cells : mcnpy.Tally.Bin.CellBins
            Cells for `SourceInfo.Cells`.
        u_m_cells : iterable of str
            UMCells for `SourceInfo.Cells`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Distributions(SourceInfoDistributionsBase, SourceSetting):
        """
        A representation of the model object `SourceInfo.Distributions`.
        
        Parameters
        ----------
        distributions : iterable of Object
            Distributions for `SourceInfo.Distributions`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Particles(SourceInfoParticlesBase, SourceSetting):
        """
        A representation of the model object `SourceInfo.Particles`.
        
        Parameters
        ----------
        particles : iterable of mcnpy.SourceParticle
            Particles for `SourceInfo.Particles`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class SourceProbability(SourceProbabilityBase, SourceSetting):
    """
    A representation of the model object `SourceProbability`.
    
    Parameters
    ----------
    name : int
        Name for `SourceProbability`.
    option : mcnpy.SourceProbabilityOption
        Option for `SourceProbability`.
    values : iterable of float
        Values for `SourceProbability`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    
    class Function(SourceProbabilityFunctionBase, SourceSetting):
        """
        A representation of the model object `SourceProbability.Function`.
        
        Parameters
        ----------
        function : str
            Function for `SourceProbability.Function`.
        a : float
            A for `SourceProbability.Function`.
        b : float
            B for `SourceProbability.Function`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class SourceBias(SourceBiasBase, SourceSetting):
    """
    A representation of the model object `SourceBias`.
    
    Parameters
    ----------
    name : int
        Name for `SourceBias`.
    option : mcnpy.SourceProbabilityOption
        Option for `SourceBias`.
    values : iterable of float
        Values for `SourceBias`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    
    class Function(SourceBiasFunctionBase, SourceSetting):
        """
        A representation of the model object `SourceBias.Function`.
        
        Parameters
        ----------
        function : str
            Function for `SourceBias.Function`.
        a : float
            A for `SourceBias.Function`.
        b : float
            B for `SourceBias.Function`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class SourceComment(SourceCommentBase, SourceSetting):
    """
    A representation of the model object `SourceComment`.
    
    Parameters
    ----------
    distribution : mcnpy.Distribution
        Distribution for `SourceComment`.
    comment : iterable of str
        Comment for `SourceComment`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EntropyMesh(EntropyMeshBase, SourceSetting):
    """
    A representation of the model object `EntropyMesh`.
    
    Parameters
    ----------
    nx : int
        Nx for `EntropyMesh`.
    x0 : float
        X0 for `EntropyMesh`.
    x1 : float
        X1 for `EntropyMesh`.
    ny : int
        Ny for `EntropyMesh`.
    y0 : float
        Y0 for `EntropyMesh`.
    y1 : float
        Y1 for `EntropyMesh`.
    nz : int
        Nz for `EntropyMesh`.
    z0 : float
        Z0 for `EntropyMesh`.
    z1 : float
        Z1 for `EntropyMesh`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Depletion(DepletionBase, SourceSetting):
    """
    A representation of the model object `Depletion`.
    
    Parameters
    ----------
    times : iterable of float
        Times for `Depletion`.
    power_fraction : iterable of float
        PowerFraction for `Depletion`.
    materials : iterable of mcnpy.Depletion.Material
        Materials for `Depletion`.
    power : float
        Power for `Depletion`.
    omitted_isotopes : mcnpy.Depletion.OmittedIsotopes
        OmittedIsotopes for `Depletion`.
    min_atom_fraction : float
        MinAtomFraction for `Depletion`.
    cinder_convergence : float
        CinderConvergence for `Depletion`.
    q_multiplier : float
        QMultiplier for `Depletion`.
    tier : int
        Tier for `Depletion`.
    high_energy_physics : str
        HighEnergyPhysics for `Depletion`.
    volumes : iterable of float
        Volumes for `Depletion`.
    material_modification : str
        MaterialModification for `Depletion`.
    fill_modification : str
        FillModification for `Depletion`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    
    class Material(DepletionMaterialBase, SourceSetting):
        """
        A representation of the model object `Depletion.Material`.
        
        Parameters
        ----------
        power_only : mcnpy.Boolean
            PowerOnly for `Depletion.Material`.
        material : mcnpy.Material
            Material for `Depletion.Material`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class OmittedIsotopes(DepletionOmittedIsotopesBase, SourceSetting):
        """
        A representation of the model object `Depletion.OmittedIsotopes`.
        
        Parameters
        ----------
        material : mcnpy.Material
            Material for `Depletion.OmittedIsotopes`.
        isotopes_count : int
            IsotopesCount for `Depletion.OmittedIsotopes`.
        isotopes : iterable of str
            Isotopes for `Depletion.OmittedIsotopes`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class SourceCell(SourceCellBase, SourceSetting):
    """
    A representation of the model object `SourceCell`.
    
    Parameters
    ----------
    z_cell : int
        ZCell for `SourceCell`.
    coordinates : str
        Coordinates for `SourceCell`.
    cell : mcnpy.Tally.Bin.UnaryCellBin
        Cell for `SourceCell`.
    distribution : mcnpy.Distribution
        Distribution for `SourceCell`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceDist(SourceDistBase, SourceSetting):
    """
    A representation of the model object `SourceDist`.
    
    Parameters
    ----------
    distribution : mcnpy.Distribution
        Distribution for `SourceDist`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceID(SourceIDBase, SourceSetting):
    """
    A representation of the model object `SourceID`.
    
    Parameters
    ----------
    keyword : mcnpy.SrcKeyword
        Keyword for `SourceID`.
    name : int
        Name for `SourceID`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SurfaceSource():
    """"""
    class Write(SurfaceSourceWriteBase, SourceSetting):
        """
        A representation of the model object `SurfaceSource.Write`.
        
        Parameters
        ----------
        crossings : iterable of mcnpy.SurfaceSource.WriteCrossing
            Crossings for `SurfaceSource.Write`.
        symmetry : str
            Symmetry for `SurfaceSource.Write`.
        particles : iterable of mcnpy.Particle
            Particles for `SurfaceSource.Write`.
        fission_cells : iterable of mcnpy.Cell
            FissionCells for `SurfaceSource.Write`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Read(SurfaceSourceReadBase, SourceSetting):
        """
        A representation of the model object `SurfaceSource.Read`.
        
        Parameters
        ----------
        surfaces_old : iterable of mcnpy.Surface
            SurfacesOld for `SurfaceSource.Read`.
        fission_cells : iterable of mcnpy.Cell
            FissionCells for `SurfaceSource.Read`.
        surfaces_new : iterable of mcnpy.Surface
            SurfacesNew for `SurfaceSource.Read`.
        collision : str
            Collision for `SurfaceSource.Read`.
        weight : float
            Weight for `SurfaceSource.Read`.
        transformation : mcnpy.Transformation
            Transformation for `SurfaceSource.Read`.
        transformations : mcnpy.Distribution
            Transformations for `SurfaceSource.Read`.
        psc : float
            Psc for `SurfaceSource.Read`.
        axis : mcnpy.Vector
            Axis for `SurfaceSource.Read`.
        cosines : mcnpy.Distribution
            Cosines for `SurfaceSource.Read`.
        angular_threshold : float
            AngularThreshold for `SurfaceSource.Read`.
        cylindrical_window : mcnpy.SurfaceSource.ReadCylindricalWindow
            CylindricalWindow for `SurfaceSource.Read`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class ReadCylindricalWindow(SurfaceSourceReadCylindricalWindowBase):
        """
        A representation of the model object `SurfaceSource.ReadCylindricalWindow`.
        
        Parameters
        ----------
        radius : float
            Radius for `SurfaceSource.ReadCylindricalWindow`.
        z0 : float
            Z0 for `SurfaceSource.ReadCylindricalWindow`.
        z1 : float
            Z1 for `SurfaceSource.ReadCylindricalWindow`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class WriteCrossing(SurfaceSourceWriteCrossingBase):
        """
        A representation of the model object `SurfaceSource.WriteCrossing`.
        
        Parameters
        ----------
        direction : mcnpy.PositiveNegative
            Direction for `SurfaceSource.WriteCrossing`.
        surface : mcnpy.Surface
            Surface for `SurfaceSource.WriteCrossing`.
        from_cells : iterable of mcnpy.SurfaceSource.WriteFromCell
            FromCells for `SurfaceSource.WriteCrossing`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class WriteFromCell(SurfaceSourceWriteFromCellBase):
        """
        A representation of the model object `SurfaceSource.WriteFromCell`.
        
        Parameters
        ----------
        direction : mcnpy.PositiveNegative
            Direction for `SurfaceSource.WriteFromCell`.
        cell : mcnpy.Cell
            Cell for `SurfaceSource.WriteFromCell`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class Distribution(DistributionBase):
    """
    A representation of the model object `Distribution`.
    
    Parameters
    ----------
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Distributions(DistributionsBase):
    """
    A representation of the model object `Distributions`.
    
    Parameters
    ----------
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSource():
    """"""
    class Volumer(DependentSourceVolumerBase):
        """
        A representation of the model object `DependentSource.Volumer`.
        
        Parameters
        ----------
        u_m_cells : iterable of str
            UMCells for `DependentSource.Volumer`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Particles(DependentSourceParticlesBase):
        """
        A representation of the model object `DependentSource.Particles`.
        
        Parameters
        ----------
        particles : iterable of mcnpy.SourceParticle
            Particles for `DependentSource.Particles`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Distributions(DependentSourceDistributionsBase):
        """
        A representation of the model object `DependentSource.Distributions`.
        
        Parameters
        ----------
        distributions : iterable of mcnpy.Distribution
            Distributions for `DependentSource.Distributions`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Cells(DependentSourceCellsBase):
        """
        A representation of the model object `DependentSource.Cells`.
        
        Parameters
        ----------
        cells : mcnpy.Tally.Bin.CellBins
            Cells for `DependentSource.Cells`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class Distribution(DependentSourceDistributionBase, SourceSetting):
        """
        A representation of the model object `DependentSource.Distribution`.
        
        Parameters
        ----------
        name : int
            Name for `DependentSource.Distribution`.
        option : mcnpy.DependentSource.DistributionOption
            Option for `DependentSource.Distribution`.
        values : iterable of float
            Values for `DependentSource.Distribution`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class DistributionBins(DependentSourceDistributionBinsBase):
        """
        A representation of the model object `DependentSource.DistributionBins`.
        
        Parameters
        ----------
        bins : iterable of float
            Bins for `DependentSource.DistributionBins`.
        distributions : iterable of mcnpy.ZeroDist
            Distributions for `DependentSource.DistributionBins`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class DistributionMatches(DependentSourceDistributionMatchesBase):
        """
        A representation of the model object `DependentSource.DistributionMatches`.
        
        Parameters
        ----------
        independent : iterable of float
            Independent for `DependentSource.DistributionMatches`.
        dependent : iterable of float
            Dependent for `DependentSource.DistributionMatches`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class NestedDistribution(NestedDistributionBase):
    """
    A representation of the model object `NestedDistribution`.
    
    Parameters
    ----------
    distributions : iterable of mcnpy.SourceDist
        Distributions for `NestedDistribution`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ZeroDist(ZeroDistBase):
    """
    A representation of the model object `ZeroDist`.
    
    Parameters
    ----------
    dist : mcnpy.Distribution
        Dist for `ZeroDist`.
    
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

subclass_overrides(SurfaceSource)
subclass_overrides(SourceProbability)
subclass_overrides(SourceBias)
subclass_overrides(DependentSource)
subclass_overrides(SourceInfo)
subclass_overrides(Depletion)