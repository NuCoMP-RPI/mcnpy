import math
import numpy as np
import pathlib
import serpy as sp
import mcnpy as mp
from mcnpy.surface_converter import serpent_surfs_to_mcnp, mcnp_surfs_to_serpent

def make_serpent_material(material):
    """Translate MCNP Material to Serpent Material.

    Parameters
    ----------
    material : mcnpy.Material
        MCNP Material to be translated.

    Returns
    -------
    material : serpy.Material
        Translated Serpent Material.
    """
    nuclides = []
    for n in material.nuclides:
        nuclides.append(sp.MaterialNuclide(n.name, n.fraction, n.unit, n.library))
    return sp.Material(name=material.name, nuclides=nuclides)

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

def make_mcnp_cell(mcnp_deck, serp_mat_ids, serp_surf_ids, serp_cell, id, 
                   outside_surfs):
    """Translate Serpent Cell to MCNP Cell.

    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck being translated to.
    serp_mat_ids : dict
        Dict mapping original Serpent Material IDs to the new numeric IDs.
    serp_surf_ids : dict
        Dict mapping original Serpent Surface IDs to the new numeric IDs.
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
    for k in serp_surf_ids:
        reg = reg.replace(str(k), str(serp_surf_ids[k]))
    region = mp.Region.from_expression(reg, mcnp_deck.surfaces, mcnp_deck.cells)
    mcnp_cell = mp.Cell(name=id, region=region)
    # Set material
    if isinstance(serp_cell.material, sp.MaterialReference):
        mcnp_cell.material = mcnp_deck.materials[serp_mat_ids[
                                                 serp_cell.material.x.name]]
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

def make_serpent_cell(serp_deck, mcnp_cell):
    """Translate Serpent Cell to MCNP Cell.

    Parameters
    ----------
    serp_deck : serpy.Deck
        Serpent Deck being translated to.
    mcnp_cell : mcnpy.Cell
        MCNP Cell being translated.

    Returns
    -------
    serp_cell : serpy.Cell
        Translated MCNP Cell.
    """
    region = sp.Region.from_expression(str(mcnp_cell.region), serp_deck.surfaces,
                                       serp_deck.cells)
    serp_cell = sp.Cell(mcnp_cell.name, region)
    if mcnp_cell.fill is None:
        if mcnp_cell.material is None:
            #TODO: link to imp data card
            if sum(mcnp_cell.importances.values()) == 0:
                fill = 'outside'
            else:
                fill = None
        else:
            density = mcnp_cell.density
            # Material has not been used by a cell yet.
            if serp_deck.materials[str(mcnp_cell.material.name)].density is None:
                if str(mcnp_cell.density_unit) == '-':
                    serp_deck.materials[str(mcnp_cell.material.name)]*density
                else:
                    serp_deck.materials[str(mcnp_cell.material.name)]@density
                fill = serp_deck.materials[str(mcnp_cell.material.name)]
            # Material has at least one density defined for it.
            else:
                exist = False
                # Check if alternate denity has already been used.
                for serp_mat in serp_deck.materials.values():
                    if serp_mat.name == mcnp_cell.material.name:
                        if serp_mat.density == density:
                            exist = True
                            fill = serp_mat
                            break
                # Add new material with different density.
                if exist is False:
                    m_id = str(mcnp_cell.material.name) + '_rho_' + str(density)
                    serp_deck += make_serpent_material(mcnp_cell.material)
                    fill = serp_deck.materials[m_id]
        serp_cell.material = fill
    else:
        pass
        #raise Exception('Cell Fill not supported yet!')

    return serp_cell

def make_mcnp_lattice(serp_lattice, u_map, mcnp_universes):
    """Translate Serpent Lattice to MCNP Lattice.

    Parameters
    ----------
    serp_lattice : serpy.Lattice
        Serpent Lattice being translated. 
    u_map : dict
        Dict mapping MCNP Cell IDs to their filling Universe IDs.
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
                    lattice[z][y][x] = u_map[serp_lat.lattice[z][y][x].name]
        if serp_lat.type == 11:
            type = 'REC'
            x = serp_lat.pitch[0]/2 
            y = serp_lat.pitch[1]/2 
            z = serp_lat.pitch[2]/2 
            element = mp.RectangularPrism(None, -x, x, -y, y, -z, z)
        trans = serp_lat.origin
        if shape[2]%2 == 0:
            dim = (shape[2]-1) / 2
            i = [-dim-0.5, dim-0.5]
            trans[0] = trans[0] + serp_lat.pitch[0]/2 
        else:
            dim = (shape[2]-1) / 2
            i = [-dim, dim]

        if shape[1]%2 == 0:
            dim = (shape[1]-1) / 2
            j = [-dim-0.5, dim-0.5]
            trans[1] = trans[1] + serp_lat.pitch[1]/2 
        else:
            dim = (shape[1]-1) / 2
            j = [-dim, dim]

        if shape[0]%2 == 0:
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
    mcnp_deck = mp.Deck()

    surf_ids = {}
    i = 0
    for surface in serp_deck.surfaces.values():
        # The "type" has the actual parameters
        i = i + 1
        surf_ids[surface.name] = i

        mcnp_surf = serpent_surfs_to_mcnp(surface)
        mcnp_surf.name = i
        mcnp_surf.comment = surface.name
        mcnp_deck += mcnp_surf

    mat_ids = {}
    i = 0
    for material in serp_deck.materials.values():
        i = i + 1
        mat_ids[material.name] = i
        mcnp_deck += make_mcnp_material(material, i)

    outside_surfs = {}
    u_fill = {}
    lat_fill = {}
    u_map = {}
    i = 0
    ui = 0
    for universe in serp_deck.universes.values():
        ui = ui + 1
        u_map[universe.name] = ui
        cells = []
        for cell in universe.cells.values():
            i = i + 1
            if cell.fill is not None:
                # Universe fill
                if cell.fill in serp_deck.universes:
                    u_fill[i] = ui
                # Lattice fill
                else:
                    lat_fill[i] = serp_deck.lattices[cell.fill.name]
            cell_trans = make_mcnp_cell(mcnp_deck, mat_ids, surf_ids, cell, i,
                                        outside_surfs)
            outside_surfs = cell_trans[1]
            cells.append(cell_trans[0])
        # Apparently universes must be assigned after cells are added to deck.
        # Appears fine until working with universe refs on lattices.
        # TODO: figure out why this makes such a big difference.
        mcnp_deck += cells
        # Assign to universe
        if str(universe.name) != str(serp_deck.root):
            mp.UniverseList(ui, cells)

    # Fill loop
    # Universe
    for k in u_fill:
        mcnp_deck.cells[k].fill = mcnp_deck.universes[u_fill[k]]
    # Lattice
    for k in lat_fill:
        _mcnp_lat = make_mcnp_lattice(lat_fill[k], u_map, mcnp_deck.universes)
        mcnp_lat = _mcnp_lat[0]
        #mcnp_lat.universes = mcnp_deck.universes
        ui = ui + 1
        mcnp_deck += _mcnp_lat[1]
        element = mp.Cell(name=None, region=-_mcnp_lat[1], fill=mcnp_lat)
        element.importances = {'n' : 1.0}
        if _mcnp_lat[2] is not None:
            mcnp_deck += _mcnp_lat[2]
            element.transformation = _mcnp_lat[2]
        mcnp_deck += element
        el_universe = mp.UniverseList(name=ui, cells=element)
        mcnp_deck.cells[k].fill = el_universe
        
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

    return mcnp_deck

