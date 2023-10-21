import math
import re
import numpy as np
import pathlib
import openmc
import mcnpy as mp
from mcnpy.surface_converter_openmc import mcnp_surfs_to_openmc, openmc_surfs_to_mcnp

DEG_RAD = 180. / math.pi
RAD_DEG = 1 / DEG_RAD

def decompose_mcnp_transformation(transform, angle='COSINES'):
    """Decompose MCNP Transformation into displacement and rotation.

    Parameters
    ----------
    transform : mcnpy.Transform
        Transform being translated.
    angle : str
        Angle unit for `transform`.

    Returns
    -------
    vector : list
        Displacement vector.
    rot_matrix : numpy.array
        Rotation matrix.
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

def plane_distance(p1, p2):
    """Distance between parallel planes.
    """
    # get_base_coefficients makes it agnostic to
    # XPlane, YPlane, Plane, or PointsPlane
    a = p1.get_base_coefficients()
    b = p2.get_base_coefficients()
    dist = abs(a['k'] - b['k']) / (a['g']**2 + a['h']**2 + a['j']**2)**0.5

    return dist

def decompose_mcnp(deck):
    """Decompose cell complements and macrobodies.

    Parameters
    ----------
    deck : mcnpy.Deck
        Deck being decomposed.
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

    for cell in deck.cells.values():
        # Decompose cell complements.
        # Note that a surface complement must be in parentheses and will not match '~\d'.
        region_str = str(cell.region)
        #print(region_str)
        while len(re.findall('~\d', region_str)) > 0:
            cell.region = mp.Region.from_expression(str(cell.region), deck.surfaces, deck.cells)
            region_str = str(cell.region)
        # Replace macrobodies with simple surfaces.
        for j in mbodies:
            # Negative halfspaces.
            region_str = re.sub('(?<!\d)\\-'+str(j)+'(?!\d)', mbodies[j][1], region_str)
            # Positive halfspaces.
            region_str = re.sub('(?<!\d)'+str(j)+'(?!\d)', mbodies[j][0], region_str)
        #print(deck.cells[k], region_str)
        cell.region = mp.Region.from_expression(region_str, deck.surfaces, deck.cells)

        # Generate densities list
        if cell.material is not None:
            rho = (cell.density, cell.density_unit)
            if cell.material.name in deck.material_densities:
                if rho not in deck.material_densities[int(cell.material.name)]:
                    deck.material_densities[int(cell.material.name)].append(rho)
            else:
                deck.material_densities[int(cell.material.name)] = [rho]

