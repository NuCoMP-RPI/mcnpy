from collections import OrderedDict
from abc import ABC
import numpy as np
from .tally import Tally
from .wrap import wrappers, overrides
from .region import *
from .points import Point, PPoint
from .mixin import IDManagerMixin

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

def convert_surface(p_surf):
    """Convert from point surface to standard surface.
    """
    if isinstance(p_surf, XPoints):
        offset = 0
    elif isinstance(p_surf, YPoints):
        offset = 1
    else:
        offset = 2
    tol = 1e-12
    tol2 = 1e12
    # Add in missing points
    c = p_surf.points
    if len(c) == 1:
        c.append(c[0])
        c.append(c[0])
    elif len(c) == 2:
        c.append(c[1])

    #print(c)

    t1 = min([c[0][0], c[1][0], c[2][0]])
    t2 = max([c[0][0], c[1][0], c[2][0]])
    t0 = max([(c[0][0]-c[1][0])**2 - (c[0][1]-c[1][1])**2, 
                (c[1][0]-c[2][0])**2 - (c[1][1]-c[2][1])**2,
                (c[0][0]-c[2][0])**2 - (c[0][1]-c[2][1])**2])**0.5
    max_r = max([abs(c[0][1] - c[1][1]), 
                    abs(c[1][1] - c[2][1]),
                    abs(c[0][1] - c[2][1])])

    # Plane
    if t2 - t1 <= tol * t0:
        if isinstance(p_surf, XPoints):
            surf = XPlane(x0=p_surf.points[0][0])
        elif isinstance(p_surf, YPoints):
            surf = YPlane(y0=p_surf.points[0][0])
        else:
            surf = ZPlane(z0=p_surf.points[0][0])
    # Cylinder
    elif max_r <= tol * t0:
        r = sum([c[0][1], c[1][1], c[2][1]])/3
        if isinstance(p_surf, XPoints):
            surf = XCylinder(r=r)
        elif isinstance(p_surf, YPoints):
            surf = YCylinder(r=r)
        else:
            surf = ZCylinder(r=r)
    # One Sheet Cone
    elif (abs(((c[1][0]-c[0][0]) * (c[2][1]-c[1][1])) 
                - ((c[2][0]-c[1][0]) * (c[1][1]-c[0][1]))) * tol2 <= t0**2):
        #print('\nOne sheet\n')
        t1 = c[0][0] + c[1][0] + c[2][0]
        t2 = c[0][1] + c[1][1] + c[2][1]
        sheet = ((3*(c[0][0]*c[0][1] + c[1][0]*c[1][1] + c[2][0]*c[2][1]) - t1*t2) 
                    / (3*(c[0][0]**2 + c[1][0]**2 + c[2][0]**2) - t1**2))
        r2 = sheet**2
        x0 = (t1-t2/sheet) / 3
        if isinstance(p_surf, XPoints):
            surf = XCone(x0=x0, r2=r2, sheet=sheet)
        elif isinstance(p_surf, YPoints):
            surf = YCone(y0=x0, r2=r2, sheet=sheet)
        else:
            surf = ZCone(z0=x0, r2=r2, sheet=sheet)
    else:
        # Plane of two sheets - Error - 
        if (abs(c[0][1]-c[1][1]) > tol2*abs(c[0][0]-c[1][0]) 
            or abs(c[1][1]-c[2][1]) > tol2*abs(c[1][0]-c[2][0]) 
            or abs(c[2][1]-c[0][1]) > tol2*abs(c[2][0]-c[0][0])):
            return 'ERROR: surface would create 2 parallel planes!'
        # Find coefficients for symmetric GQ surface.
        else:
            a = np.zeros(shape=(4,4))
            i0 = 0
            for i in range(3):
                a[0,i] = c[i][0]**2
                if a[0,i] > a[0,i0]:
                    i0 = i
                a[1,i] = c[i][0]
                a[2,i] = 1
                a[3,i] = -c[i][1]**2
            i1 = max(1, 3-i0) - 1
            for i in range(3):
                print(i,i0)
                if i != i0:
                    for j in range(1,4):
                        a[j,i] = a[j,i] - a[0,i]*a[j,i0]/a[0,i0]
                    if abs(a[1,i]) > abs(a[1,i1]):   
                        i1=i
            i2 = 3-i0-i1
            a[2,i2] = a[2,i2]-a[1,i2]*a[2,i1]/a[1,i1]
            a[2,3] = (a[3,i2]-a[1,i2]*a[3,i1]/a[1,i1])/a[2,i2]
            a[1,3] = (a[3,i1]-a[2,i1]*a[2,3])/a[1,i1]
            a[0,3] = (a[3,i0]-a[2,i0]*a[2,3]-a[1,i0]*a[1,3])/a[0,i0]

            # Sphere
            if abs(a[0,3] - 1)*tol2 <= 1:
                # At origin
                if abs(a[1,3] - 1)*tol2 <= t0:
                    surf = Sphere(r=-a[2,3])
                else:
                    x0 = -0.5*a[1,3]
                    r0 = x0**2 - a[2,3]
                    surf = Sphere(x0=x0, r=r0)
            
            # Some kind of SQ
            else:
                coefs = np.zeros(10)
                for i in range(10):
                    coefs[9-i] = (i+1)//8 # Use integer division
                # Paraboloid
                if abs(a[0,3]*tol2) <= 1:
                    """"""
                    coefs[0+offset] = 0 
                    coefs[3+offset] = 0.5 * a[1,3]
                    coefs[7+offset] = -a[2,3] / a[1,3] 
                # Hyperboloid, ellipsoid, or cone
                else:
                    coefs[0+offset] = a[0,3] 
                    coefs[6] = a[2,3] - 0.25*a[1,3]**2/a[0,3]
                    coefs[7+offset] = -0.5 * a[1,3] / a[0,3] 
                    # Two sheet cone
                    if abs(coefs[6]*tol2) <= t0**2 and a[0,3] <= 0:
                        coefs[0] = coefs[7+offset] 
                        coefs[1] = -a[0,3]
                        coefs[2] = 0
                    # Hyperbolid or ellipsoid
                    else:
                        if (coefs[6] > 0 and coefs[7+offset] < t2 
                            and coefs[7+offset] > t1):
                            print('ERROR: points on different sheets!')

                surf = XYZQuadric(a=coefs[0], b=coefs[1], c=coefs[2],
                                    d=coefs[3], e=coefs[4], f=coefs[5],
                                    g=coefs[6], x=coefs[7], y=coefs[8],
                                    z=coefs[9])

    #surf.name = p_surf.name
    surf.boundary_type = p_surf.boundary_type
    #surf.comment = p_surf.comment
    surf.transformation = p_surf.transformation
    return surf

