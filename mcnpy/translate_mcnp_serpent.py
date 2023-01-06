from logging import root
import re
import math
import numpy as np
import pathlib
import serpy as sp
import mcnpy as mp
from mcnpy.surface_converter_serpent import serpent_surfs_to_mcnp, mcnp_surfs_to_serpent

DEG_RAD = 180. / math.pi
RAD_DEG = 1 / DEG_RAD

def decompose_mcnp_transformation(transform, angle='COSINES'):
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

def make_serpent_region(region, surf_serp, serp_cell):
    if isinstance(region, mp.surfaces.Halfspace):
        surf = surf_serp[str(region.surface.name)]
        if str(region.side) == '-':
            return -surf
        else:
            return +surf
    elif isinstance(region, mp.region.Complement):
        if isinstance(region.cell, mp.Cell):
            #return sp.Complement(serp_cell[str(region.cell.name)])
            return sp.Complement(make_serpent_region(region.cell.region, surf_serp, serp_cell))
        else:
            #print(region.node, '|||', region, '|||', region.cell, '|||', region._e_object.toString())
            return sp.Complement(make_serpent_region(region.node, surf_serp, serp_cell))
    
    elif isinstance(region, mp.region.Intersection):
        serp_region = sp.Intersection()
    elif isinstance(region, mp.region.Union):
        serp_region = sp.Union()

    for node in region.nodes:
        if isinstance(region, mp.region.Intersection):
            serp_region &= make_serpent_region(node, surf_serp, serp_cell)
        elif isinstance(region, mp.region.Union):
            serp_region |= make_serpent_region(node, surf_serp, serp_cell)
    return serp_region

def make_serpent_material(material, name=None):
    """Translate MCNP Material to Serpent Material.

    Parameters
    ----------
    material : mcnpy.Material
        MCNP Material to be translated.

    name : str (Optional)
        Name for Serpent material.

    Returns
    -------
    material : serpy.Material
        Translated Serpent Material.
    """
    nuclides = []
    for n in material.nuclides:
        try:
            nuclides.append(sp.MaterialNuclide(n.name, n.fraction, n.unit, n.library))
        except AttributeError:
            #TODO: Decide best option for MCNP materials with no .lib extension.
            nuclides.append(sp.MaterialNuclide(n.name, n.fraction, n.unit, '70C'))
    if name is None:
        name = material.name
    return sp.Material(name=name, nuclides=nuclides)

def make_mcnp_material(material, id):
    """Translate Serpent Material to MCNP Material.

    Parameters
    ----------
    material : serpy.Material
        Serpent Material to be translated.
    id : int
        Material ID.

    Returns
    -------
    material : mcnpy.Material
        Translated MCNP Material.
    """
    nuclides = []
    for n in material.nuclides:
        nuclides.append(mp.Nuclide(n.name, n.fraction, n.unit, n.library))
    return mp.Material(name=id, nuclides=nuclides, comment=material.name)