def make_openmc_cell(mcnp_cell, openmc_trans, openmc_surfs, openmc_mats, 
                    openmc_universes):
    """Translate MCNP Cell to OpenMC Cell.

    Parameters
    ----------
    mcnp_cell : mcnpy.Cell
        MCNP Cell being translated.
    openmc_trans : dict
        Dict of OpenMC transformations.
    openmc_surfs : dict
        Dict of OpenMC surfaces.
    openmc_mats : dict
        Dict of OpenMC materials.
    openmc_universes : dict
        Dict of OpenMC universes.

    Returns
    -------
    openmc_cell : openmc.Cell
        Translated OpenMC Cell.
    u_list : list or None
        List of universes created during lattice conversion.
    dim : list
        Dimensions for assigning lattice parameters later.
    
    """
    u_list = []
    region = openmc.Region.from_expression(str(mcnp_cell.region), openmc_surfs)
    openmc_cell = openmc.Cell(int(mcnp_cell.name), region=region)
    mcnp_tr = mcnp_cell.transformation
    # Check for cell transformations.
    if mcnp_tr is None:
        # None means no TR card is referenced.
        transform = mcnp_cell.transform
        angle = mcnp_cell.transform_angle_unit
    # A transformation can be specifed directly instead.
    else:
        transform = mcnp_tr.transformation
        angle = mcnp_tr.unit
    # Apply transformation to openmc cell region.
    if transform is not None:
        if mcnp_tr is not None:
            tr = openmc_trans[mcnp_tr.name]
        else:
            tr = decompose_mcnp_transformation(transform, angle)
        if tr[1] is not None:
            openmc_cell.region = openmc_cell.region.rotate(tr[1])
        openmc_cell.region = openmc_cell.region.translate(tr[0])

    # Cell with no FILL card.
    if mcnp_cell.fill is None:
        if mcnp_cell.material is None:
            fill = openmc_mats[0]
        else:
            mats = openmc_mats[mcnp_cell.material.name]

            if len(mats) == 1:
                fill = mats[0]
            else:
                mcnp_density = mcnp_cell.density
                mcnp_unit = mcnp_cell.density_unit
                for mat in mats:
                    if mat.density == mcnp_density:
                        if openmc_mat_density_units(mcnp_unit) == mat.density_units:
                            fill = mat
                            break
    # Cell with FILL card.
    elif isinstance(mcnp_cell.fill, mp.Lattice) is False:
        u_id = int(mcnp_cell.fill.fill.name)
        if u_id not in openmc_universes:
            openmc_universes[u_id] = openmc.Universe(u_id)
        # Apply universe fill transformations.
        u_tr = None
        angle = mcnp_cell.fill.unit
        if mcnp_cell.fill.transform is not None:
            u_tr = decompose_mcnp_transformation(mcnp_cell.fill.transform, angle)
        elif mcnp_cell.fill.transformation is not None:
            u_tr = decompose_mcnp_transformation(mcnp_cell.fill.transformation.transformation, angle)
        if u_tr is not None:
            openmc_cell.region = openmc_cell.region.translate(u_tr[0])
            if u_tr[1] is not None:
                openmc_cell.region = openmc_cell.region.translate(u_tr[0])
        fill = openmc_universes[u_id]
    # Lattice fill.
    else:
        # Get lattice array of MCNP universes.
        lattice = mcnp_cell.fill
        # Dimensions in k, j, i order
        dim = lattice.dims[::-1]
        if str(lattice.type) == '1' or str(lattice.type).upper() == 'REC':
            openmc_lattice = np.empty(dim).astype(openmc.Universe)
            for z in range(dim[0]):
                for y in range(dim[1]):
                    for x in range(dim[2]):
                        u_id = int(lattice.lattice[z,y,x].fill.name)
                        if u_id not in openmc_universes:
                            openmc_universes[u_id] = openmc.Universe(u_id)
                        openmc_lattice[z,y,x] = openmc_universes[u_id]
                        if openmc_lattice[z,y,x] not in u_list:
                            u_list.append(openmc_lattice[z,y,x])
            fill = openmc.RectLattice()
            fill.universes = openmc_lattice
        #TODO: Work on HEX lattices
        #TODO: Find out if OpenMC supports partial rings
        else:
            # List of rings of the lattice
            rings = lattice.rings()
            openmc_rings = []
            for layer in rings[0]:
                openmc_rings.append([])
                for ring in layer:
                    openmc_ring = []
                    for r in ring:
                        u_id = int(r.name)
                        if u_id not in openmc_universes:
                            openmc_universes[u_id] = openmc.Universe(u_id)
                        openmc_ring.append(openmc_universes[u_id])
                        if openmc_ring[-1] not in u_list:
                            u_list.append(openmc_ring[-1])
                    openmc_rings[-1].append(openmc_ring)
            #TODO: get the background fill
            # Might be redundant since we need a fully specified MCNP 
            # lattice which means including elements outside the rings 
            # already.
            fill = openmc.HexLattice()
            fill.universes = openmc_rings
            # Get the pitch.
            # Since we assume equal X and Y pitch, and because the 1st 
            # and 2nd surfaces must be parallel, we just need the 
            # distance for the first plane.
            lat_surfs = list(mcnp_cell.region.get_surfaces().items())
            fill.pitch = [plane_distance(lat_surfs[0][1], lat_surfs[1][1])]
            fill.orientation = 'x'

    # Fill cell.
    openmc_cell.fill = fill
    if transform is not None and isinstance(fill, openmc.Material) is False:
        if tr[1] is not None:
            openmc_cell.rotation = tr[1]
        openmc_cell.translation = tr[0]
    # Add cell to universe in main loop.
    if u_list != []:
        return (openmc_cell, u_list, dim)
    else:
        return (openmc_cell, None, None)

