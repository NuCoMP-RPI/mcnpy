from enum import Enum

class BoundaryType(Enum):
    VACUUM = None
    REFLECTIVE = '*'
    WHITE = '+'

class LibraryQuantity(Enum):
    NEUTRON_CONTINUOUS = 'C'
    NEUTRON_N_CONTINUOUS = 'NC'
    NEUTRON_DISCRETE = 'D'
    NEUTRON_PHOTON_MULTIGROUP = 'M'
    PHOTOATOMIC = 'P'
    PHOTONUCLEAR = 'U'
    DOSIMETRY = 'Y'
    ELECTRON = 'E'
    PROTON = 'H'
    DEUTERON = 'O'
    TRITON = 'R'
    HELION = 'S'
    ALPHA = 'A'

class PartisnSolverAcceleration(Enum):
    DSA = 'DSA'
    TSA = 'TSA'
    NO = 'NO'

class EmbeddedGeometryMeshFormat(Enum):
    LNK3DNT = 'LNK3DNT'
    ABAQUS = 'ABAQUS'
    MCNPUM = 'MCNPUM'

class EmbeddedGeometryDebug(Enum):
    ECHOMESH = 'ECHOMESH'

class EmbeddedGeometryFiletype(Enum):
    ASCII = 'ASCII'
    BINARY = 'BINARY'

class EmbeddedGeometryOverlap(Enum):
    ENTRY = 'ENTRY'
    AVERAGE = 'AVERAGE'
    EXIT = 'EXIT'

class MTypeOptions(Enum):
    FLUX = 'FLUX'
    ISOTOPIC = 'ISOTROPIC'
    POPULATION = 'POPULATION'
    REACTION = 'REACTION'
    SOURCE = 'SOURCE'
    TRACKS = 'TRACKS'
    POP = 'POP'

class SabNuclide(Enum):
    Al27 = 'AL27'
    Be_METAL = 'BE'
    Be_IN_BeO = 'BE-O'
    BeO = 'BEO'
    BENZENE = 'BENZ'
    ORTHO_DEUTERIUM = 'DORTHO'
    PARA_DEUTERIUM = 'DPARA'
    Fe56 = 'FE56'
    GRAPHITE = 'GRPH'
    H_IN_ZrH = 'H-ZR'
    ORTHO_H = 'HORTHO'
    PARA_H = 'HPARA'
    DEUTERIUM_IN_HEAVY_WATER = 'HWTR'
    H_IN_LIQUID_METHANE = 'LMETH'
    H_IN_LIGHT_WATER = 'LWTR'
    O_IN_BeO = 'O-BE'
    O_IN_UO2 = 'O2-U'
    H_IN_POLYETHELENE = 'POLY'
    Si_AND_O_IN_SiO2 = 'SIO2'
    H_IN_SOLID_METHANE = 'SMETH'
    U238_IN_UO2 = 'U-O2'
    Zr_IN_ZrH = 'ZR-H'

class MultigroupTransportMode(Enum):
    FORWARD = 'F'
    ADJOINT = 'A'

class DelayedParticles(Enum):
    NONE = 'NONE'
    NEUTRON = 'N'
    GAMMA = 'P'
    BETA = 'E'
    POSITRON = 'F'
    ALPHA = 'A'
    ALL = 'ALL'

class ActivationDelayedNeutronData(Enum):
    MODEL = 'MODEL'
    LIBRARY = 'LIBRARY'
    BOTH = 'BOTH'
    PROMPT = 'PROMPT'

class ActivationDelayedGammaData(Enum):
    LINES = 'LINES'
    MG = 'MG'
    NONE = 'NONE'

class CorrUncorr(Enum):
    CORRELATE = 'CORRELATE'
    NONFISS_COR = 'NONFISS_COR'

class TransportMultipleCoulombScattering(Enum):
    OFF = 'OFF'
    FNAL1 = 'FNAL1'
    GAUSSIAN = 'GAUSSIAN'
    FNAL2 = 'FNAL2'

class TransportEnergyLoss(Enum):
    OFF = 'OFF'
    STRAG1 = 'STRAG1'
    CSDA = 'CSDA'

class TransportNuclearReactions(Enum):
    OFF = 'OFF'
    ON = 'ON'
    ATTENUATE = 'ATTEN'
    REMOVE = 'REMOVE'

class TransportNuclearElasticScattering(Enum):
    OFF = 'OFF'
    ON = 'ON'

class MagneticFieldType(Enum):
    DIPOLE = 'CONST' 
    QUADRUPOLE = 'QUAD' 
    QUADRUPOLE_FRINGE_FIELD = 'QUADFF'

