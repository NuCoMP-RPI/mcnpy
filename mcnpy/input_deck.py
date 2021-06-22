from mcnpy.cells import Cell
from mcnpy.surfaces import Surface
from mcnpy.materials import Material
from mcnpy.universe import UniverseList
from mcnpy.deck import Deck
from mcnpy.gateway import gateway
from mcnpy.deck_formatter import formatter

class InputDeck():
    """An object containing dicts for cells, surfaces, and materials. All other data cards are stored as a list."""
    def __init__(self, cells=None, surfaces=None, settings=None, materials=None, universes=None):
        self.cells = cells
        self.surfaces = surfaces
        self.settings = settings
        self.materials = materials
        self.universes = universes

        if self.cells is None:
            self.cells = {}
        if self.surfaces is None:
            self.surfaces = {}
        if self.settings is None:
            self.settings = []
        if self.materials is None:
            self.materials = {}
        if self.universes is None:
            self.universes = {}
    
    def import_from_file(self, filename='inp.mcnp'):
        """For reading a deck from a file."""
        inp = gateway.loadFile(filename)
        cells = inp.cells.cells
        surfaces = inp.surfaces.surfaces
        settings = inp.data.settings
        materials = inp.data.materials
        for i in range(len(cells)):
            #self.cells.append(cells[i])
            self.cells[cells[i].name] = cells[i]
            self.get_universe(cells[i])
        for i in range(len(surfaces)):
            #self.surfaces.append(surfaces[i])
            self.surfaces[surfaces[i].name] = surfaces[i]
        for i in range(len(settings)):
            self.settings.append(settings[i])
        for i in range(len(materials)):
            #self.materials.append(materials[i])
            self.materials[materials[i].name] = materials[i]


    def export(self, filename='inp.mcnp', title=None):
        """For exporting to a textual MCNP input file.
        As of now, it exports to a string."""
        inp = Deck()
        inp.initialize()
        for k in self.cells:
            inp.cells.cells.addUnique(self.cells[k]._e_object)
        for k in self.surfaces:
            inp.surfaces.surfaces.addUnique(self.surfaces[k]._e_object)
        for i in range(len(self.settings)):
            inp.data.settings.addUnique(self.settings[i]._e_object)
        for k in self.materials:
            inp.data.materials.addUnique(self.materials[k]._e_object)

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

    def add(self, card):
        if isinstance(card, Cell):
            self.cells[card.name] = card
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
        elif isinstance(card, Material):
            self.materials[card.name] = card
        else:
            self.settings.append(card)

    def remove(self, card):
        if isinstance(card, Cell):
            if card.universe is not None:
                self.universes[card.universe.name].remove(card)
            del self.cells[card.name]
        elif isinstance(card, Surface):
            del self.surfaces[card.name]
        elif isinstance(card, Material):
            del self.materials[card.name]
        else:
            self.settings.remove(card)

    def add_all(self, cards):
        for i in range(len(cards)):
            self.add(cards[i])

    def remove_all(self, cards):
        for i in range(len(cards)):
            self.remove(cards[i])