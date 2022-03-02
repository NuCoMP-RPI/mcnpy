from .wrap import wrappers, overrides
from .zaid_helper import element_to_zaid, zaid_to_element
from .basic_structures import Point

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

PARTICLE = {
    'COSMIC' : 'CR',
    'COSMIC_PROTONS' : 'C1001',
	'COSMIC_ALPHAS' : 'C2004',
	'BACKGROUND' : 'BG',
	'BACKGROUND_NEUTRONS' : 'BN',
	'BACKGROUND_PHOTONS' : 'BP',
	'SPONTANEOUS_FISSION' : 'SF',
	'SPONTAENOUS_PHOTON' : 'SP',
	'COSMIC_NITROGEN' : 'C7014',
	'COSMIC_SILICON' : 'C14028',
	'COSMIC_IRON' : 'C26056',
	'NEUTRON' : 'N',
	'ANTI_NEUTRON' : 'Q',
	'PHOTON' : 'P',
	'ELECTRON ' : 'E',
	'POSITRON' : 'F',
	'NEGATIVE_MUON' : '|',
	'POSITIVE_MUON' : '!',
	'ELECTRON_NEUTRINO' : 'U',
	'ANTI_ELECTRON_NEUTRINO' : '<',
	'MUON_NEUTRINO' : 'V',
	'ANTI_MUON_NEUTRINO' : '>',
	'PROTON' : 'H',
	'ANTI_PROTON' : 'G',
	'LAMBDA_BARYON' : 'L',
	'ANTI_LAMBDA_BARYON' : 'B',
	'POSITIVE_SIGMA_BARYON' : '+',
	'ANTI_POSITIVE_SIGMA_BARYON' : '_',
	'NEGATIVE_SIGMA_BARYON' : '-',
	'ANTI_NEGATIVE_SIGMA_BARYON' : '~',
	'XI_BARYON' : 'X',
	'ANTI_NEUTRAL_XI_BARYON' : 'C',
	'NEGATIVE_XI_BARYON' : 'Y',
	'POSITIVE_XI_BARYON' : 'W',
	'OMEGA_BARYON' : 'O',
	'ANTI_OMEGA_BARYON' : '@',
	'POSITIVE_PION' : '/',
	'NEGATIVE_PION' : '*',
	'NEUTRAL_PION' : 'Z',
	'POSITIVE_KAON' : 'K',
	'NEGATIVE_KAON' : '?',
	'KAON_SHORT' : '%',
	'KAON_LONG' : '^',
	'DEUTERON' : 'D',
	'TRITION' : 'T',
	'HELION' : 'S',
	'ALPHA' : 'A',
	'HEAVY_IONS' : '#'
}

# TODO: Figure out how to best andle jumps.
class CriticalitySource(CriticalitySourceBase):
    """def _init(self, histories=None, keff_guess=None, skip_cycles=None, cylces=None, source_point_count=None, normalize_tallies=None, max_cycles=None, average_by_cycles=None):

        self.histories = histories
        self.keff_guess = keff_guess
        self.skip_cycles = skip_cycles
        self.cycles = cylces
        self.source_point_count = source_point_count
        self.normalize_tallies = normalize_tallies
        self.max_cycles=max_cycles
        self.average_by_cycles = average_by_cycles"""
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

        """for k in kwargs:
            # Not a jump.
            if kwargs[k] != 'j' and kwargs[k] != 'J':
                if k.lower() == 'histories':
                    self.histories = kwargs[k]
                elif k.lower() == 'keff_guess':
                    self.keff_guess = kwargs[k]
                elif k.lower() == 'skip_cycles':
                    self.skip_cycles = kwargs[k]
                elif k.lower() == 'cycles':
                    self.cycles = kwargs[k]
                elif k.lower() == 'source_point_count':
                    self.source_point_count = kwargs[k]
                elif k.lower() == 'normalize_tallies':
                    self.normalize_tallies = kwargs[k]
                elif k.lower() == 'max_cycles':
                    self.max_cycles = kwargs[k]
                elif k.lower() == 'average_by_cycles':
                    self.average_by_cycles = kwargs[k]
            # Jump
            else:
                if k.lower() == 'histories':
                    self.j_histories = kwargs[k]
                elif k.lower() == 'keff_guess':
                    self.j_keff_guess = kwargs[k]
                elif k.lower() == 'skip_cycles':
                    self.j_skip_cycles = kwargs[k]
                elif k.lower() == 'cycles':
                    self.j_cycles = kwargs[k]
                elif k.lower() == 'source_point_count':
                    self.j_source_point_count = kwargs[k]
                elif k.lower() == 'normalize_tallies':
                    self.j_normalize_tallies = kwargs[k]
                elif k.lower() == 'max_cycles':
                    self.j_max_cycles = kwargs[k]
                elif k.lower() == 'average_by_cycles':
                    self.j_average_by_cycles = kwargs[k]"""

    def __str__(self):
        string = 'KCODE\n'
        string += 'Histories: ' + str(self.histories) + '\n'
        string += 'Guess: ' + str(self.keff_guess) + '\n'
        string += 'Skip Cycles: ' + str(self.skip_cycles) + '\n'
        string += 'Total Cycles: ' + str(self.cycles) + '\n'
        string += 'Source Points: ' + str(self.source_point_count) + '\n'
        string += 'Normalize: ' + str(self.normalize_tallies) + '\n'
        string += 'Max Cycles: ' + str(self.max_cycles) + '\n'
        string += 'Averaged: ' + str(self.average_by_cycles) + '\n'

        return string

    def __repr__(self) -> str:
        return str(self)
        

