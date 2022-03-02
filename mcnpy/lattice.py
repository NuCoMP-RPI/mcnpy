import numpy as np

class Lattice():
    def __init__(self, i=[], j=[], k=[], lattice=None, type='REC', universes=None, transforms=None, transformations=None):
        """Class for lattices. Defined by max indicies `i`, `j`, `k`, and a 3D array `lattice`. The array should be defined uning `numpy.array()` where `k` indicies are your outermost dimension followed by `j` and `i`. Elements of `lattice` can be `Universe` objects or simply their IDs. For the latter, `universes = dict()` where its keys are universe IDs and its values are the `Universe` objects.
        """
        self.dims = []
        self.i = i
        self.j = j
        self.k = k
        self.type = type
        self.transforms = transforms
        self.transformations = transformations
        self.dims.append(self.i[1]-self.i[0]+1)
        self.dims.append(self.j[1]-self.j[0]+1)
        self.dims.append(self.k[1]-self.k[0]+1)
        self.size = self.dims[0]*self.dims[1]*self.dims[2]
        self.lattice = lattice
        self.universes = universes
        
        if (str(type).upper() == 'REC' or str(type).upper() == 'RECTANGULAR' or str(type) == '1'):
            self.type = 'REC'
        elif (str(type).upper() == 'HEX' or str(type).upper() == 'HEXAGONAL' or str(type) == '2'):
            self.type = 'HEX'
        else:
            self.type = str(type) + ' (INVALID!)'

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
            
    def rings(self):
        """For HEX lattices. Lattice must have equal X and Y dimensions. Returns a list of rings describing the lattice. 
        """
        num_rings = int((self.dims[0]-1) / 2) + 1
        rings = []
        for k in range(self.dims[2]):
            rings.append([])
            for r in range(num_rings - 1):
                ring_a = []
                ring_b = []
                ring_c = []
                for j in range(self.dims[1]):
                    index = num_rings - 1 - j
                    stop = len(self.lattice[k,j]) - r 
                    if index > 0:
                        if r == j:
                            ring_c += list(self.lattice[k, j, index+r:stop])
                        elif r - j < 0:
                            ring_c.append(self.lattice[k, j, stop-1])
                            ring_b.append(self.lattice[k, j, index+r])
                    elif index < 0:
                        if r == 2*index + j:
                            ring_b += list(self.lattice[k, j, r:stop+index])
                        elif r - (2*index + j) < 0:
                            ring_a.append(self.lattice[k, j, stop+index-1])
                            ring_b.append(self.lattice[k, j, r])
                    else:
                        ring_c.append(self.lattice[k, j, stop-1])
                        ring_b.append(self.lattice[k, j, r])
                rings[k].append(ring_c[::-1] + ring_b + ring_a[::-1])

            rings[k].append([self.lattice[k, num_rings-1, num_rings-1]])

        return (rings, num_rings)
        

    def __repr__(self):
            string = 'Lattice\n'
            string += '{: <16}=\t{}\n'.format('\tType', str(self.type))
            string += '{: <16}=\t{}\n'.format('\tUniverses', '\n' + np.array2string(self.lattice, separator=' '))

            return string