import mcnpy as mp
from abc import ABC
from collections.abc import MutableSequence
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Tally(ABC):
    """
    """
    class Tally(ABC):
        """
        """
    class SurfaceCurrent(TallySurfaceCurrentBase, Tally):
        __doc__ = """F1
        """
        __doc__ += TallySurfaceCurrentBase().__doc__

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class SurfaceFlux(TallySurfaceFluxBase, Tally):
        __doc__ = """F2
        """
        __doc__ += TallySurfaceFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class CellFlux(TallyCellFluxBase, Tally):
        __doc__ = """F4
        """
        __doc__ += TallyCellFluxBase().__doc__
        
        def _init(self, name, particles, bins, unit=None, total=None):
            """
            """
            self.name = name
            self.bins = bins
            self.particles = particles
            self.unit = unit
            self.total = total

        @property
        def bins(self):
            return self._e_object.getBins()

        @bins.setter
        def bins(self, bins):
            self._e_object.setBins(Tally.Bins.CellBins(bins))

    class EnergyDeposition(TallyEnergyDepositionBase, Tally):
        __doc__ = """F6
        """
        __doc__ += TallyEnergyDepositionBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class CollisionHeating(TallyCollisionHeatingBase, Tally):
        __doc__ = """+F6
        """
        __doc__ += TallyCollisionHeatingBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class FissionHeating(TallyFissionHeatingBase, Tally):
        __doc__ = """F7
        """
        __doc__ += TallyFissionHeatingBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class PulseHeight(TallyPulseHeightBase, Tally):
        __doc__ = """F8
        """
        __doc__ += TallyPulseHeightBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class ChargeDeposition(TallyChargeDepositionBase, Tally):
        __doc__ = """+F8
        """
        __doc__ += TallyChargeDepositionBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
        
        @property
        def name(self):
            if self._e_object.getName() is None:
                return None
            else:
                return int(self._e_object.getName())
        @name.setter
        def name(self, name):
            if name is not None:
                self._e_object.setName(str(name))

    class Detector(ABC):
        """
        """

    class PointFlux(TallyPointFluxBase, Tally, Detector):
        __doc__ = """F5
        """
        __doc__ += TallyPointFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))

        class Detector(TallyPointFluxDetectorBase):
            __doc__ = TallyPointFluxDetectorBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class RingFlux(TallyRingFluxBase, Detector):
        __doc__ = """F5
        """
        __doc__ += TallyRingFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))

        class Detector(TallyRingFluxDetectorBase):
            __doc__ = TallyRingFluxDetectorBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class RadiographyFlux(ABC):
        """
        """

    class PinholeImageFlux(TallyPinholeImageFluxBase, Tally, RadiographyFlux, Detector):
        __doc__ = """FIP
        """
        __doc__ += TallyPinholeImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))

    class PlanarImageFlux(TallyPlanarImageFluxBase, Tally, RadiographyFlux, Detector):
        __doc__ = """FIR
        """
        __doc__ += TallyPlanarImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))

    class CylindricalImageFlux(TallyCylindricalImageFluxBase, Tally, RadiographyFlux, Detector):
        __doc__ = """FIC
        """
        __doc__ += TallyCylindricalImageFluxBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))


    class FMESH(TallyMeshBase, Tally):
        __doc__ = """FMESH
        """
        __doc__ += TallyMeshBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])
            
            @property
            def name(self):
                if self._e_object.getName() is None:
                    return None
                else:
                    return int(self._e_object.getName())
            @name.setter
            def name(self, name):
                if name is not None:
                    self._e_object.setName(str(name))

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

    class Bins(ABC):
        """
        """
        class Level(ABC):
            def __and__(self, other):
                return Tally.Bins.CellLevel((self, other))

            def __or__(self, other):
                return Tally.Bins.CellUnion((self, other))

            def __lshift__(self, other):
                return Tally.Bins.CellLevels([self] + [other])

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
                    or isinstance(bins, Tally.Bins.Level)): 
                    bins = [bins]
                if isinstance(bins, Tally.Bins.CellLevels):
                    _bins.append(bins)
                else:
                    for i in bins:
                        if isinstance(i, (mp.Cell, mp.Universe)):
                            _bins.append(Tally.Bins.UnaryCellBin(i))
                        else:
                            print(type(i))
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
                    or isinstance(level, Tally.Bins.Level)):
                    level = [level]
                for i in level:
                    if isinstance(i, (mp.Cell, mp.Universe)):
                        _level.append(Tally.Bins.UnaryCellBin(i))
                    else:
                        _level.append(i)

            def __and__(self, other):
                new = Tally.Bins.CellLevel(self)
                new &= other
                return new

            def __iand__(self, other):
                if isinstance(other, Tally.Bins.CellLevel):
                    self.extend(other)
                else:
                    self.level.addUnique(other._e_object)
                return self

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
                return ' & '.join(map(str, self))

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
                    or isinstance(levels, Tally.Bins.Level)):
                    levels = [levels]
                elif isinstance(levels, Tally.Bins.CellLevels):
                    self.extend(levels)
                for i in levels:
                    if isinstance(i, (Tally.Bins.UnaryCellBin, Tally.Bins.CellUnion)):
                        _levels.append(Tally.Bins.CellLevel(i))
                    elif isinstance(i, (mp.Cell, mp.Universe)):
                        _levels.append(Tally.Bins.CellLevel(Tally.Bins.UnaryCellBin(i)))
                    else:
                        _levels.append(i)


            def __lshift__(self, other):
                new = Tally.Bins.CellLevels(self)
                new <<= other
                return new

            def __ilshift__(self, other):
                if isinstance(other, Tally.Bins.CellLevels):
                    self.extend(other)
                else:
                    if isinstance(other, (Tally.Bins.CellUnion, Tally.Bins.UnaryCellBin)):
                        self.levels.addUnique(Tally.Bins.CellLevel([other])._e_object)
                    elif isinstance(other, (mp.Cell, mp.Universe)):
                        self.levels.addUnique(Tally.Bins.CellLevel([Tally.Bins.UnaryCellBin(other)])._e_object)
                    else:
                        self.levels.addUnique(other._e_object)
                return self

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

        class CellUnion(CellUnionBase, Level, MutableSequence):
            __doc__ = CellUnionBase().__doc__

            def _init(self, union):
                """
                """
                self.union = union

            def __or__(self, other):
                new = Tally.Bins.CellUnion(self)
                new |= other
                return new

            def __ior__(self, other):
                if isinstance(other, Tally.Bins.CellUnion):
                    self.extend(other)
                else:
                    self.union.addUnique(other._e_object)
                return self

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

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class SurfaceLevel(SurfaceLevelBase):
            __doc__ = SurfaceLevelBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class SurfaceLevels(SurfaceLevelsBase):
            __doc__ = SurfaceLevelsBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class SurfaceUnion(SurfaceUnionBase):
            __doc__ = SurfaceUnionBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

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
                    string = 'U=' + self.universe.name
                else:
                    string = self.cell.name

                if self.index is not None:
                    string += str(self.index)

                return string

            def __or__(self, other):
                if isinstance(other, Tally.Bins.CellUnion):
                    return Tally.Bins.CellUnion([self] + other[:])
                elif isinstance(other, (mp.Cell, mp.Universe)):
                    return Tally.Bins.CellUnion([self] + [Tally.Bins.UnaryCellBin(other)])
                else:
                    return Tally.Bins.CellUnion((self, other))

            def __and__(self, other):
                if isinstance(other, Tally.Bins.CellLevel):
                    return Tally.Bins.CellLevel([self] + other[:])
                elif isinstance(other, (mp.Cell, mp.Universe)):
                    return Tally.Bins.CellLevel([self] + [Tally.Bins.UnaryCellBin(other)])
                else:
                    return Tally.Bins.CellLevel((self, other))

            def __getitem__(self, index):
                _index = mp.Lattice.Index(index)
                self.index = _index
                return self

        class UnarySurfaceBin(UnarySurfaceBinBase):
            __doc__ = UnarySurfaceBinBase().__doc__

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])


