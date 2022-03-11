from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class VarianceReductionSetting(ABC):
    """
    """

class CellImportances(CellImportancesBase, VarianceReductionSetting):
    """IMP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class RussianRoulette(RussianRouletteBase, VarianceReductionSetting):
    """VAR RR
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowEnergies(WeightWindowEnergiesBase, VarianceReductionSetting):
    """WWE
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowTimes(WeightWindowTimesBase, VarianceReductionSetting):
    """WWT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowBounds(WeightWindowBoundsBase, VarianceReductionSetting):
    """WWN
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowParameters(WeightWindowParametersBase, VarianceReductionSetting):
    """WWP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowGenerator(WeightWindowGeneratorBase, VarianceReductionSetting):
    """WWG
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowGeneratorEnergies(WeightWindowGeneratorEnergiesBase, VarianceReductionSetting):
    """WWGE
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindowGeneratorTimes(WeightWindowGeneratorTimesBase, VarianceReductionSetting):
    """WWGT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Mesh(MeshBase, VarianceReductionSetting):
    """MESH
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergySplitting(EnergySplittingBase, VarianceReductionSetting):
    """ESPLT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TimeSplitting(TimeSplittingBase, VarianceReductionSetting):
    """TSPLT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellExponentialTransforms(CellExponentialTransformsBase, VarianceReductionSetting):
    """EXT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Vectors(VectorsBase, VarianceReductionSetting):
    """VECT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellForcedCollisions(CellForcedCollisionsBase, VarianceReductionSetting):
    """FCL
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicTransport(DeterministicTransportBase, VarianceReductionSetting):
    """DXT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DetectorDiagnostics(DetectorDiagnosticsBase, VarianceReductionSetting):
    """DD
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDetectorContributions(CellDetectorContributionsBase, VarianceReductionSetting):
    """PD
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDeterministicContributions(CellDeterministicContributionsBase, VarianceReductionSetting):
    """DXC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class BremsstrahlungBiasing(BremsstrahlungBiasingBase, VarianceReductionSetting):
    """BBREM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SecondaryParticleBiasing(SecondaryParticleBiasingBase, VarianceReductionSetting):
    """SPABI
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellPhotonWeights(CellPhotonWeightsBase, VarianceReductionSetting):
    """PWT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhotonBias(PhotonBiasBase, VarianceReductionSetting):
    """PIKMT
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