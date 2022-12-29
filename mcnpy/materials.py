from abc import ABC
from .wrap import wrappers, overrides
from .mixin import IDManagerMixin
from metapy.zaid_helper import element_to_zaid, zaid_to_element, library_check

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MaterialSetting(ABC):
    """
    """

class Material(IDManagerMixin, MaterialBase):
    __doc__ = MaterialBase().__doc__

    next_id = 1
    used_ids = set()

    def _init(self, name=None, nuclides=[], unit=None, comment=None, **kwargs):
        try:
            self.name = name
            self.nuclides = nuclides
        except:
            self.name = None
            self.nuclides = name.nuclides(Nuclide)
        if comment is not None:
            self.comment = comment
        self._unit = unit
        self._density = None
        self._density_unit = None
        self._s_alpha_beta = None

        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __add__(self, nuclide):
        #new = Material(self)
        self += nuclide
        return self

    def __iadd__(self, nuclide):
        #if self.unit is None:
        if isinstance(nuclide, list):
            self.nuclides.extend(nuclide)
        elif isinstance(nuclide, Material):
            self.nuclides.extend(nuclide.nuclides)
        else:
            self.nuclides.addUnique(nuclide._e_object)
        """else:
            if isinstance(nuclide, list):
                for i in nuclide:
                    i.unit = self.unit
                    self.nuclides.addUnique(i._e_object)
                self.nuclides.extend(nuclide)
            elif isinstance(nuclide, Material):
                for i in nuclide.nuclides:
                    i.unit = self.unit
                    self.nuclides.addUnique(i._e_object)
            else:
                nuclide.unit = self.unit
                self.nuclides.addUnique(nuclide._e_object)"""
        return self

    def __sub__(self, nuclide):
        new = Material(self)
        new -= nuclide
        return new

    def __isub__(self, nuclide):
        if isinstance(nuclide, list):
            for i in nuclide:
                self.nuclides.remove(i)
        else:
            self.nuclides.remove(nuclide)
        return self

    def __mul__(self, density):
        self.density = density
        self.density_unit = 'G_CM3'
        return self

    def __matmul__(self, density):
        self.density = density
        self.density_unit = 'A_BCM'
        return self

    """@property
    def name(self):
        if self._e_object.getName() is None:
            return None
        else:
            return int(self._e_object.getName())

    @name.setter
    def name(self, name):
        self._e_object.setName(str(name))"""
    
    @property
    def s_alpha_beta(self):
        return self._s_alpha_beta

    @s_alpha_beta.setter
    def s_alpha_beta(self, libraries):
        try:
            self._s_alpha_beta = Sab(self, libraries)
        except:
            self._s_alpha_beta = Sab(self, [libraries])

    @property
    def unit(self):
        if self.nuclides is not None:
            if len(self.nuclides) > 0:
                return self.nuclides[0].unit
        else:
            return self._unit

    @unit.setter
    def unit(self, unit):
        #self.unit = unit
        if self.unit is not None:
            for nuclide in self.nuclides:
                nuclide.unit = unit

    @property
    def density(self):
        """
        """
        return self._density

    @density.setter
    def density(self, density):
        if density is not None:
            self._density = abs(density)
            if density < 0:
                self.density_unit = 'G_CM3'
            else:
                self.density_unit = 'A_BCM'

    @property
    def _alt_densities(self):
        """"""
        return self._stored_density

    @_alt_densities.setter
    def _alt_densities(self):
        """"""

    @property
    def density_unit(self):
        """
        """
        return self._density_unit

    @density_unit.setter
    def density_unit(self, unit):
        self._density_unit = unit

    @property
    def nuclides(self):
        return self._e_object.getNuclides()

    @nuclides.setter
    def nuclides(self, nuclides):
        _nucides = self._e_object.getNuclides()
        del _nucides[:]
        if isinstance(nuclides, (list, tuple)):
            for i in nuclides:
                _nucides.addUnique(i)
        else:
            try:
                for i in nuclides.nuclides():
                    _nucides.addUnique(i)
            except:
                _nucides.addUnique(nuclides)

