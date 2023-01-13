from abc import ABC
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class VarianceReductionSetting(ABC):
    """
    """

class CellImportances(CellImportancesBase, VarianceReductionSetting):
    __doc__ = """IMP
    """
    __doc__ += CellImportancesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class RussianRoulette(RussianRouletteBase, VarianceReductionSetting):
    __doc__ = """VAR RR
    """
    __doc__ += RussianRouletteBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindow():
    """"""
    class Energies(WeightWindowEnergiesBase, VarianceReductionSetting):
        __doc__ = """WWE
        """
        __doc__ += WeightWindowEnergiesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Times(WeightWindowTimesBase, VarianceReductionSetting):
        __doc__ = """WWT
        """
        __doc__ += WeightWindowTimesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Bounds(WeightWindowBoundsBase, VarianceReductionSetting):
        __doc__ = """WWN
        """
        __doc__ += WeightWindowBoundsBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Parameters(WeightWindowParametersBase, VarianceReductionSetting):
        __doc__ = """WWP
        """
        __doc__ += WeightWindowParametersBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class WeightWindowGenerator(WeightWindowGeneratorBase, VarianceReductionSetting):
    __doc__ = """WWG
    """
    __doc__ += WeightWindowGeneratorBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class Energies(WeightWindowGeneratorEnergiesBase, VarianceReductionSetting):
        __doc__ = """WWGE
        """
        __doc__ += WeightWindowGeneratorEnergiesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Times(WeightWindowGeneratorTimesBase, VarianceReductionSetting):
        __doc__ = """WWGT
        """
        __doc__ += WeightWindowGeneratorTimesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class Mesh(MeshBase, VarianceReductionSetting):
    __doc__ = """MESH
    """
    __doc__ += MeshBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergySplitting(EnergySplittingBase, VarianceReductionSetting):
    __doc__ = """ESPLT
    """
    __doc__ += EnergySplittingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TimeSplitting(TimeSplittingBase, VarianceReductionSetting):
    __doc__ = """TSPLT
    """
    __doc__ += TimeSplittingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellExponentialTransforms(CellExponentialTransformsBase, VarianceReductionSetting):
    __doc__ = """EXT
    """
    __doc__ += CellExponentialTransformsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Vectors(VectorsBase, VarianceReductionSetting):
    __doc__ = """VECT
    """
    __doc__ += VectorsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellForcedCollisions(CellForcedCollisionsBase, VarianceReductionSetting):
    __doc__ = """FCL
    """
    __doc__ += CellForcedCollisionsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicTransport(DeterministicTransportBase, VarianceReductionSetting):
    __doc__ = """DXT
    """
    __doc__ += DeterministicTransportBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    class Sphere(DeterministicTransportSphereBase):
        __doc__ = DeterministicTransportSphereBase().__doc__
        
        def _init(self, x, y, z, ri, ro):
            self.x = x
            self.y = y
            self.z = z
            self.ri = ri
            self.ro = ro

        def __str__(self):
            string = ('(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) 
                    + str(self.ri) + ', ' + str(self.ro) + ')')
            return string

        def __repr__(self):
            return str(self)

class DetectorDiagnostics(DetectorDiagnosticsBase, VarianceReductionSetting):
    __doc__ = """DD
    """
    __doc__ += DetectorDiagnosticsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDetectorContributions(CellDetectorContributionsBase, VarianceReductionSetting):
    __doc__ = """PD
    """
    __doc__ += CellDetectorContributionsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDeterministicContributions(CellDeterministicContributionsBase, VarianceReductionSetting):
    __doc__ = """DXC
    """
    __doc__ += CellDeterministicContributionsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
class BremsstrahlungBiasing(BremsstrahlungBiasingBase, VarianceReductionSetting):
    __doc__ = """BBREM
    """
    __doc__ += BremsstrahlungBiasingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SecondaryParticleBiasing(SecondaryParticleBiasingBase, VarianceReductionSetting):
    __doc__ = """SPABI
    """
    __doc__ += SecondaryParticleBiasingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellPhotonWeights(CellPhotonWeightsBase, VarianceReductionSetting):
    __doc__ = """PWT
    """
    __doc__ += CellPhotonWeightsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhotonBias(PhotonBiasBase, VarianceReductionSetting):
    __doc__ = """PIKMT
    """
    __doc__ += PhotonBiasBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class ReacPairs(ReacPairsBase):
        __doc__ = ReacPairsBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class CutoffParams(CutoffParamsBase):
    __doc__ = CutoffParamsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DXTSpheres(DXTSpheresBase):
    __doc__ = DXTSpheresBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ExponentialTransform(ExponentialTransformBase):
    __doc__ = ExponentialTransformBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override

subclass_overrides(PhotonBias)
subclass_overrides(WeightWindow)
subclass_overrides(WeightWindowGenerator)
subclass_overrides(DeterministicTransport)