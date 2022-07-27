from collections import OrderedDict
from abc import ABC
import numpy as np

from .wrap import wrappers, overrides
from .region import *
from .points import Point

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Halfspace(HalfspaceBase):
    __doc__ = HalfspaceBase().__doc__

    def _init(self, side, surface):
        self.side = side
        self.surface = surface
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
        string = self.surface.name
        if str(self.side) == '-':
            string = '-' + string
        if self.facets is not None:
            string += str(self.facets)
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

    def _init(self, name=None, boundary_type='vacuum', comment=None):
        self.name = name
        if comment is not None:
            self.comment = comment
        self.boundary_type = boundary_type
        self.coefficients = {}

    def __pos__(self):
        return Halfspace('+', self)

    def __neg__(self):
        return Halfspace('-', self)

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

    @property
    def name(self):
        if self._e_object.getName() is None:
            return None
        else:
            return int(self._e_object.getName())

    @name.setter
    def name(self, name):
        self._e_object.setName(str(name))

class Macrobody(ABC):
    """All macrobodies with facets. Excludes Sphere and Ellipsoid.
    """
    
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
            self.facet = facet
        else:
            print(str(facet) + ' is an invalid facet number for ' 
                  + str(type(self)))
        return self

# Macrobodies

class Sphere(SphereBase, Surface):
    __doc__ = """Sphere defined by origin `(x0, y0, z0)` and radius `r`.
    """
    __doc__ += SphereBase().__doc__

    def _init(self, name, x0:float, y0:float, z0:float, r:float, 
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

class RectangularPrism(RectangularPrismBase, Surface, Macrobody):
    __doc__ = """A rectangular parallelpiped defined by X, Y, and Z limits.
    Can be infinite in 1 dimension if upper and lower bounds are equal.
    """
    __doc__ += RectangularPrismBase().__doc__

    def _init(self, name, x0:float, x1:float, y0:float, y1:float, z0:float, 
              z1:float, boundary_type='VACUUM', comment=None):
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
        self.facet = None

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

class Box(BoxBase, Surface, Macrobody):
    __doc__ = """A Box defined by a corner and 2 or 3 vectors.
    """
    __doc__ += BoxBase().__doc__

    def _init(self, name, corner:Point, vectors:list, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.corner = corner
        self.vectors = vectors
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['corner'] = self.corner
        coef['vectors'] = self.vectors

        return coef

    def __str__(self):
        return self.print_surface()

class CircularCylinder(CircularCylinderBase, Surface, Macrobody):
    __doc__ = """A right circular cylinder defined by the center of its `base`, an `axis` 
    vector, and radius `r`.
    """
    __doc__ += CircularCylinderBase().__doc__

    def _init(self, name, base:Point, axis:Point, r:float, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.axis = axis
        self.r = r
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment
        self.facet = None

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['axis'] = self.axis
        coef['radis'] = self.r

        return coef   

    def __str__(self):
        return self.print_surface()

class HexagonalPrism(HexagonalPrismBase, Surface, Macrobody):
    __doc__ = """Right Hexagonal Prism defined by a `base` point, `height` vector, and 
    facet vectors `facet1`, `facet2`, and `facet3`. The second and third facet 
    vectors are optional.
    """
    __doc__ += HexagonalPrismBase().__doc__

    def _init(self, name, base:Point, height:Point, facet1:Point, facet2=None, 
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

class EllipticalCylinder(EllipticalCylinderBase, Surface, Macrobody):
    __doc__ = """Right Elliptical Cylinder defined by a `base` point, `axis` height 
    vector, ellipse major axis vector `v1`, and ellipse minor axis vector `v1` 
    or radius `r`.
    """
    __doc__ += EllipticalCylinderBase().__doc__

    def _init(self, name, base:Point, axis:Point, v1:Point, v2=None, rm=None, 
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

class TruncatedCone(TruncatedConeBase, Surface, Macrobody):
    __doc__ = """Truncated Right Angle Cone defined by a `base` point, `axis` height 
    vector, radius of the lower cone `r0`, and radius of the upper cone `r1`.
    """
    __doc__ += TruncatedConeBase().__doc__

    def _init(self, name, base:Point, axis:Point, r0:float, r1:float, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.base = base
        self.axis = axis
        self.r0 = r0
        self.r1 = r1
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['base'] = self.base
        coef['axis'] = self.axis
        coef['lower radius'] = self.r0
        coef['upper radius'] = self.r1

        return coef   

    def __str__(self):
        return self.print_surface()

class Wedge(WedgeBase, Surface, Macrobody):
    __doc__ = """A Wedge defined by a `vertex`, 2 `vectors` for sides of the triangular 
    base, and an `axis` height vector.
    """
    __doc__ += WedgeBase().__doc__

    def _init(self, name, vertex:Point, axis:Point, vectors:list, 
              boundary_type='VACUUM', comment=None):
        self.name = name
        self.vertex = vertex
        self.axis = axis
        self.vectors = vectors
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['vertex'] = self.vertex
        coef['axis'] = self.axis
        coef['vectors'] = self.vectors

        return coef   

    def __str__(self):
        return self.print_surface()

class Ellipsoid(EllipsoidBase, Surface, Macrobody):
    __doc__ = """An Ellipsoid defined by a 2 points/vectors and a radius. By default, `rm` is the major radius and `v1` and `v2` are the coordinates of the first and second focii. If `rm < 0` (meaning `rm` is now the minor radius), then `v1` is the coordinates of the ellipsoid's center and `v2` is its major axis vector.
    """
    __doc__ += EllipsoidBase().__doc__

    def _init(self, name, v1:Point, v2:Point, rm:float, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.v1 = v1
        self.v2 = v2
        self.rm = rm
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

    def get_coefficients(self):
        coef = OrderedDict()
        coef['v1'] = self.v1
        coef['v2'] = self.v2
        coef['rm'] = self.rm

        return coef   

    def __str__(self):
        return self.print_surface()

class Polyhedron(PolyhedronBase, Surface, Macrobody):
    __doc__ = """An Arbitrary Polyhedron. There must be eight triplets of entries input for the ARB to describe the (x,y,z) of the corners, although some may not be used (just use triplets of zeros). These are followed by six more entries, ni, which follow a prescribed convention: each entry is a four-digit integer that defines a side of the ARB in terms of the corners for the side. For example, the entry 1278 would define this plane surface to be bounded by the first, second, seventh, and eighth triplets (or equivalently, corners). Since three points are sufficient to determine the plane, only the first, second, and seventh corners would be used in this example to determine the plane. The distance from the plane to the fourth corner (corner 8 in the example) is determined by MCNP6. If the absolute value of this distance is greater than 1.0E-6, an error message is given and the distance is printed in the OUTP file along with the (x,y,z) that would lie on the plane. If the fourth digit is zero, the fourth point is ignored. For a four-sided ARB, four non-zero four-digit integers (last digit is zero for four-sided since there are only three corners for each side) are required to define the sides. For a five-sided ARB, five non-zero four-digit integers are required, and six non-zero four-digit integers are required for a six-sided ARB. Since there must be 30 entries altogether for an ARB (or MCNP6 gives an error message), the last two integers are zero for the four-sided ARB and the last integer is zero for a five-sided ARB.
    """
    __doc__ += PolyhedronBase().__doc__

    def _init(self, name, corners:list, sides:list, boundary_type='VACUUM', 
              comment=None):
        self.name = name
        self.corners = corners
        self.sides = sides
        self.boundary_type = boundary_type
        if comment is not None:
            self.comment = comment

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

class Plane(PlaneBase, Surface):
    __doc__ = """A plane defined by Ax + By + Cz - D = 0.
    """
    __doc__ += PlaneBase().__doc__

    def _init(self, name, a:float, b:float, c:float, d:float, 
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

class XPlane(XPlaneBase, Surface):
    __doc__ = """A plane defined by x - x0 = 0.
    """
    __doc__ += XPlaneBase().__doc__

    def _init(self, name, x0:float, boundary_type='VACUUM', comment=None):
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

class YPlane(YPlaneBase, Surface):
    __doc__ = """A plane defined by y - y0 = 0.
    """
    __doc__ += YPlaneBase().__doc__

    def _init(self, name, y0:float, boundary_type='VACUUM', comment=None):
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

class ZPlane(ZPlaneBase, Surface):
    __doc__ = """A plane defined by z - z0 = 0.
    """
    __doc__ += ZPlaneBase().__doc__

    def _init(self, name, z0:float, boundary_type='VACUUM', comment=None):
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

class XCylinder(XCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the x-axis.
    """
    __doc__ += XCylinderBase().__doc__

    def _init(self, name, y0, z0, r, boundary_type='VACUUM', comment=None):
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

class YCylinder(YCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the y-axis.
    """
    __doc__ += YCylinderBase().__doc__

    def _init(self, name, x0, z0, r, boundary_type='VACUUM', comment=None):
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

class ZCylinder(ZCylinderBase, Surface):
    __doc__ = """A cylinder parallel to the z-axis.
    """
    __doc__ += ZCylinderBase().__doc__

    def _init(self, name, x0, y0, r, boundary_type='VACUUM', comment=None):
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

class XCone(XConeBase, Surface):
    __doc__ = """A cone parallel to the x-axis. `sheet` can be `+/-1`.
    """
    __doc__ += XConeBase().__doc__

    def _init(self, name, x0, y0, z0, r2, sheet=None, boundary_type='VACUUM', 
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
            _sheet = SheetBase()
            _sheet.value = 1
            if isinstance(sheet, str):
                _sheet.side = sheet
            else:
                if sheet > 0:
                    _sheet.side = '+'
                else:
                    _sheet.side = '-'
            self.sheet = _sheet
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

class YCone(YConeBase, Surface):
    __doc__ = """A cone parallel to the y-axis. `sheet` can be `+/-1`.
    """
    __doc__ += YConeBase().__doc__

    def _init(self, name, x0, y0, z0, r2, sheet=None, boundary_type='VACUUM', 
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
            _sheet = SheetBase()
            _sheet.value = 1
            if isinstance(sheet, str):
                _sheet.side = sheet
            else:
                if sheet > 0:
                    _sheet.side = '+'
                else:
                    _sheet.side = '-'
            self.sheet = _sheet
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

class ZCone(ZConeBase, Surface):
    __doc__ = """A cone parallel to the z-axis. `sheet` can be `+/-1`.
    """
    __doc__ += ZConeBase().__doc__

    def _init(self, name, x0, y0, z0, r2, sheet=None, boundary_type='VACUUM', 
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
            _sheet = SheetBase()
            _sheet.value = 1
            if isinstance(sheet, str):
                _sheet.side = sheet
            else:
                if sheet > 0:
                    _sheet.side = '+'
                else:
                    _sheet.side = '-'
            self.sheet = _sheet
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

class Quadric(QuadricBase, Surface):
    __doc__ = """Quadric (GQ) with axes not parallel to x-, y-, or z-axis.
    """
    __doc__ += QuadricBase().__doc__

    def _init(self, name, a=1, b=0, c=0, d=0, e=0, f=0, g=0, h=0, j=0, k=1, 
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

class XYZQuadric(XYZQuadricBase, Surface):
    __doc__ = """Quadric (SQ) with axes parallel to x-, y-, or z-axis.
    """
    __doc__ += XYZQuadricBase().__doc__

    def _init(self, name, a=1, b=0, c=0, d=0, e=0, f=0, g=0, x=0, y=0, z=1, 
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

class XTorus(XTorusBase, Surface):
    __doc__ = """Torus parallel to x-axis.
    """
    __doc__ += XTorusBase().__doc__

    def _init(self, name, x0:float, y0:float, z0:float, a:float, b:float, 
              c:float, boundary_type='VACUUM', comment=None):
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

class YTorus(YTorusBase, Surface):
    __doc__ = """Torus parallel to y-axis.
    """
    __doc__ += YTorusBase().__doc__

    def _init(self, name, x0:float, y0:float, z0:float, a:float, b:float, 
              c:float, boundary_type='VACUUM', comment=None):
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

class ZTorus(ZTorusBase, Surface):
    __doc__ = """Torus parallel to z-axis.
    """
    __doc__ += ZTorusBase().__doc__

    def _init(self, name, x0:float, y0:float, z0:float, a:float, b:float, 
              c:float, boundary_type='VACUUM', comment=None):
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

class PPoints(PPointsBase, Surface):
    __doc__ = """Plane defined by 3 points
    """
    __doc__ += PPointsBase().__doc__

    def _init(self, name, points:list, boundary_type='VACUUM', comment=None):
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

class XPoints(XPointsBase, Surface):
    __doc__ = """X symmetric surface defined by points
    """
    __doc__ += XPointsBase().__doc__

    def _init(self, name, points:list, boundary_type='VACUUM', comment=None):
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

class YPoints(YPointsBase, Surface):
    __doc__ = """Y symmetric surface defined by points
    """
    __doc__ += YPointsBase().__doc__

    def _init(self, name, points:list, boundary_type='VACUUM', comment=None):
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

class ZPoints(ZPointsBase, Surface):
    __doc__ = """Z symmetric surface defined by points
    """
    __doc__ += ZPointsBase().__doc__

    def _init(self, name, points:list, boundary_type='VACUUM', comment=None):
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


for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override