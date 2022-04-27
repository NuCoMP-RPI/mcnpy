from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class TallySetting(ABC):
    """
    """

class Tally(ABC):
    """
    """

class TallySurfaceCurrent(TallySurfaceCurrentBase, Tally):
    __doc__ = """F1
    """
    __doc__ += TallySurfaceCurrentBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySurfaceFlux(TallySurfaceFluxBase, Tally):
    __doc__ = """F2
    """
    __doc__ += TallySurfaceFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCellFlux(TallyCellFluxBase, Tally):
    __doc__ = """F4
    """
    __doc__ += TallyCellFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyEnergyDeposition(TallyEnergyDepositionBase, Tally):
    __doc__ = """F6
    """
    __doc__ += TallyEnergyDepositionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCollisionHeating(TallyCollisionHeatingBase, Tally):
    __doc__ = """+F6
    """
    __doc__ += TallyCollisionHeatingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFissionHeating(TallyFissionHeatingBase, Tally):
    __doc__ = """F7
    """
    __doc__ += TallyFissionHeatingBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPulseHeight(TallyPulseHeightBase, Tally):
    __doc__ = """F8
    """
    __doc__ += TallyPulseHeightBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyChargeDeposition(TallyChargeDepositionBase, Tally):
    __doc__ = """+F8
    """
    __doc__ += TallyChargeDepositionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyDetector(ABC):
    """
    """

class TallyPointFlux(TallyPointFluxBase, Tally, TallyDetector):
    __doc__ = """F5
    """
    __doc__ += TallyPointFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyRingFlux(TallyRingFluxBase, Tally, TallyDetector):
    __doc__ = """F5
    """
    __doc__ += TallyRingFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyRadiographyFlux(ABC):
    """
    """

class TallyPinholeImageFlux(TallyPinholeImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    __doc__ = """FIP
    """
    __doc__ += TallyPinholeImageFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPlanarImageFlux(TallyPlanarImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    __doc__ = """FIR
    """
    __doc__ += TallyPlanarImageFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCylindricalImageFlux(TallyCylindricalImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    __doc__ = """FIC
    """
    __doc__ += TallyCylindricalImageFluxBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MeshTally(ABC):
    """
    """

class TallyMesh(TallyMeshBase, Tally, MeshTally):
    __doc__ = """FMESH
    """
    __doc__ += TallyMeshBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SuperimposedTallyMesh(SuperimposedTallyMeshBase, Tally, MeshTally):
    __doc__ = """TMESH
    """
    __doc__ += SuperimposedTallyMeshBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyComment(TallyCommentBase, TallySetting):
    __doc__ = """TC
    """
    __doc__ += TallyCommentBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyEnergies(TallyEnergiesBase, TallySetting):
    __doc__ = """E
    """
    __doc__ += TallyEnergiesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTimes(TallyTimesBase, TallySetting):
    __doc__ = """T
    """
    __doc__ += TallyTimesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTimesCyclic(TallyTimesCyclicBase, TallySetting):
    __doc__ = """T
    """
    __doc__ += TallyTimesCyclicBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyAngles(TallyAnglesBase, TallySetting):
    __doc__ = """C
    """
    __doc__ += TallyAnglesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPrint(TallyPrintBase, TallySetting):
    __doc__ = """FQ
    """
    __doc__ += TallyPrintBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyMultiplier(TallyMultiplierBase, TallySetting):
    __doc__ = """FM
    """
    __doc__ += TallyMultiplierBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseEnergy(DoseEnergyBase, TallySetting):
    __doc__ = """DE
    """
    __doc__ += DoseEnergyBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseTable(DoseTableBase, TallySetting):
    __doc__ = """DF
    """
    __doc__ += DoseTableBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseFunction(DoseFunctionBase, TallySetting):
    __doc__ = """DF
    """
    __doc__ += DoseFunctionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TimeMultiplier(TimeMultiplierBase, TallySetting):
    __doc__ = """TM
    """
    __doc__ += TimeMultiplierBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergyMultiplier(EnergyMultiplierBase, TallySetting):
    __doc__ = """EM
    """
    __doc__ += EnergyMultiplierBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FlagSurfaces(FlagSurfacesBase, TallySetting):
    __doc__ = """SF
    """
    __doc__ += FlagSurfacesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySegments(TallySegmentsBase, TallySetting):
    __doc__ = """FS
    """
    __doc__ += TallySegmentsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySegmentDivisors(TallySegmentDivisorsBase, TallySetting):
    __doc__ = """SD
    """
    __doc__ += TallySegmentDivisorsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyUser(TallyUserBase, TallySetting):
    __doc__ = """FU
    """
    __doc__ += TallyUserBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFluctuation(TallyFluctuationBase, TallySetting):
    __doc__ = """FT
    """
    __doc__ += TallyFluctuationBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFluctuationROC(TallyFluctuationROCBase, TallySetting):
    __doc__ = """FT
    """
    __doc__ += TallyFluctuationROCBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class NoTransport(NoTransportBase, TallySetting):
    """NOTRN
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Perturbation(PerturbationBase, TallySetting):
    __doc__ = """PERT
    """
    __doc__ += PerturbationBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ReactivityPerturbation(ReactivityPerturbationBase, TallySetting):
    __doc__ = """KPERT
    """
    __doc__ += ReactivityPerturbationBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CriticalitySensitivity(CriticalitySensitivityBase, TallySetting):
    __doc__ = """KSEN
    """
    __doc__ += CriticalitySensitivityBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class LatticeSpeedTallyEnhancement(LatticeSpeedTallyEnhancementBase, TallySetting):
    __doc__ = """SPDTL
    """
    __doc__ += LatticeSpeedTallyEnhancementBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTreatments(TallyTreatmentsBase, TallySetting):
    __doc__ = """FT
    """
    __doc__ += TallyTreatmentsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class AngleMultiplier(AngleMultiplierBase, TallySetting):
    __doc__ = """CM
    """
    __doc__ += AngleMultiplierBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FlagCells(FlagCellsBase, TallySetting):
    __doc__ = """CF
    """
    __doc__ += FlagCellsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyDivisor(TallyDivisorBase):
    __doc__ = TallyDivisorBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DoseNormalization(DoseNormalizationBase):
    __doc__ = DoseNormalizationBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class TallyRingFluxDetector(TallyRingFluxDetectorBase):
    __doc__ = TallyRingFluxDetectorBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class TallyPointFluxDetector(TallyPointFluxDetectorBase):
    __doc__ = TallyPointFluxDetectorBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override