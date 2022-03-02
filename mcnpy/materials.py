from typing import Iterable
from numpy import string_
from .wrap import wrappers, overrides
from .zaid_helper import element_to_zaid, zaid_to_element, library_check

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Material(MaterialBase):

    def _init(self, name, nuclides, comment=None, **kwargs):
        self.name = name
        self.nuclides = nuclides
        self.comment = comment

        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def fraction_unit(self, unit):
        for nuclide in self.nuclides:
            nuclide.unit = unit

class MaterialNuclide(MaterialNuclideBase):

    def _init(self, name, fraction, unit='ATOM', library=None):
        self.name = element_to_zaid(name)
        self.fraction = abs(fraction)
        if fraction < 0:
            self.unit = 'WEIGHT'
        else:
            self.unit = unit
        if library is not None:
            if isinstance(library, Library):
                self.library = library_check(self.name, library)
                #self.library = library
            elif isinstance(library, list) or isinstance(library, tuple):
                self.library = library_check(self.name, Library(library[0], library[1]))
                #self.library = Library(library[0], library[1])
            else:
                self.library = library_check(self.name, Library(library))
                #self.library = Library(library)
            



    def element_name(self):
        return zaid_to_element(self.name)

    def __str__(self):
        #string = 'ZAID = ' + self.name + ', Fraction = ' + str(self.unit) + str(self.fraction)
        string = 'MaterialNuclide ' + zaid_to_element(self.name)

        return string

    def __repr__(self):
        return str(self)

class Library(LibraryBase):

    def _init(self, library, quantity=None):

        if isinstance(library, str):
            try:
                int(library)
                self.library = library
                if quantity is not None:
                    self.quantity = quantity
            except:
                try:
                    int(library[:-1])
                    self.library = library[:-1]
                    self.quantity = library[-1]
                except:
                    self.library = library[:-2]
                    self.quantity = library[-2:]
        else:
            self.library = str(library)
            if quantity is not None:
                self.quantity = quantity

    def __str__(self):
        if self.quantity is not None:
            return self.library + str(self.quantity)
        else:
            return str(self.library)

class Sab(SabBase):

    def _init(self, material, libraries):
        self.material = material
        self.libraries = []
        for lib in libraries:
            if isinstance(lib, SabLibrary):
                self.libraries.append(lib)
            elif isinstance(lib, list) or isinstance(lib, tuple):
                self.libraries.append(SabLibrary(lib[0], lib[1]))
            else:
                self.libraries.append(SabLibrary(lib))

class SabLibrary(SabLibraryBase):

    def _init(self, nuclide, library=None):
        self.nuclide = nuclide
        if library is not None:
            if isinstance(library, Sablib):
                self.library = library
            else:
                self.library = Sablib(library)

class Sablib(SablibBase):

    def _init(self, lib):
        if isinstance(lib, str) is False:
            self.lib = str(lib)
        else:
            if lib[-1].lower() == 't':
                self.lib = lib[:-1]
                self.t = lib[-1]
            else:
                self.lib = lib


for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override