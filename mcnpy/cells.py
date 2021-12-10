from mcnpy.wrap import wrappers, overrides
from mcnpy.region import Complement
from mcnpy.lattice import Lattice
import numpy as np

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Cell(CellBase):
    """My custom cell class."""

    def _init(self, name, region, density=0.0, material=None, universe=None, comment=None):
        self.name = name
        self.universe = universe
        self.material = material
        self.region = region
        self.density = density
        #self.density_unit = density_unit
        self.comment = comment

    def get_lattice(self):
        """Returns a `Lattice` object.
        """
        fill = self.fill
        lattice = Lattice(i=fill.i, j=fill.j, k=fill.k, type=self.lattice)
        lat = np.array(fill.lattice)
        dims = []
        dims.append(fill.i[1]-fill.i[0]+1)
        dims.append(fill.j[1]-fill.j[0]+1)
        dims.append(fill.k[1]-fill.k[0]+1)
        lat = lat.reshape(dims[2], dims[1], dims[0])
        lattice.lattice = lat

        return lattice
        

    def __invert__(self):
        return Complement(self)

    def __str__(self):
            string = 'Cell\n'
            string += '{: <16}=\t{}\n'.format('\tName', self.name)
            string += '{: <16}=\t{}\n'.format('\tComment', self.comment)
            string += '{: <16}=\t{}\n'.format('\tRegion', self.region)
            if (self.material != 0 and self.material is not None):
                string += '{: <16}=\t{}\n'.format('\tMaterial', self.material.name)
            else:
                string += '{: <16}=\t{}\n'.format('\tMaterial', self.material)
            string += '{: <16}=\t{}\n'.format('\tDensity', self.density)
            string += '{: <16}=\t{}\n'.format('\tDensity Unit', str(self.density_unit))
            #string += '{: <16}=\t{}\n'.format('\tUniverse', self.universe)

            return string

    def __repr__(self):
        return '(Cell ' + self.name + ')'

class CellFill(CellFillBase):
    """Custom CellFill class.
    """
    def _init(self, fill, unit, lattice, transformation, transform, transformations, transforms, i, j, k):
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

    def universe_fill(self, universe, cell, transform=None, transformation=None):
        """`CellFill` using a `UniverseList`, `UniverseBase`, or `UniversesBase`."""
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


for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override