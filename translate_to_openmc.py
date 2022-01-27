import openmc
import sys
import math

from openmc.model.surface_composite import XConeOneSided, YConeOneSided, ZConeOneSided
import mcnpy as mp
import numpy as np
import re
from mcnpy import InputDeck
from mcnpy.universe import UniverseBase
from mcnpy.surfaces import Plane, XPlane, YPlane, ZPlane, XCylinder, YCylinder, ZCylinder, XCone, YCone, ZCone, Quadric, XYZQuadric, PPoints, Sphere # , XTorus, YTorus, ZTorus, XPoints, YPoints, ZPoints, 

DEG_RAD = 180. / math.pi
RAD_DEG = 1 / DEG_RAD

"""Translate MCNP to OpenMC.
"""
def decompose_transformation(transform, angle='COSINES'):
    """
    """
    #TODO: Consider angle units and other options.
    #TODO: decomposed transformations should be stored for reuse.
    vector = [transform.disp1, transform.disp2, transform.disp3]
    rot = transform.rotation
    if rot is not None:
        rotX = np.array([rot.xx, rot.yx, rot.zx])
        rotY = np.array([rot.xy, rot.yy, rot.zy])
        rotZ = np.array([rot.xz, rot.yz, rot.zz])

        if str(angle) == 'DEGREES' or str(angle) == '*':
            rotX = np.cos(rotX * RAD_DEG)
            rotY = np.cos(rotY * RAD_DEG)
            rotZ = np.cos(rotZ * RAD_DEG)

        # If a set is all == 0, then it was jumped.
        # Replacing with defaults.
        #TODO: Fix this assumption for defaults.
        if rotX[0] == 0 and rotX[1] == 0 and rotX[2] == 0:
            rotX = [1.0, 0.0, 0.0]
        if rotY[0] == 0 and rotY[1] == 0 and rotY[2] == 0:
            rotY = [0.0, 1.0, 0.0]
        if rotZ[0] == 0 and rotZ[1] == 0 and rotZ[2] == 0:
            rotZ = [0.0, 0.0, 1.0]

        rot_matrix = np.array([rotX, rotY, rotZ]).transpose()
    else:
        rot_matrix = None

    return (vector, rot_matrix)

        

def decompose(deck):
    """Decompose cell complements and macrobodies.
    """
    new_surfaces = {}
    mbodies = {}
    # Define simple surface cards for macrobodies.
    for k in deck.surfaces:
        new_surfaces[k] = deck.surfaces[k]
        # Provide room for decomposing.
        if isinstance(deck.surfaces[k], mp.surfaces.Macrobody):
            surfs, region_pos, region_neg = mp.mbody_decomp.decomp(deck.surfaces[k])
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
            deck.cells[k].region = mp.region_from_expression.from_expression(str(deck.cells[k].region), deck.surfaces, deck.cells)
            region_str = str(deck.cells[k].region)
        # Replace macrobodies with simple surfaces.
        for j in mbodies:
            # Negative halfspaces.
            region_str = re.sub('(?<!\d)\\-'+j+'(?!\d)', mbodies[j][1], region_str)
            # Positive halfspaces.
            region_str = re.sub('(?<!\d)'+j+'(?!\d)', mbodies[j][0], region_str)
        #print(deck.cells[k], region_str)
        deck.cells[k].region = mp.region_from_expression.from_expression(region_str, deck.surfaces, deck.cells)

def boundary(surf):
    #TODO: Add in the other case
    bound = str(surf.boundary_type)
    if bound == '*' or bound.upper() == 'REFLECTIVE':
        return 'reflective'
    else:
        return 'transmission'
    