def make_mcnp_cell(mcnp_deck, serp_cell, id, outside_surfs):
    """Translate Serpent Cell to MCNP Cell.

    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck being translated to.
    serp_cell : serpy.Cell
        Serpent Cell being translated.
    id : int
        New MCNP Cell ID.
    outside_surfs : dict
        Dict of Serpent Surfaces that have 'outside' fill.

    Returns
    -------
    mcnp_cell : mcnpy.Cell
        Translated MCNP Cell.
    outside_surfs : dict
        Dict of Serpent Surfaces that have 'outside' fill.
    """
    # Assuming that all cell complements have been dealt with
    # Set region
    reg = str(serp_cell.region)
    #print(reg)
    """for k in serp_surf_ids:
        reg = re.sub('(?<!\d)'+str(k)+'(?!(\d|%))', str(serp_surf_ids[k])+'%', reg)
    reg = reg.replace('%', '')"""
    #print(reg)
    region = mp.Region.from_expression(reg, mcnp_deck.surfaces, mcnp_deck.cells)
    #print('+++++++++++++++++++++++++++')
    mcnp_cell = mp.Cell(name=id, region=region)
    # Set material
    if isinstance(serp_cell.material, sp.MaterialReference):
        mcnp_cell.material = mcnp_deck.materials[int(serp_cell.material.x.name)]
        mcnp_cell.density =  float(serp_cell.material.x.density)
        mcnp_cell.density_unit = serp_cell.material.x.unit
        mcnp_cell.importances = {'n' : 1.0}
    # Set Fill
    elif serp_cell.fill is not None:
        # Set fill later.
        mcnp_cell.importances = {'n' : 1.0}
    # No fill, no material
    else:
        if serp_cell.material is None:
            surfs = mcnp_cell.region.get_surfaces()
            for k in surfs:
                if k not in outside_surfs:
                    outside_surfs[k] = surfs[k]
        mcnp_cell.material = None
        mcnp_cell.importances = {'n' : 0.0}
    mcnp_cell.comment = serp_cell.name

    return (mcnp_cell, outside_surfs)

def apply_mcnp_cell_trans(mcnp_deck):
    """Apply TRCL to individual surfaces in the cell's region.
    If the cell is filled, we will also need a Serpent fill transformation.

    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP deck being translated.
    
    Returns
    -------
    fill_trans : dict
        Dict mapping TR cards to cell IDs.
    """
    fill_trans = {}
    for cell in mcnp_deck.cells.values():
        trcl = cell.transformation
        names = {}
        # No TR card.
        if trcl is None:
            transform = cell.transform
            angle = cell.transform_angle_unit
            # Directly uses transform on cell.
            # Make TR card.
            if transform is not None:
                angle = cell.transform_angle_unit
                trcl = mp.Transformation(transformation=transform, unit=angle)
                trcl.name = max(list(mcnp_deck.transformations.keys())) + 1
                mcnp_deck += trcl

        # TR card exists or was created.
        if trcl is not None:
            # Store which cells also need a fill transformation.
            fill_trans[cell.name] = trcl.name
            surfaces = cell.region.get_surfaces()
            i = 1
            for surf in surfaces.values():
                surf_new = surf.__copy__()
                surf_new.name = max(list(mcnp_deck.surfaces.keys())) + i
                i = i + 1
                surf_new.transformation = trcl
                mcnp_deck += surf_new
                names[str(surf.name)] = str(surf_new.name)
            region_str = str(cell.region)
            # Unset cell's TRCL.
            cell.transform = None
            cell.transform_angle_unit = None
            cell.transformation = None
       
        # Replace old cell region if necessary.
        for k in names:
            region_str = re.sub('(?<!\d)'+k+'(?!\d)', names[k], region_str)
            cell.region = mp.Region.from_expression(region_str, 
                                                    mcnp_deck.surfaces, 
                                                    mcnp_deck.cells)
    return fill_trans
    #mcnp_deck.remove_redundant_surfaces()
    #mcnp_deck.remove_unused_surfaces()

def make_serpent_cell(serp_deck, mcnp_cell):
    """Translate MCNP Cell to Serpent Cell.

    Parameters
    ----------
    serp_deck : serpy.Deck
        Serpent Deck being translated to.
    mcnp_cell : mcnpy.Cell
        MCNP Cell being translated.

    Returns
    -------
    serp_cell : serpy.Cell
        Translated Serpent Cell.
    """
    region = make_serpent_region(mcnp_cell.region, serp_deck.surfaces, serp_deck.cells)
    #region = sp.Region.from_expression(str(mcnp_cell.region), serp_deck.surfaces,
    #                                   serp_deck.cells)
    serp_cell = sp.Cell(str(mcnp_cell.name), region)
    if mcnp_cell.fill is None:
        if mcnp_cell.material is None:
            #TODO: link to imp data card
            if sum(mcnp_cell.importances.values()) == 0:
                fill = 'outside'
            else:
                fill = None
        else:
            mcnp_density = str(mcnp_cell.density)
            mat = serp_deck.materials[str(mcnp_cell.material.name)]
            if mcnp_density != mat.density or mcnp_cell.density_unit != mat.unit:
                match = False
                i = 1
                while match is False:
                    id = str(mat.name) + '_rho_' + str(i)
                    mat = serp_deck.materials[id]
                    if mcnp_density == mat.density and mcnp_cell.density_unit == mat.unit:
                        match = True
                    i = i + 1
            fill = mat
        serp_cell.material = fill
    else:
        pass
        #raise Exception('Cell Fill not supported yet!')

    return serp_cell