def make_openmc_material(material):
    """Translate MCNP Material to OpenMC Material.

    Parameters
    ----------
    material : mcnpy.Material
        MCNP Material to be translated.

    Returns
    -------
    material : openmc.Material
        Translated OpenMC Material.
    """

    openmc_material = openmc.Material()
    nuclides = material.nuclides
    for i in range(len(nuclides)):
        nuclide = nuclides[i]
        fraction = nuclide.fraction
        isotope = nuclide.name
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

def openmc_mat_density_units(unit):
    """Unit conversion between MCNP and OpenMC.

    Parameters
    ----------
    unit : str
        MCNP density unit.

    Returns
    -------
    openmc_unit : str
        OpenMC density unit.
    """

    if unit == '-':
        return 'g/cm3'
    else:
        return 'atom/cm3'

def mcnp_to_openmc(mcnp_deck: mp.Deck):
    """Translate MCNP Deck to OpenMC Model.
    
    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck to be translated.

    Returns
    -------
    geom : openmc.Geometry
        OpenMC model geometry.
    mats : openmc.Materials
        OpenMC model materials.
    """

    # MCNP deck decomposition and processing.
    mcnp_deck = mp.Deck.read(mcnp_deck._deck, renumber=True)
    print('Decomposing Geometry...')
    decompose_mcnp(mcnp_deck)
    print('Cleaning Up MCNP Surface Cards...')
    mcnp_deck.remove_redundant_surfaces()
    mcnp_deck.remove_unused_surfaces()
    print('Translating MCNP => OpenMC\n')

    # Storage for creating the openmc objects.
    openmc_materials = {}
    openmc_surfaces = {}
    openmc_cells = {}
    openmc_universes = {}
    openmc_transformations = {}

    # Storage for tracking lattice details.
    lat_universes = {}
    lat_dims = {}

    # Translate materials.
    # Define an initial material to stand in for MCNP void.
    openmc_materials[0] = openmc.Material(0, 'void')
    openmc_materials[0].add_nuclide('H1', 1.0)
    openmc_materials[0].set_density('g/cm3', 1e-100)
    mats = openmc.Materials([openmc_materials[0]])

    print('Translating Materials...')
    for mat in mcnp_deck.materials.values():
        try:
            densities = mcnp_deck.material_densities[mat.name]
            if len(densities) >= 1:
                openmc_mat = make_openmc_material(mat)
                openmc_mat.set_density(openmc_mat_density_units(densities[0][1]), 
                                                                densities[0][0])
                openmc_materials[mat.name] = [openmc_mat]
                mats.append(openmc_mat)
            if len(densities) > 1:
                for rho in densities[1:]:
                    mat_copy = openmc_mat.clone()
                    mat_copy.set_density(openmc_mat_density_units(rho[1]), rho[0])
                    openmc_materials[mat.name].append(mat_copy)
                    mats.append(mat_copy)
        except KeyError:
            pass

    # Store displacements and rotations from TR cards.
    # This way their matrices are only created once.
    print('Decomposing Cell Transformations...')
    for k in mcnp_deck.transformations:
        tr = mcnp_deck.transformations[k]
        openmc_transformations[k] = (decompose_mcnp_transformation(tr.transformation, 
                                                              tr.unit))

    # Translate surfaces.
    print('Translating Surfaces...')
    for k in mcnp_deck.surfaces:
        surf = mcnp_deck.surfaces[k]
        openmc_surfaces[int(k)] = mcnp_surfs_to_openmc(surf)
        
        if surf.transformation is not None:
            tr = openmc_transformations[surf.transformation.name]
            if tr[1] is not None:
                openmc_surfaces[int(k)] = openmc_surfaces[int(k)].rotate(tr[1])
            openmc_surfaces[int(k)] = openmc_surfaces[int(k)].translate(tr[0])
    print('Surface Translation Complete')

    # Translate universes.
    # Note that universe 0 contains all cells without U keyword.
    print('Translating Universes and Cells...')
    lat_u = []
    lat_disp = []
    for universe in mcnp_deck.universes.values():
        # TODO: Consider the universe's sign.
        #universe = mcnp_deck.universes[k]
        u_name = int(universe.name)
        if u_name not in openmc_universes:
            openmc_universes[u_name] = openmc.Universe(u_name)
        # Loop over all cells in universe.
        #print(universe.cells)
        #print('\n', deck.cells)
        for cell in universe.cells.values():
            cell_data = make_openmc_cell(cell, openmc_transformations, openmc_surfaces, openmc_materials, openmc_universes)
            openmc_cells[cell_data[0].id] = cell_data[0]
            # Store universe ID of cells containing a lattice.
            # Used later to condense cells/universes.
            if cell_data[1] is not None:
                lat_universes[u_name] = int(cell.name)
                lat_u.append(cell_data[1])
                # Used later for defining the pitch and translations
                lat_dims[u_name] = cell_data[2]
            openmc_universes[u_name].add_cell(cell_data[0])
    print('Universe and Cell Translation Complete')
    
    '''
    Assign lattice parameters.
    Remove redundant universes.
    Lattice corrections.
    '''
    print('Constructing Lattices...')
    q = 0
    for k in lat_universes:
        # ID of a cell containing a lattice.
        cell_id = lat_universes[k]
        # Get the lattice object.
        lat_fill = openmc_cells[cell_id].fill
        # Lattice dimensions
        dims = lat_dims[k]
        # Go through cells and change the lattice universe fill to 
        # lattice object.
        for cell in openmc_cells.values():
            if cell.fill == openmc_universes[k]:
                if isinstance(lat_fill, openmc.RectLattice):
                    #TODO: What if the boundary is not a rectangle?
                    # Use the region filled by the lattice to find the lower 
                    # left corner of the lattice.
                    # Assuming the cell is rectangular (6 planes)
                    xlim = []
                    ylim = []
                    zlim = []
                    surfs = cell.region.get_surfaces()
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

                    # Calculate the pitch from the lattice dimensions and 
                    # container cell limits.
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
                    lat_disp.append([dispX, dispY, dispZ])
                    
                    # Fill OpenMC cell with lattice.
                    #openmc_cells[j].fill = lat_fill
                #TODO: HEX Lattice!
                elif isinstance(lat_fill, openmc.HexLattice):
                    """Need to get:
                    2. outside universe - use universe from corner of MCNP definition
                    3. center of lattice - get center of region on MCNP lat cell
                    """
                    # Time for some assumptions...
                    # We assume the lattice boundary is pretty regular meaning that
                    # it is probably just defined by planes or a cylinder/quadric.
                    # We also assume the Z direction to be axial. 
                    # This should work as long as some sets of planes are axis aligned.
                    surfs = cell.region.get_surfaces()
                    x, y, z = 0, 0, 0
                    xlim = []
                    ylim = []
                    zlim = []
                    center = []
                    for s in surfs:
                        print(s)
                        print(surfs[s].bounding_box('-'))
                        print(surfs[s].bounding_box('+'))
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
                        elif isinstance(surfs[s], openmc.Quadric):
                            x = surfs[s].g * -0.5
                            y = surfs[s].h * -0.5
                            z = surfs[s].j * -0.5
                    #print(xlim, ylim, zlim)
                    if len(xlim) > 0:
                        center.append(min(xlim) + ((max(xlim)-min(xlim)) / 2))
                    else:
                        center.append(x)
                    if len(ylim) > 0:
                        center.append(min(ylim) + ((max(ylim)-min(ylim)) / 2))
                    else:
                        center.append(y)
                    if len(zlim) > 0:
                        center.append(min(zlim) + ((max(zlim)-min(zlim)) / 2))
                    else:
                        center.append(z)
                    #print(x,y,z)
                    #print(center)
                    
                    lat_fill.center = center
                    lat_disp.append([0-center[0], 0-center[1], 0-center[2]])
                    lat_fill.pitch.append((max(zlim)-min(zlim) / dims[0]))

                    print('HEX LATTICE!')

                # Fill OpenMC cell with lattice.
                cell.fill = lat_fill

        openmc_cells.pop(cell_id)
        openmc_universes.pop(k)

        '''
        Applies correction transformations to lattice elements.
        This repositions the lattice elements to be centered at 0,0,0.
        It is applied to each lattice seperately. This procedure assumes that
        all lattice elements are defined using the same center point as the lattice itself. 
        '''
        for universe in lat_u[q]:
            for cell in universe.cells.values():
                cell.region = cell.region.translate(lat_disp[q])
                if isinstance(cell.fill, openmc.Material) is False:
                    cell = cell.translation(lat_disp[q])
        q = q + 1
            
    # The root universe should always have ID 0. 
    # Universe 0 is the default universe in MCNP.
    geom = openmc.Geometry(openmc_universes[0])
    print('Cleaning Up OpenMC Surfaces...')
    geom.remove_redundant_surfaces()
    print('Done!')
    return(geom, mats)