class Halfspace(HalfspaceBase):
    __doc__ = HalfspaceBase().__doc__

    def _init(self, side, surface):
        self.side = side
        self.surface = surface
        """if isinstance(self.surface, Macrobody):
            if self.surface.facet is not None:
                self.facets = self.surface.facet"""
        """if isinstance(self.surface, Macrobody):
            if self.surface.facet is not None:
                self.facets = '.' + str(surface.facet)
            #print(self.facets)"""

    def __and__(self, other):
        if isinstance(other, Intersection):
            return Intersection([self] + other[:])
        else:
            return Intersection((self, other))

    def __or__(self, other):
        if isinstance(other, Union):
            return Union([self] + other[:])
        else:
            return Union((self, other))

    def __invert__(self):
        return -self.surface if str(self.side) == '+' else +self.surface

    def __str__(self):
        string = str(self.surface.name)
        if str(self.side) == '-':
            string = '-' + string
        """else:
            string = '+' + string"""
        if self.facets is not None:
            string = '{}.{}'.format(string, int(self.facets))
        return string

    def __repr__(self):
        return str(self)

    def get_surfaces(self, surfaces=None):
        """
        Returns the surface that this is a halfspace of.

        Parameters
        ----------
        surfaces: collections.OrderedDict, optional
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        Returns
        -------
        surfaces: collections.OrderedDict
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        """
        if surfaces is None:
            surfaces = OrderedDict()

        surfaces[self.surface.name] = self.surface
        return surfaces

    def remove_redundant_surfaces(self, redundant_surfaces):
        """Recursively remove all redundant surfaces referenced by this region

        Parameters
        ----------
        redundant_surfaces : dict
            Dictionary mapping redundant surface IDs to surface IDs for the
            :class:`mcnpy.Surface` instances that should replace them.

        """

        surf = redundant_surfaces.get(self.surface.name)
        if surf is not None:
            self.surface = surf