def mcnp_to_serpent(mcnp_deck: mp.Deck):
    """Translate Serpent Deck to MCNP Deck.
    
    Parameters
    ----------
    mcnp_deck : mcnpy.Deck
        MCNP Deck to be translated.

    Returns
    -------
    serp_deck : serpy.Deck
        Translated Serpent Deck.
    """
    mcnp_deck
    serp_deck = sp.Deck()
    bc_type = 1

    for mat in mcnp_deck.materials.values():
        serp_deck += make_serpent_material(mat)
    
    for surf in mcnp_deck.surfaces.values():
        if bc_type == 1:
            if surf.boundary_type == 'reflective' or surf.boundary_type == '*':
                bc_type = 2
        serp_deck += mcnp_surfs_to_serpent(surf).surface()

    serp_universes = {}
    u_fill = {}
    lat_fill = {}
    # Make cells and determine universe vs lattice fill.
    for universe in mcnp_deck.universes.values():
        if str(universe.name) not in serp_universes.keys():
            serp_universes[str(universe.name)] = []
        for cell in universe.cells.values():
            if cell.fill is not None:
                if isinstance(cell.fill, mp.Lattice):
                    lat_fill[str(cell.name)] = str(cell.universe.name)
                else:
                    serp_deck += make_serpent_cell(serp_deck, cell)

                    serp_universes[str(universe.name)].append(serp_deck.cells[str(cell.name)])
                    u_id = str(cell.fill.fill.name)
                    if u_id not in serp_universes.keys():
                        serp_universes[u_id] = []
                    u_fill[str(cell.name)] = u_id
            else:
                serp_deck += make_serpent_cell(serp_deck, cell)
                serp_universes[str(universe.name)].append(serp_deck.cells[str(cell.name)])

    # Make universes
    for k in serp_universes:
        sp.UniverseList(k, serp_universes[k])

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

    # Build lattices
    for k in lat_fill:
        if lat_fill[k] not in serp_deck.lattices.keys():
            serp_deck += sp.Lattice(u_lat[lat_fill[k]], 
                                    make_serpent_lattice(mcnp_deck.cells[int(k)], 
                                                         serp_deck.universes))  
    serp_deck.remove_unused_surfaces()

    for k in mcnp_deck.src_settings:
        if isinstance(k, mp.CriticalitySource):
            serp_deck += sp.NeutronPopulation(npg=k.histories, 
                                              ngen=k.cycles-k.skip_cycles, 
                                              nskip=k.skip_cycles)
    if bc_type == 2:
        serp_deck += sp.BoundaryCondition(mode=2)

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
        return serpent_to_mcnp(sp.Deck.read(file_name))