def make_mcnp_material(material: openmc.Material):
    """Translate OpenMC Material to MCNP Material.

    Parameters
    ----------
    material : openmc.Material
        OpenMC Material to be translated.

    Returns
    -------
    material : mcnpy.Material
        Translated MCNP Material.
    """

    nuclides = []
    for nuclide in material.nuclides:
        if nuclide.percent_type == 'wo':
            unit = '-'
        else:
            unit = '+'
        nuclides.append(mp.Nuclide(name=nuclide.name, 
                                  fraction = nuclide.percent,
                                  unit=unit))
    if material.density_units == 'g/cm3':
        return mp.Material(name=material.id, nuclides=nuclides)*material.density
    else:
        return mp.Material(name=material.id, nuclides=nuclides)@material.density

def make_mcnp_cell(mcnp_deck, openmc_cell):
    """Translate OpenMC Cell to MCNP Cell.

    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck being translated to.
    openmc_cell : openmc.Cell
        OpenMC Cell being translated.

    Returns
    -------
    material : mcnpy.Material
        Translated MCNP Material.
    """

    reg = str(openmc_cell.region)
    region = mp.Region.from_expression(reg, mcnp_deck.surfaces, mcnp_deck.cells)
    mcnp_cell = mp.Cell(name=openmc_cell.id, region=region)
    #TODO: check if OpenMC has anything like cell importances.
    mcnp_cell.importances = {'n' : 1.0}
    openmc_fill = openmc_cell.fill
    if isinstance(openmc_fill, openmc.Material) and openmc_fill.id != 0:
        # This will also set the density since we stored densities on the materials.
        mcnp_cell.material = mcnp_deck.materials[openmc_fill.id]
    return mcnp_cell