def make_mcnp_lattice(serp_lattice, mcnp_universes):
    """Translate Serpent Lattice to MCNP Lattice.

    Parameters
    ----------
    serp_lattice : serpy.Lattice
        Serpent Lattice being translated. 
    mcnp_universes : dict
        Dict of available MCNP Universes.

    Returns
    -------
    mcnp_lat : mcnpy.Lattice
        Translated MCNP Lattice.
    element : mcnpy.Surface
        Surface boundary of the lattice element.
    transformation : mcnpy.Transformation or None
        TR card to re-center lattice or None if not required.
    """

    serp_lat = serp_lattice.lat_type
    if isinstance(serp_lat, sp.Full3DLattice):
        shape = serp_lat.lattice.shape
        lattice = np.empty(shape, 'int32')
        for z in range(shape[0]):
            for y in range(shape[1]):
                for x in range(shape[2]):
                    lattice[z][y][x] = int(serp_lat.lattice[z][y][x].name)
        if serp_lat.type == 11:
            type = 'REC'
            x = serp_lat.pitch[0]/2 
            y = serp_lat.pitch[1]/2 
            z = serp_lat.pitch[2]/2 
            element = mp.RectangularPrism(None, serp_lat.origin[0]-x, serp_lat.origin[0]+x, 
                                                serp_lat.origin[1]-y, serp_lat.origin[1]+y, 
                                                serp_lat.origin[2]-z, serp_lat.origin[2]+z)
        trans = [0,0,0]
        if shape[2]%2 == 0 and shape[2] != 0:
            dim = (shape[2]-1) / 2
            i = [-dim-0.5, dim-0.5]
            trans[0] = trans[0] + serp_lat.pitch[0]/2 
        else:
            dim = (shape[2]-1) / 2
            i = [-dim, dim]

        if shape[1]%2 == 0 and shape[1] != 0:
            dim = (shape[1]-1) / 2
            j = [-dim-0.5, dim-0.5]
            trans[1] = trans[1] + serp_lat.pitch[1]/2 
        else:
            dim = (shape[1]-1) / 2
            j = [-dim, dim]

        if shape[0]%2 == 0 and shape[0] != 0:
            dim = (shape[0]-1) / 2
            k = [-dim-0.5, dim-0.5]
            trans[2] = trans[2] + serp_lat.pitch[2]/2 
        else:
            dim = (shape[0]-1) / 2
            k = [-dim, dim]

        mcnp_lat = mp.Lattice(i, j, k, lattice, type, mcnp_universes)

    if trans == [0,0,0]:
        return (mcnp_lat, element, None)
    else:
        return (mcnp_lat, element, mp.Transformation(transformation=[trans]))
        