class Surface(SurfaceBase):
    __doc__ = SurfaceBase().__doc__

    next_id = 1
    used_ids = set()

    """def _init(self, name=None, boundary_type='vacuum', comment=None):
        self.name = name
        if comment is not None:
            self.comment = comment
        self.boundary_type = boundary_type
        self.coefficients = {}"""

    def __pos__(self):
        return Halfspace('+', self)

    def __neg__(self):
        return Halfspace('-', self)

    def __or__(self, other):
        print('here')
        if isinstance(other, Tally.Bin.SurfaceUnion):
            return Tally.Bin.SurfaceUnion([Tally.Bin.UnarySurfaceBin(self)] 
                                         + [Tally.Bin.UnarySurfaceBin(other[:])])
        else:
            return Tally.Bin.SurfaceUnion([Tally.Bin.UnarySurfaceBin(self)] 
                                         + [Tally.Bin.UnarySurfaceBin(other)])

    def __and__(self, other):
        if isinstance(other, Tally.Bin.CellLevel):
            return Tally.Bin.CellLevel([Tally.Bin.UnaryCellBin(self)] 
                                         + Tally.Bin.UnaryCellBin(other[:]))
        else:
            return Tally.Bin.CellLevel([Tally.Bin.UnaryCellBin(self)] 
                                         + [Tally.Bin.UnaryCellBin(other)])

    def __lshift__(self, other):
        if isinstance(other, Tally.Bin.CellLevel):
            return Tally.Bin.SurfaceLevels([Tally.Bin.CellLevel(
                                          Tally.Bin.UnaryCellBin(self))] 
                                          + Tally.Bin.CellLevel(other[:]))
        else:#elif isinstance(other, (Cell, Universe)):
            return Tally.Bin.SurfaceLevels([Tally.Bin.CellLevel(
                                          Tally.Bin.UnaryCellBin(self))] 
                                          + [Tally.Bin.CellLevel(other.__copy__())])

    def get_coefficients(self):
        return self.get_coefficients()

    def print_surface(self):
        string = 'Surface\n'
        string += '{0: <16}{1}{2}\n'.format('\tID', '=\t', str(self.name))
        string += '{0: <16}{1}{2}\n'.format('\tComment', '=\t', self.comment)
        string += '{0: <16}{1}{2}\n'.format('\tType', '=\t', 
                                            type(self).__name__)
        string += '{0: <16}{1}{2}\n'.format('\tBoundary', '=\t', 
                                            self.boundary_type)

        coefficients = '{0: <16}'.format('\tCoefficients') + '\n'
        coeff = self.get_coefficients()
        for k in coeff:
            coefficients += '{0: <16}{1}{2}\n'.format(
                k, '=\t', coeff[k])
        string += coefficients
        if self.transformation is None:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 
                                                'None')
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 'TR' 
                                                + str(self.transformation.name))

        return string

class SurfaceFacet():
    def __init__(self, surface, facet):
        self.surface = surface
        self._facet = facet

    @property
    def facet(self):
        return self._facet

    @facet.setter
    def facet(self, facet):
        if isinstance(self.surface, Macrobody):
            self.facet = self.surface.facets(facet)
        else:
            self.facet = None

    def __pos__(self):
        hs = Halfspace('+', self.surface)
        hs.facets = self.facet
        return hs

    def __neg__(self):
        hs = Halfspace('-', self.surface)
        hs.facets = self.facet
        return hs

    def get_coefficients(self):
        return self.surface.get_coefficients()

    def print_surface(self):
        string = 'Surface\n'
        string += '{0: <16}{1}{2}\n'.format('\tID', '=\t', str(self.surface.name))
        string += '{0: <16}{1}{2}\n'.format('\tComment', '=\t', self.surface.comment)
        string += '{0: <16}{1}{2}\n'.format('\tType', '=\t', 
                                            type(self.surface).__name__)
        string += '{0: <16}{1}{2}\n'.format('\tBoundary', '=\t', 
                                            self.surface.boundary_type)

        coefficients = '{0: <16}'.format('\tCoefficients') + '\n'
        coeff = self.surface.get_coefficients()
        for k in coeff:
            coefficients += '{0: <16}{1}{2}\n'.format(
                k, '=\t', coeff[k])
        string += coefficients
        if self.surface.transformation is None:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 
                                                'None')
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 'TR' 
                                                + str(self.surface.transformation.name))

        return string