def make_mcnp_lattice(openmc_lat, mcnp_universes):
    """Translate OpenMC Lattice to MCNP Lattice.

    Parameters
    ----------
    openmc_lat : openmc.RectLattice
        OpenMC lattice being translated.

    Returns
    -------
    mcnp_lat : mcnpy.Lattice
        MCNP Lattice translated to.
    element : mcnpy.Surface
        Surface bounding MCNP lattice element.
    lat_disp : list
        Lattice displacement.
    lat_u : list
        Universes in lattice.
    transformation : mcnpy.Transformation or None
        Transfprmation to reposition lattice.
    """

    lat_u = []
    if isinstance(openmc_lat, openmc.RectLattice):
        shape = openmc_lat.shape[::-1] #z,y,x order
        lattice = np.empty(shape, 'int32')
        for z in range(shape[0]):
            for y in range(shape[1]):
                for x in range(shape[2]):
                    openmc_id = int(openmc_lat.universes[z][y][x].id)
                    lattice[z][y][x] = openmc_id
                    if openmc_id not in lat_u:
                        lat_u.append(openmc_id)

        pitch = openmc_lat.pitch
        lleft = openmc_lat.lower_left
        xmin = lleft[0] / shape[2]
        xmax = xmin + pitch[0]
        ymin = lleft[1] / shape[1]
        ymax = ymin + pitch[1]
        zmin = lleft[2] / shape[0]
        zmax = zmin + pitch[2]
        element = mp.RectangularPrism(None, xmin, xmax, ymin, ymax, zmin, zmax)

        lat_disp = []
        lat_disp.append(lleft[0] + 0.5*(shape[2]*pitch[0]))
        lat_disp.append(lleft[1] + 0.5*(shape[1]*pitch[1]))
        lat_disp.append(lleft[2] + 0.5*(shape[0]*pitch[2]))

        trans = [0,0,0]
        if shape[2]%2 == 0 and shape[2] != 0:
            dim = (shape[2]-1) / 2
            i = [-dim-0.5, dim-0.5]
            trans[0] = trans[0] + openmc_lat.pitch[0]/2 
        else:
            dim = (shape[2]-1) / 2
            i = [-dim, dim]

        if shape[1]%2 == 0 and shape[1] != 0:
            dim = (shape[1]-1) / 2
            j = [-dim-0.5, dim-0.5]
            trans[1] = trans[1] + openmc_lat.pitch[1]/2 
        else:
            dim = (shape[1]-1) / 2
            j = [-dim, dim]

        if shape[0]%2 == 0 and shape[0] != 0:
            dim = (shape[0]-1) / 2
            k = [-dim-0.5, dim-0.5]
            trans[2] = trans[2] + openmc_lat.pitch[2]/2 
        else:
            dim = (shape[0]-1) / 2
            k = [-dim, dim]

        mcnp_lat = mp.Lattice(i, j, k, lattice, 'REC', mcnp_universes)

        if trans == [0,0,0]:
            return (mcnp_lat, element, lat_disp, lat_u, None)
        else:
            return (mcnp_lat, element, lat_disp, lat_u, 
                    mp.Transformation(transformation=[trans]))

