import mcnpy as mp
from abc import ABC
from collections.abc import MutableSequence
from .mixin import IDManagerMixin, NoIDMixin
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

def str_name(obj):
    if isinstance(obj, mp.Surface):
        return str(obj.name)
    elif isinstance(obj, mp.SurfaceFacet):
        return str(obj.surface.name)
    else:
        return str(obj)

# The cell and surface bins run into issues when they are reused. e.g. the same 
# bin object cannot appear on 2 different tallies. To get around this, we can 
# make copies so that each tally gets a unique object with the same semantics.
# The exception is that proper cells and surfaces should not be copied because
# they can be referenced freely throughout the input. The bins themselves
# cannot be referenced. Conceptually, the copying is just like the user typing
# out the same bins for multiple tallies.
def copy_inputs(obj, other):
    cp = obj.__copy__()
    if isinstance(other, (mp.Cell, mp.Universe, mp.UniverseList, mp.Surface, 
                          mp.SurfaceFacet)) is False:
        return cp, other.__copy__()
    else:
        return cp, other

class TallyABC(IDManagerMixin, ABC):
    """
    """
    used_ids = set()

    @property
    def bins(self):
        return self._e_object.getBins()

    @bins.setter
    def bins(self, bins):
        if bins is None:
            pass
        else:
            try:
                self._e_object.setBins(Tally.Bin.CellBins(bins.__copy__()))
            except:
                self._e_object.setBins(Tally.Bin.SurfaceBins(bins.__copy__()))

    """@property
    def particles(self):
        return self._e_object.getParticles()

    @particles.setter
    def particles(self, particles):
        _par = self._e_object.getParticles()
        del _par[:]
        if particles is not None:
            if isinstance(particles, list) is False:
                particles = [particles]
            for p in particles:
                _par.append(p)"""
                
class FTallyABC(TallyABC):
    """General class for F1, F2, F4, F6, F7, and F8 tallies.
    """
    def _init(self, name=None, particles=None, bins=None, unit=None, 
              total=None):
        """
        """
        self.name = name
        self.bins = bins
        self.particles = particles
        self.unit = unit
        self.total = total

class DetTallyABC(TallyABC):
    """F5 point and ring flux tallies.
    """
    def _init(self, name=None, particles=None, detectors=None, unit=None, 
              no_direct=None):
        """
        """
        self.name = name
        self.detectors = detectors
        self.particles = particles
        self.unit = unit
        self.no_direct = no_direct

class RadTallyABC(TallyABC):
    """F5 radiography image tallies.
    """
    def _init(self, name=None, particles=None, center=None, r0=None, 
              reference=None, unit=None, no_direct=None):
        """
        """
        self.name = name
        self.center = center
        self.r0 = r0
        self.reference = reference
        self.particles = particles
        self.unit = unit
        self.no_direct = no_direct

class TallySettingABC(ABC):
    pass

class TallyRef(TallySettingABC):
    @property
    def tally(self):
        return self._e_object.getTally()

    @tally.setter
    def tally(self, tally):
        if tally == 0:
            self._e_object.setTally(None)
        else:
            self._e_object.setTally(tally)

