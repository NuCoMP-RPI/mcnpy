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

def make_mcnp_cell(mcnp_deck, serp_mat_ids, serp_surf_ids, serp_cell, id, outside_surfs):
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

def make_serpent_cell(serp_deck, mcnp_cell, universe):
    """Translate Serpent Cell to MCNP Cell.

    Parameters
    ----------
    serp_deck : serpy.Deck
        Serpent Deck being translated to.
    mcnp_cell : mcnpy.Cell
        MCNP Cell being translated.
    universe : serpy.Universe
        Serpent Universe that owns the Cell.

    Returns
    -------
    serp_cell : serpy.Cell
        Translated MCNP Cell.
    """
    region = sp.Region.from_expression(str(mcnp_cell.region), serp_deck.surfaces,
                                       serp_deck.cells)
    serp_cell = sp.Cell(mcnp_cell.name, region, universe=universe)
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
                    serp_deck += make_serpent_material(mcnp_cell.material, m_id)
                    fill = serp_deck.materials[m_id]
        serp_cell.material = fill
    else:
        raise Exception('Cell Fill not supported yet!')

    return serp_cell

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
    i = 0
    ui = 0
    for universe in serp_deck.universes.values():
        ui = ui +1
        cells = []
        for cell in universe.cells.values():
            i = i + 1
            cell_trans = make_mcnp_cell(mcnp_deck, mat_ids, surf_ids, cell, i,
                                        outside_surfs)
            outside_surfs = cell_trans[1]
            cells.append(cell_trans[0])
        # Assign to universe
        if str(universe.name) != str(serp_deck.root):
            mp.UniverseList(ui, cells)
        mcnp_deck += cells
        
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
    serp_deck = sp.Deck()
    bc_type = 1

    for mat in mcnp_deck.materials.values():
        serp_deck += make_serpent_material(mat)
    
    for surf in mcnp_deck.surfaces.values():
        if bc_type == 1:
            if surf.boundary_type == 'reflective' or surf.boundary_type == '*':
                bc_type = 2
        serp_deck += mcnp_surfs_to_serpent(surf).surface()

    for universe in mcnp_deck.universes.values():
        for cell in universe.cells.values():
            serp_deck += make_serpent_cell(serp_deck, cell, 
                                           sp.Universe(universe.name))

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

"""if __name__ == '__main__':
    import sys
    name = str(pathlib.Path(sys.argv[1]))[:-len(str(pathlib.Path(sys.argv[1]).suffix))]
    if pathlib.Path(sys.argv[1]).suffix.lower() == '.mcnp':
        name += '.serpent'
    elif pathlib.Path(sys.argv[1]).suffix.lower() == '.serpent':
        name += '.mcnp'

    translate_file(sys.argv[1]).write(name)"""