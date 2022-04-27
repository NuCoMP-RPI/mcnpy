from abc import ABC
from mcnpy.structures import Vector
from mcnpy.variance_reduction import DeterministicTransportSphere as DTS
from mcnpy.wrap import wrappers, overrides
from mcnpy.region import Complement
from mcnpy.lattice import Lattice
import numpy as np

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Cell(CellBase):
    __doc__ = CellBase().__doc__

    def _init(self, name, region, density=0.0, material=None, universe=None, 
              comment=None, **kwargs):
        """Define a `Cell`."""
        self.name = name
        self.universe = universe
        self.material = material
        self.region = region
        self.density = abs(density)
        if density < 0:
            self.density_unit = '-'
        #self.density_unit = density_unit
        if comment is not None:
            self.comment = comment
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    @property
    def name(self):
        return self._e_object.getName()

    @property
    def density(self):
        return self._e_object.getDensity()

    @property
    def no_fission(self):
        return self._e_object.getNoFission()

    @property
    def importances(self):
        imp = self._e_object.getImportances()
        _importances = {}
        for i in imp:
            _importances[i.importance] = i.particles
        return _importances

    @property
    def temperature(self):
        return (self._e_object.getTemperature(), self.tmp_id)

    @property
    def fill(self):
        _fill = self._e_object.getFill()
        if self.lattice is not None:
            lattice = Lattice(i=_fill.i, j=_fill.j, k=_fill.k, type=self.lattice)
            lat = np.array(_fill.lattice)
            dims = []
            dims.append(_fill.i[1]-_fill.i[0]+1)
            dims.append(_fill.j[1]-_fill.j[0]+1)
            dims.append(_fill.k[1]-_fill.k[0]+1)
            lat = lat.reshape(dims[2], dims[1], dims[0])
            lattice.lattice = lat

            return lattice
        else:
            return _fill
    
    @name.setter
    def name(self, name):
        """name : str
        Unique numeric identifier for the cell."""
        if name is not None:
            self._e_object.setName(str(name))

    @density.setter
    def density(self, density):
        if density < 0:
            self.density_unit = '-'
        self._e_object.setDensity(abs(density))

    @no_fission.setter
    def no_fission(self, nonu):
        if nonu <= 0:
            self._e_object.setNoFission(0)
        else:
            self._e_object.setNoFission(1)

    @temperature.setter
    def temperature(self, temp):
        _tmp = self._e_object.getTemperature()
        _tmp_id = self._e_object.getTmpID()
        if isinstance(temp, (list, tuple)):
            if isinstance(temp[0], (list, tuple)):
                for i in range(len(temp[0])):
                    _tmp.append(temp[0][i])
                    _tmp_id.append(temp[1][i])
            else:
                for i in range(len(temp)):
                    _tmp.append(temp[i])
        else:
            _tmp.append(temp)

    @fill.setter
    def fill(self, fill, transform=None, transformation=None):
        _fill = CellFill()
        if isinstance(fill, Lattice):
            _fill.lattice = fill.flatten()
            _fill.i = fill.i
            _fill.j = fill.j
            _fill.k = fill.k
            if fill.transforms is not None:
                _fill.transforms = fill.transforms
            if fill.transformations is not None:
                _fill.transformations = fill.transformations
            if fill.type == 'REC':
                self.lattice = '1'
            else:
                self.lattice = '2'
        else:
            if type(fill).__name__ == 'UniverseList':
                _fill.fill = fill._e_object
            else:
                _fill.fill = fill
            if transform is not None:
                _fill.transform = transform
            if transformation is not None:
                _fill.transformation = transformation
        
        self._e_object.setFill(_fill)

    @importances.setter
    def importances(self, importances:dict):
        imp = self._e_object.getImportances()
        for i in importances:
            imp.append(CellImportance(i, importances[i]))


    def __invert__(self):
        return Complement(self)

    def __str__(self):
            string = 'Cell\n'
            string += '{: <16}=\t{}\n'.format('\tName', self.name)
            string += '{: <16}=\t{}\n'.format('\tComment', self.comment)
            string += '{: <16}=\t{}\n'.format('\tRegion', self.region)
            if (self.material != 0 and self.material is not None):
                string += '{: <16}=\t{}\n'.format('\tMaterial', 
                                                  self.material.name)
            else:
                string += '{: <16}=\t{}\n'.format('\tMaterial', self.material)
            string += '{: <16}=\t{}\n'.format('\tDensity', self.density)
            string += '{: <16}=\t{}\n'.format('\tDensity Unit', 
                                              str(self.density_unit))
            #string += '{: <16}=\t{}\n'.format('\tUniverse', self.universe)

            return string

    def __repr__(self):
        return '(Cell ' + self.name + ')'

