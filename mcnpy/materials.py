from abc import ABC
from .wrap import wrappers, overrides
from .zaid_helper import element_to_zaid, zaid_to_element, library_check

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MaterialSetting(ABC):
    """
    """

class Material(MaterialBase):
    __doc__ = MaterialBase().__doc__

    def _init(self, name, nuclides, comment=None, **kwargs):
        self.name = name
        self.nuclides = nuclides
        if comment is not None:
            self.comment = comment

        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def fraction_unit(self, unit):
        for nuclide in self.nuclides:
            nuclide.unit = unit

class MaterialNuclide(MaterialNuclideBase):
    __doc__ = MaterialNuclideBase().__doc__
    
    def _init(self, name, fraction, unit='ATOM', library=None):
        self.name = element_to_zaid(name)
        self.fraction = abs(fraction)
        if fraction < 0:
            self.unit = 'WEIGHT'
        else:
            self.unit = unit
        if library is not None:
            self.library = library

    @property
    def library(self):
        return self._e_object.getLibrary()

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
        string = 'MaterialNuclide ' + zaid_to_element(self.name)

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