class DependentDistribution(Enum):
    CELL = 'FCEL'
    SURFACE = 'FSUR'
    ENERGY = 'FERG'
    TIME = 'FTME'
    COSINE = 'FDIR'
    VECTOR = 'FVEC'
    NORMAL = 'FNRM'
    POSITION = 'FPOS'
    RADIAL = 'FRAD'
    EXTENT = 'FEXT'
    AXIS = 'FAXS'
    X = 'FX'
    Y = 'FY'
    Z = 'FZ'
    TRANSPORT = 'FTR'
    PARTICLE = 'FPAR'
    COOKIE = 'FCCC'
    AREA = 'FARA'
    WEIGHT = 'FWGT'
    EFFICIENCY = 'FEFF'
    
class DependentDistributionPos(Enum):
    CELL = 'FCEL'
    SURFACE = 'FSUR'
    ENERGY = 'FERG'
    TIME = 'FTME'
    COSINE = 'FDIR'
    VECTOR = 'FVEC'
    NORMAL = 'FNRM'
    POSITION = 'FPOS'
    RADIAL = 'FRAD'
    EXTENT = 'FEXT'
    AXIS = 'FAXS'
    X = 'FX'
    Y = 'FY'
    Z = 'FZ'
    TRANSPORT = 'FTR'
    PARTICLE = 'FPAR'
    COOKIE = 'FCCC'
    AREA = 'FARA'
    WEIGHT = 'FWGT'
    EFFICIENCY = 'FEFF'

class SourceInfoOption(Enum):
    HISTOGRAM = 'H'
    DISCRETE = 'L'
    PROBABILITIES = 'A'

class SourceProbabilityOption(Enum):
    PROBABILITIES = 'D'
    CUMULATIVE_PROBABILITIES = 'C'
    CELL_PROBABILITIES = 'V'
    PARTICLE_WEIGHTS = 'W'

class SrcKeyword(Enum):
    INFO = 'SI'
    PROBABILITY = 'SP'
    BIAS = 'SB'

class VerticalSrcOptions(Enum):
    DISCRET = 'L'
    HISTOGRAM = 'H'
    PROBABILITIES = 'A'
    CUMULATIVE_PROBABILITIES = 'C'
    CELL_PROBABILITIES = 'V'
    PARTICLE_WEIGHTS = 'W'

class DependentSourceDistributionOption(Enum):
    HISTOGRAM = 'H' 
    DISCRETE = 'L'

class CriticalityOptionsSensitivityProfile(Enum):
    MCTAL = 'MCTAL'

class FAxis(Enum):
    X = 'FX'
    Y = 'FY'
    Z = 'FZ'

class TallyQuantity(Enum):
    GEOMETRY = 'F'
    DIRECT = 'D'
    USER = 'U'
    SEGMENT = 'S'
    MULTIPLER = 'M'
    ANGLE = 'C'
    ENERGY = 'E'
    TIME = 'T'

class Interpolation(Enum):
    LOG = 'LOG' 
    LINEAR = 'LIN'

class TTreatment(Enum):
    FIXED_REF = 'FRV'
    GAUSSIAN_BROADENING = 'GEB'
    TIME_CONVOLUTION = 'TMC'
    NUM_COLLISIONS = 'INC'
    DET_SCORE_CELL = 'ICD'
    SAMPLE_INDEX_SRC_DIST = 'SCX'
    SPECIFIED_SRC_DIST = 'SCD'
    ELECTRON_CURRENT_TALLY = 'ELC'
    MULTIGROUP_USER_BINS = 'PTT'
    PULSE_HEIGHT_TALLY = 'PHL'
    COINCIDENCE_CAPTURE = 'CAP'
    HI_RESIDUAL_ISOTOPES = 'RES'
    TALLY_TAGGING = 'TAG'
    LET = 'LET'
    RECEIVER_OP_CHAR = 'ROC'
    POINT_DET_SAMPLING = 'PDS'
    FIRST_FISSION_TALLY = 'FFT'
    COMPTON_IMAGE_TALLY = 'COM'

class CriticalitySensitivityType(Enum):
    XS = 'XS'

class Tmesh1(Enum):
    TRACKS = 'TRAKS' 
    FLUX = 'FLUX' 
    POPULATION = 'POPUL' 
    DEPOSITION = 'PEDEP'

class Tmesh3(Enum):
    TOTAL = 'TOTAL' 
    IONIZATION = 'DE'
    RECOIL = 'RECOIL' 
    TRACKLENGTH = 'TLEST' 
    NON_TRACKED = 'EDLCT'

class MeshType(Enum):
    RECTANGULAR = 'RMESH'
    CYLINDRICAL = 'CMESH'
    SPHERICAL = 'SMESH'