#TODO: Would be nice if particles were automatically added to mode from here.
class CellImportance(CellImportanceBase):
    __doc__ = CellImportanceBase().__doc__

    def _init(self, importance, particles):
        self.importance = importance
        self.particles = particles

    def __str__(self):
        string = 'IMP=' + str(self.importance) + ' for ' + str(self.particles)
        return string

    def __repr__(self) -> str:
        return str(self)


class CellFill(CellFillBase):
    __doc__ = CellFillBase().__doc__

    def _init(self, fill, unit, lattice, transformation, transform, 
             transformations, transforms, i, j, k):
        self.fill = fill
        self.unit = unit
        self.lattice = lattice
        self.transformation = transformation
        self.transform = transform
        self.transformations = transformations
        self.transforms = transforms
        self.i = i
        self.j = j
        self.k = k

    def universe_fill(self, universe, cell, transform=None, 
                      transformation=None):
        """`CellFill` using a `UniverseList`, `UniverseBase`, or 
        `UniversesBase`.
        """
        if type(universe).__name__ == 'UniverseList':
            self.fill = universe._e_object
        else:
            self.fill = universe
        if transform is not None:
            self.transform = transform
        if transformation is not None:
            self.transformation = transformation
        cell.fill = self

    def lattice_fill(self, lattice, cell):
        """`CellFill` using a `Lattice`.
        """
        self.lattice = lattice.flatten()
        self.i = lattice.i
        self.j = lattice.j
        self.k = lattice.k
        if lattice.transforms is not None:
            self.transforms = lattice.transforms
        if lattice.transformations is not None:
            self.transformations = lattice.transformations
        cell.fill = self
        if (lattice.type == 'REC'):
            cell.lattice = '1'
        else:
            cell.lattice = '2'


class CellExponentialTransform(CellExponentialTransformBase):
    __doc__ = CellExponentialTransformBase().__doc__
    
    def _init(self, particles, magnitude, axis=None, vector=None):
        """
        """
        self.particles = particles
        self.magnitiude = magnitude
        self.axis = axis
        self.vector = vector

    @property
    def vector(self):
        _v = self._e_object.getVector()
        if _v is None:
            return None
        else:
            return (_v.name, _v.x, _v.y, _v.z)

    @vector.setter
    def vector(self, v):
        if isinstance(v, Vector):
            self._e_object.setVector(v)
        else:
            self._e_object.setVector(Vector(str(v[0]), v[1], v[2], v[3]))

class CellForcedCollision(CellForcedCollisionBase):
    __doc__ = CellForcedCollisionBase().__doc__
    
    def _init(self, particles, which_particles):
        """
        """
        self.particles = particles
        self.which_particles = which_particles

class CellWeightWindow(CellWeightWindowBase):
    __doc__ = CellWeightWindowBase().__doc__
    
    def _init(self, particles, weight_window, index=None):
        """
        """
        self.particles = particles
        self.weight_window = weight_window
        self.index = index

class CellDeterministicContribution(CellDeterministicContributionBase):
    __doc__ = CellDeterministicContributionBase().__doc__
    
    def _init(self, particles, sphere):
        """
        """
        self.particles = particles
        self.sphere = sphere

    @property
    def sphere(self):
        _s = self._e_object.getSphere()
        if _s is None:
            return None
        else:
            return (_s.x, _s.y, _s.z, _s.ri, _s.ro)

    @sphere.setter
    def sphere(self, s):
        if isinstance(s, ):
            self._e_object.setSphere(s)
        else:
            self._e_object.setSphere(DTS(str(s[0]), s[1], s[2], s[3], s[4]))

class CellDetectorContribution(CellDetectorContributionBase):
    __doc__ = CellDetectorContributionBase().__doc__
    
    def _init(self, tally, probability):
        """
        """
        self.tally = tally
        self.probability = probability

class CellEnergyCutoff(CellEnergyCutoffBase):
    __doc__ = CellEnergyCutoffBase().__doc__
    
    def _init(self, particles, lower_cutoff):
        """
        """
        self.particles = particles
        self.lower_cutoff = lower_cutoff

class CellUncollidedSecondaries(CellUncollidedSecondariesBase):
    __doc__ = CellUncollidedSecondariesBase().__doc__
    
    def _init(self, particles, uncollided):
        """
        """
        self.particles = particles
        self.uncollided = uncollided

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override