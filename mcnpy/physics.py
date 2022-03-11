from abc import ABC
from mcnpy.wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class PhysicsSetting(ABC):
    """
    """

class ParticlePhysics(ABC):
    """
    """

class Mode(ModeBase, PhysicsSetting):
    """Set particle physics modes.

    PARAMETERS
    ----------
    particles : list<particle>
    """

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
    
    PARAMETERS
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

    """PROPERTIES = ['max_energy',
               'max_analog',
               'unresolved_resonance',
               'recoil',
               'phys_cutoff',
               'photon_prod',
               'interaction',
               'els_scattering']"""

    """def _init(self, emax=100, emcnf=0, iunr=0, colif=0, cut=-1, 
              ngam=1, i_int_model=0, i_els_model=0):
        self.max_energy = emax
        self.max_analog = emcnf
        self.unresolved_resonance = iunr
        self.recoil = colif
        self.phys_cutoff = cut
        self.photon_prod = ngam
        self.interaction = i_int_model
        self.els_scattering = i_els_model"""
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

    # Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    """def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""


class PhotonPhysics(PhotonPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Photon physics options.
    
    PARAMETERS
    ----------
    empf : float (DEFAULT=100MeV)
    ides : 0 or 1 (DEFAULT=0)
    nocoh : 0 or 1 (DEFAULT=0)
    ispn : -1, 0, or 1 (DEFAULT=0)
    nodop : 0 or 1 (DEFAULT=0)
    fism : 0 or 1 (DEFAULT=0)
    """

    PROPERTIES = ['max_energy',
               'particle_prod',
               'coh_scattering',
               'photonuclear',
               'doppler',
               'photofission']

    """def _init(self, empf=100, ides=0, nocoh=0, ispn=0, nodop=0, fism=0):
        
        self.max_energy = empf
        self.particle_prod = ides
        self.coh_scattering = nocoh
        self.photonuclear = ispn
        self.doppler = nodop
        self.photofission = fism"""
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

    # Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    """def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""

        

class ElectronPhysics(ElectronPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Electron physics options.
    
    PARAMETERS
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

    """PROPERTIES = ['max_energy',
                  'prod_by_photons',
                  'photon_prod',
                  'brem_dist',
                  'straggling',
                  'brem_mult',
                  'xray_mult',
                  'knock_on',
                  'electron_mult',
                  'brem_prod',
                  'clmb_scattering',
                  'els_scattering',
                  'stopping_power',
                  'single_event_energy',
                  'cerenkov']"""

    """def _init(self, emax=100, ides=0, iphot=0, ibad=0, istrg=0, bnum=1,
              xnum=1, rnok=1, enum=1, numb=0, i_mcs_model=0, el_scatt='J',
              efac=0.917, electron_method_boundary=1.0e-3, ckvnum=0):

        self.max_energy = emax
        self.prod_by_photons = ides
        self.photon_prod = iphot
        self.brem_dist = ibad
        self.straggling = istrg
        self.brem_mult = bnum
        self.xray_mult = xnum
        self.knock_on = rnok
        self.electron_multiplier = enum
        self.brem_prod = numb
        self.clmb_scattering = i_mcs_model
        self.els_scattering = el_scatt
        self.stopping_power = efac
        self.single_event_energy = electron_method_boundary
        self.cerenkov = ckvnum"""

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

    # Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    """def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""


class ProtonPhysics(ProtonPhysicsBase, PhysicsSetting, ParticlePhysics):
    """Proton physics options.
    
    PARAMETERS
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

    """PROPERTIES = ['max_energy',
                  'max_analog',
                  'phys_cutoff',
                  'straggling',
                  'recoil',
                  'clmb_scattering',
                  'interaction',
                  'els_scattering',
                  'stopping_power',
                  'single_event_energy',
                  'cerenkov',
                  'delta_ray_cutoff']"""

    """def _init(self, emax=100, ean=0, tabl=-1, istrg=0, recl=0, 
              i_mcs_model=0, i_int_model=0, i_els_model=0, efac=0.917, ckvnum=0, 
              drp=0):

        self.max_energy = emax
        self.max_analog = ean
        self.phys_cutoff = tabl
        self.straggling = istrg
        self.recoil = recl
        self.clmb_scattering = i_mcs_model
        self.interaction = i_int_model
        self.els_scattering = i_els_model
        self.stopping_power = efac
        self.cerenkov = ckvnum
        self.delta_ray_cutoff = drp
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

    # Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    """def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""


class OtherParticlePhysics(OtherParticlePhysicsBase, PhysicsSetting, ParticlePhysics):
    """Other Particle physics options.
    
    PARAMETERS
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

    """PROPERTIES = ['max_energy',
                  'straggling',
                  'muon_xrays',
                  'k_shell_photon',
                  'clmb_scattering',
                  'interaction',
                  'els_scattering',
                  'stopping_power',
                  'cerenkov',
                  'delta_ray_cutoff']"""

    """def _init(self, particle, emax=100, istrg=0, 
              xmunum=-1, xmugam=0.65, i_mcs_model=0, 
              i_int_model=0, i_els_model=0, efac=0.917, 
              ckvnum=0, drp=0):

        self.particle = particle
        self.max_energy = emax
        self.straggling = istrg
        self.muon_xrays = xmunum
        self.k_shell_photon = xmugam
        self.clmb_scattering = i_mcs_model
        self.interaction = i_int_model
        self.els_scattering = i_els_model
        self.stopping_power = efac
        self.cerenkov = ckvnum
        self.delta_ray_cutoff = drp"""

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

    # Applies defaults to avoid serializing nulls.
    # Automatically called when adding card to deck.
    """def _defaults(self):
        entry = len(self.PROPERTIES)-1
        for k in self.PROPERTIES:
            if getattr(self, k) is None:
                setattr(self, k, 'J')
            else:
                entry = self.PROPERTIES.index(k)
        # Avoid printing all options if possible
        if entry != len(self.PROPERTIES)-1:
            for k in self.PROPERTIES[entry+1:]:
                setattr(self, k, None)"""


class Activation(ActivationBase, PhysicsSetting):
    """ACT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergyCutoffs(EnergyCutoffsBase, PhysicsSetting):
    """ELPT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Temperatures(TemperaturesBase, PhysicsSetting):
    """TMP
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ThermalTimes(ThermalTimesBase, PhysicsSetting):
    """THTME
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ModelPhysics(ModelPhysicsBase, PhysicsSetting):
    """MPHYS
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Multiplicity(MultiplicityBase, PhysicsSetting):
    """FMULT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Transport(TransportBase, PhysicsSetting):
    """TROPT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class UncollidedSecondaries(UncollidedSecondariesBase, PhysicsSetting):
    """UNC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MagneticField(MagneticFieldBase, PhysicsSetting):
    """BFLD
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MagneticFieldAssign(MagneticFieldAssignBase, PhysicsSetting):
    """BFLCL
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCA(PhysModelLCABase, PhysicsSetting):
    """LCA
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCB(PhysModelLCBBase, PhysicsSetting):
    """LCB
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCC(PhysModelLCCBase, PhysicsSetting):
    """LCC
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEA(PhysModelLEABase, PhysicsSetting):
    """LEA
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEB(PhysModelLEBBase, PhysicsSetting):
    """LEB
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysicsCutoff(PhysicsCutoffBase, PhysicsSetting):
    """CUT
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CosyMap(CosyMapBase, PhysicsSetting):
    """COSYP
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