def openmc_to_mcnp(openmc_geometry: openmc.Geometry, 
                   openmc_materials: openmc.Materials,
                   openmc_settings=None):
    """Translate OpenMC Model to MCNP Deck.

    Parameters
    ----------
    openmc_geometry : openmc.Geometry
        OpenMC Geometry.
    openmc_materials : openmc.Materials
        OpenMC Materials.
    openmc_settings : openmc.Settings or None
        OpenMC Settings.

    Returns
    -------
    mcnp_deck : mcnpy.Deck
        Translated MCNP Deck.
    """
    mcnp_deck = mp.Deck()
    openmc_surfaces = openmc_geometry.get_all_surfaces()
    openmc_universes = openmc_geometry.get_all_universes()
    openmc_lattices = openmc_geometry.get_all_lattices()
    openmc_cells = openmc_geometry.get_all_cells()

    print('Translating Materials...')
    for mat in openmc_materials:
        # Assume material 0 is void.
        # Default OpenMC numbering begins at 1.
        if mat.id != 0:
            mcnp_deck += make_mcnp_material(mat)

    print('Translating Surfaces...')
    for surf in openmc_surfaces.values():
        mcnp_deck += openmc_surfs_to_mcnp(surf)

    print('Translating Universes and Cells...')
    mcnp_universes = {}
    u_fill = {}
    lat_fill = {}
    for universe in openmc_universes.values():
        u_name = universe.id
        if u_name not in mcnp_universes:
            mcnp_universes[u_name] = []
        for cell in universe.cells.values():
            mcnp_cell = make_mcnp_cell(mcnp_deck, cell)
            mcnp_deck += mcnp_cell
            if cell.fill is not None and isinstance(cell.fill, openmc.Material) is False:
                # Universe fill.
                if isinstance(cell.fill, openmc.Universe):
                    mcnp_universes[u_name].append(mcnp_cell)
                    u_id = cell.fill.id
                    if u_id not in mcnp_universes:
                        mcnp_universes[u_id] = []
                    u_fill[cell.id] = u_id
                # Lattice fill.
                else:
                    lat_fill[cell.id] = openmc_lattices[cell.fill.id]
            else:
                mcnp_universes[u_name].append(mcnp_cell)
            """if u_name != 0:
                if uid in mcnp_deck.universes:
                    mcnp_deck.universes.add(mcnp_cell)
                else:
                    mp.UniverseList(uid, mcnp_cell)"""
                    
    print('Making Universes...')
    # Make universes
    for k in mcnp_universes:
        if k != 0:
            mp.UniverseList(k, mcnp_universes[k])

    print('Filling Cells...')
    # Fill cells
    for k in u_fill:
        # We need to apply a transformation to the universe.
        openmc_cell = openmc_cells[k]
        transform = None
        if openmc_cell.translation is not None:
            if openmc_cell.rotation is not None:
                transform = mp.Transform(openmc_cell.translation, 
                                         openmc_cell.rotation)
            else:
                transform = mp.Transform(openmc_cell.translation)
        if transform is not None:
            mcnp_deck.cells[k].fill = (mcnp_deck.universes[u_fill[k]], transform)
        else:
            mcnp_deck.cells[k].fill = mcnp_deck.universes[u_fill[k]]

    print('Constructing Lattices...')
    lat_universes = {}
    for k in lat_fill:
        _mcnp_lat = make_mcnp_lattice(lat_fill[k], mcnp_deck.universes)
        mcnp_lat = _mcnp_lat[0]
        mcnp_deck += _mcnp_lat[1]
        for u in _mcnp_lat[3]:
            lat_universes[u] = _mcnp_lat[2]
        element = mp.Cell(name=None, region=-_mcnp_lat[1], fill=mcnp_lat)
        element.importances = {'n' : 1.0}
        if _mcnp_lat[4] is not None:
            mcnp_deck += _mcnp_lat[4]
            element.transformation = _mcnp_lat[4]
        mcnp_deck += element
        el_universe = mp.UniverseList(name=lat_fill[k].id, cells=element)
        mcnp_deck.cells[k].fill = el_universe

    for k in lat_universes:
        for cell in mcnp_deck.universes[k].cells.values():
            cell.transform = mp.Transform(lat_universes[k])

    if openmc_settings is not None:
        pass

    print('\nDone!\n')
    return mcnp_deck