def make_plane(surf:Plane):
    """
    """
    openmc_surf = openmc.Plane(a=surf.a, b=surf.b, c=surf.c, d=surf.d, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_xplane(surf:XPlane):
    """
    """
    openmc_surf = openmc.Plane(a=1, b=0, c=0, d=surf.x0, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_yplane(surf:XPlane):
    """
    """
    openmc_surf = openmc.Plane(a=0, b=1, c=0, d=surf.y0, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_zplane(surf:XPlane):
    """
    """
    openmc_surf = openmc.Plane(a=0, b=0, c=1, d=surf.z0, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_points_plane(surf:PPoints):
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
    openmc_surf = openmc.Plane(a=a/d, b=b/d, c=c/d, d=d/d, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_sphere(surf:Sphere):
    """
    """
    openmc_surf = openmc.Sphere(x0=surf.x0, y0=surf.y0, z0=surf.z0, r=surf.r, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_xcylinder(surf:XCylinder):
    """
    """
    #openmc_surf = openmc.XCylinder(y0=surf.y0, z0=surf.z0, r=surf.r, boundary_type=boundary(surf), name=surf.name)
    #openmc_surf = openmc.Cylinder(x0=0, y0=surf.y0, z0=surf.z0, r=surf.r, dx=1, dy=0, dz=0, boundary_type=boundary(surf), name=surf.name)
    coef = surf.get_base_coefficients()
    openmc_surf = openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], j=coef['j'], k=coef['k'], boundary_type=boundary(surf), name=surf.name)
    return openmc_surf    

def make_ycylinder(surf:YCylinder):
    """
    """
    #openmc_surf = openmc.YCylinder(x0=surf.x0, z0=surf.z0, r=surf.r, boundary_type=boundary(surf), name=surf.name)
    #openmc_surf = openmc.Cylinder(x0=surf.x0, y0=0, z0=surf.z0, r=surf.r, dx=0, dy=1, dz=0, boundary_type=boundary(surf), name=surf.name)
    coef = surf.get_base_coefficients()
    openmc_surf = openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], j=coef['j'], k=coef['k'], boundary_type=boundary(surf), name=surf.name)
    return openmc_surf  

def make_zcylinder(surf:ZCylinder):
    """
    """
    #openmc_surf = openmc.ZCylinder(x0=surf.x0, y0=surf.y0, r=surf.r, boundary_type=boundary(surf), name=surf.name)
    #openmc_surf = openmc.Cylinder(x0=surf.x0, y0=surf.y0, z0=0, r=surf.r, dx=0, dy=0, dz=1, boundary_type=boundary(surf), name=surf.name)
    coef = surf.get_base_coefficients()
    openmc_surf = openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], j=coef['j'], k=coef['k'], boundary_type=boundary(surf), name=surf.name)
    return openmc_surf  

def make_quadric(surf:Quadric):
    """
    """
    openmc_surf = openmc.Quadric(a=surf.a, b=surf.b, c=surf.c, d=surf.d, e=surf.e, f=surf.f, g=surf.g, h=surf.h, j=surf.j, k=surf.k, boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_xyzquadric(surf:XYZQuadric):
    """
    """
    coef = surf.get_base_coefficients()
    openmc_surf = openmc.Quadric(a=coef['a'], b=coef['b'], c=coef['c'], d=coef['d'], e=coef['e'], f=coef['f'], g=coef['g'], h=coef['h'], j=coef['j'], k=coef['k'], boundary_type=boundary(surf), name=surf.name)
    return openmc_surf

def make_xcone(surf:XCone):
    """
    """
    if surf.sheet is None:
        openmc_surf = openmc.XCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '+':
        openmc_surf = XConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=True, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '-':
        openmc_surf = XConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=False, boundary_type=boundary(surf), name=surf.name)
    else:
        print('This XCone is up sheet creek!', str(surf.sheet.side))
    return openmc_surf 

def make_ycone(surf:YCone):
    """
    """
    if surf.sheet is None:
        openmc_surf = openmc.YCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '+':
        openmc_surf = YConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=True, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '-':
        openmc_surf = YConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=False, boundary_type=boundary(surf), name=surf.name)
    else:
        print('This YCone is up sheet creek!', str(surf.sheet.side))
    return openmc_surf 

def make_zcone(surf:ZCone):
    """
    """
    if surf.sheet is None:
        openmc_surf = openmc.ZCone(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '+':
        openmc_surf = ZConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=True, boundary_type=boundary(surf), name=surf.name)
    elif str(surf.sheet.side) == '-':
        openmc_surf = ZConeOneSided(x0=surf.x0, y0=surf.y0, z0=surf.z0, r2=surf.r2, up=False, boundary_type=boundary(surf), name=surf.name)
    else:
        print('This ZCone is up sheet creek!', str(surf.sheet.side))
    return openmc_surf 

"""def make_cell(cell, openmc_surfaces):
    openmc_cell = openmc.Cell(int(cell.name))
    openmc_cell.region = openmc.Region.from_expression(str(cell.region), openmc_surfaces)
    # Check for cell transformations.
    cell_tr = cell.transformation
    if cell_tr is None:
        transform = cell.transformation
    else:
        transform = cell_tr.transform
    # Apply transformation to openmc cell region.
    if transform is not None:
        tr = decompose_transformation(transform)
        #openmc_cell.region = openmc_cell.region.translate(tr[0])
        openmc_cell.region = openmc_cell.region.rotate(tr[1])
        openmc_cell.region = openmc_cell.region.translate(tr[0])
    
    return openmc_cell"""

