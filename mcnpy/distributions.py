from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Distribution(DistributionBase):
    __doc__ = DistributionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Distributions(DistributionsBase):
    __doc__ = DistributionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceVolumer(DependentSourceVolumerBase):
    __doc__ = DependentSourceVolumerBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceParticles(DependentSourceParticlesBase):
    __doc__ = DependentSourceParticlesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributions(DependentSourceDistributionsBase):
    __doc__ = DependentSourceDistributionsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceCells(DependentSourceCellsBase):
    __doc__ = DependentSourceCellsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributionBins(DependentSourceDistributionBinsBase):
    __doc__ = DependentSourceDistributionBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DependentSourceDistributionMatches(DependentSourceDistributionMatchesBase):
    __doc__ = DependentSourceDistributionMatchesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class NestedDistribution(NestedDistributionBase):
    __doc__ = NestedDistributionBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ZeroDist(ZeroDistBase):
    __doc__ = ZeroDistBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override