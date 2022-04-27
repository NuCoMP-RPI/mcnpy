from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class ContDontPrintTallies(ContDontPrintTalliesBase):
    __doc__ = ContDontPrintTalliesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ContEmbeddedGeometry(ContEmbeddedGeometryBase):
    __doc__ = ContEmbeddedGeometryBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ContinueData(ContinueDataBase):
    __doc__ = ContinueDataBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ContTallyPrint(ContTallyPrintBase):
    __doc__ = ContTallyPrintBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override