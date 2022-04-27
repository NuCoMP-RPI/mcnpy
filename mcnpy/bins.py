from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class CellBins(CellBinsBase):
    __doc__ = CellBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class CellLevel(CellLevelBase):
    __doc__ = CellLevelBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class CellLevels(CellLevelsBase):
    __doc__ = CellLevelsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class CellUnion(CellUnionBase):
    __doc__ = CellUnionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

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

class UnaryCellBin(UnaryCellBinBase):
    __doc__ = UnaryCellBinBase().__doc__

    def _init(self, cell, index, universe):
        """
        """
        self.cell = cell
        self.index = index
        self.universe = universe

    def __str__(self):
        if self.cell is None and self.universe is None:
            return None
        elif self.universe is not None:
            return 'U=' + self.universe.name
        else:
            return self.cell.name

class UnarySurfaceBin(UnarySurfaceBinBase):
    __doc__ = UnarySurfaceBinBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override