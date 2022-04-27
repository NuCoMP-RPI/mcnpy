from abc import ABC
from mcnpy.wrap import wrappers, overrides
from mcnpy.structures import Point

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class PhysicsSetting(ABC):
    """
    """

class ParticlePhysics(ABC):
    """
    """

class Mode(ModeBase, PhysicsSetting):
    __doc__ = ModeBase().__doc__

    def _init(self, particles):
        self.particles = particles

    def __str__(self):
        return 'MODE: ' + str(self.particles)

    def __repr__(self):
        return str(self)

class VerticalMode(VerticalModeBase, PhysicsSetting):
    """
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class NeutronPhysics(NeutronPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Neutron physics options.
    
    Parameters
    ----------
    emax : float (DEFAULT=100MeV)
    emcnf : float (DEFAULT=0MeV)
    iunr : 0 or 1 (DEFAULT=0)
    colif : float (DEFAULT=0)
    cut : float (DEFAULT=-1)
    ngam : 0, 1, or 2 (DEFAULT=1)
    i_int_model : -1, 0, 1, or 2 (DEFAULT=0)
    i_els_model : -1 or 0 (DEFAULT=0)
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'PHYS:N\n'
        for k in self.PROPERTIES:
            string += '{0: <16}{1}{2}\n'.format('\t'+k, '=\t', getattr(self, k))

        return string

    def __repr__(self):
        return str(self)

class PhotonPhysics(PhotonPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Photon physics options.
    
    Parameters
    ----------
    empf : float (DEFAULT=100MeV)
    ides : 0 or 1 (DEFAULT=0)
    nocoh : 0 or 1 (DEFAULT=0)
    ispn : -1, 0, or 1 (DEFAULT=0)
    nodop : 0 or 1 (DEFAULT=0)
    fism : 0 or 1 (DEFAULT=0)
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'PHYS:P\n'
        for k in self.PROPERTIES:
            string += '{0: <16}{1}{2}\n'.format('\t'+k, '=\t', getattr(self, k))

        return string

    def __repr__(self):
        return str(self)

class ElectronPhysics(ElectronPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Electron physics options.
    
    Parameters
    ----------
    emax : float (DEFAULT=100MeV)
    ides : 0 or 1 (DEFAULT=0)
    iphot : 0 or 1 (DEFAULT=0)
    ibad : 0 or 1 (DEFAULT=0)
    istrg : 0 or 1 (DEFAULT=0)
    bnum : float (DEFAULT=1)
    xnum : float (DEFAULT=1)
    rnok : float (DEFAULT=1)
    enum : float (DEFAULT=1)
    numb : float (DEFAULT=0)
    i_mcs_model : -1 or 0 (DEFAULT=0)
    el_scatt : float (DEFAULT=J)
    efac : float 0.8 to 0.99 (DEFAULT=0.917)
    electron_method_boundary : float (DEFAULT=1.0e-3)
    ckvnum : float (DEFAULT=0)
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'PHYS:E\n'
        for k in self.PROPERTIES:
            string += '{0: <16}{1}{2}\n'.format('\t'+k, '=\t', getattr(self, k))

        return string

    def __repr__(self):
        return str(self)

class ProtonPhysics(ProtonPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Proton physics options.
    
    Parameters
    ----------
    emax : float (DEFAULT=100MeV)
    ean : float (DEFAULT=0)
    tabl : float (DEFAULT=-1)
    istrg : 0 or 1 (DEFAULT=0)
    recl : float (DEFAULT=0)
    i_mcs_model : -1, 0, 1, 2 (DEFAULT=0)
    i_int_model : -1, 0, 1, 2 (DEFAULT=0)
    i_els_model : -1 or 0 (DEFAULT=0)
    efac : float 0.8 to 0.99 (DEFAULT=0.917)
    ckvnum : float (DEFAULT=0)
    drp : float (DEFAULT=0MeV)
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'PHYS:H\n'
        for k in self.PROPERTIES:
            string += '{0: <16}{1}{2}\n'.format('\t'+k, '=\t', getattr(self, k))

        return string

    def __repr__(self):
        return str(self)

class OtherParticlePhysics(OtherParticlePhysicsBase, PhysicsSetting, ParticlePhysics):
    """Other Particle physics options.
    
    Parameters
    ----------
    particle : particle (other than N, P, E, H)
    emax : float (DEFAULT=100MeV)
    istrg : 0 or 1 (DEFAULT=0)
    xmunum : -1 or 1 (DEFAULT=1)
    xmugam : float (DEFAULT=0.65)
    i_mcs_model : -1, 0, 1, 2 (DEFAULT=0)
    i_int_model : -1, 0, 1, 2 (DEFAULT=0)
    i_els_model : -1 or 0 (DEFAULT=0)
    efac : float 0.8 to 0.99 (DEFAULT=0.917)
    ckvnum : float (DEFAULT=0)
    drp : float (DEFAULT=0MeV)
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    def __str__(self):
        string = 'PHYS:' + str(self.particle) + '\n'
        for k in self.PROPERTIES:
            string += '{0: <16}{1}{2}\n'.format('\t'+k, '=\t', getattr(self, k))

        return string

    def __repr__(self):
        return str(self)