class TallyMeshGeometry(Enum):
    CARTESIAN = 'XYZ'   
    CYLINDRICAL = 'RZT' 

class TallyMeshFormat(Enum):
    COLUMNS = 'COL' 
    COLUMNS_WITH_VOLUMES = 'COLUMNS_WITH_VOLUMES'
    IJ = 'IJ'
    IK = 'IK'
    JK = 'JK'
    NONE = 'NONE'

class TallyQuantityType(Enum):
    FLUX = 'FLUX' 
    SOURCE = 'SOURCE'

class ForceOff(Enum):
    FORCE = 'FORCE' 
    OFF = 'OFF'

class MeshGeometry(Enum):
    CARTESIAN = 'XYZ'   
    CYLINDRICAL = 'RZT' 
    YLINDRICAL = 'CYL'
    SPHERICAL = 'RPT'   

class ParticleTrackFormat(Enum):
    ASCII = 'ASC' 
    BINARY = 'BIN' 
    ASCII_OVERWRITE = 'AOV' 
    BINARY_OVERWRITE = 'BOV'

class ParticleTrackWrite(Enum):
    POSITIONS = 'POS' 
    ALL = 'ALL'

class ParticleTrackEvent(Enum):
    SOURCE = 'SRC' 
    BANK = 'BNK' 
    SURFACE = 'SUR' 
    COLLISION = 'COL'
    TERMINATION = 'TER' 
    CAPTURE = 'CAP'

class ParticleTrackFilterQuantity(Enum):
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    U = 'U'
    V = 'V'
    W = 'W'
    ENERGY = 'ERG' 
    WEIGHT = 'WGT' 
    TIME = 'TME'
    SPEED = 'VEL'
    IMPORTANCE_NEUTRON = 'IMP1'
    IMPORTANCE_PHOTON = 'IMP2'
    IMPORTANCE_ELECTRON = 'IMP3'
    SPARE1 = 'SPARE1'
    SPARE2 = 'SPARE2'
    SPARE3 = 'SPARE3'
    CELL = 'ICL'
    SURFACE = 'JSU'
    DETERMINISTIC_TRANSPORT_SPHERE = 'IDX'
    NUM_COLLISIONS = 'NCP'
    GEOMETRY_LEVEL = 'LEV'
    LATTICE_I = 'III'
    LATTICE_J = 'JJJ'
    LATTICE_K = 'KKK'

class ParameterCommand(Enum):
    COPLOT = 'COPLOT'
    ALL = 'ALL'

class FixedVariable(Enum):
    CELL_SURF_DET = 'F'
    TOT_VS_DIRECT = 'D'
    USER_DEF = 'U'
    SEGMENT = 'S'
    MULT = 'M'
    COSINE = 'C'
    ENERGY = 'E'
    TIME = 'T'
    FIRST_LAT_INDEX = 'I'
    SECOND_LAT_INDEX = 'J'
    THIRD_LAT_INDEX = 'K'

class TallyFluctuationList(Enum):
    MEAN = 'M'
    REL_ERROR = 'E'
    FOM = 'F'
    LARGEST_TALLIES = 'L'
    NUM_FRACTION = 'N'
    PROBABILITY = 'P'
    SLOPE = 'S'
    CUMULATIVE_TALLY = 'T'
    VOV_FUNCTION = 'V'

class LogLin(Enum):
    LOG = 'LOG'
    LINEAR = 'LIN'

class FileAccess(Enum):
    SEQUENTIAL = 'SEQUENTIAL' 
    DIRECT = 'DIRECT' 
    SEQUENTIAL_SHORT = 'S' 
    DIRECT_SHORT = 'D'

class FileFormat(Enum):
    FORMATTED = 'FORMATTED' 
    UNFORMATTED = 'UNFORMATTED' 
    FORMATTED_SHORT = 'F' 
    UNFORMATTED_SHORT = 'U'

class DensityUnit(Enum):
    A_BCM = '+' 
    G_CM3 = '-' 

class FractionUnit(Enum):
    ATOM = '+' 
    WEIGHT = '-'

class AngleUnit(Enum):
    COSINES = None
    DEGREES = '*'

class CurrentUnit(Enum):
    PARTICLES = None
    MEV = '*'

class FluxUnit(Enum):
    PARTICLES_CM2 = None
    MEV_CM2 = '*'

class DepositionUnit(Enum):
    MEV_G = None
    JERKS_G = '*'

class PulseUnit(Enum):
    PULSES = None
    MEV = '*'

class Axis(Enum):
    X = 'X'
    Y = 'Y'
    Z = 'Z'

class YesNo(Enum):
    YES = 'YES'
    NO = 'NO'