class Macrobody(ABC):
    """All macrobodies with facets. Excludes Sphere and Ellipsoid.
    """
    def __getitem__(self, facet):
        return SurfaceFacet(self, facet)

    def facets(self, facet:int):
        """
        """
        mbody_facets = {}
        mbody_facets['RectangularPrism'] = 6
        mbody_facets['Box'] = 6
        mbody_facets['CircularCylinder'] = 3
        mbody_facets['HexagonalPrism'] = 8
        mbody_facets['EllipticalCylinder'] = 3
        mbody_facets['TruncatedCone'] = 3
        mbody_facets['Wedge'] = 5
        mbody_facets['Polyhedron'] = 6

        if (facet >= 0 and facet <= mbody_facets[self.__class__.__name__]):
            return facet
        else:
            print(str(facet) + ' is an invalid facet number for ' 
                  + str(type(self)))
            return None

# Macrobodies

class Sphere(IDManagerMixin, SphereBase, Surface):
    __doc__ = """Sphere defined by origin `(x0, y0, z0)` and radius `r`.
    """
    __doc__ += SphereBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, r=1.0, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['r'] = self.r

        return coef

    def __str__(self):
        return self.print_surface()

class RectangularPrism(IDManagerMixin, RectangularPrismBase, Surface, Macrobody):
    __doc__ = """A rectangular parallelpiped defined by X, Y, and Z limits.
    Can be infinite in 1 dimension if upper and lower bounds are equal.
    """
    __doc__ += RectangularPrismBase().__doc__

    def _init(self, name=None, x0=0.0, x1=0.0, y0=0.0, y1=0.0, z0=0.0, 
              z1=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['x1'] = self.x1
        coef['y0'] = self.y0
        coef['y1'] = self.y1
        coef['z0'] = self.z0
        coef['z1'] = self.z1

        return coef

    def __str__(self):
        return self.print_surface()

class Box(IDManagerMixin, BoxBase, Surface, Macrobody):
    __doc__ = """A Box defined by a corner and 2 or 3 vectors.
    """
    __doc__ += BoxBase().__doc__

    def _init(self, name=None, corner=Point(), vectors=[], boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.corner = corner
        self.vectors = vectors
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['corner'] = self.corner
        coef['vectors'] = self.vectors

        return coef

    def __str__(self):
        return self.print_surface()

class CircularCylinder(IDManagerMixin, CircularCylinderBase, Surface, Macrobody):
    __doc__ = """A right circular cylinder defined by the center of its `base`, an `axis` 
    vector, and radius `r`.
    """
    __doc__ += CircularCylinderBase().__doc__

    def _init(self, name=None, base=Point(), axis=Point(), r=1.0, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.axis = axis
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['axis'] = self.axis
        coef['radis'] = self.r

        return coef   

    def __str__(self):
        return self.print_surface()

class HexagonalPrism(IDManagerMixin, HexagonalPrismBase, Surface, Macrobody):
    __doc__ = """Right Hexagonal Prism defined by a `base` point, `height` vector, and 
    facet vectors `facet1`, `facet2`, and `facet3`. The second and third facet 
    vectors are optional.
    """
    __doc__ += HexagonalPrismBase().__doc__

    def _init(self, name=None, base=Point(), height=Point(), facet1=Point(), facet2=None, 
              facet3=None, boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.height = height
        self.facet1 = facet1
        self.facet2 = facet2
        self.facet3 = facet3
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['height'] = self.height
        coef['facet1'] = self.facet1
        coef['facet2'] = self.facet2
        coef['facet3'] = self.facet3

        return coef   

    def __str__(self):
        return self.print_surface()

class EllipticalCylinder(IDManagerMixin, EllipticalCylinderBase, Surface, Macrobody):
    __doc__ = """Right Elliptical Cylinder defined by a `base` point, `axis` height 
    vector, ellipse major axis vector `v1`, and ellipse minor axis vector `v1` 
    or radius `r`.
    """
    __doc__ += EllipticalCylinderBase().__doc__

    def _init(self, name=None, base=Point(), axis=Point(), v1=Point(), v2=None, rm=None, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.axis = axis
        self.v1 = v1
        self.v2 = v2
        self.rm = rm
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['axis'] = self.axis
        coef['v1'] = self.v1
        coef['v2'] = self.v2
        coef['rm'] = self.rm

        return coef   

    def __str__(self):
        return self.print_surface()

class TruncatedCone(IDManagerMixin, TruncatedConeBase, Surface, Macrobody):
    __doc__ = """Truncated Right Angle Cone defined by a `base` point, `axis` height 
    vector, radius of the lower cone `r0`, and radius of the upper cone `r1`.
    """
    __doc__ += TruncatedConeBase().__doc__

    def _init(self, name=None, base=Point(), axis=Point(), r0=0.0, r1=1.0, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.axis = axis
        self.r0 = r0
        self.r1 = r1
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['axis'] = self.axis
        coef['lower radius'] = self.r0
        coef['upper radius'] = self.r1

        return coef   

    def __str__(self):
        return self.print_surface()

class Wedge(IDManagerMixin, WedgeBase, Surface, Macrobody):
    __doc__ = """A Wedge defined by a `vertex`, 2 `vectors` for sides of the triangular 
    base, and an `axis` height vector.
    """
    __doc__ += WedgeBase().__doc__

    def _init(self, name=None, vertex=Point(), axis=Point(), vectors=[], 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.vertex = vertex
        self.axis = axis
        self.vectors = vectors
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['vertex'] = self.vertex
        coef['axis'] = self.axis
        coef['vectors'] = self.vectors

        return coef   

    def __str__(self):
        return self.print_surface()

class Ellipsoid(IDManagerMixin, EllipsoidBase, Surface, Macrobody):
    __doc__ = """An Ellipsoid defined by a 2 points/vectors and a radius. By default, `rm` is the major radius and `v1` and `v2` are the coordinates of the first and second focii. If `rm < 0` (meaning `rm` is now the minor radius), then `v1` is the coordinates of the ellipsoid's center and `v2` is its major axis vector.
    """
    __doc__ += EllipsoidBase().__doc__

    def _init(self, name=None, v1=Point(), v2=Point(), rm=1.0, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.v1 = v1
        self.v2 = v2
        self.rm = rm
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['v1'] = self.v1
        coef['v2'] = self.v2
        coef['rm'] = self.rm

        return coef   

    def __str__(self):
        return self.print_surface()

class Polyhedron(IDManagerMixin, PolyhedronBase, Surface, Macrobody):
    __doc__ = """An Arbitrary Polyhedron. There must be eight triplets of entries input for the ARB to describe the (x,y,z) of the corners, although some may not be used (just use triplets of zeros). These are followed by six more entries, ni, which follow a prescribed convention: each entry is a four-digit integer that defines a side of the ARB in terms of the corners for the side. For example, the entry 1278 would define this plane surface to be bounded by the first, second, seventh, and eighth triplets (or equivalently, corners). Since three points are sufficient to determine the plane, only the first, second, and seventh corners would be used in this example to determine the plane. The distance from the plane to the fourth corner (corner 8 in the example) is determined by MCNP6. If the absolute value of this distance is greater than 1.0E-6, an error message is given and the distance is printed in the OUTP file along with the (x,y,z) that would lie on the plane. If the fourth digit is zero, the fourth point is ignored. For a four-sided ARB, four non-zero four-digit integers (last digit is zero for four-sided since there are only three corners for each side) are required to define the sides. For a five-sided ARB, five non-zero four-digit integers are required, and six non-zero four-digit integers are required for a six-sided ARB. Since there must be 30 entries altogether for an ARB (or MCNP6 gives an error message), the last two integers are zero for the four-sided ARB and the last integer is zero for a five-sided ARB.
    """
    __doc__ += PolyhedronBase().__doc__

    def _init(self, name=None, corners=[], sides=[], boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.corners = corners
        self.sides = sides
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self._facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['corners'] = self.corners
        coef['sides'] = self.sides

        return coef   

    def __str__(self):
        return self.print_surface()

    def validate(self):
        """Checks that the corners and sides for a valid ARB."""

        num_sides = len(self.sides)
        if (num_sides != 6 and num_sides != 5 and num_sides != 4):
            print('ERROR! Surface ' + str(self.name) + ' has ' + str(num_sides) 
                  + ' sides. Only 4, 5, or 6 sides are allowed.')
        else:
            # Fill in empty positions.
            if (num_sides < 6):
                self.sides.resize(6)
            # Redefine as number of specified sides.
            if (self.sides[4] == 0):
                num_sides = 4
            elif (self.sides[4] != 0 and self.sides[5] == 0):
                num_sides = 5
            else:
                num_sides = 6
            for i in range(num_sides):
                side = str(self.sides[i])
                if (len(side) != 4):
                    if (len(side) == 3):
                        side = side + '0'
                        self.sides[i] = int(side)
                    else:
                        print('Error! Side ' + str(self.name) + '.' + str(i+1) 
                              + ' does not have 4 corners!')
                        break
                else:
                    for j in range(4):
                        if (int(side[j]) < 0 or int(side[j]) > 8):
                            print('Error! Side ' + str(self.name) + '.' + 
                                  str(i+1) + ' has an invalid corner ID number!')
                            break


# Simple Surfaces.
#TODO: Add transformation functions for tori and X, Y, Z surfaces.

class Plane(IDManagerMixin, PlaneBase, Surface):
    __doc__ = """A plane defined by Ax + By + Cz - D = 0.
    """
    __doc__ += PlaneBase().__doc__

    def _init(self, name=None, a=0.0, b=0.0, c=0.0, d=0.0, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c
        coef['d'] = self.d

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 0
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = self.a
        coef['h'] = self.b
        coef['j'] = self.c
        coef['k'] = -self.d

        return coef

    def __str__(self):
        return self.print_surface()

class XPlane(IDManagerMixin, XPlaneBase, Surface):
    __doc__ = """A plane defined by x - x0 = 0.
    """
    __doc__ += XPlaneBase().__doc__

    def _init(self, name=None, x0=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 0
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 1
        coef['h'] = 0
        coef['j'] = 0
        coef['k'] = -self.x0

        return coef

    def __str__(self):
        return self.print_surface()

class YPlane(IDManagerMixin, YPlaneBase, Surface):
    __doc__ = """A plane defined by y - y0 = 0.
    """
    __doc__ += YPlaneBase().__doc__

    def _init(self, name=None, y0=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.y0 = y0
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['y0'] = self.y0

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 0
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 0
        coef['h'] = 1
        coef['j'] = 0
        coef['k'] = -self.y0

        return coef

    def __str__(self):
        return self.print_surface()

class ZPlane(IDManagerMixin, ZPlaneBase, Surface):
    __doc__ = """A plane defined by z - z0 = 0.
    """
    __doc__ += ZPlaneBase().__doc__

    def _init(self, name=None, z0=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.z0 = z0
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['z0'] = self.z0

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 0
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 0
        coef['h'] = 0
        coef['j'] = 1
        coef['k'] = -self.z0

        return coef

    def __str__(self):
        return self.print_surface()

class XCylinder(IDManagerMixin, XCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the x-axis.
    """
    __doc__ += XCylinderBase().__doc__

    def _init(self, name=None, y0=0.0, z0=0.0, r=1.0, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.y0 = y0
        self.z0 = z0
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['r'] = self.r

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 1
        coef['c'] = 1
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 0
        coef['h'] = -2*self.y0
        coef['j'] = -2*self.z0
        coef['k'] = -self.r**2 + self.y0**2 + self.z0**2

        return coef

    def __str__(self):
        return self.print_surface()

class YCylinder(IDManagerMixin, YCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the y-axis.
    """
    __doc__ += YCylinderBase().__doc__

    def _init(self, name=None, x0=0.0, z0=0.0, r=1.0, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.x0 = x0
        self.z0 = z0
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['z0'] = self.z0
        coef['r'] = self.r

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 1
        coef['b'] = 0
        coef['c'] = 1
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = -2*self.x0
        coef['h'] = 0
        coef['j'] = -2*self.z0
        coef['k'] = -self.r**2 + self.x0**2 + self.z0**2

        return coef

    def __str__(self):
        return self.print_surface()

class ZCylinder(IDManagerMixin, ZCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the z-axis.
    """
    __doc__ += ZCylinderBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, r=1.0, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['r'] = self.r

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = 1
        coef['b'] = 1
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = -2*self.x0
        coef['h'] = -2*self.y0
        coef['j'] = 0
        coef['k'] = -self.r**2 + self.x0**2 + self.y0**2

        return coef    

    def __str__(self):
        return self.print_surface()

class XCone(IDManagerMixin, XConeBase, Surface):
    __doc__ = """A cone parallel to the x-axis. `sheet` can be `+/-1`.
    """
    __doc__ += XConeBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, r2=1.0, sheet=None, 
              boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r2 = r2
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        if sheet is not None:
            self.sheet = Sheet(side=sheet)
        else:
            self.sheet = sheet

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['r2'] = self.r2
        coef['sheet'] = self.sheet

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = self.r2
        coef['b'] = -1
        coef['c'] = -1
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = -2*self.r2*self.x0
        coef['h'] = 2*self.y0
        coef['j'] = 2*self.z0
        coef['k'] = self.r2*self.x0**2 - self.y0**2 - self.z0**2

        return coef

    def __str__(self):
        return self.print_surface()

class YCone(IDManagerMixin, YConeBase, Surface):
    __doc__ = """A cone parallel to the y-axis. `sheet` can be `+/-1`.
    """
    __doc__ += YConeBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, r2=1.0, sheet=None, 
              boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r2 = r2
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        if sheet is not None:
            self.sheet = Sheet(side=sheet)
        else:
            self.sheet = sheet

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['r2'] = self.r2
        coef['sheet'] = self.sheet

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = -1
        coef['b'] = self.r2
        coef['c'] = -1
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 2*self.x0
        coef['h'] = -2*self.r2*self.y0
        coef['j'] = 2*self.z0
        coef['k'] = self.r2*self.y0**2 - self.x0**2 - self.z0**2

        return coef

    def __str__(self):
        return self.print_surface()

class ZCone(IDManagerMixin, ZConeBase, Surface):
    __doc__ = """A cone parallel to the z-axis. `sheet` can be `+/-1`.
    """
    __doc__ += ZConeBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, r2=1.0, sheet=None, 
              boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r2 = r2
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        if sheet is not None:
            self.sheet = Sheet(side=sheet)
        else:
            self.sheet = sheet

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['r2'] = self.r2
        coef['sheet'] = self.sheet

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = -1
        coef['b'] = -1
        coef['c'] = self.r2
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = 2*self.x0
        coef['h'] = 2*self.y0
        coef['j'] = -2*self.r2*self.z0
        coef['k'] = self.r2*self.z0**2 - self.x0**2 - self.y0**2

        return coef

    def __str__(self):
        return self.print_surface()

class Quadric(IDManagerMixin, QuadricBase, Surface):
    __doc__ = """Quadric (GQ) with axes not parallel to x-, y-, or z-axis.
    """
    __doc__ += QuadricBase().__doc__

    def _init(self, name=None, a=1, b=0, c=0, d=0, e=0, f=0, g=0, h=0, j=0, k=1, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.j = j
        self.k = k
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c
        coef['d'] = self.d
        coef['e'] = self.e
        coef['f'] = self.f
        coef['g'] = self.g
        coef['h'] = self.h
        coef['j'] = self.j
        coef['k'] = self.k

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """

        return self.get_coefficients

    def __str__(self):
        return self.print_surface()

class XYZQuadric(IDManagerMixin, XYZQuadricBase, Surface):
    __doc__ = """Quadric (SQ) with axes parallel to x-, y-, or z-axis.
    """
    __doc__ += XYZQuadricBase().__doc__

    def _init(self, name=None, a=1, b=0, c=0, d=0, e=0, f=0, g=0, x=0, y=0, z=1, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.x = x
        self.y = y
        self.z = z
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c
        coef['d'] = self.d
        coef['e'] = self.e
        coef['f'] = self.f
        coef['g'] = self.g
        coef['x'] = self.x
        coef['y'] = self.y
        coef['z'] = self.z

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        coef = OrderedDict()
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c
        coef['d'] = self.d
        coef['e'] = self.e
        coef['f'] = self.f
        coef['g'] = 2*(self.d - self.a*self.x)
        coef['h'] = 2*(self.e - self.b*self.y)
        coef['j'] = 2*(self.f - self.c*self.z)
        coef['k'] = (self.a*self.x**2 + self.b*self.y**2 + self.c*self.z**2 
                     - 2*(self.d*self.x + self.e*self.y + self.f*self.z) 
                     + self.g)

        return coef

    def __str__(self):
        return self.print_surface()

class XTorus(IDManagerMixin, XTorusBase, Surface):
    __doc__ = """Torus parallel to x-axis.
    """
    __doc__ += XTorusBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, a=0.0, b=0.0, 
              c=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.a = a
        self.b = b
        self.c = c
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c

        return coef

    def __str__(self):
        return self.print_surface()

class YTorus(IDManagerMixin, YTorusBase, Surface):
    __doc__ = """Torus parallel to y-axis.
    """
    __doc__ += YTorusBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, a=0.0, b=0.0, 
              c=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.a = a
        self.b = b
        self.c = c
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c

        return coef

    def __str__(self):
        return self.print_surface()

class ZTorus(IDManagerMixin, ZTorusBase, Surface):
    __doc__ = """Torus parallel to z-axis.
    """
    __doc__ += ZTorusBase().__doc__

    def _init(self, name=None, x0=0.0, y0=0.0, z0=0.0, a=0.0, b=0.0, 
              c=0.0, boundary_type='VACUUM', comment=None):
        self.name = name
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.a = a
        self.b = b
        self.c = c
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['x0'] = self.x0
        coef['y0'] = self.y0
        coef['z0'] = self.z0
        coef['a'] = self.a
        coef['b'] = self.b
        coef['c'] = self.c

        return coef

    def __str__(self):
        return self.print_surface()

class PPoints(IDManagerMixin, PPointsBase, Surface):
    __doc__ = """Plane defined by 3 points
    """
    __doc__ += PPointsBase().__doc__

    def _init(self, name=None, points=[], boundary_type='VACUUM', comment=None):
        self.name = name
        self.points = points
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['points'] = self.points

        return coef

    def get_base_coefficients(self):
        """Returns coefficients for general quadric (GQ). Used for 
        transformations.
        """
        points = self.points
        p1 = np.array([points[0].x, points[0].y, points[0].z])
        p2 = np.array([points[1].x, points[1].y, points[1].z])
        p3 = np.array([points[2].x, points[2].y, points[2].z])
        v1 = p3 - p1
        v2 = p2 - p1
        cp = np.cross(v1, v2)
        a, b, c = cp
        d = np.dot(cp, p3)
        coef = OrderedDict()
        coef['a'] = 0
        coef['b'] = 0
        coef['c'] = 0
        coef['d'] = 0
        coef['e'] = 0
        coef['f'] = 0
        coef['g'] = a
        coef['h'] = b
        coef['j'] = c
        coef['k'] = -d

        return coef

    def __str__(self):
        return self.print_surface()

class XPoints(IDManagerMixin, XPointsBase, Surface):
    __doc__ = """X symmetric surface defined by points
    """
    __doc__ += XPointsBase().__doc__

    def _init(self, name=None, points=[], boundary_type='VACUUM', comment=None):
        self.name = name
        self.points = points
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['points'] = self.points

        return coef

    def __str__(self):
        return self.print_surface()

    def convert(self):
        return convert_surface(self)

    @property
    def points(self):
        _points = self._e_object.getPoints()
        points = []
        for p in _points:
            points.append(p.aslist())
        return points

    @points.setter
    def points(self, points):
        _points = self._e_object.getPoints()
        del _points[:]
        for p in points:
            _points.append(PPoint.aspoint(p))
            
class YPoints(IDManagerMixin, YPointsBase, Surface):
    __doc__ = """Y symmetric surface defined by points
    """
    __doc__ += YPointsBase().__doc__

    def _init(self, name=None, points=[], boundary_type='VACUUM', comment=None):
        self.name = name
        self.points = points
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['points'] = self.points

        return coef

    def __str__(self):
        return self.print_surface()

    def convert(self):
        return convert_surface(self)

    @property
    def points(self):
        _points = self._e_object.getPoints()
        points = []
        for p in _points:
            points.append(p.aslist())
        return points

    @points.setter
    def points(self, points):
        _points = self._e_object.getPoints()
        del _points[:]
        for p in points:
            _points.append(PPoint.aspoint(p))

class ZPoints(IDManagerMixin, ZPointsBase, Surface):
    __doc__ = """Z symmetric surface defined by points
    """
    __doc__ += ZPointsBase().__doc__

    def _init(self, name=None, points=[], boundary_type='VACUUM', comment=None):
        self.name = name
        self.points = points
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['points'] = self.points

        return coef

    def __str__(self):
        return self.print_surface()

    def convert(self):
        return convert_surface(self)

    @property
    def points(self):
        _points = self._e_object.getPoints()
        points = []
        for p in _points:
            points.append(p.aslist())
        return points

    @points.setter
    def points(self, points):
        _points = self._e_object.getPoints()
        del _points[:]
        for p in points:
            _points.append(PPoint.aspoint(p))

class Sheet(SheetBase):
    __doc__ = SheetBase().__doc__

    def _init(self, side='+'):
        if isinstance(side, str):
            self.side = side
        elif side < 0:
            self.side = '-'
        else:
            self.side = '+'
        self.value = 1
    
    def __str__(self):
        if self.side == '+':
            return 'positive'
        else:
            return 'negative'

    def __repr__(self):
        return str(self)

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override