class Activation(ActivationBase, PhysicsSetting):
    __doc__ = ActivationBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergyCutoffs(EnergyCutoffsBase, PhysicsSetting):
    __doc__ = EnergyCutoffsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Temperatures(TemperaturesBase, PhysicsSetting):
    __doc__ = TemperaturesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ThermalTimes(ThermalTimesBase, PhysicsSetting):
    __doc__ = ThermalTimesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ModelPhysics(ModelPhysicsBase, PhysicsSetting):
    __doc__ = ModelPhysicsBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Multiplicity(MultiplicityBase, PhysicsSetting):
    __doc__ = MultiplicityBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Transport(TransportBase, PhysicsSetting):
    __doc__ = TransportBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class UncollidedSecondaries(UncollidedSecondariesBase, PhysicsSetting):
    __doc__ = UncollidedSecondariesBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MagneticField(MagneticFieldBase, PhysicsSetting):
    __doc__ = MagneticFieldBase().__doc__
    
    def _init(self, name, type, **kwargs):
        """
        """
        self.name = name
        self.type = type
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    @property
    def name(self):
        return self._e_object.getName()

    @property
    def vector(self):
        _v = self._e_object.getVector()
        return (_v.x, _v.y, _v.z)

    @property
    def axis(self):
        _v = self._e_object.getAxis()
        return (_v.x, _v.y, _v.z) 

    @property
    def fringe_field_surfaces(self):
        if self.type == 'QUADFF':
            return self._e_object.getFringeFieldSurfaces()
        else:
            return None

    @property
    def reference_point(self):
        _v = self._e_object.getReferencePoint()
        return (_v.x, _v.y, _v.z) 

    @name.setter
    def name(self, name):
        if name is not None:
            self._e_object.setName(str(name))

    @vector.setter
    def vector(self, v):
        if isinstance(v, Point):
            self._e_object.setVector(v)
        else:
            self._e_object.setVector(Point(v[0], v[1], v[2]))

    @axis.setter
    def axis(self, v):
        if isinstance(v, Point):
            self._e_object.setAxis(v)
        else:
            self._e_object.setAxis(Point(v[0], v[1], v[2]))

    @fringe_field_surfaces.setter
    def fringe_field_surfaces(self, ffs):
        if self.type == 'QUADFF':
            self._e_object.setFringeFieldSurfaces(ffs)
        else:
            self._e_object.setFringeFieldSurfaces(None)

    @reference_point.setter
    def reference_point(self, v):
        if isinstance(v, Point):
            self._e_object.setReferencePoint(v)
        else:
            self._e_object.setReferencePoint(Point(v[0], v[1], v[2]))

class MagneticFieldAssign(MagneticFieldAssignBase, PhysicsSetting):
    __doc__ = MagneticFieldAssignBase().__doc__
    
    def _init(self, mag_field):
        """
        """
        self.mag_field = mag_field

class PhysModelLCA(PhysModelLCABase, PhysicsSetting):
    __doc__ = PhysModelLCABase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCB(PhysModelLCBBase, PhysicsSetting):
    __doc__ = PhysModelLCBBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCC(PhysModelLCCBase, PhysicsSetting):
    __doc__ = PhysModelLCCBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEA(PhysModelLEABase, PhysicsSetting):
    __doc__ = PhysModelLEABase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEB(PhysModelLEBBase, PhysicsSetting):
    __doc__ = PhysModelLEBBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysicsCutoff(PhysicsCutoffBase, PhysicsSetting):
    __doc__ = PhysicsCutoffBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CosyMap(CosyMapBase, PhysicsSetting):
    __doc__ = CosyMapBase().__doc__
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override