#TODO: Better distribution support
class Source(SourceBase):

    def _init(self, **kwargs):
        for k in kwargs:
            if k.lower() == 'loc':
                self.lattitude = kwargs[k][0]
                self.longitude = kwargs[k][1]
                self.altitude = kwargs[k][2]
            elif k.lower() == 'ara':
                self.area = kwargs[k]
            elif k.lower() == 'axs':
                if isinstance(kwargs[k], Point):
                    self.axis = kwargs[k]
                else:
                    #self.axis = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.axis = Point.aspoint(kwargs[k])
            elif k.lower() == 'bem':
                self.x_beam_emittance = kwargs[k][0]
                self.y_beam_emittance = kwargs[k][1]
                self.beam_distance = kwargs[k][2]
            elif k.lower() == 'cel':
                self.cells = kwargs[k]
            elif k.lower() == 'ccc':
                self.cookie_cutter_cell = kwargs[k]
            elif k.lower() == 'dir':
                self.cosine = kwargs[k]
            elif k.lower() == 'dat':
                self.month = kwargs[k][0]
                self.day = kwargs[k][1]
                self.year = kwargs[k][2]
            elif k.lower() == 'nrm':
                self.direction = kwargs[k]
            elif k.lower() == 'erg':
                self.energy = kwargs[k]
            elif k.lower() == 'ext':
                self.extent = kwargs[k]
            elif k.lower() == 'par':
                self.particle = SourceParticle(kwargs[k])
            elif k.lower() == 'pos':
                if isinstance(kwargs[k], Point):
                    self.position = kwargs[k]
                else:
                    #self.position = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.position = Point.aspoint(kwargs[k])
            elif k.lower() == 'rad':
                self.radial_distance = kwargs[k]
            elif k.lower() == 'eff':
                self.rejection_efficiency = kwargs[k]
            elif k.lower() == 'sur':
                self.surface = kwargs[k]
            elif k.lower() == 'tme':
                self.time = kwargs[k]
            elif k.lower() == 'tr':
                self.transformation = kwargs[k]
            elif k.lower() == 'bap':
                self.x_beam_aperature = kwargs[k][0]
                self.y_beam_aperature = kwargs[k][1]
                self.u = kwargs[k][2]
            elif k.lower() == 'vec':
                if isinstance(kwargs[k], Point):
                    self.vector = kwargs[k]
                else:
                    #self.vector = Point(kwargs[k][0], kwargs[k][1], kwargs[k][2])
                    self.vector = Point.aspoint(kwargs[k])
            elif k.lower() == 'wgt':
                self.weight = kwargs[k]
            elif k.lower() == 'x':
                self.x_coord = kwargs[k]
            elif k.lower() == 'y':
                self.y_coord = kwargs[k]
            elif k.lower() == 'z':
                self.z_coord = kwargs[k]
            elif k.lower() == 'normalize':
                self.normal = kwargs[k]
            else:
                setattr(self, k.lower(), kwargs[k])

        """def __str__(self):
            string = 

            return string

        def __repr__(self):
            return str(self)"""

class CriticalitySourcePoints(CriticalitySourcePointsBase):
    """
    """
    def _init(self, points):
        self.points = []
        for p in points:
            if isinstance(p, Point) is False:
                p = Point.aspoint(p)
            self.points.append(p)

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return str(self)

class SourceParticle(SourceParticleBase):
    """
    """
    def _init(self, par):
        """
        """
        # For when an enum is used.
        if str(par).upper() in PARTICLE.keys() or str(par).upper() in PARTICLE.values():
            self.particle = par
        # For when a ZAID is used.
        else:
            self.ion = int(element_to_zaid(str(par)))

    def __str__(self):
        if self.ion is not None:
            string = zaid_to_element(self.ion)
        elif self.particle is not None:
            string = str(self.particle)
        else:
            string = ''
        
        return string

    def __repr__(self):
            return str(self)
    

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override