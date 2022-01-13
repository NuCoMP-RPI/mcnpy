from collections import OrderedDict, defaultdict
from mcnpy.cells import Cell
from mcnpy.surfaces import Surface, RectangularPrism, CircularCylinder, HexagonalPrism, Polyhedron, Wedge, EllipticalCylinder, Box, TruncatedCone, Ellipsoid
from mcnpy.materials import Material
from mcnpy.universe import UniverseList
from mcnpy import TransformationBase
from mcnpy.deck import Deck
from mcnpy.gateway import gateway, is_instance_of
from mcnpy.deck_formatter import formatter, preprocessor

class InputDeck():
    """An object containing dicts for cells, surfaces, and materials. All other data cards are stored as a list."""
    def __init__(self, cells=None, surfaces=None, settings=None, transformations=None, materials=None, universes=None):
        self.cells = cells
        self.surfaces = surfaces
        self.settings = settings
        self.transformations = transformations
        self.materials = materials
        self.universes = universes
        self.deck = None
        self.serialized = False

        if self.cells is None:
            self.cells = {}
        if self.surfaces is None:
            self.surfaces = {}
        if self.settings is None:
            self.settings = []
        if self.transformations is None:
            self.transformations = {}
        if self.materials is None:
            self.materials = {}
        if self.universes is None:
            self.universes = {}
    
    def import_from_file(self, filename='inp.mcnp', renumber=False, preprocess=False):
        """For reading a deck from a file.
        """
        try:
            if preprocess is True:
                filename = preprocessor(filename)
            inp = gateway.loadFile(filename)
            self.deck = inp
        except:
            raise Exception('Error importing MCNP Deck from file "' + filename + '"')
        cells = inp.cells.cells
        surfaces = inp.surfaces.surfaces
        settings = inp.data.settings
        materials = inp.data.materials
        for i in range(len(cells)):
            #self.cells.append(cells[i])
            if renumber is True:
                cells[i].name = str(i+1)
            self.cells[cells[i].name] = cells[i]
            self.get_universe(cells[i])
        id = 0
        for i in range(len(surfaces)):
            id = id + 1
            if renumber is True:
                surfaces[i].name = str(id)
                # Leave room for adding macrobodies.
                if isinstance(surfaces[i], RectangularPrism) or isinstance(surfaces[i], Box) or isinstance(surfaces[i], Polyhedron):
                    #print('HERE')
                    id = id+6
                elif isinstance(surfaces[i], CircularCylinder) or isinstance(surfaces[i], EllipticalCylinder) or isinstance(surfaces[i], TruncatedCone):
                    id = id+3
                elif isinstance(surfaces[i], Wedge):
                    id = id+5
                elif isinstance(surfaces[i], HexagonalPrism):
                    id = id+8
                elif isinstance(surfaces[i], Ellipsoid):
                    id = id+1
            #self.surfaces.append(surfaces[i])
            self.surfaces[surfaces[i].name] = surfaces[i]
        for i in range(len(settings)):
            if isinstance(settings[i], TransformationBase):
                if renumber is True:
                    settings[i].name = str(i+1)
                self.transformations[settings[i].name] = settings[i]
            else:
                self.settings.append(settings[i])
        for i in range(len(materials)):
            if renumber is True:
                materials[i].name = str(i+1)
            #self.materials.append(materials[i])
            self.materials[materials[i].name] = materials[i]

    def direct_export(self, title=None):
        """For serializing the original deck. Will preserve comments and most user formatting.
        Line comments may conflict with additions to an existing card. Only call this when your
        modifications are complete.
        """
        if self.serialized is False:
            self.serialized = True
            deck_string = gateway.printDeck(self.deck)
            return deck_string 
        else:
            message = 'The original deck has already been serialized. Use `.export()` instead or restart your script.'
            return message

    def export(self, filename='inp.mcnp', title=None, renumber=False):
        """For exporting to a textual MCNP input file.
        As of now, it exports to a string."""
        inp = Deck()
        inp.initialize()
        if renumber is False:
            for k in self.cells:
                inp.cells.cells.addUnique(self.cells[k]._e_object)
            for k in self.surfaces:
                inp.surfaces.surfaces.addUnique(self.surfaces[k]._e_object)
            for i in range(len(self.settings)):
                inp.data.settings.addUnique(self.settings[i]._e_object)
            for k in self.materials:
                inp.data.materials.addUnique(self.materials[k]._e_object)
            for k in self.transformations:
                inp.data.settings.addUnique(self.transformations[k]._e_object)
        else:
            i = 0
            for k in self.cells:
                i = i+1
                self.cells[k].name = str(i)
                inp.cells.cells.addUnique(self.cells[k]._e_object)
            i = 0
            for k in self.surfaces:
                i = i+1
                self.surfaces[k].name = str(i)
                inp.surfaces.surfaces.addUnique(self.surfaces[k]._e_object)
            for i in range(len(self.settings)):
                inp.data.settings.addUnique(self.settings[i]._e_object)
            i = 0
            for k in self.materials:
                i = i+1
                self.materials[k].name = str(i)
                inp.data.materials.addUnique(self.materials[k]._e_object)
            i = 0
            for k in self.transformations:
                i = i+1
                self.transformations[k].name = str(i)
                inp.data.settings.addUnique(self.transformations[k]._e_object)

        deck_string = gateway.printDeck(gateway.deckResource(inp, filename))

        return formatter(deck_string, title)

    def __repr__(self):
        string = 'MCNP Deck'
        if self.cells is not None:
            string += '\n\t# Cells:\t' + str(len(self.cells))
        else:
            string += '\n\t# Cells:\tNone'
        if self.surfaces is not None:
            string += '\n\t# Surfaces:\t' + str(len(self.surfaces))
        else:
            string += '\n\t# Surfaces:\tNone'
        if self.settings is not None:
            string += '\n\t# Settings:\t' + str(len(self.settings))
        else:
            string += '\n\t# Settings:\tNone'
        if self.materials is not None:
            string += '\n\t# Materials:\t' + str(len(self.materials))
        else:
            string += '\n\t# Materials:\tNone'
        if self.transformations is not None:
            string += '\n\t# TR Cards:\t' + str(len(self.transformations))
        else:
            string += '\n\t# Materials:\tNone'
        if self.universes is not None:
            string += '\n\t# Universes:\t' + str(len(self.universes))
        else:
            string += '\n\t# Universes:\tNone'

        return string

    def get_universe(self, cell):
        if cell.universe is not None:
            u_id = cell.universe.name
            #cell_id = cell.name
            if u_id in self.universes:
                _universe = self.universes[u_id] #.cells[cell_id].add(cell)
                _universe.add_only(cell)
            else:
                _universe = UniverseList(name=u_id, cells=None)
                if cell.universe.sign is not None:
                    _universe.sign = cell.universe.sign
                _universe.add_only(cell)
                self.universes[u_id] = _universe
                _universe._e_object = cell.universe
        # Makes a 0 universe for all non-assigned cells. Has no _e_object.
        else:
            u_id = '0'
            if u_id in self.universes:
                _universe = self.universes[u_id]
                _universe.add_only(cell)
            else:
                _universe = UniverseList(name=u_id, cells=None)
                _universe.add_only(cell)
                self.universes[u_id] = _universe

    def add(self, card):
        if isinstance(card, Cell):
            self.cells[card.name] = card
            if self.serialized is False:
                self.deck.cells.cells.addUnique(self.cells[card.name]._e_object)
            """if card.universe is not None:
                u_id = card.universe.name
                if u_id in self.universes is False:
                    _universe = UniverseList(name=u_id)
                    if card.universe.sign is not None:
                        _universe.sign = card.universe.sign
                    _universe.add(card)
                    self.universes[u_id] = _universe"""
            self.get_universe(card)
        elif isinstance(card, Surface):
            self.surfaces[card.name] = card
            if self.serialized is False:
                self.deck.surfaces.surfaces.addUnique(self.surfaces[card.name]._e_object)
        elif isinstance(card, Material):
            self.materials[card.name] = card
            if self.serialized is False:
                self.deck.data.materials.addUnique(self.materials[card.name]._e_object)
        elif isinstance(card, TransformationBase):
            self.transformations[card.name] = card
            if self.serialized is False:
                self.deck.data.settings.addUnique(self.settings[card.name]._e_object)
        else:
            self.settings.append(card)
            if self.serialized is False:
                self.deck.data.settings.addUnique(self.settings[-1]._e_object)

    def remove(self, card):
        if isinstance(card, Cell):
            if card.universe is not None:
                self.universes[card.universe.name].remove(card)
            del self.cells[card.name]
            if self.serialized is False:
                self.deck.cells.cells.remove(card)
        elif isinstance(card, Surface):
            del self.surfaces[card.name]
            if self.serialized is False:
                self.deck.surfaces.surfaces.remove(card)
        elif isinstance(card, Material):
            del self.materials[card.name]
            if self.serialized is False:
                self.deck.data.materials.remove(card)
        elif isinstance(card, TransformationBase):
            del self.transformations[card.name]
            if self.serialized is False:
                self.deck.data.settings.remove(card)
        else:
            self.settings.remove(card)
            if self.serialized is False:
                self.deck.data.settings.remove(card)

    def add_all(self, cards):
        for i in range(len(cards)):
            self.add(cards[i])

    def remove_all(self, cards):
        for i in range(len(cards)):
            self.remove(cards[i])

    def get_all_surfaces(self):
        """
        Return all surfaces used in the geometry

        Returns
        -------
        collections.OrderedDict
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        """
        surfaces = OrderedDict()

        for c in self.cells:
            cell = self.cells[c]
            #print(cell, '\n')
            if cell.region is not None:
                #print('\nRegion:', cell.region)
                surfaces = cell.region.get_surfaces(surfaces)
        return surfaces

    def get_redundant_surfaces(self):
        """Return all of the topologically redundant surface IDs

        Returns
        -------
        dict
            Dictionary whose keys are the ID of a redundant surface and whose
            values are the topologically equivalent :class:`mcnpy.Surface`
            that should replace it.

        """
        tally = defaultdict(list)
        for s in self.surfaces:
            surf = self.surfaces[s]
            #coeffs = surf.get_coefficients() #tuple(surf.coefficients[k] for k in surf.get_coefficients())
            coeffs = tuple(surf.get_coefficients().values())
            #key = (type(surf).__name__,) + coeffs
            if surf.transformation is None:
                key = (type(surf).__name__, None) + coeffs
            else:
                key = (type(surf).__name__, surf.transformation.name) + coeffs
            #print(key)
            #if surf.transformation is not None:
            #    key = surf.transformation.name + key
            tally[key].append(surf)
        return {replace.name: keep
                for keep, *redundant in tally.values()
                for replace in redundant}

    def remove_redundant_surfaces(self):
        """Remove redundant surfaces from the geometry"""

        # Get redundant surfaces
        redundant_surfaces = self.get_redundant_surfaces()

        # Iterate through all cells contained in the geometry
        for c in self.cells:
            cell = self.cells[c]
            # Recursively remove redundant surfaces from regions
            if cell.region:
                cell.region.remove_redundant_surfaces(redundant_surfaces)

    def remove_unused_surfaces(self):
        """Removes any surface cards that are unused from the deck.
        """

        used_surfs = self.get_all_surfaces()
        unused = []

        for k in self.surfaces:
            surface = self.surfaces[k]
            if k not in used_surfs.keys():
                unused.append(surface)
                
        self.remove_all(unused)
        print(str(len(unused))+' Surfaces were removed for being the same as others.')
