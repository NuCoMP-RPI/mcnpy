from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Deck(DeckBase):
    """
    A representation of the model object `Deck`.
    
    Parameters
    ----------
    file : str
        File for `Deck`.
    mcnpy.Deck#getContinueContinue : str
        Continue for `Deck`.
    cont_data : iterable of mcnpy.ContinueData
        ContData for `Deck`.
    cells : mcnpy.Cells
        Cells for `Deck`.
    surfaces : mcnpy.Surfaces
        Surfaces for `Deck`.
    data : mcnpy.Data
        Data for `Deck`.
    
    """

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
    """
    A representation of the model object `Cells`.
    
    Parameters
    ----------
    
    """

    def _init(self, cells):
        self.cells = cells

class Surfaces(SurfacesBase):
    """
    A representation of the model object `Surfaces`.
    
    Parameters
    ----------
    
    """

    def _init(self, surfaces):
        self.surfaces = surfaces

class Data(DataBase):
    """
    A representation of the model object `Data`.
    
    Parameters
    ----------
    materials : iterable of mcnpy.Material
        Materials for `Data`.
    settings : iterable of mcnpy.Setting
        Settings for `Data`.
    
    """

    def _init(self, materials, settings):
        self.materials = materials
        self.settings = settings


        
for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override