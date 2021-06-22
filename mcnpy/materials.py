from .wrap import wrappers, overrides
from .zaid_helper import element_to_zaid, zaid_to_element

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Material(MaterialBase):

    def _init(self, name, nuclides, comment=None):
        self.name = name
        self.nuclides = nuclides
        self.comment = comment

class MaterialNuclide(MaterialNuclideBase):

    def _init(self, name, fraction, unit='ATOM'):
        self.name = element_to_zaid(name)
        self.fraction = fraction
        self.unit = unit

    def __str__(self):
        #string = 'ZAID = ' + self.name + ', Fraction = ' + str(self.unit) + str(self.fraction)
        string = 'MaterialNuclide ' + zaid_to_element(self.name)

        return string

    def __repr__(self):
        return str(self)

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override