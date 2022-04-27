from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

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

class TMESH(TMESHBase):
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

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override