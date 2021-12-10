from mcnpy import MaterialNuclide as Nuclide
from mcnpy import Material

class LWTR_Moderator():
    """Stainless steel cladding from RPI's RCF.
    """
    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment
        self.nuclides = [Nuclide(name='h1', fraction=0.666667), 
            Nuclide(name='o16', fraction=0.333333)]
        self.density = 0.998113
        self.density_unit = '-'
        self.material = Material(name=self.name, nuclides=self.nuclides, comment=self.comment)

class RCF_Cladding():
    """Stainless steel cladding from RPI's RCF.
    """
    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment
        self.nuclides = [Nuclide(name='fe54', fraction=0.041105547, unit='-'), 
            Nuclide(name='fe56', fraction=0.64526918, unit='-'),
            Nuclide(name='fe57', fraction=0.014902079, unit='-'),
            Nuclide(name='fe58', fraction=0.001983193, unit='-'),
            Nuclide(name='cr50', fraction=0.0080817, unit='-'),
            Nuclide(name='cr52', fraction=0.15584754, unit='-'),
            Nuclide(name='cr53', fraction=0.01767186, unit='-'),
            Nuclide(name='cr54', fraction=0.0043989, unit='-'),
            Nuclide(name='ni58', fraction=0.065081612, unit='-'),
            Nuclide(name='ni60', fraction=0.025069188, unit='-'),
            Nuclide(name='ni61', fraction=0.00108984, unit='-'),
            Nuclide(name='ni62', fraction=0.003474104, unit='-'),
            Nuclide(name='ni64', fraction=0.000885256, unit='-'),
            Nuclide(name='mn55', fraction=0.0106, unit='-'),
            Nuclide(name='mo92', fraction=0.0002968, unit='-'),
            Nuclide(name='mo94', fraction=0.000185, unit='-'),
            Nuclide(name='mo95', fraction=0.0003184, unit='-'),
            Nuclide(name='mo96', fraction=0.0003336, unit='-'),
            Nuclide(name='mo97', fraction=0.000191, unit='-'),
            Nuclide(name='mo98', fraction=0.0004826, unit='-'),
            Nuclide(name='mo100', fraction=0.0001926, unit='-'),
            Nuclide(name='cu63', fraction=0.00117589, unit='-'), 
            Nuclide(name='cu65', fraction=0.00052411, unit='-'),
            Nuclide(name='co59', fraction=0.00084, unit='-')]
        self.density = 8.0
        self.density_unit = '-'
        self.material = Material(name=self.name, nuclides=self.nuclides, comment=self.comment)

class Human():
    """Homogenized material equivalent to an average human male.
    """
    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment
        self.nuclides = [Nuclide(name='O16', fraction=6.1358e-1, unit='-'),
            Nuclide(name='C', fraction=2.2831e-1, unit='-'),
            Nuclide(name='H1', fraction=9.9885e-2, unit='-'),
            Nuclide(name='N14', fraction=2.5685e-2, unit='-'),
            Nuclide(name='Ca', fraction=1.4269e-2, unit='-'),
            Nuclide(name='P31', fraction=1.1130e-2, unit='-'),
            Nuclide(name='S', fraction=1.9977e-3, unit='-'),
            Nuclide(name='K', fraction=1.9977e-3, unit='-'),
            Nuclide(name='Na23', fraction=1.4269e-3, unit='-'),
            Nuclide(name='Cl', fraction=1.3556e-3, unit='-'),
            Nuclide(name='Mg', fraction=2.7112e-4, unit='-'),
            Nuclide(name='Fe56', fraction=5.9931e-5, unit='-'),
            Nuclide(name='Zn', fraction=3.2819e-5, unit='-'),
            Nuclide(name='Cu', fraction=1.0274e-6, unit='-'),
            Nuclide(name='I127', fraction=1.8550e-7, unit='-'),
            Nuclide(name='Mn55', fraction=1.7123e-7, unit='-')]
        self.density = 1.068502
        self.density_unit = '-'
        self.material = Material(name=self.name, nuclides=self.nuclides, comment=self.comment)