def make_serpent_lattice(mcnp_cell, serp_universes):
    """
    Parameters
    ----------
    mcnp_cell : mcnpy.Cell
        MCNP Cell with lattice fill.
    serp_universes : dict
        Dict of Serpent Universes.

    Returns
    -------
    lat : serpy.Full3DLattice or serpy.LatticeType
    """
    mcnp_lattice = mcnp_cell.fill
    shape = mcnp_lattice.lattice.shape
    lattice = np.empty(shape, dtype='str')
    for z in range(shape[0]):
        for y in range(shape[1]):
            for x in range(shape[2]):
                lattice[z][y][x] = str(mcnp_lattice.lattice[z][y][x].fill.name)
    surfaces = mcnp_cell.region.get_surfaces()
    xlim = []
    ylim = []
    zlim = []
    for surf in surfaces.values():
        if isinstance(surf, mp.XPlane):
            xlim.append(surf.x0)
        elif isinstance(surf, mp.YPlane):
            ylim.append(surf.y0)
        elif isinstance(surf, mp.ZPlane):
            zlim.append(surf.z0)
        elif isinstance(surf, mp.Plane):
            #TODO: Consider off axis planes
            if surf.a == 1 and surf.b == 0 and surf.c == 0:
                xlim.append(surf.d)
            elif surf.a == 0 and surf.b == 1 and surf.c == 0:
                ylim.append(surf.d)
            elif surf.a == 0 and surf.b == 0 and surf.c == 1:
                zlim.append(surf.d)
            else:
                print("Lattice bounding box off-axis")
        elif isinstance(surf, mp.RectangularPrism):
            xlim = [surf.x0, surf.x1]
            ylim = [surf.y0, surf.y1]
            zlim = [surf.z0, surf.z1]
        else:
            print(surf)
            print("LATTICE ERROR!")

    # Calculate the pitch from the lattice dimensions and container cell limits.
    # Note that the lattice dims are in z,y,x order.
    pitch = []
    pitch.append((max(xlim)-min(xlim)))
    pitch.append((max(ylim)-min(ylim)))
    pitch.append((max(zlim)-min(zlim)))
    
    origin = []
    origin.append(max(xlim) - 0.5*pitch[0])
    origin.append(max(ylim) - 0.5*pitch[1])
    origin.append(max(zlim) - 0.5*pitch[2])

    range_i =  mcnp_lattice.i[0] + (mcnp_lattice.i[1] - mcnp_lattice.i[0])*0.5
    range_j =  mcnp_lattice.j[0] + (mcnp_lattice.j[1] - mcnp_lattice.j[0])*0.5
    range_k =  mcnp_lattice.k[0] + (mcnp_lattice.k[1] - mcnp_lattice.k[0])*0.5

    origin[0] = origin[0] + range_i*pitch[0]
    origin[1] = origin[1] + range_j*pitch[1]
    origin[2] = origin[2] + range_k*pitch[2]
    
    return sp.Full3DLattice(lattice=lattice, universes=serp_universes, 
                            pitch=pitch, origin=origin)    

