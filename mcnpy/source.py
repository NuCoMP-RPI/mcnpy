from abc import ABC
from .wrap import wrappers, overrides
from .zaid_helper import element_to_zaid, zaid_to_element
from .points import Point

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
    __doc__ = CriticalitySourceBase().__doc__

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
        
#TODO: Better distribution support
class Source(SourceBase, SourceSetting):
    __doc__ = SourceBase().__doc__

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

class CriticalitySourcePoints(CriticalitySourcePointsBase, SourceSetting):
    __doc__ = CriticalitySourcePointsBase().__doc__
    
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

class SourceParticle(SourceParticleBase):
    __doc__ = SourceParticleBase().__doc__
    
    def _init(self, par):
        """
        """
        # For when an enum is used.
        if str(par).upper() in PARTICLE.keys() or str(par).upper() in PARTICLE.values():
            self.particle = par
        # For when a ZAID is used.
        else:
            self.ion = int(element_to_zaid(str(par)))

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
    __doc__ = SourceInfoBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SourceProbability(SourceProbabilityBase, SourceSetting):
    __doc__ = SourceProbabilityBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SourceBias(SourceBiasBase, SourceSetting):
    __doc__ = SourceBiasBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DependentSourceDistribution(DependentSourceDistributionBase, SourceSetting):
    __doc__ = DependentSourceDistributionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SourceComment(SourceCommentBase, SourceSetting):
    __doc__ = SourceCommentBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SurfaceSourceWrite(SurfaceSourceWriteBase, SourceSetting):
    __doc__ = SurfaceSourceWriteBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SurfaceSourceRead(SurfaceSourceReadBase, SourceSetting):
    __doc__ = SurfaceSourceReadBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CriticalityOptions(CriticalityOptionsBase, SourceSetting):
    __doc__ = CriticalityOptionsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EntropyMesh(EntropyMeshBase, SourceSetting):
    __doc__ = EntropyMeshBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Depletion(DepletionBase, SourceSetting):
    __doc__ = DepletionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    
class DepletionMaterial(DepletionMaterialBase, SourceSetting):
    __doc__ = DepletionMaterialBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DepletionOmittedIsotopes(DepletionOmittedIsotopesBase, SourceSetting):
    __doc__ = DepletionOmittedIsotopesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceBiasFunction(SourceBiasFunctionBase, SourceSetting):
    __doc__ = SourceBiasFunctionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceCell(SourceCellBase, SourceSetting):
    __doc__ = SourceCellBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceDist(SourceDistBase, SourceSetting):
    __doc__ = SourceDistBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceID(SourceIDBase, SourceSetting):
    __doc__ = SourceIDBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceInfoCells(SourceInfoCellsBase, SourceSetting):
    __doc__ = SourceInfoCellsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceInfoDistributions(SourceInfoDistributionsBase, SourceSetting):
    __doc__ = SourceInfoDistributionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceInfoParticles(SourceInfoParticlesBase, SourceSetting):
    __doc__ = SourceInfoParticlesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SourceProbabilityFunction(SourceProbabilityFunctionBase, SourceSetting):
    __doc__ = SourceProbabilityFunctionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SurfaceSourceReadCylindricalWindow(SurfaceSourceReadCylindricalWindowBase):
    __doc__ = SurfaceSourceReadCylindricalWindowBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SurfaceSourceWriteCrossing(SurfaceSourceWriteCrossingBase):
    __doc__ = SurfaceSourceWriteCrossingBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class SurfaceSourceWriteFromCell(SurfaceSourceWriteFromCellBase):
    __doc__ = SurfaceSourceWriteFromCellBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Distribution(DistributionBase):
    __doc__ = DistributionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Distributions(DistributionsBase):
    __doc__ = DistributionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceVolumer(DependentSourceVolumerBase):
    __doc__ = DependentSourceVolumerBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceParticles(DependentSourceParticlesBase):
    __doc__ = DependentSourceParticlesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributions(DependentSourceDistributionsBase):
    __doc__ = DependentSourceDistributionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceCells(DependentSourceCellsBase):
    __doc__ = DependentSourceCellsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributionBins(DependentSourceDistributionBinsBase):
    __doc__ = DependentSourceDistributionBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributionMatches(DependentSourceDistributionMatchesBase):
    __doc__ = DependentSourceDistributionMatchesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class NestedDistribution(NestedDistributionBase):
    __doc__ = NestedDistributionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ZeroDist(ZeroDistBase):
    __doc__ = ZeroDistBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])


for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override