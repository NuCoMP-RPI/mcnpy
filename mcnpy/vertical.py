from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class CellKeyword(CellKeywordBase):
    __doc__ = CellKeywordBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalCellEntry(VerticalCellEntryBase):
    __doc__ = VerticalCellEntryBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalCellValue(VerticalCellValueBase):
    __doc__ = VerticalCellValueBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalSourceOptions(VerticalSourceOptionsBase):
    __doc__ = VerticalSourceOptionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalSourceValues(VerticalSourceValuesBase):
    __doc__ = VerticalSourceValuesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class VerticalSurfaceEntry(VerticalSurfaceEntryBase):
    __doc__ = VerticalSurfaceEntryBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override