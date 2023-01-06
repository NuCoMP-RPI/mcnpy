import numpy as np

import openmc
from openmc.model.surface_composite import XConeOneSided, YConeOneSided, ZConeOneSided
import mcnpy as mp

def make_openmc_boundary(surf):
    bound = str(surf.boundary_type)
    if bound == '*' or bound.upper() == 'REFLECTIVE':
        return 'reflective'
    elif bound == '+' or bound.upper() == 'WHITE':
        return 'white'
    else:
        return 'vacuum'

def make_mcnp_boundary(surf):
    bound = str(surf.boundary_type).upper()
    if bound == 'REFLECTIVE':
        return bound
    elif bound == 'WHITE':
        return bound
    else:
        return 'VACUUM'
    
def make_openmc_plane(surf: mp.Plane):
    """
    """
    return openmc.Plane(a=surf.a, b=surf.b, c=surf.c, d=surf.d, 
                        boundary_type=make_openmc_boundary(surf), 
                        name=str(surf.name))

def make_openmc_xplane(surf: mp.XPlane):
    """
    """
    return openmc.Plane(a=1, b=0, c=0, d=surf.x0, 
                        boundary_type=make_openmc_boundary(surf), 
                        name=str(surf.name))

def make_openmc_yplane(surf: mp.YPlane):
    """
    """
    return openmc.Plane(a=0, b=1, c=0, d=surf.y0,
                        boundary_type=make_openmc_boundary(surf), 
                        name=str(surf.name))

def make_openmc_zplane(surf: mp.ZPlane):
    """
    """
    return openmc.Plane(a=0, b=0, c=1, d=surf.z0, 
                        boundary_type=make_openmc_boundary(surf), 
                        name=str(surf.name))

def make_openmc_points_plane(surf: mp.PPoints):
    """
    """
    points = surf.points
    p1 = np.array([points[0].x, points[0].y, points[0].z])
    p2 = np.array([points[1].x, points[1].y, points[1].z])
    p3 = np.array([points[2].x, points[2].y, points[2].z])
    v1 = p3 - p1
    v2 = p2 - p1
    cp = np.cross(v2, v1)
    a, b, c = cp
    d = np.dot(cp, p3)
    return openmc.Plane(a=a/d, b=b/d, c=c/d, d=d/d, 
                        boundary_type=make_openmc_boundary(surf), 
                        name=str(surf.name))

def make_openmc_sphere(surf: mp.Sphere):
    """
    """
    return openmc.Sphere(x0=surf.x0, y0=surf.y0, z0=surf.z0, r=surf.r, 
                         boundary_type=make_openmc_boundary(surf), 
                         name=str(surf.name))

def make_openmc_xcylinder(surf: mp.XCylinder):
    """
    """
    coef = surf.get_base_coefficients()
    return openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], 
                          e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], 
                          j=coef['j'], k=coef['k'], 
                          boundary_type=make_openmc_boundary(surf), 
                          name=str(surf.name))

def make_openmc_ycylinder(surf: mp.YCylinder):
    """
    """
    coef = surf.get_base_coefficients()
    return openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], 
                          e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], 
                          j=coef['j'], k=coef['k'], 
                          boundary_type=make_openmc_boundary(surf), 
                          name=str(surf.name))

def make_openmc_zcylinder(surf: mp.ZCylinder):
    """
    """
    coef = surf.get_base_coefficients()
    return openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], 
                          e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], 
                          j=coef['j'], k=coef['k'], 
                          boundary_type=make_openmc_boundary(surf), 
                          name=str(surf.name))

def make_openmc_quadric(surf: mp.Quadric):
    """
    """
    return openmc.Quadric(a=surf.a, b=surf.b, c=surf.c, d=surf.d, e=surf.e, 
                          f=surf.f, g=surf.g, h=surf.h, j=surf.j, k=surf.k, 
                          boundary_type=make_openmc_boundary(surf), 
                          name=str(surf.name))

def make_openmc_xyzquadric(surf: mp.XYZQuadric):
    """
    """
    coef = surf.get_base_coefficients()
    return openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], 
                          e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], 
                          j=coef['j'], k=coef['k'], 
                          boundary_type=make_openmc_boundary(surf), 
                          name=str(surf.name))

def make_openmc_xcone(surf: mp.XCone):
    """
    """
    if surf.sheet is None:
        return openmc.XCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                            boundary_type=make_openmc_boundary(surf), 
                            name=str(surf.name))
    elif str(surf.sheet.side) == '+':
        return XConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=True, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    elif str(surf.sheet.side) == '-':
        return XConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=False, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    else:
        print('This XCone is up sheet creek!', str(surf.sheet.side))

def make_openmc_ycone(surf: mp.YCone):
    """
    """
    if surf.sheet is None:
        return openmc.YCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                            boundary_type=make_openmc_boundary(surf), 
                            name=str(surf.name))
    elif str(surf.sheet.side) == '+':
        return YConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=True, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    elif str(surf.sheet.side) == '-':
        return YConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=False, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    else:
        print('This YCone is up sheet creek!', str(surf.sheet.side))

