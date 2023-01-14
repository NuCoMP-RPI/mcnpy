from .wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Point(PointBase):
    """
    A representation of the model object `Point`.
    
    Parameters
    ----------
    x : float
        X for `Point`.
    y : float
        Y for `Point`.
    z : float
        Z for `Point`.
    
    """

    def _init(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def aspoint(p):
        if isinstance(p, Point):
            return p
        else:
            return Point(p[0], p[1], p[2])

    def aslist(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        string = '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
        return string

    def __repr__(self):
        return 'Point: ' + str(self)

class PPoint(PPointBase):
    """
    A representation of the model object `PPoint`.
    
    Parameters
    ----------
    d : float
        D for `PPoint`.
    r : float
        R for `PPoint`.
    
    """
    
    def _init(self, d:float, r:float):
        self.d = d
        self.r = r

    def aspoint(p):
        if isinstance(p, PPoint):
            return p
        else:
            return PPoint(p[0], p[1])

    def aslist(self):
        return [self.d, self.r]

    def __str__(self):
        string = '(' + str(self.d) + ', ' + str(self.r) + ')'
        return string

    def __repr__(self):
        return 'PPoint: ' + str(self)

class Vector(VectorBase):
    """
    A representation of the model object `Vector`.
    
    Parameters
    ----------
    name : int
        Name for `Vector`.
    x : float
        X for `Vector`.
    y : float
        Y for `Vector`.
    z : float
        Z for `Vector`.
    
    """
    
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

class Point_WS(Point_WSBase):
    """
    A representation of the model object `Point_WS`.
    
    Parameters
    ----------
    x : float
        X for `Point_WS`.
    y : float
        Y for `Point_WS`.
    z : float
        Z for `Point_WS`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override