class PositiveNegative(Enum):
    POSITIVE = '+'
    NEGATIVE = '-'

class Particle(Enum):
    COSMIC = 'CR'
    COSMIC_PROTONS = 'C1001'
    COSMIC_ALPHAS = 'C2004'
    BACKGROUND = 'BG'
    BACKGROUND_NEUTRONS = 'BN'
    BACKGROUND_PHOTONS = 'BP'
    SPONTANEOUS_FISSION = 'SF'
    SPONTAENOUS_PHOTON = 'SP'
    COSMIC_NITROGEN = 'C7014'
    COSMIC_SILICON = 'C14028'
    COSMIC_IRON = 'C26056'
    NEUTRON = 'N'
    ANTI_NEUTRON = 'Q'
    PHOTON = 'P'
    ELECTRON = 'E'
    POSITRON = 'F'
    NEGATIVE_MUON = '|'
    POSITIVE_MUON = '!'
    ELECTRON_NEUTRINO = 'U'
    ANTI_ELECTRON_NEUTRINO = '<'
    MUON_NEUTRINO = 'V'
    ANTI_MUON_NEUTRINO = '>'
    PROTON = 'H'
    ANTI_PROTON = 'G'
    LAMBDA_BARYON = 'L'
    ANTI_LAMBDA_BARYON = 'B'
    POSITIVE_SIGMA_BARYON = '+'
    ANTI_POSITIVE_SIGMA_BARYON = '_'
    NEGATIVE_SIGMA_BARYON = '-'
    ANTI_NEGATIVE_SIGMA_BARYON = '~'
    XI_BARYON = 'X'
    ANTI_NEUTRAL_XI_BARYON = 'C'
    NEGATIVE_XI_BARYON = 'Y'
    POSITIVE_XI_BARYON = 'W'
    OMEGA_BARYON = 'O'
    ANTI_OMEGA_BARYON = '@'
    POSITIVE_PION = '/'
    NEGATIVE_PION = '*'
    NEUTRAL_PION = 'Z'
    POSITIVE_KAON = 'K'
    NEGATIVE_KAON = '?'
    KAON_SHORT = '%'
    KAON_LONG = '^'
    DEUTERON = 'D'
    TRITION = 'T'
    HELION = 'S'
    ALPHA = 'A'
    HEAVY_IONS = '#'

class SourceParticleCategory(Enum):
    NEUTRON = 'N'
    ANTI_NEUTRON = 'Q'
    PHOTON = 'P'
    ELECTRON  = 'E'
    POSITRON = 'F'
    NEGATIVE_MUON = '|'
    POSITIVE_MUON = '!'
    ELECTRON_NEUTRINO = 'U'
    ANTI_ELECTRON_NEUTRINO = '<'
    MUON_NEUTRINO = 'V'
    ANTI_MUON_NEUTRINO = '>'
    PROTON = 'H'
    ANTI_PROTON = 'G'
    LAMBDA_BARYON = 'L'
    ANTI_LAMBDA_BARYON = 'B'
    POSITIVE_SIGMA_BARYON = '+'
    ANTI_POSITIVE_SIGMA_BARYON = '_'
    NEGATIVE_SIGMA_BARYON = '-'
    ANTI_NEGATIVE_SIGMA_BARYON = '~'
    XI_BARYON = 'X'
    ANTI_NEUTRAL_XI_BARYON = 'C'
    NEGATIVE_XI_BARYON = 'Y'
    POSITIVE_XI_BARYON = 'W'
    OMEGA_BARYON = 'O'
    ANTI_OMEGA_BARYON = '@'
    POSITIVE_PION = '/'
    NEGATIVE_PION = '*'
    NEUTRAL_PION = 'Z'
    POSITIVE_KAON = 'K'
    NEGATIVE_KAON = '?'
    KAON_SHORT = '%'
    KAON_LONG = '^'
    DEUTERON = 'D'
    TRITION = 'T'
    HELION = 'S'
    ALPHA = 'A'
    HEAVY_IONS = '#'
    COSMIC = 'CR'
    COSMIC_PROTONS = 'C1001'
    COSMIC_ALPHAS = 'C2004'
    BACKGROUND = 'BG'
    BACKGROUND_NEUTRONS = 'BN'
    BACKGROUND_PHOTONS = 'BP'
    SPONTANEOUS_FISSION = 'SF'
    SPONTAENOUS_PHOTON = 'SP'
    COSMIC_NITROGEN = 'C7014'
    COSMIC_SILICON = 'C14028'
    COSMIC_IRON = 'C26056'

class Boolean(Enum):
    ONE = 1
    ZERO = 0
    TRUE = 1
    FALSE = 0