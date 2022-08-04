from subprocess import Popen, PIPE
from os.path import isfile, join
import os
from collections import OrderedDict, defaultdict
from .materials import Nuclide
from .surfaces import Surface, RectangularPrism, CircularCylinder
from .surfaces import HexagonalPrism, Polyhedron, Wedge, EllipticalCylinder
from .surfaces import Box, TruncatedCone, Ellipsoid
from .materials import Material, MaterialSetting
from .geometry import Cell, Transformation, GeometrySetting, UniverseList
from .output import OutputSetting
from .data import MiscSetting, TerminationSetting
from .source import SourceSetting
from .physics import PhysicsSetting
from .variance_reduction import VarianceReductionSetting
from .tally import TallyABC, TallySettingABC
from ._deck import Deck as _Deck
from .gateway import gateway
from .deck_formatter import formatter, preprocessor, deck_cleanup

def run_mcnp(input, exe='mcnp6', exe_op='IXR', inp=True, mcnp_path=None, 
        data_path=None, ics_path=None, options=[], **kwargs):
    """Initiate MCNP simulation. Also supports calling the plotter.

    Parameters
    ==========
    input : str
        Name of the MCNP textual input file.
    exe : str
        Name of the MCNP executable.
    exe_op : str
        MCNP executions options.
    inp : boolean
        Set to True to run with 'I=input'. False for 'N=input'.
    mcnp_path : str or None
        The path to the MCNP executable. 
    data_path : str or None
        The path to the MCNP XS directory file.
    ics_path : str or None
        The path to ISC data.
    options : iterable of str
        A list of other options that require no arguments.
    **kwargs : str
        Keyword arguments for MCNP.
    """

    cmd = []
    if mcnp_path is None:
        mcnp_path = os.getenv('PATH')
    
    if data_path is None:
        data_path = os.getenv('DATAPATH')
        if data_path is None:
            raise Exception('MCNP datapath not found!')
    
    if ics_path is None:
        ics_path = os.getenv('ISCDATA')
        if data_path is None:
            raise Exception('MCNP ISC datapath not found!')

    # mcnp_path was supplied or PATH envvar exists.
    if mcnp_path is not None:
        paths = mcnp_path.split(':')
        # Check if exe exists on the path.
        for p in paths:
            find_exe = isfile(join(p, exe))
            if find_exe is True:
                # Provide absolute exe path is not using PATH envvar.
                if mcnp_path is not None:
                    exe = join(p, exe)
                cmd.append(exe)
                break
        if find_exe is False:
            raise Exception('MCNP executable not found!')
    else:
        raise Exception('No path to MCNP executable!')

    if exe_op.upper() != 'IXR':
        cmd.append(exe_op)

    # MCNP kwargs entered without an '='.
    kwargs_no_equals = ['c', 'cn', 'dbug', 'tasks']

    for k in kwargs:
        if k.lower() in kwargs_no_equals:
            mcnp_kwarg = k + ' ' + str(kwargs[k])
        else:
            mcnp_kwarg = k + '=' + str(kwargs[k])
        cmd.append(mcnp_kwarg)

    cmd += options

    if inp is True:
        cmd.append('I=' + input)
    else:
        cmd.append('N=' + input)

    #print(cmd)
    with Popen(cmd, stdin=PIPE, stdout=PIPE, bufsize=1, 
                universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here
        #print(p.returncode)
        """if p.returncode != 0:
            raise CalledProcessError(p.returncode, p.args)"""
    
    #proc = Popen(cmd)

def run_script(script, exe, *args, **kwargs):
    cmd = [exe, script, args]

    for k in kwargs:
        cmd.append(k + '=' + str(kwargs[k]))
    
    proc = Popen()

class Deck():
    """An object containing dicts for cells, surfaces, and materials. Most other 
    data cards are stored as lists.

    Parameters
    ----------
    cells : dict, optional
        Dictionary mapping mcnpy.cells.Cell objects by ID.
    surfaces : dict, optional
        Dictionary mapping mcnpy.surfaces.Surface objects by ID.
    materials : dict, optional
        Dictionary mapping mcnpy.materials.Material objects by ID.
    """
    def __init__(self, cells=None, surfaces=None, materials=None, 
                 geom_settings=None, mat_settings=None, out_settings=None, 
                 misc_settings=None, src_settings=None, phys_settings=None, 
                 vr_settings=None, tally_settings=None, tallies=None, 
                 term_settings=None, settings=None, transformations=None, 
                 universes=None, continue_run=None):
        self.cells = cells
        self.surfaces = surfaces
        self.settings = settings #Just a catch-all if something isn't subclassed
        self.transformations = transformations
        self.geom_settings = geom_settings
        self.mat_settings = mat_settings
        self.out_settings = out_settings
        self.misc_settings = misc_settings
        self.src_settings = src_settings
        self.phys_settings = phys_settings
        self.vr_settings = vr_settings
        self.tally_settings = tally_settings
        self.tallies = tallies
        self.term_settings = term_settings
        self.materials = materials
        self.universes = universes
        self.continue_run = continue_run
        self._deck = None
        self.serialized = True

        if self.cells is None:
            self.cells = {}
        if self.surfaces is None:
            self.surfaces = {}
        if self.tallies is None:
            self.tallies = {}
        if self.transformations is None:
            self.transformations = {}
        if self.materials is None:
            self.materials = {}
        if self.universes is None:
            self.universes = {}

        if self.settings is None:
            self.settings = []

        if self.geom_settings is None:
            self.geom_settings = []
        if self.out_settings is None:
            self.out_settings = []
        if self.misc_settings is None:
            self.misc_settings = []
        if self.src_settings is None:
            self.src_settings = []
        if self.vr_settings is None:
            self.vr_settings = []
        if self.tally_settings is None: #TODO: Most classes have IDs
            self.tally_settings = []
        if self.term_settings is None:
            self.term_settings = []
        if self.phys_settings is None:
            self.phys_settings = []
        if self.mat_settings is None:
            self.mat_settings = []
    
    def read(self, filename='inp.mcnp', renumber=False, 
                         preprocess=False):
        """For reading a deck from a file.
        """
        self.serialized = False
        try:
            if preprocess is True:
                filename = preprocessor(filename)
            inp = gateway.loadFile(filename)
            self._deck = inp
        except:
            #print('Parsing failed. Cleaning up the deck and trying again.')
            """try:
                filename = deck_cleanup(filename)
                inp = gateway.loadFile(filename)
                #print('Parsing successful! New file: ' + filename)
                self._deck = inp

            except:"""
            raise Exception('Error importing MCNP Deck from file "' + filename 
                            + '"')
        try: 
            cells = inp.cells.cells
            surfaces = inp.surfaces.surfaces
            settings = inp.data.settings
            materials = inp.data.materials
            for i in range(len(cells)):
                #self.cells.append(cells[i])
                if renumber is True:
                    cells[i].name = i+1
                self.cells[int(cells[i].name)] = cells[i]
                self.get_universe(cells[i])
            id = 0
            for i in range(len(surfaces)):
                id = id + 1
                if renumber is True:
                    surfaces[i].name = id
                    # Leave room for adding macrobodies.
                    if (isinstance(surfaces[i], RectangularPrism) 
                        or isinstance(surfaces[i], Box) 
                        or isinstance(surfaces[i], Polyhedron)):
                        #print('HERE')
                        id = id+6
                    elif (isinstance(surfaces[i], CircularCylinder) 
                        or isinstance(surfaces[i], EllipticalCylinder) 
                        or isinstance(surfaces[i], TruncatedCone)):
                        id = id+3
                    elif isinstance(surfaces[i], Wedge):
                        id = id+5
                    elif isinstance(surfaces[i], HexagonalPrism):
                        id = id+8
                    elif isinstance(surfaces[i], Ellipsoid):
                        id = id+1
                #self.surfaces.append(surfaces[i])
                self.surfaces[int(surfaces[i].name)] = surfaces[i]
            for i in range(len(settings)):
                if isinstance(settings[i], Transformation):
                    if renumber is True:
                        settings[i].name = i+1
                    self.transformations[int(settings[i].name)] = settings[i]
                elif isinstance(settings[i], TallyABC):
                    self.tallies[int(settings[i].name)] = settings[i]
                elif isinstance(settings[i], GeometrySetting):
                    self.geom_settings.append(settings[i])
                elif isinstance(settings[i], OutputSetting):
                    self.out_settings.append(settings[i])
                elif isinstance(settings[i], MiscSetting):
                    self.misc_settings.append(settings[i])
                elif isinstance(settings[i], SourceSetting):
                    self.src_settings.append(settings[i])
                elif isinstance(settings[i], VarianceReductionSetting):
                    self.vr_settings.append(settings[i])
                elif isinstance(settings[i], TallySetting.Setting):
                    self.tally_settings.append(settings[i])
                elif isinstance(settings[i], MaterialSetting):
                    self.mat_settings.append(settings[i])
                elif isinstance(settings[i], TerminationSetting):
                    self.term_settings.append(settings[i])
                elif isinstance(settings[i], PhysicsSetting):
                    self.phys_settings.append(settings[i])
                else:
                    self.settings.append(settings[i])
            for i in range(len(materials)):
                if renumber is True:
                    materials[i].name = i+1
                #self.materials.append(materials[i])
                self.materials[int(materials[i].name)] = materials[i]
        except:
            # For CONTINUE decks
            self.continue_run = inp._e_object.getContinue()
            settings = inp.cont_data
            for i in range(len(settings)):
                self.settings.append(settings[i])

    def _direct_export(self):
        """For serializing the original deck. Will preserve comments and most 
        user formatting. Line comments may conflict with additions to an 
        existing card. Only call this when your modifications are complete.
        """
        if self.serialized is False:
            self.serialized = True
            deck_string = gateway.printDeck(self._deck)
            return deck_string 
        else:
            message = ('The original deck has already been serialized. Use ' 
                       + '`.write()` instead or restart your script.')
            return message

    def write(self, filename='deck.mcnp', title=None, renumber=False, direct=False):
        """Write the deck to file.

        Parameters
        ----------
        filename : str
            The name of the file to be written.
        title : str, optional
            Title line added to the MCNP deck.
        renumber : boolean, optional
            Use sequential numbering for named objects.
        direct : boolean, optional
            Use to preserve comments and formatting when starting with an existing deck.
        """
        with open(filename, 'w') as f:
            if direct is False:
                f.write(self.serialize(title, renumber))
            else:
                f.write(self._direct_export())

    def serialize(self, title=None, renumber=False):
        """Serialize the MCNP deck to a string.

        Parameters
        ----------
        title : str, optional
            User specified title for the deck.
        renumber : boolean, optional
            Use sequential numbering for named objects.

        Returns
        -------
        deck_string : str
            A textual representation of the MCNP deck.
        """

        inp = _Deck()
        if self.continue_run is not None:
            data_settings = inp.cont_data
        else:
            inp.initialize()
            data_settings = inp.data.settings
        if renumber is False:
            # CELLS
            for k in self.cells:
                inp.cells.cells.addUnique(self.cells[k]._e_object)
            # SURFACES
            for k in self.surfaces:
                inp.surfaces.surfaces.addUnique(self.surfaces[k]._e_object)

            # DATA
            for k in self.geom_settings:
                data_settings.addUnique(k._e_object)
            for k in self.transformations:
                data_settings.addUnique(self.transformations[k]._e_object)
            for k in self.phys_settings:
                data_settings.addUnique(k._e_object)
            for k in self.src_settings:
                data_settings.addUnique(k._e_object)
            for k in self.vr_settings:
                data_settings.addUnique(k._e_object)
            for k in self.tallies:
                data_settings.addUnique(self.tallies[k]._e_object)
            for k in self.tally_settings:
                data_settings.addUnique(k._e_object)
            for k in self.out_settings:
                data_settings.addUnique(k._e_object)
            for k in self.term_settings:
                data_settings.addUnique(k._e_object)
            for k in self.misc_settings:
                data_settings.addUnique(k._e_object)
            
            # Materials
            for k in self.materials:
                inp.data.materials.addUnique(self.materials[k]._e_object)
            # Material Settings
            for k in self.mat_settings:
                data_settings.addUnique(k._e_object)

            # Other DATA
            for k in self.settings:
                data_settings.addUnique(k._e_object)

        else:
            # CELLS
            i = 0
            for k in self.cells:
                i = i+1
                self.cells[k].name = str(i)
                inp.cells.cells.addUnique(self.cells[k]._e_object)
            # SURFACES
            i = 0
            for k in self.surfaces:
                i = i+1
                self.surfaces[k].name = str(i)
                inp.surfaces.surfaces.addUnique(self.surfaces[k]._e_object)
            # DATA
            for k in self.geom_settings:
                data_settings.addUnique(k._e_object)
            i = 0
            for k in self.transformations:
                i = i+1
                self.transformations[k].name = str(i)
                data_settings.addUnique(self.transformations[k]._e_object)
            for k in self.phys_settings:
                data_settings.addUnique(k._e_object)
            for k in self.src_settings:
                data_settings.addUnique(k._e_object)
            for k in self.vr_settings:
                data_settings.addUnique(k._e_object)
            for k in self.tallies:
                data_settings.addUnique(self.tallies[k]._e_object)
            for k in self.tally_settings:
                data_settings.addUnique(k._e_object)
            for k in self.out_settings:
                data_settings.addUnique(k._e_object)
            for k in self.term_settings:
                data_settings.addUnique(k._e_object)
            for k in self.misc_settings:
                data_settings.addUnique(k._e_object)
            
            # Materials
            i = 0
            for k in self.materials:
                i = i+1
                self.materials[k].name = str(i)
                inp.data.materials.addUnique(self.materials[k]._e_object)
            # Material Settings
            for k in self.mat_settings:
                data_settings.addUnique(k._e_object)

            # Other DATA
            for k in self.settings:
                data_settings.addUnique(k._e_object)

        deck_string = gateway.printDeck(gateway.deckResource(inp, 'deck.mcnp'))

        return formatter(deck_string, title)

    def __repr__(self):
        string = 'MCNP Deck\n'
        
        string += '\n\t**CELL CARDS**\n'
        if self.cells is not None:
            string += '{0: <16}{1}{2}\n'.format('\tCells', '=\t', 
                                                str(len(self.cells)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tCells', '=\t', 'None')
        if self.universes is not None:
            string += '{0: <16}{1}{2}\n'.format('\tUniverses', '=\t', 
                                                str(len(self.universes)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tUniverses', '=\t', 'None')
        
        string += '\n\t**SURFACE CARDS**\n'
        if self.surfaces is not None:
            string += '{0: <16}{1}{2}\n'.format('\tSurfaces', '=\t', 
                                                str(len(self.surfaces)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tSurfaces', '=\t', 
                                                str(len(self.surfaces)))
        
        string += '\n\t**DATA CARDS**\n'
        if self.geom_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tGeometry', '=\t', 
                                                str(len(self.geom_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tGeometry', '=\t', 'None')
        if self.transformations is not None:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 
                                                str(len(self.transformations)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTransformation', '=\t', 
                                                'None')
        if self.phys_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tPhysics', '=\t', 
                                                str(len(self.phys_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tPhysics', '=\t', 'None')
        if self.src_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tSource', '=\t', 
                                                str(len(self.src_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tSource', '=\t', 'None')
        if self.vr_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tVar. Reduction', '=\t', 
                                                str(len(self.vr_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tVar. Reduction', '=\t', 
                                                'None')
        if self.tallies is not None:
            string += '{0: <16}{1}{2}\n'.format('\tTallies', '=\t', 
                                                str(len(self.tallies)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTallies', '=\t', 'None')
        if self.tally_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tTal. Settings', '=\t', 
                                                str(len(self.tally_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTal. Settings', '=\t', 
                                                'None')
        if self.out_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tOutput', '=\t', 
                                                str(len(self.out_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tOutput', '=\t', 'None')
        if self.term_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tTermination', '=\t', 
                                                str(len(self.term_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tTermination', '=\t', 
                                                'None')
        if self.misc_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tMisc', '=\t', 
                                                str(len(self.misc_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tMisc', '=\t', 'None')
        
        
        if self.settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tOther Data', '=\t', 
                                                str(len(self.settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tOther Data', '=\t', 'None')
        
        string += '\n\t**MATERIAL CARDS**\n'
        if self.materials is not None:
            string += '{0: <16}{1}{2}\n'.format('\tMaterials', '=\t', 
                                                str(len(self.materials)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tMaterials', '=\t', 'None')
        if self.mat_settings is not None:
            string += '{0: <16}{1}{2}\n'.format('\tMat. Settings', '=\t', 
                                                str(len(self.mat_settings)))
        else:
            string += '{0: <16}{1}{2}\n'.format('\tMat. Settings', '=\t', 
                                                'None')

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
            u_id = 0
            if u_id in self.universes:
                _universe = self.universes[u_id]
                _universe.add_only(cell)
            else:
                _universe = UniverseList(name=u_id, cells=None)
                _universe.add_only(cell)
                self.universes[u_id] = _universe

    def __add__(self, card):
        #new = Deck(self)
        self += card
        return self

    def __iadd__(self, card):
        if isinstance(card, list):
            self.add_all(card)
        else:
            self.add(card)
        return self

    def __sub__(self, card):
        new = Deck(self)
        new -= card
        return new

    def __isub__(self, card):
        if isinstance(card, list):
            self.remove_all(card)
        else:
            self.remove(card)
        return self

    def add(self, card):
        """Add a card to the deck.
        """
        # Ensure there are no nulls before seriaization.
        # _defaults must be added to each class.
        defaults = getattr(card, '_defaults', None)
        if callable(defaults):
            card._defaults()
        if isinstance(card, Cell):
            self.set_id(card, self.cells)
            # Because I'm just used to making the density negative.
            if card.density < 0:
                card.density = abs(card.density)
                card.density_unit = '-'
            if self.serialized is False:
                self._deck.cells.cells.addUnique(self.cells[card.name]._e_object)
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
            self.set_id(card, self.surfaces)
            if self.serialized is False:
                self._deck.surfaces.surfaces.addUnique(self.surfaces
                                                      [card.name]._e_object)
        elif isinstance(card, Nuclide):
            _card = Material()
            _card += card
            self.set_id(_card, self.materials)
            if self.serialized is False:
                self._deck.data.materials.addUnique(self.materials
                                                   [card.name]._e_object)
        elif isinstance(card, Material):
            self.set_id(card, self.materials)
            if self.serialized is False:
                self._deck.data.materials.addUnique(self.materials
                                                   [card.name]._e_object)
        elif isinstance(card, Transformation):
            self.set_id(card, self.transformations)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.settings
                                                  [card.name]._e_object)
        elif isinstance(card, TallyABC):
            self.set_id(card, self.tallies)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.settings
                                                  [card.name]._e_object)
        
        elif isinstance(card, GeometrySetting):
            self.geom_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.geom_settings
                                                  [-1]._e_object)
        elif isinstance(card, PhysicsSetting):
            self.phys_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.phys_settings
                                                  [-1]._e_object)
        elif isinstance(card, SourceSetting):
            self.src_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.src_settings
                                                 [-1]._e_object)
        elif isinstance(card, VarianceReductionSetting):
            self.vr_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.vr_settings
                                                  [-1]._e_object)
        elif isinstance(card, TallySetting.Setting):
            self.tally_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.tally_settings
                                                  [-1]._e_object)
        elif isinstance(card, OutputSetting):
            self.out_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.out_settings
                                                  [-1]._e_object)
        elif isinstance(card, TerminationSetting):
            self.term_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.term_settings
                                                  [-1]._e_object)
        elif isinstance(card, MiscSetting):
            self.misc_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.misc_settings
                                                  [-1]._e_object)
        elif isinstance(card, MaterialSetting):
            self.mat_settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.mat_settings
                                                  [-1]._e_object)
        
        else:
            self.settings.append(card)
            if self.serialized is False:
                self._deck.data.settings.addUnique(self.settings[-1]._e_object)

    def remove(self, card):
        """Remove a card from the deck.
        """
        if isinstance(card, Cell):
            if card.universe is not None:
                self.universes[card.universe.name].remove(card)
            del self.cells[card.name]
            if self.serialized is False:
                self._deck.cells.cells.remove(card)
        elif isinstance(card, Surface):
            del self.surfaces[card.name]
            if self.serialized is False:
                try:
                    self._deck.surfaces.surfaces.remove(card)
                except:
                    pass
        elif isinstance(card, Material):
            del self.materials[card.name]
            if self.serialized is False:
                self._deck.data.materials.remove(card)
        elif isinstance(card, Transformation):
            del self.transformations[card.name]
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, TallyABC):
            del self.tallies[card.name]
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, GeometrySetting):
            self.geom_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, PhysicsSetting):
            self.phys_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, SourceSetting):
            self.src_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, VarianceReductionSetting):
            self.vr_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, TallySetting.Setting):
            self.tally_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, OutputSetting):
            self.out_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, TerminationSetting):
            self.term_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, MiscSetting):
            self.misc_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        elif isinstance(card, MaterialSetting):
            self.mat_settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)
        else:
            self.settings.remove(card)
            if self.serialized is False:
                self._deck.data.settings.remove(card)

    def add_all(self, cards):
        """Add a list of cards to the deck.
        """
        for i in range(len(cards)):
            self.add(cards[i])

    def remove_all(self, cards):
        """Remove a list of cards from the deck.
        """
        for i in range(len(cards)):
            self.remove(cards[i])

    # Should be redundant with the IDManagerMixin class.
    def set_id(self, card, dict:dict):
        """To ensure every card is numbered.
        """
        if card.name is None:
            if len(dict.keys()) > 0:
                new_name = max(dict.keys()) + 1
            else:
                new_name = 1
            card.name = new_name
        else:
            new_name = card.name
        if new_name in dict:
            print(str(type(card)) + ' Card with ID ' + str(new_name) 
                  + ' was overriden!')
        dict[card.name] = card

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
            coeffs = tuple(surf.get_coefficients().values())
            if surf.transformation is None:
                key = (type(surf).__name__, None) + coeffs
            else:
                key = (type(surf).__name__, surf.transformation.name) + coeffs
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
        print(str(len(unused))+' Surfaces were removed for being the same as ' 
              + 'others.')
