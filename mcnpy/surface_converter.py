import re
import mcnpy as mp
import serpy as sp

def mcnp_quadric_base(surf):
    """Returns a Serpent Quadratic using MCNP coefs.
    """
    coefs = surf.get_base_coefficients()
    return sp.Quadratic(coefs['a'], coefs['b'], coefs['c'], coefs['d'], 
                        coefs['e'], coefs['f'], coefs['g'], coefs['h'], 
                        coefs['j'], coefs['k'], surf.name)

def serpent_quadratic_base(surf):
    """Returns an MCNP Quadric using Serpent coefs.
    """
    coefs = surf.get_base_coefficients()
    return mp.Quadric(None, coefs['a'], coefs['b'], coefs['c'], coefs['d'], 
                      coefs['e'], coefs['f'], coefs['g'], coefs['h'], 
                      coefs['j'], coefs['k'])

def decompose_mcnp(deck:mp.Deck):
    """Decompose cell complements and macrobodies.
    """
    new_surfaces = {}
    mbodies = {}
    # Define simple surface cards for macrobodies.
    for k in deck.surfaces:
        new_surfaces[k] = deck.surfaces[k]
        # Provide room for decomposing.
        if isinstance(deck.surfaces[k], mp.Macrobody):
            surfs, region_pos, region_neg = mp.decomp(deck.surfaces[k])
            for s in range(len(surfs)):
                new_surfaces[surfs[s].name] = surfs[s]
            # Store lists of the decomposed surfaces.
            mbodies[k] = (str(region_pos), (str(region_neg).replace('(', '').replace(')','')))
    deck.surfaces = new_surfaces

    for k in deck.cells:
        # Decompose cell complements.
        # Note that a surface complement must be in parentheses and will not match '~\d'.
        region_str = str(deck.cells[k].region)
        #print(region_str)
        while len(re.findall('~\d', region_str)) > 0:
            deck.cells[k].region = mp.Region.from_expression(str(deck.cells[k].region), deck.surfaces, deck.cells)
            region_str = str(deck.cells[k].region)
        # Replace macrobodies with simple surfaces.
        for j in mbodies:
            # Negative halfspaces.
            region_str = re.sub('(?<!\d)\\-'+j+'(?!\d)', mbodies[j][1], region_str)
            # Positive halfspaces.
            region_str = re.sub('(?<!\d)'+j+'(?!\d)', mbodies[j][0], region_str)
        #print(deck.cells[k], region_str)
        deck.cells[k].region = mp.Region.from_expression(region_str, deck.surfaces, deck.cells)

def decompose_serpent(deck:sp.Deck):
    """Decompose cell complements and macrobodies.
    """
    new_surfaces = {}
    mbodies = {}
    # Define simple surface cards for macrobodies.
    for k in deck.surfaces:
        new_surfaces[k] = deck.surfaces[k]
        # Provide room for decomposing.
        if isinstance(deck.surfaces[k], sp.Macrobody):
            surfs, region_pos, region_neg = sp.mbody_decomp.decomp(deck.surfaces[k])
            for s in range(len(surfs)):
                new_surfaces[surfs[s].name] = surfs[s]
            # Store lists of the decomposed surfaces.
            mbodies[k] = (str(region_pos), (str(region_neg).replace('(', '').replace(')','')))
    deck.surfaces = new_surfaces

    for k in deck.cells:
        # Decompose cell complements.
        # Note that a surface complement must be in parentheses and will not match '~\d'.
        region_str = str(deck.cells[k].region)
        #print(region_str)
        while len(re.findall('~\d', region_str)) > 0:
            deck.cells[k].region = sp.Region.from_expression(str(deck.cells[k].region), deck.surfaces, deck.cells)
            region_str = str(deck.cells[k].region)
        # Replace macrobodies with simple surfaces.
        for j in mbodies:
            # Negative halfspaces.
            region_str = re.sub('(?<!\d)\\-'+j+'(?!\d)', mbodies[j][1], region_str)
            # Positive halfspaces.
            region_str = re.sub('(?<!\d)'+j+'(?!\d)', mbodies[j][0], region_str)
        #print(deck.cells[k], region_str)
        deck.cells[k].region = sp.Region.from_expression(region_str, deck.surfaces, deck.cells)

