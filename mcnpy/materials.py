from abc import ABC
from .wrap import wrappers, overrides
from .mixin import IDManagerMixin
from metapy.zaid_helper import element_to_zaid, zaid_to_element, library_check

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class MaterialSetting(ABC):
    """
    """

class Material(IDManagerMixin, MaterialBase):
    """
    A representation of the model object `Material`.
    
    Parameters
    ----------
    name : int
        Name for `Material`.
    nuclides : iterable of mcnpy.Nuclide
        Nuclides for `Material`.
    gas : int
        Gas for `Material`.
    electron_substep_count : int
        ElectronSubstepCount for `Material`.
    heavy_ion_substep_count : int
        HeavyIonSubstepCount for `Material`.
    neutron_library : mcnpy.Library
        NeutronLibrary for `Material`.
    photoatomic_library : mcnpy.Library
        PhotoatomicLibrary for `Material`.
    photonuclear_library : mcnpy.Library
        PhotonuclearLibrary for `Material`.
    electron_library : mcnpy.Library
        ElectronLibrary for `Material`.
    proton_library : mcnpy.Library
        ProtonLibrary for `Material`.
    conductor : float
        Conductor for `Material`.
    a : float
        A for `Material`.
    b : float
        B for `Material`.
    c : float
        C for `Material`.
    d : float
        D for `Material`.
    b1 : float
        B1 for `Material`.
    c1 : float
        C1 for `Material`.
    b2 : float
        B2 for `Material`.
    c2 : float
        C2 for `Material`.
    b3 : float
        B3 for `Material`.
    c3 : float
        C3 for `Material`.
    comment : str
        Comment for `Material`.
    
    """

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
    """
    A representation of the model object `Nuclide`.
    
    Parameters
    ----------
    name : int
        Name for `Nuclide`.
    library : mcnpy.Library
        Library for `Nuclide`.
    unit : mcnpy.FractionUnit
        Unit for `Nuclide`.
    fraction : float
        Fraction for `Nuclide`.
    
    """
    
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
    """
    A representation of the model object `Library`.
    
    Parameters
    ----------
    
    """
    
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
    """
    A representation of the model object `Sab`.
    
    Parameters
    ----------
    material : mcnpy.Material
        Material for `Sab`.
    libraries : iterable of mcnpy.SabLibrary
        Libraries for `Sab`.
    
    """
    
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
    """
    A representation of the model object `SabLibrary`.
    
    Parameters
    ----------
    nuclide : mcnpy.SabNuclide
        Nuclide for `SabLibrary`.
    library : mcnpy.Sablib
        Library for `SabLibrary`.
    
    """
    
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
    """
    A representation of the model object `Sablib`.
    
    Parameters
    ----------
    lib : str
        Lib for `Sablib`.
    t : str
        T for `Sablib`.
    
    """
    
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
    """
    A representation of the model object `NuclideSubstitution`.
    
    Parameters
    ----------
    material : mcnpy.Material
        Material for `NuclideSubstitution`.
    nuclides : iterable of str
        Nuclides for `NuclideSubstitution`.
    particles : iterable of mcnpy.Particle
        Particles for `NuclideSubstitution`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhotonuclearNuclideSelection(PhotonuclearNuclideSelectionBase, MaterialSetting):
    """
    A representation of the model object `PhotonuclearNuclideSelection`.
    
    Parameters
    ----------
    material : mcnpy.Material
        Material for `PhotonuclearNuclideSelection`.
    zaids : iterable of str
        Zaids for `PhotonuclearNuclideSelection`.
    particles : iterable of mcnpy.Particle
        Particles for `PhotonuclearNuclideSelection`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class OnTheFlyDopplerBroadening(OnTheFlyDopplerBroadeningBase, MaterialSetting):
    """
    A representation of the model object `OnTheFlyDopplerBroadening`.
    
    Parameters
    ----------
    zaids : iterable of str
        Zaids for `OnTheFlyDopplerBroadening`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TotalFission(TotalFissionBase, MaterialSetting):
    """
    A representation of the model object `TotalFission`.
    
    Parameters
    ----------
    prompt_only : mcnpy.Boolean
        PromptOnly for `TotalFission`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class FissionTurnoff(FissionTurnoffBase, MaterialSetting):
    """
    A representation of the model object `FissionTurnoff`.
    
    Parameters
    ----------
    options : iterable of str
        Options for `FissionTurnoff`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class AtomicWeight(AtomicWeightBase, MaterialSetting):
    """
    A representation of the model object `AtomicWeight`.
    
    Parameters
    ----------
    nuclides : iterable of str
        Nuclides for `AtomicWeight`.
    library : iterable of mcnpy.Library
        Library for `AtomicWeight`.
    ratios : iterable of float
        Ratios for `AtomicWeight`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CrossSectionFile(CrossSectionFileBase, MaterialSetting):
    """
    A representation of the model object `CrossSectionFile`.
    
    Parameters
    ----------
    name : int
        Name for `CrossSectionFile`.
    nuclides : mcnpy.Nuclide
        Nuclides for `CrossSectionFile`.
    x_s_file : str
        XSFile for `CrossSectionFile`.
    entries : iterable of float
        Entries for `CrossSectionFile`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Void(VoidBase, MaterialSetting):
    """
    A representation of the model object `Void`.
    
    Parameters
    ----------
    cells : iterable of mcnpy.Cell
        Cells for `Void`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MultigroupTransport(MultigroupTransportBase, MaterialSetting):
    """
    A representation of the model object `MultigroupTransport`.
    
    Parameters
    ----------
    mode : mcnpy.MultigroupTransportMode
        Mode for `MultigroupTransport`.
    combined_electron_photon_xsecs : str
        CombinedElectronPhotonXsecs for `MultigroupTransport`.
    energy_group_count : int
        EnergyGroupCount for `MultigroupTransport`.
    importances : str
        Importances for `MultigroupTransport`.
    adjoint_biasing : str
        AdjointBiasing for `MultigroupTransport`.
    reference_cell : mcnpy.Cell
        ReferenceCell for `MultigroupTransport`.
    weight_window_normalization : float
        WeightWindowNormalization for `MultigroupTransport`.
    compression_limit : str
        CompressionLimit for `MultigroupTransport`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DiscreteReactionCrossSection(DiscreteReactionCrossSectionBase, MaterialSetting):
    """
    A representation of the model object `DiscreteReactionCrossSection`.
    
    Parameters
    ----------
    nuclides : iterable of str
        Nuclides for `DiscreteReactionCrossSection`.
    library : iterable of mcnpy.Library
        Library for `DiscreteReactionCrossSection`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override