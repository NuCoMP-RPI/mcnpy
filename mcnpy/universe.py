from mcnpy.wrap import wrappers, overrides
#from mcnpy import UniverseBase
globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class UniverseList():
    """Class to assign `mcnpy.Universe` objects to a list of `mcnpy.Cell` objects.

    Parameters
    ----------
    name : str
        The universe ID number.
    cells : iterable of mcnpy.Cell, optional
        List of cells.
    sign : str, optional
        '-' turns off distance to universe boundary calculations.
    
    Attributes
    ----------
    name : str
        The universe ID number.
    cells : dict
        Dictionary storing all cells in the universe by their IDs.
    sign : str
        '-' turns off distance to universe boundary calculations.
    """
    def __init__(self, name, cells=None, sign=None):
        
        # self._e_object exists because the universe keyword on each cell
        # creates a separate referenceable object. Using self._e_object gives
        # the Universe class a singular reference.
        self._e_object = None
        self.name = name
        self.cells = {}
        self.sign = sign
        if cells is not None:
            if isinstance(cells, list):
                self.add_all(cells)
            else:
                self.add(cells)

    def apply_to_cell(self, cell):
        _universe = Universe(name=self.name)
        #_universe.name = self.name
        if self.sign is not None:
            _universe.sign = self.sign
        cell.universe = _universe

        # self._e_object is set to the reference of the universe keyword of 
        # the first cell listed.
        if self._e_object is None:
            self._e_object = _universe

        return cell

    def add(self, cell):
        """Add a cell to a `mcnpy.UniverseList`.

        Parameters
        ----------
        cell : mcnpy.Cell
            Cell to be added.
        """

        self.cells[cell.name] = self.apply_to_cell(cell)

    def add_all(self, cells):
        """Add a list of cells to a `mcnpy.UniverseList`.

        Parameters
        ----------
        cells : iterable of mcnpy.Cell
            Cells to be added.
        """

        for cell in cells:
            self.add(cell)

    def remove(self, cell):
        """Remove a cell from a `mcnpy.UniverseList`.

        Parameters
        ----------
        cell : mcnpy.Cell
            Cell to be removed.
        """

        del self.cells[cell.name]
        # This should ensure that references aren't broken when removing cells
        # from the universe. 
        if self._e_object == cell.universe:
            key = list(self.cells.keys())[0]
            #self._e_object = self.cells[key].universe
            self.cells[key].universe = self._e_object
        cell.universe = None

    def remove_all(self, cells):
        """Remove a list of cells from a `mcnpy.UniverseList`.

        Parameters
        ----------
        cells : iterable of mcnpy.Cell
            Cells to be removed.
        """

        for cell in cells:
            self.remove(cell)

    def add_only(self, cell):
        self.cells[cell.name] = cell

class Universe(UniverseBase):
    __doc__ = UniverseBase().__doc__

    def _init(self, name):
        self.name = name
        
    def __str__(self):
        return 'U' + str(self.name)

    def __repr__(self):
        return 'U' + str(self.name)

class Universes(UniversesBase):
    __doc__ = UniversesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override