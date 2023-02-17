from abc import ABC
from enum import Enum
from .wrap import wrappers, overrides, subclass_overrides
from .wrap import package as ePackage
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

def _list_to_dist(values):
    """Function to convert lists into Distributions"""
    return Distributions(distributions=values)

def _dist_to_list(dist):
    """Function to convert Distributions to lists"""
    if dist is not None:
        return dist.distributions
    else:
        return None

class SourceSetting(ABC):
    """
    """

class Distribution(DistributionBase):
    """
    A representation of the model object `Distribution`.
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
        The `cells` distribution is a function of `dependent_cel`.
    cells : iterable of mcnpy.SourceCell
        Cells for `Source`.
    dependent_sur : mcnpy.DependentDistributionPos
        The `surfaces` distribution is a function of `dependent_sur`.
    surface : mcnpy.Tally.Bin.UnarySurfaceBin
        Surface for `Source`.
    surfaces : mcnpy.Distributions
        Surface distribution for `Source`.
    dependent_erg : mcnpy.DependentDistribution
        The `energies` distribution is a function of `dependent_erg`.
    energy : float
        Kinetic energy for `Source`.
    energies : mcnpy.Distributions
        Energy distribution for `Source`.
    dependent_tme : mcnpy.DependentDistribution
        The `times` distribution is a function of `dependent_tme`.
    time : float
        Time (in shakes) for `Source`.
    times : mcnpy.Distributions
        Time distribution for `Source`.
    dependent_dir : mcnpy.DependentDistribution
        The `cosines` distribution is a function of `dependent_dir`.
    cosine : float
        Cosine of the angle between `vector` and the particle's direction of flight.
    cosines : mcnpy.Distributions
        Cosine (angular) distribution for `Source`.
    dependent_vec : mcnpy.DependentDistribution
        The `vectors` distribution is a function of `dependent_vec`.
    vector : mcnpy.Point
        Reference vector for `cosine`.
    vectors : mcnpy.Distributions
        Vectors for `Source`.
    dependent_nrm : mcnpy.DependentDistribution
        The `directions` distribution is a function of `dependent_nrm`.
    direction : float
        Sign of the surface normal.
    directions : mcnpy.Distributions
        Distribution of surface normals for `Source`.
    dependent_pos : mcnpy.DependentDistributionPos
        The `positions` distribution is a function of `dependent_pos`.
    position : mcnpy.Point
        Position reference point.
    points : mcnpy.Distributions
        Position distribution for `Source`.
    volumer : str
        Volumer for `Source`.
    dependent_rad : mcnpy.DependentDistributionPos
        The `radial_distances` distribution is a function of `dependent_rad`.
    radial_distance : float
        Radial distance of the position from `position` or `axis`.
    radial_distances : mcnpy.Distributions
        RadialDistances for `Source`.
    dependent_ext : mcnpy.DependentDistributionPos
        The `extents` distribution is a function of `dependent_ext`.
    extent : float
        For a volume source, the distance from `position` along `axis`. For a surface source, the cosine of angle from `axis`.
    extents : mcnpy.Distributions
        Distribution of extents for `Source`.
    dependent_axs : mcnpy.DependentDistributionPos
        The `axes` distribution is a function of `dependent_axs`.
    axis : mcnpy.Point
        Reference vector for `extent` and `radial_distance`.
    axes : mcnpy.Distributions
        Distribution of axes for `Source`.
    dependent_x : mcnpy.DependentDistributionPos
        The `x_coords` distribution is a function of `dependent_x`.
    x_coord : float
        X-coordinate of the position.
    x_coords : mcnpy.Distributions
        Distribution of x-coordinates.
    dependent_y : mcnpy.DependentDistributionPos
        The `y_coords` distribution is a function of `dependent_y`.
    y_coord : float
        Y-coordinate of the position.
    y_coords : mcnpy.Distributions
        Distribution of y-coordinates.
    dependent_z : mcnpy.DependentDistributionPos
        The `z_coords` distribution is a function of `dependent_z`.
    z_coord : float
        Z-coordinate of the position.
    z_coords : mcnpy.Distributions
        Distribution of z-coordinates.
    dependent_ccc : mcnpy.DependentDistributionPos
        The `cookie_cutter_cells` distribution is a function of `dependent_ccc`.
    cookie_cutter_cell : mcnpy.Cell
        CookieCutterCell for `Source`.
    cookie_cutter_cells : mcnpy.Distributions
        Distribution of CookieCutterCells for `Source`.
    dependent_ara : mcnpy.DependentDistribution
        The `areas` distribution is a function of `dependent_ara`.
    area : float
        Area of surface.
    areas : mcnpy.Distributions
        Distribution of surface areas for `Source`.
    dependent_wgt : mcnpy.DependentDistribution
        The `weights` distribution is a function of `dependent_wgt`.
    weight : float
        Particle weight for `Source`.
    weights : mcnpy.Distributions
        Distribution of particle weights for `Source`.
    dependent_tr : mcnpy.DependentDistribution
        The `transformations` distribution is a function of `dependent_tr`.
    transformation : mcnpy.Transformation
        Source particle transformation for `Source`.
    transformations : mcnpy.Distributions
        Distribution of source particle transformations for `Source`.
    dependent_eff : mcnpy.DependentDistribution
        The `rejection_efficiencies` distribution is a function of `dependent_eff`.
    rejection_efficiency : float
        Rejection efficiency for `Source`.
    rejection_efficiencies : mcnpy.Distributions
        Distribution of rejection efficiencies for `Source`.
    dependent_par : mcnpy.DependentDistribution
        The `particles` distribution is a function of `dependent_par`.
    particles : mcnpy.Distributions
        Distribution of source particles for `Source`.
    normalize : boolean
        Source particle weight normalization.
    particle : mcnpy.SourceParticleCategory or mcnpy.SourceParticle
        Source particle for `Source`. Refer to `mcnpy.SourceParticleCategory` for a list of accepted particle types. Heavy ions may also be specified symbolically or by ZAID. E.g. uranium-235 could be specified as `"u235"`, `"U235"`, or `92235`. `U[235]` is also valid if `U` from `mcnpy.elements` has been imported.
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

    @property
    def cells(self):
        """"""
        return _dist_to_list(self._e_object.getCells())

    @cells.setter
    def cells(self, value):
        if isinstance(value, list):
            self._e_object.setCells(_list_to_dist(value))
        else:
            self._e_object.setCells(value)

    @property
    def energy(self):
        """"""
        return self._e_object.getEnergy()

    @energy.setter
    def energy(self, value):
        """"""
        self._e_object.setEnergy(float(value))
        self._e_object.eUnset(ePackage.SOURCE__ENERGIES)

    @property
    def energies(self):
        return _dist_to_list(self._e_object.getEnergies())

    @energies.setter
    def energies(self, value):
        if isinstance(value, list):
            self._e_object.setEnergies(_list_to_dist(value))
        else:
            self._e_object.setEnergies(value)
        self._e_object.eUnset(ePackage.SOURCE__ENERGY)

    @property
    def surface(self):
        """"""
        return self._e_object.getSurface()

    @surface.setter
    def surface(self, value):
        """"""
        self._e_object.setSurface(value)
        self._e_object.eUnset(ePackage.SOURCE__SURFACES)

    @property
    def surfaces(self):
        return _dist_to_list(self._e_object.getSurfaces())

    @surfaces.setter
    def surfaces(self, value):
        if isinstance(value, list):
            self._e_object.setSurfaces(_list_to_dist(value))
        else:
            self._e_object.setSurfaces(value)
        self._e_object.eUnset(ePackage.SOURCE__SURFACE)

    @property
    def transformation(self):
        """"""
        return self._e_object.getTransformation()

    @transformation.setter
    def transformation(self, value):
        """"""
        self._e_object.setTransformation(value)
        self._e_object.eUnset(ePackage.SOURCE__TRANSFORMATIONS)

    @property
    def transformations(self):
        return _dist_to_list(self._e_object.getTransformations())

    @transformations.setter
    def transformations(self, value):
        if isinstance(value, list):
            self._e_object.setTransformations(_list_to_dist(value))
        else:
            self._e_object.setTransformations(value)
        self._e_object.eUnset(ePackage.SOURCE__TRANSFORMATION)

    @property
    def particle(self):
        """"""
        return self._e_object.getParticle().particle

    @particle.setter
    def particle(self, value):
        """"""
        if isinstance(value, SourceParticle):
            self._e_object.setParticle(value)
        else:
            self._e_object.setParticle(SourceParticle(value))
        self._e_object.eUnset(ePackage.SOURCE__PARTICLES)

    @property
    def particles(self):
        return _dist_to_list(self._e_object.getParticles())

    @particles.setter
    def particles(self, value):
        if isinstance(value, list):
            self._e_object.setParticles(_list_to_dist(value))
        else:
            self._e_object.setParticles(value)
        self._e_object.eUnset(ePackage.SOURCE__PARTICLE)

    @property
    def time(self):
        """"""
        return self._e_object.getTime()

    @time.setter
    def time(self, value):
        """"""
        self._e_object.setTime(float(value))
        self._e_object.eUnset(ePackage.SOURCE__TIMES)

    @property
    def times(self):
        return _dist_to_list(self._e_object.getTimes())

    @times.setter
    def times(self, value):
        if isinstance(value, list):
            self._e_object.setTimes(_list_to_dist(value))
        else:
            self._e_object.setTimes(value)
        self._e_object.eUnset(ePackage.SOURCE__TIME)

    @property
    def cosine(self):
        """"""
        return self._e_object.getCosine()

    @cosine.setter
    def cosine(self, value):
        """"""
        self._e_object.setCosine(float(value))
        self._e_object.eUnset(ePackage.SOURCE__COSINES)

    @property
    def cosines(self):
        return _dist_to_list(self._e_object.getCosines())

    @cosines.setter
    def cosines(self, value):
        if isinstance(value, list):
            self._e_object.setCosines(_list_to_dist(value))
        else:
            self._e_object.setCosines(value)
        self._e_object.eUnset(ePackage.SOURCE__COSINE)

    @property
    def vector(self):
        """"""
        return self._e_object.getVector().aslist()

    @vector.setter
    def vector(self, value):
        """"""
        if isinstance(value, Point):
            self._e_object.setVector(value)
        else:
            self._e_object.setVector(Point.aspoint(value))
        self._e_object.eUnset(ePackage.SOURCE__VECTORS)

    @property
    def vectors(self):
        return _dist_to_list(self._e_object.getVectors())

    @vectors.setter
    def vectors(self, value):
        if isinstance(value, list):
            self._e_object.setVectors(_list_to_dist(value))
        else:
            self._e_object.setVectors(value)
        self._e_object.eUnset(ePackage.SOURCE__VECTOR)

    @property
    def direction(self):
        """"""
        return self._e_object.getDirection()

    @direction.setter
    def direction(self, value):
        """"""
        if value >= 0:
            value = 1
        else:
            value = -1
        self._e_object.setDirection(float(value))
        self._e_object.eUnset(ePackage.SOURCE__DIRECTIONS)

    @property
    def directions(self):
        return _dist_to_list(self._e_object.getDirections())

    @directions.setter
    def directions(self, value):
        if isinstance(value, list):
            self._e_object.setDirections(_list_to_dist(value))
        else:
            self._e_object.setDirections(value)
        self._e_object.eUnset(ePackage.SOURCE__DIRECTION)

    @property
    def position(self):
        """"""
        return self._e_object.getPosition().aslist()

    @position.setter
    def position(self, value):
        """"""
        if isinstance(value, Point):
            self._e_object.setPosition(value)
        else:
            self._e_object.setPosition(Point.aspoint(value))
        self._e_object.eUnset(ePackage.SOURCE__POINTS)

    @property
    def points(self):
        return _dist_to_list(self._e_object.getPoints())

    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self._e_object.setPoints(_list_to_dist(value))
        else:
            self._e_object.setPoints(value)
        self._e_object.eUnset(ePackage.SOURCE__POSITION)

    @property
    def radial_distance(self):
        """"""
        return self._e_object.getTime()

    @radial_distance.setter
    def radial_distance(self, value):
        """"""
        self._e_object.setRadialDistance(float(value))
        self._e_object.eUnset(ePackage.SOURCE__RADIAL_DISTANCES)

    @property
    def radial_distances(self):
        return _dist_to_list(self._e_object.getRadialDistances())

    @radial_distances.setter
    def radial_distances(self, value):
        if isinstance(value, list):
            self._e_object.setRadialDistances(_list_to_dist(value))
        else:
            self._e_object.setRadialDistances(value)
        self._e_object.eUnset(ePackage.SOURCE__RADIAL_DISTANCE)

    @property
    def extent(self):
        """"""
        return self._e_object.getExtent()

    @extent.setter
    def extent(self, value):
        """"""
        self._e_object.setExtent(float(value))
        self._e_object.eUnset(ePackage.SOURCE__EXTENTS)

    @property
    def extents(self):
        return _dist_to_list(self._e_object.getExtents())

    @extents.setter
    def extents(self, value):
        if isinstance(value, list):
            self._e_object.setExtents(_list_to_dist(value))
        else:
            self._e_object.setExtents(value)
        self._e_object.eUnset(ePackage.SOURCE__EXTENT)

    @property
    def axis(self):
        """"""
        return self._e_object.getAxis().aslist()

    @axis.setter
    def axis(self, value):
        """"""
        if isinstance(value, Point):
            self._e_object.setAxis(value)
        else:
            self._e_object.setAxis(Point.aspoint(value))
        self._e_object.eUnset(ePackage.SOURCE__AXES)

    @property
    def axes(self):
        return _dist_to_list(self._e_object.getAxes())

    @axes.setter
    def axes(self, value):
        if isinstance(value, list):
            self._e_object.setAxes(_list_to_dist(value))
        else:
            self._e_object.setAxes(value)
        self._e_object.eUnset(ePackage.SOURCE__AXIS)

    @property
    def x_coord(self):
        """"""
        return self._e_object.getXCoord()

    @x_coord.setter
    def x_coord(self, value):
        """"""
        self._e_object.setXCoord(float(value))
        self._e_object.eUnset(ePackage.SOURCE__X_COORDS)

    @property
    def x_coords(self):
        return _dist_to_list(self._e_object.getXCoords())

    @x_coords.setter
    def x_coords(self, value):
        if isinstance(value, list):
            self._e_object.setXCoords(_list_to_dist(value))
        else:
            self._e_object.setXCoords(value)
        self._e_object.eUnset(ePackage.SOURCE__X_COORD)

    @property
    def y_coord(self):
        """"""
        return self._e_object.getYCoord()

    @y_coord.setter
    def y_coord(self, value):
        """"""
        self._e_object.setYCoord(float(value))
        self._e_object.eUnset(ePackage.SOURCE__Y_COORDS)

    @property
    def y_coords(self):
        return _dist_to_list(self._e_object.getYCoords())

    @y_coords.setter
    def y_coords(self, value):
        if isinstance(value, list):
            self._e_object.setYCoords(_list_to_dist(value))
        else:
            self._e_object.setYCoords(value)
        self._e_object.eUnset(ePackage.SOURCE__Y_COORD)

    @property
    def z_coord(self):
        """"""
        return self._e_object.getZCoord()

    @z_coord.setter
    def z_coord(self, value):
        """"""
        self._e_object.setZCoord(float(value))
        self._e_object.eUnset(ePackage.SOURCE__Z_COORDS)

    @property
    def z_coords(self):
        return _dist_to_list(self._e_object.getZCoords())

    @z_coords.setter
    def z_coords(self, value):
        if isinstance(value, list):
            self._e_object.setZCoords(_list_to_dist(value))
        else:
            self._e_object.setZCoords(value)
        self._e_object.eUnset(ePackage.SOURCE__Z_COORD)

    @property
    def area(self):
        """"""
        return self._e_object.getArea()

    @area.setter
    def area(self, value):
        """"""
        self._e_object.setArea(float(value))
        self._e_object.eUnset(ePackage.SOURCE__AREAS)

    @property
    def areas(self):
        return _dist_to_list(self._e_object.getAreas())

    @areas.setter
    def areas(self, value):
        if isinstance(value, list):
            self._e_object.setAreas(_list_to_dist(value))
        else:
            self._e_object.setAreas(value)
        self._e_object.eUnset(ePackage.SOURCE__AREA)

    @property
    def weight(self):
        """"""
        return self._e_object.getWeight()

    @weight.setter
    def weight(self, value):
        """"""
        self._e_object.setWeight(float(value))
        self._e_object.eUnset(ePackage.SOURCE__WEIGHTS)

    @property
    def weights(self):
        return _dist_to_list(self._e_object.getWeights())

    @weights.setter
    def weights(self, value):
        if isinstance(value, list):
            self._e_object.setWeights(_list_to_dist(value))
        else:
            self._e_object.setWeights(value)
        self._e_object.eUnset(ePackage.SOURCE__WEIGHT)

    @property
    def rejection_efficiency(self):
        """"""
        return self._e_object.getRejectionEfficiency()

    @rejection_efficiency.setter
    def rejection_efficiency(self, value):
        """"""
        self._e_object.setRejectionEfficiency(float(value))
        self._e_object.eUnset(ePackage.SOURCE__REJECTION_EFFICIENCIES)

    @property
    def rejection_efficiencies(self):
        return _dist_to_list(self._e_object.getRejectionEfficiencies())

    @rejection_efficiencies.setter
    def rejection_efficiencies(self, value):
        if isinstance(value, list):
            self._e_object.setRejectionEfficiencies(_list_to_dist(value))
        else:
            self._e_object.setRejectionEfficiencies(value)
        self._e_object.eUnset(ePackage.SOURCE__REJECTION_EFFICIENCY)


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
        self.particle = par

    @property
    def particle(self):
        if self._e_object.eIsSet(ePackage.SOURCE_PARTICLE__ION):
            return zaid_to_element(self._e_object.getIon())
        else:
            return mcnpy.SourceParticleCategory(self._e_object.getParticle().getLiteral()).name

    @particle.setter
    def particle(self, par):
        attr = self.eClass().getEStructuralFeatures()[0].getEAttributeType()
        if isinstance(par, Enum):
            value = attr.getEEnumLiteralByLiteral(par.value).getInstance()
            self._e_object.setParticle(value)
            self._e_object.eUnset(ePackage.SOURCE_PARTICLE__ION)
        elif isinstance(par, str):
            if par.upper() in PARTICLE or par.upper() in PARTICLE.values():
                value = attr.getEEnumLiteralByLiteral(par.upper()).getInstance()
                self._e_object.setParticle(value)
                self._e_object.eUnset(ePackage.SOURCE_PARTICLE__ION)
            else:
                self._e_object.eUnset(ePackage.SOURCE_PARTICLE__PARTICLE)
                self._e_object.setIon(element_to_zaid(par))
        elif hasattr(par, 'zaid'):
            self._e_object.eUnset(ePackage.SOURCE_PARTICLE__PARTICLE)
            self._e_object.setIon(element_to_zaid(par.zaid()))
        else:
            self._e_object.eUnset(ePackage.SOURCE_PARTICLE__PARTICLE)
            self._e_object.setIon(element_to_zaid(str(par)))

    @property
    def ion(self):
        return self._e_object.getIon()

    @ion.setter
    def ion(self, par):
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

class SourceInfo(SourceInfoBase, SourceSetting, Distribution):
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

    def __repr__(self) -> str:
        return 'SI' + str(self.name)

    def __str__(self) -> str:
        string = 'Source Info\n'
        string += '{0: <16}{1}{2}\n'.format('\tID', '=\t', str(self.name))
        string += '{0: <16}{1}{2}\n'.format('\Option', '=\t', 
                                            mcnpy.SourceInfoOption(self.option).name)
        string += '{0: <16}{1}{2}\n'.format('\tValues', '=\t', 
                                            str(self.values))
        return string

    
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

class SourceProbability(SourceProbabilityBase, SourceSetting, Distribution):
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

    def __repr__(self) -> str:
        return 'SP' + str(self.name)

    def __str__(self) -> str:
        string = 'Source Probability\n'
        string += '{0: <16}{1}{2}\n'.format('\tID', '=\t', str(self.name))
        string += '{0: <16}{1}{2}\n'.format('\Option', '=\t', 
                                            mcnpy.SourceInfoOption(self.option).name)
        string += '{0: <16}{1}{2}\n'.format('\tValues', '=\t', 
                                            str(self.values))
        return string
    
    class Function(SourceProbabilityFunctionBase, SourceSetting, Distribution):
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

        def maxwell(self, a=1.2895):
            """Maxwell fission energy spectrum of the form :math:`p(E) = CE^{1/2} e^{-E/a}`, :math:`a` is temperature in MeV.
            """
            self.function = 2
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def watt(self, a=0.965, b=2.29):
            """Watt fission spectrum of the form :math:`p(E) = C e^{-E/a} sinh(bE)^{1/2}`.
            """
            self.function = 3
            self.a = a
            self.b = b
            return self

        def gaussian_fusion(self, a=-0.01, b=-1.0):
            """Gaussian fusion spectrum of the form :math:`p(E) = C e^{-((E-b)/a)^{2}}`, :math:`a` is the width in MeV and :math:`b` is the average energy in MeV."""
            self.function = 4
            self.a = a
            self.b = b
            return self

        def evaporation(self, a=1.2895):
            """Evaporation energy spectrum of the form :math:`p(E) = CE e^{-E/a}`."""
            self.function = 5
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def muir_fusion(self, a=-0.01, b=-1.0):
            """Muir velocity Gaussian fusion spectrum of the form :math:`p(E) = C e^{-(E^{1/2}-b^{1/2})/a)^{2}}`, :math:`a` is the width in :math:`MeV^{1/2}` and :math:`b` is the energy in MeV corresponding to the average speed."""
            self.function = 6
            self.a = a
            self.b = b
            return self

        def exp_decay(self, a=1.0):
            """Exponential decay of the form :math:`\\alpha(t) = \\alpha_{0}(1/2)^{t/a}`, :math:`a` is the half-life in shakes."""
            self.function = 7
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def power(self, a):
            """Power law of the form :math:`p(x) = c |x|^{a}`."""
            self.function = 21
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def exponential(self, a=0.0):
            """Exponential of the form :math:`p(\\mu) = ce^{a|\\mu|}`, :math:`a` is the width in MeV and :math:`b` is the average energy in MeV."""
            self.function = 31
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def gaussian(self, a, b=0.0):
            """Gaussian distribution of time or position of the form :math:`p(t) = c exp[-(1.6651092(t-b)/a)^{2}]`, :math:`a` is the width at the half maximum and :math:`b` is the mean. Units of shakes for time and units of cm for position."""
            self.function = 41
            self.a = a
            self.b = b
            return self

class SourceBias(SourceBiasBase, SourceSetting, Distribution):
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

    def __repr__(self) -> str:
        return 'SB' + str(self.name)

    def __str__(self) -> str:
        string = 'Source Bias\n'
        string += '{0: <16}{1}{2}\n'.format('\tID', '=\t', str(self.name))
        string += '{0: <16}{1}{2}\n'.format('\Option', '=\t', 
                                            mcnpy.SourceInfoOption(self.option).name)
        string += '{0: <16}{1}{2}\n'.format('\tValues', '=\t', 
                                            str(self.values))
        return string
    
    class Function(SourceBiasFunctionBase, SourceSetting, Distribution):
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

        def power(self, a):
            """Power law of the form :math:`p(x) = c |x|^{a}`."""
            self.function = 21
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

        def exponential(self, a=0.0):
            """Exponential of the form :math:`p(\\mu) = ce^{a|\\mu|}`, :math:`a` is the width in MeV and :math:`b` is the average energy in MeV."""
            self.function = 31
            self.a = a
            self._e_object.eUnset(ePackage.SOURCE_PROBABILITY_FUNCTION__B)
            return self

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

    @property
    def cell(self):
        """"""
        return self._e_object.getCell()

    @cell.setter
    def cell(self, value):
        if isinstance(value, mcnpy.Tally.Bin.UnaryCellBin) is False:
            self._e_object.setCell(mcnpy.Tally.Bin.UnaryCellBin(value))
        else:
            self._e_object.setCell(value)
        self._e_object.eUnset(ePackage.SOURCE_CELL__ZCELL)
        self._e_object.eUnset(ePackage.SOURCE_CELL__DISTRIBUTION)

    @property
    def distribution(self):
        return _dist_to_list(self._e_object.getDistribution())

    @distribution.setter
    def distribution(self, value):
        if isinstance(value, list):
            self._e_object.setDistribution(_list_to_dist(value))
        else:
            self._e_object.setDistribution(value)
        self._e_object.eUnset(ePackage.SOURCE_CELL__ZCELL)
        self._e_object.eUnset(ePackage.SOURCE_CELL__CELL)
        self._e_object.eUnset(ePackage.SOURCE_CELL__COORDINATES)

    @property
    def z_cell(self):
        return self._e_object.geZCell()

    @z_cell.setter
    def z_cell(self, value):
        self._e_object.setZCell(int(value))
        self._e_object.eUnset(ePackage.SOURCE_CELL__DISTRIBUTION)
        self._e_object.eUnset(ePackage.SOURCE_CELL__CELL)
        self._e_object.eUnset(ePackage.SOURCE_CELL__COORDINATES)

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

class SourceID(SourceIDBase, SourceSetting, Distribution):
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

class Distributions(DistributionsBase):
    """
    A representation of the model object `Distributions`.
    
    Parameters
    ----------
    distributions : iterable of mcnpy.Distribution
        Distributions for `Distributions`.
    
    """

    def _init(self, distributions):
        """
        """
        self.distributions = distributions

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

    class Distribution(DependentSourceDistributionBase, SourceSetting, Distribution):
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