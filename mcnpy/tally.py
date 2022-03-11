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
    """F1
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySurfaceFlux(TallySurfaceFluxBase, Tally):
    """F2
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCellFlux(TallyCellFluxBase, Tally):
    """F4
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyEnergyDeposition(TallyEnergyDepositionBase, Tally):
    """F6
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCollisionHeating(TallyCollisionHeatingBase, Tally):
    """+F6
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFissionHeating(TallyFissionHeatingBase, Tally):
    """F7
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPulseHeight(TallyPulseHeightBase, Tally):
    """F8
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyChargeDeposition(TallyChargeDepositionBase, Tally):
    """+F8
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyDetector(ABC):
    """
    """

class TallyPointFlux(TallyPointFluxBase, Tally, TallyDetector):
    """F5
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyRingFlux(TallyRingFluxBase, Tally, TallyDetector):
    """F5
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyRadiographyFlux(ABC):
    """
    """

class TallyPinholeImageFlux(TallyPinholeImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    """FIP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPlanarImageFlux(TallyPlanarImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    """FIR
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyCylindricalImageFlux(TallyCylindricalImageFluxBase, Tally, TallyRadiographyFlux, TallyDetector):
    """FIC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MeshTally(ABC):
    """
    """

class TallyMesh(TallyMeshBase, Tally, MeshTally):
    """FMESH
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SuperimposedTallyMesh(SuperimposedTallyMeshBase, Tally, MeshTally):
    """TMESH
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyComment(TallyCommentBase, TallySetting):
    """TC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyEnergies(TallyEnergiesBase, TallySetting):
    """E
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTimes(TallyTimesBase, TallySetting):
    """T
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTimesCyclic(TallyTimesCyclicBase, TallySetting):
    """T
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyAngles(TallyAnglesBase, TallySetting):
    """C
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyPrint(TallyPrintBase, TallySetting):
    """FQ
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyMultiplier(TallyMultiplierBase, TallySetting):
    """FM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseEnergy(DoseEnergyBase, TallySetting):
    """DE
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseTable(DoseTableBase, TallySetting):
    """DF
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DoseFunction(DoseFunctionBase, TallySetting):
    """DF
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TimeMultiplier(TimeMultiplierBase, TallySetting):
    """TM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergyMultiplier(EnergyMultiplierBase, TallySetting):
    """EM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FlagSurfaces(FlagSurfacesBase, TallySetting):
    """SF
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySegments(TallySegmentsBase, TallySetting):
    """FS
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallySegmentDivisors(TallySegmentDivisorsBase, TallySetting):
    """SD
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyUser(TallyUserBase, TallySetting):
    """FU
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFluctuation(TallyFluctuationBase, TallySetting):
    """FT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyFluctuationROC(TallyFluctuationROCBase, TallySetting):
    """FT
    """
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
    """PERT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ReactivityPerturbation(ReactivityPerturbationBase, TallySetting):
    """KPERT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CriticalitySensitivity(CriticalitySensitivityBase, TallySetting):
    """KSEN
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class LatticeSpeedTallyEnhancement(LatticeSpeedTallyEnhancementBase, TallySetting):
    """SPDTL
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TallyTreatments(TallyTreatmentsBase, TallySetting):
    """FT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class AngleMultiplier(AngleMultiplierBase, TallySetting):
    """CM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FlagCells(FlagCellsBase, TallySetting):
    """CF
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