class TallySetting(ABC):
    """
    """
    class Setting(ABC):
        """
        """

    class Comment(TallyCommentBase, Setting):
        __doc__ = """TC
        """
        __doc__ += TallyCommentBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Energies(TallyEnergiesBase, Setting):
        __doc__ = """E
        """
        __doc__ += TallyEnergiesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Times(TallyTimesBase, Setting):
        __doc__ = """T
        """
        __doc__ += TallyTimesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class TimesCyclic(TallyTimesCyclicBase, Setting):
        __doc__ = """T
        """
        __doc__ += TallyTimesCyclicBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Angles(TallyAnglesBase, Setting):
        __doc__ = """C
        """
        __doc__ += TallyAnglesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Print(TallyPrintBase, Setting):
        __doc__ = """FQ
        """
        __doc__ += TallyPrintBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Multiplier(TallyMultiplierBase, Setting):
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

    class Segments(TallySegmentsBase, Setting):
            __doc__ = """FS
            """
            __doc__ += TallySegmentsBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

    class SegmentDivisors(TallySegmentDivisorsBase, Setting):
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

    class User(TallyUserBase, Setting):
        __doc__ = """FU
        """
        __doc__ += TallyUserBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Fluctuation(TallyFluctuationBase, Setting):
        __doc__ = """FT
        """
        __doc__ += TallyFluctuationBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class FluctuationROC(TallyFluctuationROCBase, Setting):
        __doc__ = """FT
        """
        __doc__ += TallyFluctuationROCBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Treatments(TallyTreatmentsBase, Setting):
            __doc__ = """FT
            """
            __doc__ += TallyTreatmentsBase().__doc__
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])



    class DoseEnergy(DoseEnergyBase, Setting):
        __doc__ = """DE
        """
        __doc__ += DoseEnergyBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class DoseTable(DoseTableBase, Setting):
        __doc__ = """DF
        """
        __doc__ += DoseTableBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class DoseFunction(DoseFunctionBase, Setting):
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

    class TimeMultiplier(TimeMultiplierBase, Setting):
        __doc__ = """TM
        """
        __doc__ += TimeMultiplierBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class EnergyMultiplier(EnergyMultiplierBase, Setting):
        __doc__ = """EM
        """
        __doc__ += EnergyMultiplierBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class FlagSurfaces(FlagSurfacesBase, Setting):
        __doc__ = """SF
        """
        __doc__ += FlagSurfacesBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class NoTransport(NoTransportBase, Setting):
        """NOTRN
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Perturbation(PerturbationBase, Setting):
        __doc__ = """PERT
        """
        __doc__ += PerturbationBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class ReactivityPerturbation(ReactivityPerturbationBase, Setting):
        __doc__ = """KPERT
        """
        __doc__ += ReactivityPerturbationBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class CriticalitySensitivity(CriticalitySensitivityBase, Setting):
        __doc__ = """KSEN
        """
        __doc__ += CriticalitySensitivityBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class LatticeSpeedTallyEnhancement(LatticeSpeedTallyEnhancementBase, Setting):
        __doc__ = """SPDTL
        """
        __doc__ += LatticeSpeedTallyEnhancementBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class AngleMultiplier(AngleMultiplierBase, Setting):
        __doc__ = """CM
        """
        __doc__ += AngleMultiplierBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class FlagCells(FlagCellsBase, Setting):
        __doc__ = """CF
        """
        __doc__ += FlagCellsBase().__doc__
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override

subclass_overrides(Tally, ignore=[Tally.Tally, Tally.Detector, 
                                  Tally.RadiographyFlux, Tally.Bins])
subclass_overrides(Tally.Bins, ignore=[Tally.Bins.Level])
subclass_overrides(TallySetting, ignore=[TallySetting.Setting])