def make_openmc_zcone(surf: mp.ZCone):
    """
    """
    if surf.sheet is None:
        return openmc.ZCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                            boundary_type=make_openmc_boundary(surf), 
                            name=str(surf.name))
    elif str(surf.sheet.side) == '+':
        return ZConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=True, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    elif str(surf.sheet.side) == '-':
        return ZConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             up=False, boundary_type=make_openmc_boundary(surf), 
                             name=str(surf.name))
    else:
        print('This ZCone is up sheet creek!', str(surf.sheet.side))

def make_openmc_xtorus(surf: mp.XTorus):
    """
    """
    return openmc.XTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_openmc_boundary(surf), 
                         name=str(surf.name))

def make_openmc_ytorus(surf: mp.YTorus):
    """
    """
    return openmc.YTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_openmc_boundary(surf), 
                         name=str(surf.name))

def make_openmc_ztorus(surf: mp.ZTorus):
    """
    """
    return openmc.ZTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_openmc_boundary(surf), 
                         name=str(surf.name))

def make_openmc_xpoints(surf: mp.XPoints):
    """
    """
    new_surf = surf.convert()
    if isinstance(new_surf, mp.XPlane):
        _surf = make_openmc_xplane(new_surf)
    elif isinstance(new_surf, mp.XCone):
        _surf = make_openmc_xcone(new_surf)
    elif isinstance(new_surf, mp.XCylinder):
        _surf = make_openmc_xcylinder(new_surf)
    elif isinstance(new_surf, mp.XYZQuadric):
        _surf = make_openmc_xyzquadric(new_surf)

    _surf.name = surf.name
    return surf

def make_openmc_ypoints(surf: mp.YPoints):
    """
    """
    new_surf = surf.convert()
    if isinstance(new_surf, mp.YPlane):
        _surf = make_openmc_yplane(new_surf)
    elif isinstance(new_surf, mp.YCone):
        _surf = make_openmc_ycone(new_surf)
    elif isinstance(new_surf, mp.YCylinder):
        _surf = make_openmc_ycylinder(new_surf)
    elif isinstance(new_surf, mp.XYZQuadric):
        _surf = make_openmc_xyzquadric(new_surf)

    _surf.name = surf.name
    return surf

def make_openmc_zpoints(surf: mp.ZPoints):
    """
    """
    new_surf = surf.convert()
    if isinstance(new_surf, mp.ZPlane):
        _surf = make_openmc_zplane(new_surf)
    elif isinstance(new_surf, mp.ZCone):
        _surf = make_openmc_zcone(new_surf)
    elif isinstance(new_surf, mp.ZCylinder):
        _surf = make_openmc_zcylinder(new_surf)
    elif isinstance(new_surf, mp.XYZQuadric):
        _surf = make_openmc_xyzquadric(new_surf)

    _surf.name = surf.name
    return surf

def mcnp_surfs_to_openmc(surf):
    if isinstance(surf, mp.Sphere):
        return make_openmc_sphere(surf)
    elif isinstance(surf, mp.Plane):
        return make_openmc_plane(surf)
    elif isinstance(surf, mp.XPlane):
        return make_openmc_xplane(surf)
    elif isinstance(surf, mp.YPlane):
        return make_openmc_yplane(surf)
    elif isinstance(surf, mp.ZPlane):
        return make_openmc_zplane(surf)
    elif isinstance(surf, mp.PPoints):
        return make_openmc_points_plane(surf)
    elif isinstance(surf, mp.Quadric):
        return make_openmc_quadric(surf)
    elif isinstance(surf, mp.XYZQuadric):
        return make_openmc_xyzquadric(surf)
    elif isinstance(surf, mp.XCylinder):
        return make_openmc_xcylinder(surf)
    elif isinstance(surf, mp.YCylinder):
        return make_openmc_ycylinder(surf)
    elif isinstance(surf, mp.ZCylinder):
        return make_openmc_zcylinder(surf)
    elif isinstance(surf, mp.XCone):
        return make_openmc_xcone(surf)
    elif isinstance(surf, mp.YCone):
        return make_openmc_ycone(surf)
    elif isinstance(surf, mp.ZCone):
        return make_openmc_zcone(surf)
    elif isinstance(surf, mp.XTorus):
        return make_openmc_xtorus(surf)
    elif isinstance(surf, mp.YTorus):
        return make_openmc_ytorus(surf)
    elif isinstance(surf, mp.YTorus):
        return make_openmc_ztorus(surf)
    elif isinstance(surf, mp.XPoints):
        return make_openmc_xpoints(surf)
    elif isinstance(surf, mp.YPoints):
        return make_openmc_ypoints(surf)
    elif isinstance(surf, mp.ZPoints):
        return make_openmc_zpoints(surf)
    #TODO: Cones might need to become quadrics for rotations.
    else:
        print('SURFACE ERROR!\n', surf)

def make_mcnp_plane(surf: openmc.Plane):
    """
    """
    return mp.Plane(a=surf.a, b=surf.b, c=surf.c, d=surf.d, 
                        boundary_type=make_openmc_boundary(surf), 
                        name=surf.id)