class Tally():
    """
    """
    class SurfaceCurrent(FTallyABC, TallySurfaceCurrentBase):
        next_id = 1
        increment = 10

        __doc__ = """F1
        """
        __doc__ += TallySurfaceCurrentBase().__doc__

    class SurfaceFlux(FTallyABC, TallySurfaceFluxBase):
        next_id = 2
        increment = 10

        __doc__ = """F2
        """
        __doc__ += TallySurfaceFluxBase().__doc__

    class CellFlux(FTallyABC, TallyCellFluxBase):
        next_id = 4
        increment = 10

        __doc__ = """F4
        """
        __doc__ += TallyCellFluxBase().__doc__

    class EnergyDeposition(FTallyABC, TallyEnergyDepositionBase):
        next_id = 6
        increment = 10

        __doc__ = """F6
        """
        __doc__ += TallyEnergyDepositionBase().__doc__

    class CollisionHeating(FTallyABC, TallyCollisionHeatingBase):
        next_id = 6
        increment = 10
        
        __doc__ = """+F6
        """
        __doc__ += TallyCollisionHeatingBase().__doc__

    class FissionHeating(FTallyABC, TallyFissionHeatingBase):
        next_id = 7
        increment = 10

        __doc__ = """F7
        """
        __doc__ += TallyFissionHeatingBase().__doc__
        
    class PulseHeight(FTallyABC, TallyPulseHeightBase):
        next_id = 8
        increment = 10

        __doc__ = """F8
        """
        __doc__ += TallyPulseHeightBase().__doc__
        
    class ChargeDeposition(FTallyABC, TallyChargeDepositionBase):
        next_id = 8
        increment = 10

        __doc__ = """+F8
        """
        __doc__ += TallyChargeDepositionBase().__doc__

    class PointFlux(DetTallyABC, TallyPointFluxBase):
        next_id = 5
        increment = 10

        __doc__ = """F5
        """
        __doc__ += TallyPointFluxBase().__doc__

        class Detector(TallyPointFluxDetectorBase):
            __doc__ = TallyPointFluxDetectorBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class RingFlux(DetTallyABC, TallyRingFluxBase):
        next_id = 5
        increment = 10

        __doc__ = """F5
        """
        __doc__ += TallyRingFluxBase().__doc__

        class Detector(TallyRingFluxDetectorBase):
            __doc__ = TallyRingFluxDetectorBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class PinholeImageFlux(RadTallyABC, TallyPinholeImageFluxBase):
        next_id = 5
        increment = 10

        __doc__ = """FIP
        """
        __doc__ += TallyPinholeImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class PlanarImageFlux(RadTallyABC, TallyPlanarImageFluxBase):
        next_id = 5
        increment = 10

        __doc__ = """FIR
        """
        __doc__ += TallyPlanarImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class CylindricalImageFlux(RadTallyABC, TallyCylindricalImageFluxBase):
        next_id = 5
        increment = 10

        __doc__ = """FIC
        """
        __doc__ += TallyCylindricalImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class FMESH(TallyABC, TallyMeshBase):
        next_id = 4
        increment = 10

        __doc__ = """FMESH
        """
        __doc__ += TallyMeshBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    # This is really just the container around a TMESH block.
    # All of the numbered meshes are their own set of cards/classes.
    #TODO: Work on better combining these cards.
    class TMESH(SuperimposedTallyMeshBase):
        __doc__ = """TMESH
        """
        __doc__ += SuperimposedTallyMeshBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

        class CORA(CORABase):
            __doc__ = CORABase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class CORB(CORBBase):
            __doc__ = CORBBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class CORC(CORCBase):
            __doc__ = CORCBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class dParams(dParamsBase):
            __doc__ = dParamsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class EnergyLimits(EnergyLimitsBase):
            __doc__ = EnergyLimitsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class energyPairs(energyPairsBase):
            __doc__ = energyPairsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class MeshData(MeshDataBase):
            __doc__ = MeshDataBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class MeshMF(MeshMFBase):
            __doc__ = MeshMFBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class MeshMultiplier(MeshMultiplierBase):
            __doc__ = MeshMultiplierBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class MeshOptions(MeshOptionsBase):
            __doc__ = MeshOptionsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class Mesh(TMESHBase):
            __doc__ = TMESHBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class TMESHType(TMESHTypeBase):
            __doc__ = TMESHTypeBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class TypeOne(TypeOneBase):
            __doc__ = TypeOneBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class TypeTwo(TypeTwoBase):
            __doc__ = TypeTwoBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class TypeThree(TypeThreeBase):
            __doc__ = TypeThreeBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class TypeFour(TypeFourBase):
            __doc__ = TypeFourBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class Bin(ABC):
        """
        """
        class Level(ABC):
            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceLevel((cp, cp2))
                else:
                    return Tally.Bin.CellLevel((cp, cp2))

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceUnion((cp, cp2))
                else:
                    return Tally.Bin.CellUnion((cp, cp2))

            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceLevels([cp] + [cp2])
                else:
                    return Tally.Bin.CellLevels([cp] + [cp2])

        class CellBins(CellBinsBase):
            __doc__ = CellBinsBase().__doc__

            def _init(self, bins):
                """
                """
                self.bins = bins

            @property
            def bins(self):
                return self._e_object.getBins()

            @bins.setter
            def bins(self, bins):
                _bins = self._e_object.getBins()
                del _bins[:]
                if (isinstance(bins, (MutableSequence, tuple)) is False 
                    or isinstance(bins, Tally.Bin.Level)): 
                    bins = [bins]
                if isinstance(bins, Tally.Bin.CellLevels):
                    _bins.append(bins)
                else:
                    for i in bins:
                        if isinstance(i, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                            _bins.append(Tally.Bin.UnaryCellBin(i))
                        else:
                            if i is not None:
                                _bins.append(i)

        class CellLevel(CellLevelBase, Level, MutableSequence):
            __doc__ = CellLevelBase().__doc__

            def _init(self, level):
                """
                """
                self.level = level

            @property
            def level(self):
                return self._e_object.getLevel()

            @level.setter
            def level(self, level):
                _level = self._e_object.getLevel()
                del _level[:]
                if (isinstance(level, (MutableSequence, tuple)) is False 
                    or isinstance(level, Tally.Bin.Level)):
                    level = [level]
                for i in level:
                    if isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _level.append(Tally.Bin.UnaryCellBin(i))
                    else:
                        _level.append(i)

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellLevel(cp)
                new &= cp2
                return new

            def __iand__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevel):
                    cp.extend(cp2)
                else:
                    cp.level.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.level[key]

            def __setitem__(self, key, value):
                self.level[key] = value

            def __delitem__(self, key):
                del self.level[key]

            def __len__(self):
                return len(self.level)

            def insert(self, index, value):
                self.level.insert(index, value)

            def __str__(self):
                return ' & '.join(map(str_name, self))

            def __repr__(self):
                return str(self)

        class CellLevels(CellLevelsBase, MutableSequence):
            __doc__ = CellLevelsBase().__doc__

            def _init(self, levels):
                """
                """
                self.levels = levels

            @property
            def levels(self):
                return self._e_object.getLevels()

            @levels.setter
            def levels(self, levels):
                _levels = self._e_object.getLevels()
                del _levels[:]
                if (isinstance(levels, (MutableSequence, tuple)) is False 
                    or isinstance(levels, Tally.Bin.Level)):
                    levels = [levels]
                elif isinstance(levels, Tally.Bin.CellLevels):
                    self.extend(levels)
                for i in levels:
                    if isinstance(i, (Tally.Bin.UnaryCellBin, 
                                      Tally.Bin.CellUnion)):
                        _levels.append(Tally.Bin.CellLevel(i))
                    elif isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _levels.append(Tally.Bin.CellLevel(Tally.Bin.
                                                           UnaryCellBin(i)))
                    else:
                        _levels.append(i)


            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellLevels(cp)
                new <<= cp2
                return new

            def __ilshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevels):
                    cp.extend(cp2)
                else:
                    if isinstance(cp2, (Tally.Bin.CellUnion, 
                                        Tally.Bin.UnaryCellBin)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [cp2])._e_object)
                    elif isinstance(cp2, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [Tally.Bin.UnaryCellBin(
                                            cp2)])._e_object)
                    else:
                        cp.levels.addUnique(cp2._e_object)
                return cp

            def __getitem__(self, key):
                return self.levels[key]

            def __setitem__(self, key, value):
                self.levels[key] = value

            def __delitem__(self, key):
                del self.levels[key]

            def __len__(self):
                return len(self.levels)

            def insert(self, index, value):
                self.levels.insert(index, value)

            def __str__(self):
                return '(' + ' << '.join(map(str, self)) + ')'
            
            def __repr__(self):
                return str(self)

        class CellUnion(CellUnionBase, Level, MutableSequence):
            __doc__ = CellUnionBase().__doc__

            def _init(self, union):
                """
                """
                if isinstance(union, Tally.Bin.CellUnion):
                    self.union = union.union
                else:
                    self.union = union

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellUnion(cp)
                new |= cp2
                return new

            def __ior__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellUnion):
                    cp.extend(cp2)
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    cp.union.addUnique(Tally.Bin.UnaryCellBin(cp2)._e_object)
                else:
                    cp.union.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.union[key]

            def __setitem__(self, key, value):
                self.union[key] = value

            def __delitem__(self, key):
                del self.union[key]

            def __len__(self):
                return len(self.union)

            def insert(self, index, value):
                self.union.insert(index, value)

            def __str__(self):
                return '(' + ' | '.join(map(str, self)) + ')'

        class FS_halfspace(FS_halfspaceBase):
            __doc__ = FS_halfspaceBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class ROCBin(ROCBinBase):
            __doc__ = ROCBinBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class ROCBinRange(ROCBinRangeBase):
            __doc__ = ROCBinRangeBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class SurfaceBins(SurfaceBinsBase):
            __doc__ = SurfaceBinsBase().__doc__

            def _init(self, bins):
                """
                """
                self.bins = bins

            @property
            def bins(self):
                return self._e_object.getBins()

            @bins.setter
            def bins(self, bins):
                _bins = self._e_object.getBins()
                del _bins[:]
                if (isinstance(bins, (MutableSequence, tuple)) is False 
                    or isinstance(bins, Tally.Bin.Level)): 
                    bins = [bins]
                if isinstance(bins, Tally.Bin.SurfaceLevels):
                    _bins.append(bins)
                else:
                    for i in bins:
                        if isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                            _bins.append(Tally.Bin.UnarySurfaceBin(i))
                        else:
                            if i is not None:
                                _bins.append(i)

        class SurfaceLevel(SurfaceLevelBase, Level, MutableSequence):
            __doc__ = SurfaceLevelBase().__doc__

            def _init(self, level):
                """
                """
                self.level = level

            @property
            def level(self):
                return self._e_object.getLevel()

            @level.setter
            def level(self, level):
                _level = self._e_object.getLevel()
                del _level[:]
                if (isinstance(level, (MutableSequence, tuple)) is False 
                    or isinstance(level, Tally.Bin.Level)):
                    level = [level]
                for i in level:
                    if isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                        _level.append(Tally.Bin.UnarySurfaceBin(i))
                    else:
                        _level.append(i)

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceLevel(cp)
                new &= cp2
                return new

            def __iand__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceLevel):
                    cp.extend(cp2)
                else:
                    cp.level.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.level[key]

            def __setitem__(self, key, value):
                self.level[key] = value

            def __delitem__(self, key):
                del self.level[key]

            def __len__(self):
                return len(self.level)

            def insert(self, index, value):
                self.level.insert(index, value)

            def __str__(self):
                return ' & '.join(map(str_name, self))

            def __repr__(self):
                return str(self)

        class SurfaceLevels(SurfaceLevelsBase, MutableSequence):
            __doc__ = SurfaceLevelsBase().__doc__

            def _init(self, levels):
                """
                """
                self.levels = levels

            @property
            def levels(self):
                _levels = []
                _levels.append(self._e_object.getSurface_levels())
                for i in range(len(self._e_object.getCell_levels())):
                    _levels.append(_levels[i])

                return _levels 

            @levels.setter
            def levels(self, levels):
                _levels = []
                if (isinstance(levels, (MutableSequence, tuple)) is False 
                    or isinstance(levels, Tally.Bin.Level)):
                    levels = [levels]
                elif isinstance(levels, Tally.Bin.SurfaceLevels):
                    self.extend(levels)
                for i in levels:
                    if isinstance(i, (Tally.Bin.UnarySurfaceBin, 
                                      Tally.Bin.SurfaceUnion)):
                        _levels.append(Tally.Bin.SurfaceLevel(i))
                    elif isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                        _levels.append(Tally.Bin.SurfaceLevel(
                                       Tally.Bin.UnarySurfaceBin(i)))
                    elif isinstance(i, (Tally.Bin.UnaryCellBin, 
                                        Tally.Bin.CellUnion)):
                        _levels.append(Tally.Bin.CellLevel(i))
                    elif isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _levels.append(Tally.Bin.CellLevel(
                                       Tally.Bin.UnaryCellBin(i)))
                    elif isinstance(i, Tally.Bin.SurfaceLevel):
                        _levels.append(i)
                    elif isinstance(i, Tally.Bin.CellLevels):
                        for j in i:
                            _levels.append(j)
                    else:
                        _levels.append(i)
                self._e_object.setSurface_levels(_levels[0].__copy__())
                _cell_levels = self._e_object.getCell_levels()
                del _cell_levels[:]
                for i in range(1, len(_levels)):
                    _cell_levels.append(_levels[i])



            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceLevels(cp)
                new <<= cp2
                return new

            def __ilshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevels):
                    cp.extend(cp2)
                else:
                    if isinstance(cp2, (Tally.Bin.CellUnion, 
                                        Tally.Bin.UnaryCellBin)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [cp2])._e_object)
                    elif isinstance(cp2, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [Tally.Bin.UnaryCellBin(
                                            cp2)])._e_object)
                    else:
                        cp.levels.addUnique(cp2._e_object)
                return cp

            def __getitem__(self, key):
                return self.levels[key]

            def __setitem__(self, key, value):
                self.levels[key] = value

            def __delitem__(self, key):
                del self.levels[key]

            def __len__(self):
                return len(self.levels)

            def insert(self, index, value):
                self.levels.insert(index, value)

            def __str__(self):
                return '(' + ' << '.join(map(str_name, self)) + ')'

            def __repr__(self):
                return str(self)

        class SurfaceUnion(SurfaceUnionBase, Level, MutableSequence):
            __doc__ = SurfaceUnionBase().__doc__

            def _init(self, union):
                """
                """
                if isinstance(union, Tally.Bin.SurfaceUnion):
                    self.union = union.union
                else:
                    self.union = union

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceUnion(cp)
                new |= cp2
                return new

            def __ior__(self, other):
                cp, cp2 = copy_inputs(cp, other)
                if isinstance(cp2, Tally.Bin.SurfaceUnion):
                    cp.extend(cp2)
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    cp.union.addUnique(Tally.Bin.UnarySurfaceBin(cp2)._e_object)
                else:
                    cp.union.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.union[key]

            def __setitem__(self, key, value):
                self.union[key] = value

            def __delitem__(self, key):
                del self.union[key]

            def __len__(self):
                return len(self.union)

            def insert(self, index, value):
                self.union.insert(index, value)

            def __str__(self):
                return '(' + ' | '.join(map(str, self)) + ')'

        class UnaryCellBin(UnaryCellBinBase, Level):
            __doc__ = UnaryCellBinBase().__doc__

            def _init(self, unary_cell, index=None):
                """
                """
                if isinstance(unary_cell, mp.Cell):
                    self.cell = unary_cell
                    self.universe = None
                else:
                    self.cell = None
                    self.universe = unary_cell
                if index is not None:
                    if isinstance(index, mp.Lattice.Index):
                        self.index = index
                    else:
                        self.index = mp.Lattice.Index(index)

            def __str__(self):
                if self.cell is None and self.universe is None:
                    return None
                elif self.universe is not None:
                    string = 'U=' + str(self.universe.name)
                else:
                    string = str(self.cell.name)

                if self.index is not None:
                    string += str(self.index)

                return string

            def __repr__(self):
                return str(self)

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellUnion):
                    return Tally.Bin.CellUnion([cp] + cp2[:])
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    return (Tally.Bin.CellUnion([cp] 
                            + [Tally.Bin.UnaryCellBin(cp2)]))
                else:
                    return Tally.Bin.CellUnion([cp, cp2])

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevel):
                    return Tally.Bin.CellLevel([cp] + cp2[:])
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    return (Tally.Bin.CellLevel([cp] 
                            + [Tally.Bin.UnaryCellBin(cp2)]))
                else:
                    return Tally.Bin.CellLevel([cp, cp2])

            def __getitem__(self, index):
                _index = mp.Lattice.Index(index)
                self.index = _index
                return self

        class UnarySurfaceBin(UnarySurfaceBinBase, Level):
            __doc__ = UnarySurfaceBinBase().__doc__

            def _init(self, surface, facet=None):
                """
                """
                self.surface = surface
                if facet is not None:
                    self.facets = '.' + str(facet)

            def __str__(self):
                string = str(self.surface.name)
                if self.facets is not None:
                    string = '{}.{}'.format(string, int(self.facets))
                return string

            def __repr__(self):
                return str(self)

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceUnion):
                    return Tally.Bin.SurfaceUnion([cp] + cp2[:])
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    return (Tally.Bin.SurfaceUnion([cp] 
                            + [Tally.Bin.UnarySurfaceBin(cp2)]))
                else:
                    return Tally.Bin.SurfaceUnion((self, cp2))

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceLevel):
                    return Tally.Bin.SurfaceLevel([cp] + cp2[:])
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    return (Tally.Bin.SurfaceLevel([cp] 
                            + [Tally.Bin.UnarySurfaceBin(cp2)]))
                else:
                    return Tally.Bin.SurfaceLevel((cp, cp2))

            @property
            def surface(self):
                return self._e_object.getSurface()
            
            @surface.setter
            def surface(self, surface):
                if isinstance(surface, mp.Surface):
                    self._e_object.setSurface(surface._e_object)
                else:
                    self._e_object.setSurface(surface.surface._e_object)
                    self._e_object.setFacets('.' + str(surface.facet))


    class Bins(ABC):
        """
        """
        class Energies(TallyRef, TallyEnergiesBase):
            __doc__ = """E
            """
            __doc__ += TallyEnergiesBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Times(TallyRef, TallyTimesBase):
            __doc__ = """T
            """
            __doc__ += TallyTimesBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class TimesCyclic(TallyRef, TallyTimesCyclicBase):
            __doc__ = """T
            """
            __doc__ += TallyTimesCyclicBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Angles(TallyRef, TallyAnglesBase):
            __doc__ = """C
            """
            __doc__ += TallyAnglesBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class User(TallyRef, TallyUserBase):
            __doc__ = """FU
            """
            __doc__ += TallyUserBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        
        class Multiplier(TallyRef, TallyMultiplierBase):
            __doc__ = """FM
            """
            __doc__ += TallyMultiplierBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class AttnMatSet(AttnMatSetBase):
                __doc__ = AttnMatSetBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class AttnSet(AttnSetBase):
                __doc__ = AttnSetBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBin(MultBinBase):
                __doc__ = MultBinBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBinSet(MultBinSetBase):
                __doc__ = MultBinSetBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBinSets(MultBinSetsBase):
                __doc__ = MultBinSetsBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultSet(MultSetBase):
                __doc__ = MultSetBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultSetSpecial(MultSetSpecialBase):
                __doc__ = MultSetSpecialBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnLists(RxnListsBase):
                __doc__ = RxnListsBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnMult(RxnMultBase):
                __doc__ = RxnMultBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnNum(RxnNumBase):
                __doc__ = RxnNumBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class Rxns(RxnsBase):
                __doc__ = RxnsBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnSum(RxnSumBase):
                __doc__ = RxnSumBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

        class Segments(TallyRef, TallySegmentsBase):
                __doc__ = """FS
                """
                __doc__ += TallySegmentsBase().__doc__
                
                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k.lower(), kwargs[k])

        class AngleMultiplier(TallyRef, AngleMultiplierBase):
            __doc__ = """CM
            """
            __doc__ += AngleMultiplierBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FlagCells(TallyRef, FlagCellsBase):
            __doc__ = """CF
            """
            __doc__ += FlagCellsBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Fluctuation(TallyRef, TallyFluctuationBase):
            __doc__ = """TF
            """
            __doc__ += TallyFluctuationBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FluctuationROC(TallyRef, TallyFluctuationROCBase):
            __doc__ = """FT
            """
            __doc__ += TallyFluctuationROCBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Treatments(TallyRef, TallyTreatmentsBase):
                __doc__ = """FT
                """
                __doc__ += TallyTreatmentsBase().__doc__
                
                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k.lower(), kwargs[k])

        class DoseEnergy(TallyRef, DoseEnergyBase):
            __doc__ = """DE
            """
            __doc__ += DoseEnergyBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseTable(TallyRef, DoseTableBase):
            __doc__ = """DF
            """
            __doc__ += DoseTableBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseFunction(TallyRef, DoseFunctionBase):
            __doc__ = """DF
            """
            __doc__ += DoseFunctionBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class Normalization(DoseNormalizationBase):
                __doc__ = DoseNormalizationBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

        class TimeMultiplier(TallyRef, TimeMultiplierBase):
            __doc__ = """TM
            """
            __doc__ += TimeMultiplierBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class EnergyMultiplier(TallyRef, EnergyMultiplierBase):
            __doc__ = """EM
            """
            __doc__ += EnergyMultiplierBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FlagSurfaces(TallyRef, FlagSurfacesBase):
            __doc__ = """SF
            """
            __doc__ += FlagSurfacesBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        
        class SegmentDivisors(TallyRef, TallySegmentDivisorsBase):
            __doc__ = """SD
            """
            __doc__ += TallySegmentDivisorsBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class Divisor(TallyDivisorBase):
                __doc__ = TallyDivisorBase().__doc__

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

    class Setting(ABC):
        class Comment(TallyRef, TallySettingABC, TallyCommentBase):
            __doc__ = """TC
            """
            __doc__ += TallyCommentBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Print(TallyRef, TallySettingABC, TallyPrintBase):
            __doc__ = """FQ
            """
            __doc__ += TallyPrintBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class NoTransport(NoIDMixin, TallySettingABC, NoTransportBase):
            """NOTRN
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Perturbation(IDManagerMixin, TallySettingABC, PerturbationBase):
            next_id = 1
            used_ids = set()

            __doc__ = """PERT
            """
            __doc__ += PerturbationBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class ReactivityPerturbation(IDManagerMixin, TallySettingABC, 
                                     ReactivityPerturbationBase):
            next_id = 1
            used_ids = set()

            __doc__ = """KPERT
            """
            __doc__ += ReactivityPerturbationBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class CriticalitySensitivity(IDManagerMixin, TallySettingABC, 
                                     CriticalitySensitivityBase):
            next_id = 1
            used_ids = set()

            __doc__ = """KSEN
            """
            __doc__ += CriticalitySensitivityBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class LatticeSpeedTallyEnhancement(NoIDMixin, TallySettingABC, 
                                           LatticeSpeedTallyEnhancementBase):
            __doc__ = """SPDTL
            """
            __doc__ += LatticeSpeedTallyEnhancementBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override

subclass_overrides(Tally, ignore=[Tally.Bin, Tally.Bins, Tally.Setting])
subclass_overrides(Tally.Bin, ignore=[Tally.Bin.Level])
subclass_overrides(Tally.Bins)
subclass_overrides(Tally.Setting)
