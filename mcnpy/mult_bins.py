from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

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

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override