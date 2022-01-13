from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Deck(DeckBase):
    """My custom deck class."""

    def _init(self, cells, surfaces, data):
        self.cells = cells
        self.surfaces = surfaces
        self.data = data

    def initialize(self):
        """Adds empty Cells, Surfaces, and Data objects to the Deck."""
        self.cells = Cells()
        self.surfaces = Surfaces()
        self.data = Data()

class Cells(CellsBase):
    """My custom cells class."""

    def _init(self, cells):
        self.cells = cells

class Surfaces(SurfacesBase):
    """My custom surfaces class."""

    def _init(self, surfaces):
        self.surfaces = surfaces

class Data(DataBase):
    """My custom data class."""

    def _init(self, materials, settings):
        self.materials = materials
        self.settings = settings
        
for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override