def make_material(material, id:str):
    openmc_material = openmc.Material(int(id), id)
    nuclides = material.nuclides
    for i in range(len(nuclides)):
        nuclide = nuclides[i]
        fraction = nuclide.fraction
        isotope = nuclide.element_name()
        unit = 'ao'
        if str(nuclide.unit) == '-':
            unit = 'wo'
        # No C13 is present in the nuclear data library I downloaded.
        # This causes an error when using natural carbon. Use C0 instead.
        if isotope == 'C0':
            openmc_material.add_nuclide(isotope, fraction, unit)
        elif isotope[-1] == '0' and isotope[-2].isdigit() is False:
            openmc_material.add_element(isotope[:-1], fraction, unit)
        else:
            openmc_material.add_nuclide(isotope, fraction, unit)
    return openmc_material

def mcnp_to_openmc(deck:InputDeck):
    """Generate an OpenMC file from MCNP deck.
    """
    openmc_materials = {}
    openmc_surfaces = {}
    openmc_cells = {}
    openmc_universes = {}
    openmc_transformations = {}
    lat_universes = {}
    lat_dims = {}

    # Translate materials.
    openmc_materials[0] = openmc.Material(0, 'void')
    openmc_materials[0].add_nuclide('H1', 1.0)
    openmc_materials[0].set_density('g/cm3', 1e-100)
    mats = openmc.Materials([openmc_materials[0]])

    for k in deck.materials:
        openmc_materials[int(k)] = make_material(deck.materials[k], k)
        mats.append(openmc_materials[int(k)])
    print('Materials Translation Complete')

    # Store displacements and rotations from TR cards.
    # This way their matrices are only created once.
    for k in deck.transformations:
        tr = deck.transformations[k]
        openmc_transformations[k] = (decompose_transformation(tr.transformation, tr.unit))

    # Translate surfaces.
    for k in deck.surfaces:
        surf = deck.surfaces[k]
        if isinstance(surf, Sphere):
            openmc_surfaces[int(k)] = make_sphere(surf)
        elif isinstance(surf, Plane):
            openmc_surfaces[int(k)] = make_plane(surf)
        elif isinstance(surf, XPlane):
            openmc_surfaces[int(k)] = make_xplane(surf)
        elif isinstance(surf, YPlane):
            openmc_surfaces[int(k)] = make_yplane(surf)
        elif isinstance(surf, ZPlane):
            openmc_surfaces[int(k)] = make_zplane(surf)
        elif isinstance(surf, PPoints):
            openmc_surfaces[int(k)] = make_points_plane(surf)
        elif isinstance(surf, Quadric):
            openmc_surfaces[int(k)] = make_quadric(surf)
        elif isinstance(surf, XYZQuadric):
            openmc_surfaces[int(k)] = make_xyzquadric(surf)
        elif isinstance(surf, XCylinder):
            openmc_surfaces[int(k)] = make_xcylinder(surf)
        elif isinstance(surf, YCylinder):
            openmc_surfaces[int(k)] = make_ycylinder(surf)
        elif isinstance(surf, ZCylinder):
            openmc_surfaces[int(k)] = make_zcylinder(surf)
        elif isinstance(surf, XCone):
            openmc_surfaces[int(k)] = make_xcone(surf)
        elif isinstance(surf, YCone):
            openmc_surfaces[int(k)] = make_ycone(surf)
        elif isinstance(surf, ZCone):
            openmc_surfaces[int(k)] = make_zcone(surf)
        #TODO: Add in the rest of the conversions.
        #TODO: This includes, Torii and X, Y, Z point surfaces.
        #TODO: Cones might need to become quadrics for rotations.
        else:
            print('SURFACE ERROR!\n', surf)
        
        if surf.transformation is not None:
            tr = openmc_transformations[surf.transformation.name]
            if tr[1] is not None:
                openmc_surfaces[int(k)] = openmc_surfaces[int(k)].rotate(tr[1])
            openmc_surfaces[int(k)] = openmc_surfaces[int(k)].translate(tr[0])
    print('Surface Translation Complete')

    # Translate universes.
    # Note that universe 0 contains all cells without U keyword.
    lat_u = []
    lat_disp = []
    for k in deck.universes:
        # TODO: Consider the universe's sign.
        universe = deck.universes[k]
        if int(k) not in openmc_universes.keys():
            openmc_universes[int(k)] = openmc.Universe(universe_id=int(k))
        # Loop over all cells in universe.
        #print(universe.cells)
        #print('\n', deck.cells)
        for c in universe.cells:
            # Define cell.
            cell = deck.cells[c]
            #openmc_cells[int(c)] = make_cell(cell, openmc_surfaces)
            openmc_cells[int(c)] = openmc.Cell(int(c))
            #print(str(cell.region), openmc_surfaces.keys())
            openmc_cells[int(c)].region = openmc.Region.from_expression(str(cell.region), openmc_surfaces)
            # TODO: Test cell transformations containing rotations.
            # Check for cell transformations.
            cell_tr = cell.transformation
            # None means no TR card is referenced.
            if cell_tr is None:
                transform = cell.transform
                angle = cell.transform_angle_unit
            # A transformation can be specifed directly instead.
            else:
                transform = cell_tr.transformation
                angle = cell_tr.unit
            # Apply transformation to openmc cell region.
            if transform is not None:
                if cell_tr is not None:
                    tr = openmc_transformations[cell_tr.name]
                else:
                    tr = decompose_transformation(transform, angle)
                if tr[1] is not None:
                    openmc_cells[int(c)].region = openmc_cells[int(c)].region.rotate(tr[1])
                openmc_cells[int(c)].region = openmc_cells[int(c)].region.translate(tr[0])
            
            # Cell with no FILL card.
            if cell.fill is None:
                if cell.material is None:
                    fill = openmc_materials[0]
                else:
                    density = cell.density
                    # Material has not been used by a cell yet.
                    if openmc_materials[int(cell.material.name)].density is None:
                        if str(cell.density_unit) == '-':
                            openmc_materials[int(cell.material.name)].set_density('g/cm3', density)
                        else:
                            openmc_materials[int(cell.material.name)].set_density('atom/cm3', density)
                        fill = openmc_materials[int(cell.material.name)]
                    # Material has at least one density defined for it.
                    else:
                        exist = False
                        # Check if alternate denity has already been used.
                        for m in openmc_materials:
                            if openmc_materials[m].name == cell.material.name:
                                if openmc_materials[m].density == density:
                                    exist = True
                                    fill = openmc_materials[m]
                                    break
                        # Add new material with different density.
                        if exist is False:
                            m_id = str(len(openmc_materials)+1)
                            openmc_materials[m_id] = make_material(cell.material, m_id)
                            fill = openmc_materials[m_id]
                            mats.append(fill)
            # Cell with FILL card.
            elif isinstance(cell.fill.fill, UniverseBase):
                u_id = int(cell.fill.fill.name)
                if u_id not in openmc_universes.keys():
                    openmc_universes[u_id] = openmc.Universe(universe_id=u_id)
                fill = openmc_universes[int(cell.fill.fill.name)]
            # Lattice fill.
            else:
                u_list = []
                # Get lattice array of MCNP universes.
                lattice = cell.get_lattice()
                if lattice.type == '1' or lattice.type.upper() == 'REC':
                    dim = ((1+lattice.k[1]-lattice.k[0]), (1+lattice.j[1]-lattice.j[0]), (1+lattice.i[1]-lattice.i[0]))
                    openmc_lattice = np.empty(dim).astype(openmc.Universe)
                    for z in range(dim[0]):
                        for y in range(dim[1]):
                            for x in range(dim[2]):
                                #print(lattice.lattice[z,y,x])
                                u_id = int(lattice.lattice[z,y,x].name)
                                if u_id not in openmc_universes.keys():
                                    openmc_universes[u_id] = openmc.Universe(universe_id=u_id)
                                openmc_lattice[z,y,x] = openmc_universes[u_id]
                                #print('\n', openmc_lattice[z,y,x], '\n')
                                if openmc_lattice[z,y,x] not in u_list:
                                    u_list.append(openmc_lattice[z,y,x])
                    lat_u.append(u_list)
                    fill = openmc.RectLattice()
                    fill.universes = openmc_lattice
                #TODO: Work on HEX lattices
                else:
                    fill = openmc.HexLattice()

                # Store universe ID of cells containing a lattice.
                # Used later to condense cells/universes.
                lat_universes[int(cell.universe.name)] = int(cell.name)
                # Used later for defining the pitch and translations
                lat_dims[int(cell.universe.name)] = dim

            # Fill cell.
            openmc_cells[int(c)].fill = fill
            # Apply cell transformation to filling universe.
            if transform is not None and isinstance(fill, openmc.Material) is False:
                #print(fill, openmc_cells[int(c)], tr[0])
                #openmc_cells[int(c)] = openmc_cells[int(c)].translation(tr[0])
                #
                #print(fill, openmc_cells[int(c)], tr[0])
                if tr[1] is not None:
                    #openmc_cells[int(c)] = openmc_cells[int(c)].rotation(tr[1])
                    openmc_cells[int(c)].rotation = tr[1]
                openmc_cells[int(c)].translation = tr[0]
            openmc_universes[int(k)].add_cell(openmc_cells[int(c)])
    print('Universe and Cell Translation Complete')
    
    '''
    Assign lattice parameters.
    Remove redundant universes.
    Lattice corrections.
    '''
    q = 0
    for k in lat_universes:
        # ID of a cell containing a lattice.
        cell_id = lat_universes[k]
        # Get the lattice object.
        lat_fill = openmc_cells[cell_id].fill
        # Lattice dimensions
        dims = lat_dims[k]
        # Go through cells and change the lattice universe fill to lattice object.
        for j in openmc_cells:
            if openmc_cells[j].fill == openmc_universes[k]:
                # Use the region filled by the lattice to find the lower left corner of the lattice.
                # Assuming the cell is rectangular (6 planes)
                xlim = []
                ylim = []
                zlim = []
                surfs = openmc_cells[j].region.get_surfaces()
                for s in surfs:
                    if isinstance(surfs[s], openmc.XPlane):
                        xlim.append(surfs[s].x0)
                    elif isinstance(surfs[s], openmc.YPlane):
                        ylim.append(surfs[s].y0)
                    elif isinstance(surfs[s], openmc.ZPlane):
                        zlim.append(surfs[s].z0)
                    elif isinstance(surfs[s], openmc.Plane):
                        #TODO: Consider off axis planes
                        if surfs[s].a == 1 and surfs[s].b == 0 and surfs[s].c == 0:
                            xlim.append(surfs[s].d)
                        elif surfs[s].a == 0 and surfs[s].b == 1 and surfs[s].c == 0:
                            ylim.append(surfs[s].d)
                        elif surfs[s].a == 0 and surfs[s].b == 0 and surfs[s].c == 1:
                            zlim.append(surfs[s].d)
                        else:
                            print("Lattice bounding box off-axis")
                    else:
                        print("LATTICE ERROR!")
                lat_fill.lower_left = [min(xlim), min(ylim), min(zlim)]

                # Calculate the pitch from the lattice dimensions and container cell limits.
                # Note that the lattice dims are in z,y,x order.
                pitch = []
                pitch.append((max(xlim)-min(xlim)) / dims[2])
                pitch.append((max(ylim)-min(ylim)) / dims[1])
                pitch.append((max(zlim)-min(zlim)) / dims[0])
                lat_fill.pitch = pitch

                # Find transformation to center the lattice element at 0,0,0
                dispX = 0 - (max(xlim) - (0.5*dims[2]*pitch[0]))
                dispY = 0 - (max(ylim) - (0.5*dims[1]*pitch[1]))
                dispZ = 0 - (max(zlim) - (0.5*dims[0]*pitch[2]))
                # Currently assume no rotation.
                lat_disp.append( [dispX, dispY, dispZ])
                
                # Fill OpenMC cell with lattice.
                openmc_cells[j].fill = lat_fill

        openmc_cells.pop(cell_id)
        openmc_universes.pop(k)

        '''
        Applies correction transformations to lattice elements.
        This repositions the lattice elements to be centered at 0,0,0.
        It is applied to each lattice seperately. This procedure assumes that
        all lattice elements are defined using the same center point as the lattice itself. 
        '''
        u_list = lat_u[q]
        #print(u_list)
        for r in range(len(u_list)):
            cells = u_list[r].cells
            for c in cells:
                #print(cells[c], lat_disp[q])
                cells[c].region = cells[c].region.translate(lat_disp[q])
                if isinstance(cells[c].fill, openmc.Material) is False:
                    cells[c] = cells[c].translation(lat_disp[q])
        q = q + 1
            
    # The root universe should always have ID 0. 
    # Universe 0 is the default universe in MCNP.
    geom = openmc.Geometry(openmc_universes[0])
    geom.remove_redundant_surfaces()
    return(geom, mats)

if __name__ == '__main__':
    deck = mp.InputDeck()
    deck.import_from_file(filename=sys.argv[1], renumber=True)
    decompose(deck)
    #print(deck.export())
    deck.remove_redundant_surfaces()
    deck.remove_unused_surfaces()
    #print(deck.export(renumber=False))
    print('MCNP Geometry Decomposed\nStarting Translation\n')

    # Tuple with geometry and materials.
    model = mcnp_to_openmc(deck)
    model[1].cross_sections = '/home/peter/openmc_XS/mcnp_endfb71/cross_sections.xml'
    model[1].export_to_xml() # materials
    model[0].export_to_xml() # geometry
    