def serpent_to_mcnp(serp_deck:sp.Deck):
    """Translate Serpent Deck to MCNP Deck.
    
    Parameters
    ----------
    serp_deck : serpy.Deck
        Serpent Deck to be translated.

    Returns
    -------
    mcnp_deck : mcnpy.Deck
        Translated MCNP Deck.
    """
    print('Translating Serpent => MCNP\n')
    mcnp_deck = mp.Deck()

    print('Translating Materials...')
    for material in serp_deck.materials.values():
        mcnp_deck += make_mcnp_material(material, int(material.name))

    print('Translating Surfaces...')
    for surface in serp_deck.surfaces.values():
        mcnp_surf = serpent_surfs_to_mcnp(surface, int(surface.name))
        mcnp_surf.comment = surface.name
        if surface.name in serp_deck.transformations_surf:
            trans = serp_deck.transformations_surf[surface.name].transform
            if trans.transform.rot_matrix.all() == 0:
                tr = mp.Transformation(transformation=[trans.transform.displacement, None])
            else:
                tr = mp.Transformation(transformation=[trans.transform.displacement, 
                                                    trans.transform.rot_matrix])
            if len(mcnp_deck.transformations.keys()) > 0:
                tr_exist = False
                for trans in mcnp_deck.transformations.copy().items():
                    if tr.transformation.displacement == trans[1].transformation.displacement:
                        if tr.transformation.rotation is not None and trans[1].transformation.rotation is not None:
                            if tr.transformation.rotation.matrix.all() == trans[1].transformation.rotation.matrix.all():
                                mcnp_surf.transformation = mcnp_deck.transformations[trans[0]]
                                tr_exist = True
                                break
                        else:
                            mcnp_surf.transformation = mcnp_deck.transformations[trans[0]]
                            tr_exist = True
                            break
                if tr_exist == False:
                    mcnp_deck += tr
                    mcnp_surf.transformation = tr
            else:
                mcnp_deck += tr
                mcnp_surf.transformation = tr

        mcnp_deck += mcnp_surf

    print('Translating Universes and Cells...')
    outside_surfs = {}
    mcnp_universes = {}
    u_fill = {}
    lat_fill = {}
    fill_trans = {}

    # Renumber universes.
    u_name = 0
    serp_orig_universes = serp_deck.universes.copy().items()
    for u in serp_orig_universes:
        universe = serp_deck.universes[u[0]]
        while str(u_name) in serp_deck.universes or str(u_name) in serp_deck.lattices:
            u_name = u_name + 1
        universe.name = str(u_name)
        if u[0] == serp_deck.root:
            serp_deck.root = str(u_name)
    for universe in serp_deck.universes.values():
        u_name = int(universe.name)
        #ui = ui + 1
        #u_map[universe.name] = ui
        #cells = []
        for cell in universe.cells.values():
            #u_name = universe.name
            if u_name not in mcnp_universes:
                mcnp_universes[u_name] = []
            cell_trans = make_mcnp_cell(mcnp_deck, cell, int(cell.name),
                                        outside_surfs)
            mcnp_cell = cell_trans[0]
            if cell.name in serp_deck.transformations_fill:
                trans = serp_deck.transformations_fill[cell.name].transform
                if trans.transform.rot_matrix.all() == 0:
                    tr = mp.Transformation(transformation=[trans.transform.displacement, None])
                else:
                    tr = mp.Transformation(transformation=[trans.transform.displacement, 
                                                        trans.transform.rot_matrix])
                mcnp_deck += tr
                #mcnp_cell.transformation = tr
                surfaces = mcnp_cell.region.get_surfaces()
                # Test if all surfaces use the same TR card.
                trcl = True
                for surf in surfaces.values():
                    if surf.transformation is not None:
                        if surf.transformation.transformation != tr:
                            trcl = False
                            break
                    else:
                        trcl = False
                        break
                # If the fill and surfaces use the same TR, remove TR from surfaces and just use an MCNP cell transformation.
                if trcl == True:
                    mcnp_cell.transformation = tr
                    for surf in surfaces.values():
                        mcnp_deck -= surf.transformation
                        surf.transformation = None
                else:
                    fill_trans[mcnp_cell.name] = tr
            outside_surfs = cell_trans[1]
            mcnp_deck += mcnp_cell
            if cell.fill is not None:
                # Universe fill
                if cell.fill.name in serp_deck.universes:
                    mcnp_universes[u_name].append(mcnp_cell)
                    u_id = int(cell.fill.name)
                    if u_id not in mcnp_universes:
                        mcnp_universes[u_id] = []
                    u_fill[mcnp_cell.name] = u_id
                        
                # Lattice fill
                else:
                    lat_fill[int(cell.name)] = serp_deck.lattices[cell.fill.name]
            else:
                mcnp_universes[u_name].append(mcnp_cell)
            """if universe.name != str(serp_deck.root):
                u_id = int(universe.name)
                if u_id in mcnp_deck.universes:
                    mcnp_deck.universes[u_id].add(cell_trans[0])
                else:
                    mp.UniverseList(u_id, cell_trans[0])"""

            #cells.append(cell_trans[0])
        # Apparently universes must be assigned after cells are added to deck.
        # Appears fine until working with universe refs on lattices.
        # TODO: figure out why this makes such a big difference.

    print('Making Universes...')
    # Make universes
    for k in mcnp_universes:
        if str(k) != serp_deck.root:
            mp.UniverseList(k, mcnp_universes[k])
    
    print('Filling Cells...')
    # Fill cells
    for k in u_fill:
        # We need to apply a transformation to the universe.
        if k in fill_trans:
            mcnp_deck.cells[k].fill = (mcnp_deck.universes[u_fill[k]], fill_trans[k])
        else:
            mcnp_deck.cells[k].fill = mcnp_deck.universes[u_fill[k]]

    print('Constructing Lattices...')
    # Lattice
    for k in lat_fill:
        _mcnp_lat = make_mcnp_lattice(lat_fill[k], mcnp_deck.universes)
        mcnp_lat = _mcnp_lat[0]
        mcnp_deck += _mcnp_lat[1]
        element = mp.Cell(name=None, region=-_mcnp_lat[1], fill=mcnp_lat)
        element.importances = {'n' : 1.0}
        if _mcnp_lat[2] is not None:
            mcnp_deck += _mcnp_lat[2]
            element.transformation = _mcnp_lat[2]
        mcnp_deck += element
        el_universe = mp.UniverseList(name=int(lat_fill[k].name.name), cells=element)
        mcnp_deck.cells[k].fill = el_universe
        
    print('Translating Data cards...')
    for card in serp_deck.settings:
        if isinstance(card, sp.NeutronPopulation):
            kcode = mp.CriticalitySource(histories=card.npg, 
                                            cycles=card.ngen+card.nskip, 
                                            skip_cycles=card.nskip, 
                                            keff_guess=1.0)
            mcnp_deck += kcode
        elif isinstance(card, sp.BoundaryCondition):
            for surf in outside_surfs.values():
                if int(card.mode) == 2:
                    surf.boundary_type = 'reflective'
        else:
            print(card)
            #raise Exception('Data translation not supported yet!')

    print('\nDone!\n')
    return mcnp_deck

