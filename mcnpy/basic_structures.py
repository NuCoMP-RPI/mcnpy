from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Point(PointBase):
    """Custom Point Class"""
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
    """Custom PPoint class"""
    def _init(self, d:float, r:float):
        self.d = d
        self.r = r

    def __str__(self):
        string = '(' + str(self.d) + ', ' + str(self.r) + ')'
        return string

    def __repr__(self):
        return 'PPoint: ' + str(self)

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override