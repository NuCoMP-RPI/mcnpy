import numpy as np

class Lattice():
    def __init__(self, i=[], j=[], k=[], lattice=None, type='REC', universes=None, transforms=None, transformations=None):
        """Class for lattices. Defined by max indicies `i`, `j`, `k`, and a 3D array `lattice`. The array should be defined uning `numpy.array()` where `k` indicies are your outermost dimension followed by `j` and `i`. Elements of `lattice` can be `Universe` objects or simply their IDs. For the latter, `universes = dict()` where its keys are universe IDs and its values are the `Universe` objects.
        """
        dims = []
        self.i = i
        self.j = j
        self.k = k
        self.type = type
        self.transforms = transforms
        self.transformations = transformations
        dims.append(self.i[1]-self.i[0]+1)
        dims.append(self.j[1]-self.j[0]+1)
        dims.append(self.k[1]-self.k[0]+1)
        self.size = dims[0]*dims[1]*dims[2]
        self.lattice = lattice
        self.universes = universes
        
        if (type.upper() == 'REC' or type.upper() == 'RECTANGULAR' or str(type) == '1'):
            self.type = 'REC'
        elif (type.upper() == 'HEX' or type.upper() == 'HEXAGONAL' or str(type) == '2'):
            self.type = 'HEX'
        else:
            self.type = type + ' (INVALID!)'

    def flatten(self):
        """Flattens the provided lattice.
        """
        lattice = self.lattice.reshape(self.size).astype('int32')
        _lattice = []
        for i in range(self.size):
            if self.universes is not None:
                _lattice.append(self.universes[lattice[i]]._e_object)
            else:
                _lattice.append(lattice[i]._e_object)
        return _lattice
            
        

    def __repr__(self):
            string = 'Lattice\n'
            string += '{: <16}=\t{}\n'.format('\tType', self.type)
            string += '{: <16}=\t{}\n'.format('\tUniverses', '\n' + np.array2string(self.lattice, separator=' '))

            return string