def mcnp_surfs_to_serpent(surf):
    """Convert MCNP surface to direct Serpent equivalent
    """
    # Surfaces defined by equations
    # Planes
    if isinstance(surf, mp.Plane):
        return sp.Plane(surf.a, surf.b, surf.c, surf.d, surf.name)
    elif isinstance(surf, mp.XPlane):
        return sp.XPlane(surf.x0, surf.name)
    elif isinstance(surf, mp.YPlane):
        return sp.YPlane(surf.y0, surf.name)
    elif isinstance(surf, mp.ZPlane):
        return sp.ZPlane(surf.z0, surf.name)
    # Points
    elif isinstance(surf, mp.PPoints):
        points = []
        for p in surf.points:
            points.append(p.aslist())
        return sp.PPoints(points, surf.name)
    elif isinstance(surf, mp.XPoints):
        points = []
        for p in surf.points:
            points.append(p.aslist())
        return sp.XPoints(points, surf.name)
    elif isinstance(surf, mp.YPoints):
        points = []
        for p in surf.points:
            points.append(p.aslist())
        return sp.YPoints(points, surf.name)
    elif isinstance(surf, mp.ZPoints):
        points = []
        for p in surf.points:
            points.append(p.aslist())
        return sp.ZPoints(points, surf.name)
    # Torii
    elif isinstance(surf, mp.XTorus):
        return sp.XTorus(surf.x0, surf.y0, surf.z0, surf.a, surf.b, surf.c, 
                         surf.name)
    elif isinstance(surf, mp.YTorus):
        return sp.YTorus(surf.x0, surf.y0, surf.z0, surf.a, surf.b, surf.c, 
                         surf.name)
    elif isinstance(surf, mp.ZTorus):
        return sp.ZTorus(surf.x0, surf.y0, surf.z0, surf.a, surf.b, surf.c, 
                         surf.name)
    # Quadrics
    elif isinstance(surf, mp.Quadric):
        return sp.Quadratic(surf.a, surf.b, surf.c, surf.d, surf.e, surf.f, 
                            surf.g, surf.h, surf.j, surf.k, surf.name)
    elif isinstance(surf, mp.XYZQuadric):
        return mcnp_quadric_base(surf)
    # Cones
    elif isinstance(surf, mp.XCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return sp.XCone(surf.x0, surf.y0, surf.z0, surf.r2, sheet, surf.name)
    elif isinstance(surf, mp.YCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return sp.YCone(surf.x0, surf.y0, surf.z0, surf.r2, sheet, surf.name)
    elif isinstance(surf, mp.ZCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return sp.ZCone(surf.x0, surf.y0, surf.z0, surf.r2, sheet, surf.name)
    # Cylinders
    elif isinstance(surf, mp.XCylinder):
        return sp.XCylinder(surf.y0, surf.z0, surf.r, surf.name)
    elif isinstance(surf, mp.YCylinder):
        return sp.YCylinder(surf.x0, surf.z0, surf.r, surf.name)
    elif isinstance(surf, mp.ZCylinder):
        return sp.ZCylinder(surf.x0, surf.y0, surf.r, surf.name)
    # Sphere
    elif isinstance(surf, mp.Sphere):
        return sp.Sphere(surf.x0, surf.y0, surf.z0, surf.r, surf.name)

    # Macrobodies
    # RPP
    elif isinstance(surf, mp.RectangularPrism):
        #TODO: include 4 plane case
        if surf.z0 == surf.z1:
            return sp.RectangularPrism(surf.x0, surf.x1, surf.y0, surf.y1, surf.name)
        return sp.Cuboid(surf.x0, surf.x1, surf.y0, surf.y1, surf.z0, surf.z1,
                         surf.name)
    # RCC
    elif isinstance(surf, mp.CircularCylinder):
            return sp.CircularCylinder(surf.base.aslist(), surf.axis.aslist(), 
                                       surf.r, surf.name)
    # BOX
    elif isinstance(surf, mp.Box):
        points = []
        for p in surf.vectors:
            points.append(p.aslist())
        return sp.Box(surf.corner.aslist(), points, surf.name)
    else:
        pass
        # Should be handled by decomposition
    
def serpent_surfs_to_mcnp(surf, name=None):
    """Convert Serpent surface to direct MCNP equivalent
    """
    # Surfaces defined by equations
    # Planes
    if isinstance(surf, sp.Plane):
        return mp.Plane(name, surf.a, surf.b, surf.c, surf.d)
    elif isinstance(surf, sp.XPlane):
        return mp.XPlane(name, surf.x0)
    elif isinstance(surf, sp.YPlane):
        return mp.YPlane(name, surf.y0)
    elif isinstance(surf, sp.ZPlane):
        return mp.ZPlane(name, surf.z0)
    # Points
    elif isinstance(surf, sp.PPoints):
        points = []
        for p in surf.points:
            points.append(mp.Point.aspoint(p))
        return mp.PPoints(name, points)
    elif isinstance(surf, sp.XPoints):
        points = []
        for p in surf.points:
            points.append(mp.PPoint.aspoint(p))
        return mp.XPoints(name, points)
    elif isinstance(surf, sp.YPoints):
        points = []
        for p in surf.points:
            points.append(mp.PPoint.aspoint(p))
        return mp.YPoints(name, points)
    elif isinstance(surf, sp.ZPoints):
        points = []
        for p in surf.points:
            points.append(mp.PPoint.aspoint(p))
        return mp.ZPoints(name, points)
    # Torii
    elif isinstance(surf, sp.XTorus):
        return mp.XTorus(name, surf.x0, surf.y0, surf.z0, surf.r, surf.r1, surf.r2)
    elif isinstance(surf, sp.YTorus):
        return mp.YTorus(name, surf.x0, surf.y0, surf.z0, surf.r, surf.r1, surf.r2)
    elif isinstance(surf, sp.ZTorus):
        return mp.ZTorus(name, surf.x0, surf.y0, surf.z0, surf.r, surf.r1, surf.r2)
    # Quadratic
    elif isinstance(surf, sp.Quadratic):
        return mp.Quadric(name, surf.a, surf.b, surf.c, surf.d, surf.e, surf.f, 
                            surf.g, surf.h, surf.i, surf.j)
    # Cones
    elif isinstance(surf, sp.XCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return mp.XCone(name, surf.x0, surf.y0, surf.z0, surf.r2, sheet)
    elif isinstance(surf, sp.YCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return mp.YCone(name, surf.x0, surf.y0, surf.z0, surf.r2, sheet)
    elif isinstance(surf, sp.ZCone):
        if surf.sheet is not None:
            sheet = sp.Sheet(surf.sheet.side)
        else:
            sheet = None
        return mp.ZCone(name, surf.x0, surf.y0, surf.z0, surf.r2, sheet)
    elif isinstance(surf, sp.Cone):
        return mp.TruncatedCone(name, mp.Point.aspoint(surf.base), 
                                mp.Point.aspoint(surf.axis), 0.0, surf.r)
    # Cylinders
    elif isinstance(surf, sp.XCylinder):
        return mp.XCylinder(name, surf.y0, surf.z0, surf.r)
    elif isinstance(surf, sp.YCylinder):
        return mp.YCylinder(name, surf.x0, surf.z0, surf.r)
    elif isinstance(surf, sp.ZCylinder):
        return mp.ZCylinder(name, surf.x0, surf.y0, surf.r)
    # Sphere
    elif isinstance(surf, sp.Sphere):
        return mp.Sphere(name, surf.x0, surf.y0, surf.z0, surf.r)
    
    # Macrobodies
    # Cuboid
    elif isinstance(surf, sp.Cuboid):
        #TODO: include 4 plane case
        return mp.RectangularPrism(name, surf.x1, surf.x2, surf.y1, surf.y2, surf.z1, surf.z2)
    # CircularCylinder
    elif isinstance(surf, sp.CircularCylinder):
        return mp.CircularCylinder(name, mp.Point.aspoint(surf.base), 
                                   mp.Point.aspoint(surf.axis), surf.r)
    # Box
    elif isinstance(surf, sp.Box):
        points = []
        for p in surf.vectors:
            points.append(mp.Point.aspoint(p))
        return mp.Box(name, mp.Point.aspoint(surf.corner), points)
    # CircularCylinder
    elif isinstance(surf, sp.CircularCylinder):
        return mp.CircularCylinder(name, mp.Point.aspoint(surf.base), mp.Point.aspoint(surf.axis), surf.r)
    else:
        pass
        # Should be handled by decomposition