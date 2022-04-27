from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Point(PointBase):
    __doc__ = PointBase().__doc__

    def _init(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def aspoint(p):
        return Point(p[0], p[1], p[2])

    def __str__(self):
        string = '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
        return string

    def __repr__(self):
        return 'Point: ' + str(self)

class PPoint(PPointBase):
    __doc__ = PPointBase().__doc__
    
    def _init(self, d:float, r:float):
        self.d = d
        self.r = r

    def __str__(self):
        string = '(' + str(self.d) + ', ' + str(self.r) + ')'
        return string

    def __repr__(self):
        return 'PPoint: ' + str(self)

class Vector(VectorBase):
    __doc__ = VectorBase().__doc__
    
    def _init(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y,
        self.z = z

    def __str__(self):
        string = ('V' + self.name + ':(' + str(self.x) + ', ' + str(self.y) 
                  + ', ' + str(self.z) + ')')
        return string

    def __repr__(self):
        return 'V' + self.name

class RangeInt(RangeIntBase):
    __doc__ = RangeIntBase().__doc__

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
    __doc__ = LatticeRangeBase().__doc__

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
    __doc__ = LatticeCoordinateBase().__doc__

    def _init(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def __str__(self):
        return '( ' + str(self.i) + ' ' + str(self.j) + ' ' + str(self.k) + ' )'

class LatticeCoordinates(LatticeCoordinatesBase):
    __doc__ = LatticeCoordinatesBase().__doc__

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
    __doc__ = LatticeFlatIndexBase().__doc__

    def _init(self, i):
        self.i = i

    def __str__(self):
        return str(self.i)

class LatticeIndex(LatticeIndexBase):
    __doc__ = LatticeIndexBase().__doc__

    def _init(self, index=None, universe=None):
        self.index = index
        self.universe = universe

class File(FileBase):
    __doc__ = FileBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Point_WS(Point_WSBase):
    __doc__ = Point_WSBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ReacPairs(ReacPairsBase):
    __doc__ = ReacPairsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Values(ValuesBase):
    __doc__ = ValuesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override