def mcnp_to_serpent(mcnp_deck: mp.Deck):
    """Translate MCNP Deck to Serpent Deck.
    
    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck to be translated.

    Returns
    -------
    serp_deck : serpy.Deck
        Translated Serpent Deck.
    """
    print('Translating MCNP => Serpent\n')
    serp_deck = sp.Deck()
    bc_type = 1

    print('Translating Materials...')
    for mat in mcnp_deck.materials.values():
        try:
            densities = mcnp_deck.material_densities[mat.name]
            if len(densities) >= 1:
                serp_mat = make_serpent_material(mat)
                serp_mat.density = str(densities[0][0])
                serp_mat.unit = densities[0][1]
                serp_deck += serp_mat
            if len(densities) > 1:
                i = 1
                for rho in densities[1:]:
                    mat_copy = serp_mat.__copy__()
                    mat_copy.density = str(rho[0])
                    mat_copy.unit = rho[1]
                    mat_copy.name = str(mat.name) + '_rho_' + str(i)
                    serp_deck += mat_copy
                    i = i + 1
        except KeyError:
            pass
    
    # Apply cell transformations.
    print('Decomposing Cell Transformations...')
    fill_trans = apply_mcnp_cell_trans(mcnp_deck)

    print('Translating Surfaces...')
    for surf in mcnp_deck.surfaces.values():
        if bc_type == 1:
            if surf.boundary_type == 'reflective' or surf.boundary_type == '*':
                bc_type = 2
        serp_surf = mcnp_surfs_to_serpent(surf).surface()
        serp_deck += serp_surf
        #serp_deck += mcnp_surfs_to_serpent(surf).surface()
        # Surface transformations
        if surf.transformation is not None:
            tr = mcnp_deck.transformations[surf.transformation.name]
            disp, rot = decompose_mcnp_transformation(tr.transformation)
            strans = sp.Transform.Surface(unit=serp_surf, transform=sp.Transform.Data(displacement=disp, rot_matrix=rot))
            serp_deck += sp.Transformation.Surface(unit=serp_surf, transform=strans)

    print('Translating Universes and Cells...')
    serp_universes = {}
    u_fill = {}
    lat_fill = {}
    # Make cells and determine universe vs lattice fill.
    for universe in mcnp_deck._universes.values():
        u_name = str(universe.name)
        if u_name not in serp_universes:
            serp_universes[u_name] = []
        for cell in universe.cells.values():
            cell_name = str(cell.name)
            serp_cell = make_serpent_cell(serp_deck, cell)
            if cell.fill is not None:
                if isinstance(cell.fill, mp.Lattice):
                    lat_fill[cell_name] = str(cell.universe.name)
                else:
                    serp_deck += serp_cell

                    serp_universes[u_name].append(serp_cell)
                    u_id = str(cell.fill.fill.name)
                    if u_id not in serp_universes:
                        serp_universes[u_id] = []
                    u_fill[cell_name] = u_id
                    if cell.name in fill_trans:
                        tr = mcnp_deck.transformations[fill_trans[cell.name]]
                        disp, rot = decompose_mcnp_transformation(tr.transformation)
                        ftrans = sp.Transform.Fill(unit=serp_cell, transform=sp.Transform.Data(displacement=disp, rot_matrix=rot))
                        serp_deck += sp.Transformation.Fill(unit=serp_cell, transform=ftrans)
            else:
                serp_deck += serp_cell
                serp_universes[u_name].append(serp_cell)

            """if u_name == '0':
                serp_cell.universe = sp.Universe(u_name)"""

    print('Making Universes...')
    # Make universes
    for k in serp_universes:
        #if k != '0':
            sp.UniverseList(k, serp_universes[k])

    print('Filling Cells...')
    # Fill cells
    u_lat = {}
    for k in u_fill:
        try:
            # Filled by universe
            serp_deck.cells[k].fill = serp_deck.universes[u_fill[k]]
        except KeyError:
            # Filled by lattice
            if u_fill[k] not in u_lat.keys():
                u_lat[u_fill[k]] = sp.Universe(u_fill[k])
            serp_deck.cells[k].fill = u_lat[u_fill[k]]

    print('Constructing Lattices...')
    # Build lattices
    for k in lat_fill:
        if lat_fill[k] not in serp_deck.lattices.keys():
            serp_deck += sp.Lattice(u_lat[lat_fill[k]], 
                                    make_serpent_lattice(mcnp_deck.cells[int(k)], 
                                                         serp_deck.universes))  
    #print('Cleaning Up Surfaces...')
    #serp_deck.remove_unused_surfaces()

    print('Translating Data cards...')
    for k in mcnp_deck.src_settings:
        if isinstance(k, mp.CriticalitySource):
            serp_deck += sp.NeutronPopulation(npg=k.histories, 
                                              ngen=k.cycles-k.skip_cycles, 
                                              nskip=k.skip_cycles)
    if bc_type == 2:
        serp_deck += sp.BoundaryCondition(mode=2)

    print('\nDone!\n')
    return serp_deck

def translate_file(file_name: str):
    """Parse file and translate to MCNP or Serpent.

    Parameters
    ----------
    file_name : str
        Name of file to translate.

    Returns
    -------
    trans_deck : mcnpy.Deck or serpy.Deck
    """

    ext = pathlib.Path(file_name).suffix.lower()

    if ext == '.mcnp':
        return mcnp_to_serpent(mp.Deck.read(file_name))
    elif ext == '.serpent':
        return serpent_to_mcnp(sp.Deck.read(file_name, True))