class Nuclide(NuclideBase):
    __doc__ = NuclideBase().__doc__
    
    def _init(self, name, fraction, unit='ATOM', library=None):
        self.name = name
        self.unit = unit
        self.fraction = fraction
        if library is not None:
            self.library = library

    def __add__(self, other):
        if isinstance(other, list):
            new = Material()
            new.nuclides = [self] + other
        elif isinstance(other, Material):
            other.nuclides.addUnique(self._e_object)
            return other
        else:
            new = Material()
            new.nuclides = [self, other]
        return new

    @property
    def name(self):
        return zaid_to_element(self._e_object.getName())

    @name.setter
    def name(self, name):
        self._e_object.setName(element_to_zaid(name))

    @property
    def library(self):
        return self._e_object.getLibrary()

    @property
    def fraction(self):
        return self._e_object.getFraction()

    @fraction.setter
    def fraction(self, fraction):
        if fraction < 0:
            self.unit = 'WEIGHT'
        self._e_object.setFraction(abs(float(fraction)))

    @library.setter
    def library(self, lib):
        if isinstance(lib, Library):
            self._e_object.setLibrary(library_check(self.name, lib))
        elif isinstance(lib, (list, tuple)):
            self._e_object.setLibrary(library_check(self.name, Library(lib[0], 
                                                                       lib[1])))
        else:
            self._e_object.setLibrary(library_check(self.name, Library(lib)))

    def element_name(self):
        return zaid_to_element(self.name)

    def __str__(self):
        #string = 'ZAID = ' + self.name + ', Fraction = ' + str(self.unit) + str(self.fraction)
        string = 'Nuclide ' + str(self.name)

        return string

    def __repr__(self):
        return str(self)

class Library(LibraryBase):
    __doc__ = LibraryBase().__doc__
    
    def _init(self, library, quantity=None):

        self.library = library
        if quantity is not None:
            self.quantity = quantity

    def __str__(self):
        if self.quantity is not None:
            return self.library + str(self.quantity)
        else:
            return str(self.library)

    @property
    def library(self):
        return self._e_object.getLibrary()

    @library.setter
    def library(self, lib):
        if isinstance(lib, str):
            try:
                int(lib)
                self._e_object.setLibrary(lib)
            except:
                try:
                    int(lib[:-1])
                    self._e_object.setLibrary(lib[:-1])
                    self.quantity = lib[-1]
                except:
                    self._e_object.setLibrary(lib[:-2])
                    self.quantity = lib[-2:]
        else:
            self._e_object.setLibrary(str(lib))

class Sab(SabBase, MaterialSetting):
    __doc__ = SabBase().__doc__
    
    def _init(self, material, libraries):
        self.material = material
        self.libraries = libraries

    @property
    def libraries(self):
        return self._e_object.getLibraries()

    @libraries.setter
    def libraries(self, _libraries):
        libraries = self._e_object.getLibraries()
        for lib in _libraries:
            if isinstance(lib, SabLibrary):
                libraries.append(lib)
            elif isinstance(lib, (list, tuple)):
                libraries.append(SabLibrary(lib[0], lib[1]))
            else:
                libraries.append(SabLibrary(lib))

    @property
    def material(self):
        return self._e_object.getMaterial()

    @material.setter
    def material(self, material):
        self._e_object.setMaterial(material._e_object)
        material._s_alpha_beta = self

class SabLibrary(SabLibraryBase):
    __doc__ = SabLibraryBase().__doc__
    
    def _init(self, nuclide, library=None):
        self.nuclide = nuclide
        if library is not None:
            self.library = library

    @property
    def library(self):
        return self._e_object.getLibrary()

    @library.setter
    def library(self, lib):
        if isinstance(lib, Sablib):
            self._e_object.setLibrary(lib)
        else:
            self._e_object.setLibrary(Sablib(lib))

class Sablib(SablibBase):
    __doc__ = SablibBase().__doc__
    
    def _init(self, lib):
        self.lib = lib

    @property
    def lib(self):
        if self.t is not None:
            return self._e_object.getLib() + 't'
        else:
            return self._e_object.getLib()

    @lib.setter
    def lib(self, _lib):
        if isinstance(_lib, str) is False:
            self._e_object.setLib(str(_lib))
        else:
            if _lib[-1].lower() == 't':
                self._e_object.setLib(_lib[:-1])
                self.t = _lib[-1]
            else:
                self._e_object.setLib(_lib)

class NuclideSubstitution(NuclideSubstitutionBase, MaterialSetting):
    __doc__ = NuclideSubstitutionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhotonuclearNuclideSelection(PhotonuclearNuclideSelectionBase, MaterialSetting):
    __doc__ = PhotonuclearNuclideSelectionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class OnTheFlyDopplerBroadening(OnTheFlyDopplerBroadeningBase, MaterialSetting):
    __doc__ = OnTheFlyDopplerBroadeningBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TotalFission(TotalFissionBase, MaterialSetting):
    __doc__ = TotalFissionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FissionTurnoff(FissionTurnoffBase, MaterialSetting):
    __doc__ = FissionTurnoffBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class AtomicWeight(AtomicWeightBase, MaterialSetting):
    __doc__ = AtomicWeightBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CrossSectionFile(CrossSectionFileBase, MaterialSetting):
    __doc__ = CrossSectionFileBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Void(VoidBase, MaterialSetting):
    __doc__ = VoidBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MultigroupTransport(MultigroupTransportBase, MaterialSetting):
    __doc__ = MultigroupTransportBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DiscreteReactionCrossSection(DiscreteReactionCrossSectionBase, MaterialSetting):
    __doc__ = DiscreteReactionCrossSectionBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override