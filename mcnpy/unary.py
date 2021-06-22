from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class UnaryCellBins(UnaryCellBinBase):
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

class RangeInt(RangeIntBase):
    def _init(self, value, sign=None):
        """
        """
        self.value = value
        if value < 0:
            self.sign = '-'
        else:
            self.sign = sign

    def __str__(self):
        if self.sign is not None:
            return str(self.sign) + str(self.value)
        else:
            return str(self.value)

class LatticeRange(LatticeRangeBase):
    def _init(self, i0, j0, k0, i1=None, j1=None, k1=None):
        if i0 is not None:
            self.i0 = RangeInt(i0)
        if i1 is not None:
            self.i1 = RangeInt(i1)
        if j0 is not None:
            self.j0 = RangeInt(j0)
        if j1 is not None:
            self.j1 = RangeInt(j1)
        if k0 is not None:
            self.k0 = RangeInt(k0)
        if k1 is not None:
            self.k1 = RangeInt(k1)

    def __str__(self):
        string = '[ '
        if self.i1 is not None:
            string += str(self.i0) + ':' + str(self.i1) + ' '
        else:
            string += str(self.i0) + ' '

        if self.j1 is not None:
            string += str(self.j0) + ':' + str(self.j1) + ' '
        else:
            string += str(self.j0) + ' '

        if self.k1 is not None:
            string += str(self.k0) + ':' + str(self.k1) + ' ]'
        else:
            string += str(self.k0) + ' ]'

        return string

class LatticeCoordinate(LatticeCoordinateBase):
    def _init(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def __str__(self):
        return '( ' + str(self.i) + ' ' + str(self.j) + ' ' + str(self.k) + ' )'

class LatticeCoordinates(LatticeCoordinatesBase):
    def _init(self, coordinates:list):
        self.coordinates = coordinates

    def __str__(self):
        string = '[ '
        for i in range(len(self.coordinates)):
            string += str(self.coordinates[i])
            if (i != len(self.coordinates)):
                string += ', '
        string += ' ]'
        return string

class LatticeFlatIndex(LatticeFlatIndexBase):
    def _init(self, i):
        self.i = i

    def __str__(self):
        return str(self.i)

class LatticeIndex(LatticeIndexBase):
    def _init(self, index=None, universe=None):
        self.index = index
        self.universe = universe

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override