def translate_file(file_name: str, materials=None, settings=None):
    """Parse file and translate MCNP to OpenMC.

    Parameters
    ----------
    file_name : str
        Name of file to translate.

    Returns
    -------
    geom : openmc.Geometry
        OpenMC model geometry.
    mats : openmc.Materials
        OpenMC model materials.
    """

    ext = pathlib.Path(file_name).suffix.lower()

    if ext == '.mcnp':
        # Tuple with geometry and materials.
        model = mcnp_to_openmc(mp.Deck().read(filename=file_name, renumber=True))
        model[1].export_to_xml(file_name.replace(ext, '.materials.xml')) # materials
        model[0].export_to_xml(file_name.replace(ext, '.geometry.xml')) # geometry

        return model

    elif ext == '.xml':
        # Geometry and materials are required.
        geom = openmc.Geometry.from_xml(file_name)
        if materials is None:
            mats = openmc.Materials.from_xml(file_name[:-3]+'materials'+ext)
        else:
            mats = openmc.Materials.from_xml(materials)

        set = None
        if settings is None:
            try:
                set = openmc.Settings.from_xml(file_name[:-3]+'settings'+ext)
            except:
                pass
        else:
            set = openmc.Settings.from_xml(settings)
        
        return openmc_to_mcnp(geom, mats, set)