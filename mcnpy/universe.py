from mcnpy.wrap import wrappers, overrides
#from mcnpy import UniverseBase
globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class UniverseList():
    """`Universe` containing a list of `Cell` objects. Handles assigning `Universe` IDs to each MCNP `Cell`.
    """
    def __init__(self, name, cells=None, sign=None):
        
        # self._e_object exists because the universe keyword on each cell
        # creates a separate referenceable object. Using self._e_object gives
        # the Universe class a singular reference.
        self._e_object = None
        self.name = name
        self.cells = {}
        self.sign = sign
        """if isinstance(cells, list):
            for i in range(len(cells)):
                self.add(cells[i])
                #self.cells[cells[i].name] = cells[i]
        else:"""
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
        self.cells[cell.name] = self.apply_to_cell(cell)

    def add_all(self, cells):
        for i in range(len(cells)):
            self.cells[cells[i].name] = self.apply_to_cell(cells[i])

    def remove(self, cell):
        del self.cells[cell.name]
        # This should ensure that references aren't broken when removing cells
        # from the universe. 
        if self._e_object == cell.universe:
            key = list(self.cells.keys())[0]
            #self._e_object = self.cells[key].universe
            self.cells[key].universe = self._e_object
        cell.universe = None

    def remove_all(self, cells):
        for i in range(len(cells)):
            self.remove(cells[i])

    def add_only(self, cell):
        self.cells[cell.name] = cell

class Universe(UniverseBase):
    def _init(self, name):
        self.name = name
        
    def __str__(self):
        return 'U' + str(self.name)

    def __repr__(self):
        return 'U' + str(self.name)

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override