def make_mcnp_xplane(surf: openmc.XPlane):
    """
    """
    return mp.Plane(a=1, b=0, c=0, d=surf.x0, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_yplane(surf: openmc.YPlane):
    """
    """
    return mp.Plane(a=0, b=1, c=0, d=surf.y0,
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_zplane(surf: openmc.ZPlane):
    """
    """
    return mp.Plane(a=0, b=0, c=1, d=surf.z0, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_xcylinder(surf: openmc.XCylinder):
    """
    """
    return mp.XCylinder(y0=surf.y0, z0=surf.z0, r=surf.r, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_ycylinder(surf: openmc.YCylinder):
    """
    """
    return mp.YCylinder(x0=surf.x0, z0=surf.z0, r=surf.r, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_zcylinder(surf: openmc.ZCylinder):
    """
    """
    return mp.ZCylinder(x0=surf.x0, y0=surf.y0, r=surf.r, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_sphere(surf: openmc.Sphere):
    """
    """
    return mp.Sphere(x0=surf.x0, y0=surf.y0, z0=surf.z0, r=surf.r, 
                         boundary_type=make_mcnp_boundary(surf), 
                         name=surf.id)

def make_mcnp_quadric(surf: openmc.Quadric):
    """
    """
    return mp.Quadric(a=surf.a, b=surf.b, c=surf.c, d=surf.d, e=surf.e, 
                          f=surf.f, g=surf.g, h=surf.h, j=surf.j, k=surf.k, 
                          boundary_type=make_mcnp_boundary(surf), 
                          name=surf.id)

def make_mcnp_xcone(surf: openmc.XCone):
    """
    """
    return mp.XCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_xcone_1side(surf: XConeOneSided):
    """
    """
    if surf.up is True:
        return mp.XCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='+', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)
    else:
        return mp.XCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='-', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)

def make_mcnp_ycone(surf: openmc.YCone):
    """
    """
    return mp.YCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_ycone_1side(surf: YConeOneSided):
    """
    """
    if surf.up is True:
        return mp.YCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='+', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)
    else:
        return mp.YCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='-', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)

def make_mcnp_zcone(surf: openmc.ZCone):
    """
    """
    return mp.ZCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                        boundary_type=make_mcnp_boundary(surf), 
                        name=surf.id)

def make_mcnp_zcone_1side(surf: ZConeOneSided):
    """
    """
    if surf.up is True:
        return mp.ZCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='+', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)
    else:
        return mp.ZCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, 
                             sheet='-', boundary_type=make_mcnp_boundary(surf), 
                             name=surf.id)

def make_mcnp_xtorus(surf: openmc.XTorus):
    """
    """
    return mp.XTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_mcnp_boundary(surf), 
                         name=surf.id)

def make_mcnp_ytorus(surf: openmc.YTorus):
    """
    """
    return mp.YTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_mcnp_boundary(surf), 
                         name=surf.id)

def make_mcnp_ztorus(surf: openmc.ZTorus):
    """
    """
    return mp.ZTorus(x0=surf.x0, y0=surf.y0, z0=surf.z0, a=surf.a, b=surf.b, 
                         c=surf.c, boundary_type=make_mcnp_boundary(surf), 
                         name=surf.id)

def openmc_surfs_to_mcnp(surf):
    """"""
    if isinstance(surf, openmc.Sphere):
        return make_mcnp_sphere(surf)
    elif isinstance(surf, openmc.Plane):
        return make_mcnp_plane(surf)
    elif isinstance(surf, openmc.XPlane):
        return make_mcnp_xplane(surf)
    elif isinstance(surf, openmc.YPlane):
        return make_mcnp_yplane(surf)
    elif isinstance(surf, openmc.ZPlane):
        return make_mcnp_zplane(surf)
    elif isinstance(surf, openmc.Quadric):
        return make_mcnp_quadric(surf)
    elif isinstance(surf, openmc.XCylinder):
        return make_mcnp_xcylinder(surf)
    elif isinstance(surf, openmc.YCylinder):
        return make_mcnp_ycylinder(surf)
    elif isinstance(surf, openmc.ZCylinder):
        return make_mcnp_zcylinder(surf)
    elif isinstance(surf, openmc.XCone):
        return make_mcnp_xcone(surf)
    elif isinstance(surf, openmc.YCone):
        return make_mcnp_ycone(surf)
    elif isinstance(surf, openmc.ZCone):
        return make_mcnp_zcone(surf)
    elif isinstance(surf, openmc.XTorus):
        return make_mcnp_xtorus(surf)
    elif isinstance(surf, openmc.YTorus):
        return make_mcnp_ytorus(surf)
    elif isinstance(surf, openmc.YTorus):
        return make_mcnp_ztorus(surf)
    # These are composite surfaces that would never appear in the XML file.
    # But I already made the functions...
    elif isinstance(surf, XConeOneSided):
        return make_mcnp_xcone_1side(surf)
    elif isinstance(surf, YConeOneSided):
        return make_mcnp_ycone_1side(surf)
    elif isinstance(surf, ZConeOneSided):
        return make_mcnp_zcone_1side(surf)
    else:
        print('SURFACE ERROR!\n', surf)