from abc import ABC
from mcnpy.wrap import wrappers, overrides
from .points import Point

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class PhysicsSetting(ABC):
    """
    """

class ParticlePhysics(ABC):
    """
    """

class Mode(ModeBase, PhysicsSetting):
    """
    A representation of the model object `Mode`.
    
    Parameters
    ----------
    particles : iterable of mcnpy.Particle
        Particles for `Mode`.
    
    """

    def _init(self, particles):
        self.particles = particles

    def __str__(self):
        return 'MODE: ' + str(self.particles)

    def __repr__(self):
        return str(self)

class NeutronPhysics(NeutronPhysicsBase, PhysicsSetting, ParticlePhysics):
    """
    A representation of the model object `NeutronPhysics`.
    
    Parameters
    ----------
    max_analog : float
        MaxAnalog for `NeutronPhysics`.
    j_max_analog : str
        J_maxAnalog for `NeutronPhysics`.
    unresolved_resonance : int
        UnresolvedResonance for `NeutronPhysics`.
    j_unresolved_resonance : str
        J_unresolvedResonance for `NeutronPhysics`.
    recoil : float
        Recoil for `NeutronPhysics`.
    j_recoil : str
        J_recoil for `NeutronPhysics`.
    phys_cutoff : float
        PhysCutoff for `NeutronPhysics`.
    j_phys_cutoff : str
        J_physCutoff for `NeutronPhysics`.
    photon_prod : int
        PhotonProd for `NeutronPhysics`.
    j_photon_prod : str
        J_photonProd for `NeutronPhysics`.
    interaction : int
        Interaction for `NeutronPhysics`.
    j_interaction : str
        J_interaction for `NeutronPhysics`.
    els_scattering : int
        ElsScattering for `NeutronPhysics`.
    j_els_scattering : str
        J_elsScattering for `NeutronPhysics`.
    
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
    """
    A representation of the model object `PhotonPhysics`.
    
    Parameters
    ----------
    particle_prod : int
        ParticleProd for `PhotonPhysics`.
    j_particle_prod : str
        J_particleProd for `PhotonPhysics`.
    coh_scattering : int
        CohScattering for `PhotonPhysics`.
    j_coh_scattering : str
        J_cohScattering for `PhotonPhysics`.
    photonuclear : int
        Photonuclear for `PhotonPhysics`.
    j_photonuclear : str
        J_photonuclear for `PhotonPhysics`.
    doppler : int
        Doppler for `PhotonPhysics`.
    j_doppler : str
        J_doppler for `PhotonPhysics`.
    photofission : int
        Photofission for `PhotonPhysics`.
    j_photofission : str
        J_photofission for `PhotonPhysics`.
    
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
    """
    A representation of the model object `ElectronPhysics`.
    
    Parameters
    ----------
    prod_by_photons : int
        ProdByPhotons for `ElectronPhysics`.
    photon_prod : int
        PhotonProd for `ElectronPhysics`.
    brem_dist : int
        BremDist for `ElectronPhysics`.
    straggling : int
        Straggling for `ElectronPhysics`.
    brem_mult : float
        BremMult for `ElectronPhysics`.
    xray_mult : float
        XrayMult for `ElectronPhysics`.
    knock_on : float
        KnockOn for `ElectronPhysics`.
    electron_mult : float
        ElectronMult for `ElectronPhysics`.
    brem_prod : float
        BremProd for `ElectronPhysics`.
    clmb_scattering : int
        ClmbScattering for `ElectronPhysics`.
    els_scattering : str
        ElsScattering for `ElectronPhysics`.
    stopping_power : float
        StoppingPower for `ElectronPhysics`.
    single_event_energy : float
        SingleEventEnergy for `ElectronPhysics`.
    cerenkov : float
        Cerenkov for `ElectronPhysics`.
    j_prod_by_photons : str
        J_prodByPhotons for `ElectronPhysics`.
    j_photon_prod : str
        J_photonProd for `ElectronPhysics`.
    j_brem_dist : str
        J_bremDist for `ElectronPhysics`.
    j_straggling : str
        J_straggling for `ElectronPhysics`.
    j_brem_mult : str
        J_bremMult for `ElectronPhysics`.
    j_xray_mult : str
        J_xrayMult for `ElectronPhysics`.
    j_knock_on : str
        J_knockOn for `ElectronPhysics`.
    j_electron_mult : str
        J_electronMult for `ElectronPhysics`.
    j_brem_prod : str
        J_bremProd for `ElectronPhysics`.
    j_clm_scattering : str
        J_clmScattering for `ElectronPhysics`.
    j_stopping_power : str
        J_stoppingPower for `ElectronPhysics`.
    j_single_event_energy : str
        J_singleEventEnergy for `ElectronPhysics`.
    j_cerenkov : str
        J_cerenkov for `ElectronPhysics`.
    
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
    """
    A representation of the model object `ProtonPhysics`.
    
    Parameters
    ----------
    max_analog : float
        MaxAnalog for `ProtonPhysics`.
    phys_cutoff : float
        PhysCutoff for `ProtonPhysics`.
    straggling : int
        Straggling for `ProtonPhysics`.
    recoil : float
        Recoil for `ProtonPhysics`.
    clmb_scattering : int
        ClmbScattering for `ProtonPhysics`.
    interaction : int
        Interaction for `ProtonPhysics`.
    els_scattering : int
        ElsScattering for `ProtonPhysics`.
    stopping_power : float
        StoppingPower for `ProtonPhysics`.
    cerenkov : float
        Cerenkov for `ProtonPhysics`.
    delta_ray_cutoff : float
        DeltaRayCutoff for `ProtonPhysics`.
    j_max_analog : str
        J_maxAnalog for `ProtonPhysics`.
    j_phys_cutoff : str
        J_physCutoff for `ProtonPhysics`.
    j_straggling : str
        J_straggling for `ProtonPhysics`.
    j_recoil : str
        J_recoil for `ProtonPhysics`.
    j_clmb_scattering : str
        J_clmbScattering for `ProtonPhysics`.
    j_interaction : str
        J_interaction for `ProtonPhysics`.
    j_els_scattering : str
        J_elsScattering for `ProtonPhysics`.
    j_stopping_power : str
        J_stoppingPower for `ProtonPhysics`.
    j_cerenkov : str
        J_cerenkov for `ProtonPhysics`.
    j_delta_ray_cutoff : str
        J_deltaRayCutoff for `ProtonPhysics`.
    
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
    """
    A representation of the model object `OtherParticlePhysics`.
    
    Parameters
    ----------
    particle : mcnpy.Particle
        Particle for `OtherParticlePhysics`.
    straggling : int
        Straggling for `OtherParticlePhysics`.
    muon_xrays : int
        MuonXrays for `OtherParticlePhysics`.
    k_shell_photon : float
        KShellPhoton for `OtherParticlePhysics`.
    clmb_scattering : int
        ClmbScattering for `OtherParticlePhysics`.
    interaction : int
        Interaction for `OtherParticlePhysics`.
    els_scattering : int
        ElsScattering for `OtherParticlePhysics`.
    stopping_power : float
        StoppingPower for `OtherParticlePhysics`.
    cerenkov : float
        Cerenkov for `OtherParticlePhysics`.
    delta_ray_cutoff : float
        DeltaRayCutoff for `OtherParticlePhysics`.
    j_straggling : str
        J_straggling for `OtherParticlePhysics`.
    j_muon_xrays : str
        J_muonXrays for `OtherParticlePhysics`.
    j_k_shell_photon : str
        J_kShellPhoton for `OtherParticlePhysics`.
    j_clmb_scattering : str
        J_clmbScattering for `OtherParticlePhysics`.
    j_interaction : str
        J_interaction for `OtherParticlePhysics`.
    j_els_scattering : str
        J_elsScattering for `OtherParticlePhysics`.
    j_stopping_power : str
        J_stoppingPower for `OtherParticlePhysics`.
    j_cerenkov : str
        J_cerenkov for `OtherParticlePhysics`.
    j_delta_ray_cutoff : str
        J_deltaRayCutoff for `OtherParticlePhysics`.
    
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
    """
    A representation of the model object `Activation`.
    
    Parameters
    ----------
    delayed_particles_from_fission : mcnpy.DelayedParticles
        DelayedParticlesFromFission for `Activation`.
    delayed_particles_from_non_fission : mcnpy.DelayedParticles
        DelayedParticlesFromNonFission for `Activation`.
    delayed_neutron_data : mcnpy.ActivationDelayedNeutronData
        DelayedNeutronData for `Activation`.
    delayed_gamma_data : mcnpy.ActivationDelayedGammaData
        DelayedGammaData for `Activation`.
    gamma_line_threshold : float
        GammaLineThreshold for `Activation`.
    delayed_neutron_production : float
        DelayedNeutronProduction for `Activation`.
    product_distribution_count : int
        ProductDistributionCount for `Activation`.
    weight : float
        Weight for `Activation`.
    energy : float
        Energy for `Activation`.
    delayed_gamma_cutoff : float
        DelayedGammaCutoff for `Activation`.
    spontaneous_decay_half_life_threshold : float
        SpontaneousDecayHalfLifeThreshold for `Activation`.
    flag_correlated_uncorrelated : mcnpy.CorrUncorr
        FlagCorrelatedUncorrelated for `Activation`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergyCutoffs(EnergyCutoffsBase, PhysicsSetting):
    """
    A representation of the model object `EnergyCutoffs`.
    
    Parameters
    ----------
    particles : iterable of mcnpy.Particle
        Particles for `EnergyCutoffs`.
    min_energies : iterable of float
        MinEnergies for `EnergyCutoffs`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Temperatures(TemperaturesBase, PhysicsSetting):
    """
    A representation of the model object `Temperatures`.
    
    Parameters
    ----------
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ThermalTimes(ThermalTimesBase, PhysicsSetting):
    """
    A representation of the model object `ThermalTimes`.
    
    Parameters
    ----------
    times : iterable of float
        Times for `ThermalTimes`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class ModelPhysics(ModelPhysicsBase, PhysicsSetting):
    """
    A representation of the model object `ModelPhysics`.
    
    Parameters
    ----------
    enabled : mcnpy.EBoolean
        Enabled for `ModelPhysics`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Multiplicity(MultiplicityBase, PhysicsSetting):
    """
    A representation of the model object `Multiplicity`.
    
    Parameters
    ----------
    nuclide : str
        Nuclide for `Multiplicity`.
    nu_distribution : iterable of float
        NuDistribution for `Multiplicity`.
    gaussian_width : float
        GaussianWidth for `Multiplicity`.
    spontaneous_fission_yield : float
        SpontaneousFissionYield for `Multiplicity`.
    watt_a : float
        WattA for `Multiplicity`.
    watt_b : float
        WattB for `Multiplicity`.
    gaussian_sampling : str
        GaussianSampling for `Multiplicity`.
    data : str
        Data for `Multiplicity`.
    nu_shift : int
        NuShift for `Multiplicity`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Transport(TransportBase, PhysicsSetting):
    """
    A representation of the model object `Transport`.
    
    Parameters
    ----------
    multiple_coulomb_scattering : mcnpy.TransportMultipleCoulombScattering
        MultipleCoulombScattering for `Transport`.
    energy_loss : mcnpy.TransportEnergyLoss
        EnergyLoss for `Transport`.
    reactions : mcnpy.TransportNuclearReactions
        Reactions for `Transport`.
    elastic_scattering : mcnpy.TransportNuclearElasticScattering
        ElasticScattering for `Transport`.
    genxs_file : str
        GenxsFile for `Transport`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class UncollidedSecondaries(UncollidedSecondariesBase, PhysicsSetting):
    """
    A representation of the model object `UncollidedSecondaries`.
    
    Parameters
    ----------
    uncollided : iterable of int
        Uncollided for `UncollidedSecondaries`.
    particles : iterable of mcnpy.Particle
        Particles for `UncollidedSecondaries`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class MagneticField(MagneticFieldBase, PhysicsSetting):
    """
    A representation of the model object `MagneticField`.
    
    Parameters
    ----------
    name : int
        Name for `MagneticField`.
    type : mcnpy.MagneticFieldType
        Type for `MagneticField`.
    strength : float
        Strength for `MagneticField`.
    vector : mcnpy.Point
        Vector for `MagneticField`.
    max_deflection_per_step : float
        MaxDeflectionPerStep for `MagneticField`.
    max_step_size : float
        MaxStepSize for `MagneticField`.
    axis : mcnpy.Point
        Axis for `MagneticField`.
    fringe_field_surfaces : iterable of mcnpy.Surface
        FringeFieldSurfaces for `MagneticField`.
    reference_point : mcnpy.Point
        ReferencePoint for `MagneticField`.
    
    """
    
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
    """
    A representation of the model object `MagneticFieldAssign`.
    
    Parameters
    ----------
    mag_field : iterable of mcnpy.MagneticField
        MagField for `MagneticFieldAssign`.
    
    """
    
    def _init(self, mag_field):
        """
        """
        self.mag_field = mag_field

class PhysModelLCA(PhysModelLCABase, PhysicsSetting):
    """
    A representation of the model object `PhysModelLCA`.
    
    Parameters
    ----------
    els_scattering : int
        ElsScattering for `PhysModelLCA`.
    pre_eq_model : int
        PreEqModel for `PhysModelLCA`.
    model_choice : int
        ModelChoice for `PhysModelLCA`.
    intranuclear_cascade : int
        IntranuclearCascade for `PhysModelLCA`.
    clmb_barrier : int
        ClmbBarrier for `PhysModelLCA`.
    excitation_energy : int
        ExcitationEnergy for `PhysModelLCA`.
    cutoff : int
        Cutoff for `PhysModelLCA`.
    part_transport : int
        PartTransport for `PhysModelLCA`.
    alt_phys : int
        AltPhys for `PhysModelLCA`.
    light_ion : int
        LightIon for `PhysModelLCA`.
    evaporation : int
        Evaporation for `PhysModelLCA`.
    j_els_scattering : str
        J_elsScattering for `PhysModelLCA`.
    j_pre_eq_model : str
        J_preEqModel for `PhysModelLCA`.
    j_model_choice : str
        J_modelChoice for `PhysModelLCA`.
    j_intranuclear_cascade : str
        J_intranuclearCascade for `PhysModelLCA`.
    j_clmb_barrier : str
        J_clmbBarrier for `PhysModelLCA`.
    j_excitation_energy : str
        J_excitationEnergy for `PhysModelLCA`.
    j_cutoff : str
        J_cutoff for `PhysModelLCA`.
    j_alt_phys : str
        J_altPhys for `PhysModelLCA`.
    j_part_transport : str
        J_partTransport for `PhysModelLCA`.
    j_light_ion : str
        J_lightIon for `PhysModelLCA`.
    j_evaporation : str
        J_evaporation for `PhysModelLCA`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCB(PhysModelLCBBase, PhysicsSetting):
    """
    A representation of the model object `PhysModelLCB`.
    
    Parameters
    ----------
    k_energy1 : float
        KEnergy1 for `PhysModelLCB`.
    k_energy2 : float
        KEnergy2 for `PhysModelLCB`.
    k_energy3 : float
        KEnergy3 for `PhysModelLCB`.
    k_energy4 : float
        KEnergy4 for `PhysModelLCB`.
    k_energy5 : float
        KEnergy5 for `PhysModelLCB`.
    k_energy6 : float
        KEnergy6 for `PhysModelLCB`.
    cutoff : float
        Cutoff for `PhysModelLCB`.
    max_correction : float
        MaxCorrection for `PhysModelLCB`.
    j_k_energy1 : str
        J_kEnergy1 for `PhysModelLCB`.
    j_k_energy2 : str
        J_kEnergy2 for `PhysModelLCB`.
    j_k_energy3 : str
        J_kEnergy3 for `PhysModelLCB`.
    j_k_energy4 : str
        J_kEnergy4 for `PhysModelLCB`.
    j_k_energy5 : str
        J_kEnergy5 for `PhysModelLCB`.
    j_k_energy6 : str
        J_kEnergy6 for `PhysModelLCB`.
    j_cutoff : str
        J_cutoff for `PhysModelLCB`.
    j_max_correction : str
        J_maxCorrection for `PhysModelLCB`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLCC(PhysModelLCCBase, PhysicsSetting):
    """
    A representation of the model object `PhysModelLCC`.
    
    Parameters
    ----------
    rescaling_factor : float
        RescalingFactor for `PhysModelLCC`.
    potential_depth : float
        PotentialDepth for `PhysModelLCC`.
    max_impact : float
        MaxImpact for `PhysModelLCC`.
    pauli_blocking : int
        PauliBlocking for `PhysModelLCC`.
    diffuse_nuclear_surf : int
        DiffuseNuclearSurf for `PhysModelLCC`.
    bertini : float
        Bertini for `PhysModelLCC`.
    no_i_n_c_l_part : float
        NoINCLPart for `PhysModelLCC`.
    no_a_b_l_a_part : float
        NoABLAPart for `PhysModelLCC`.
    j_rescaling_factor : str
        J_rescalingFactor for `PhysModelLCC`.
    j_potential_depth : str
        J_potentialDepth for `PhysModelLCC`.
    j_max_impact : str
        J_maxImpact for `PhysModelLCC`.
    j_pauli_blocking : str
        J_pauliBlocking for `PhysModelLCC`.
    j_diffuse_nuclear_surf : str
        J_diffuseNuclearSurf for `PhysModelLCC`.
    j_bertini : str
        J_bertini for `PhysModelLCC`.
    j_no_i_n_c_l_part : str
        J_noINCLPart for `PhysModelLCC`.
    j_no_a_b_l_a_part : str
        J_noABLAPart for `PhysModelLCC`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEA(PhysModelLEABase, PhysicsSetting):
    """
    A representation of the model object `PhysModelLEA`.
    
    Parameters
    ----------
    gen_control : int
        GenControl for `PhysModelLEA`.
    levelof_physto_p_h_t : int
        LevelofPhystoPHT for `PhysModelLEA`.
    mass_energy_cascade : int
        MassEnergyCascade for `PhysModelLEA`.
    mass_energy_evap : int
        MassEnergyEvap for `PhysModelLEA`.
    fermi_breakup : int
        FermiBreakup for `PhysModelLEA`.
    level_density : int
        LevelDensity for `PhysModelLEA`.
    evap_fission : int
        EvapFission for `PhysModelLEA`.
    fission_control : int
        FissionControl for `PhysModelLEA`.
    j_gen_control : str
        J_genControl for `PhysModelLEA`.
    j_levelof_physto_p_h_t : str
        J_levelofPhystoPHT for `PhysModelLEA`.
    j_mass_energy_cascade : str
        J_massEnergyCascade for `PhysModelLEA`.
    j_mass_energy_evap : str
        J_massEnergyEvap for `PhysModelLEA`.
    j_fermi_breakup : str
        J_fermiBreakup for `PhysModelLEA`.
    j_level_density : str
        J_levelDensity for `PhysModelLEA`.
    j_evap_fission : str
        J_evapFission for `PhysModelLEA`.
    j_fission_control : str
        J_fissionControl for `PhysModelLEA`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysModelLEB(PhysModelLEBBase, PhysicsSetting):
    """
    A representation of the model object `PhysModelLEB`.
    
    Parameters
    ----------
    y_zero_low : float
        YZeroLow for `PhysModelLEB`.
    b_zero_low : float
        BZeroLow for `PhysModelLEB`.
    y_zero_high : float
        YZeroHigh for `PhysModelLEB`.
    b_zero_high : float
        BZeroHigh for `PhysModelLEB`.
    j_y_zero_low : str
        J_yZeroLow for `PhysModelLEB`.
    j_b_zero_low : str
        J_bZeroLow for `PhysModelLEB`.
    j_y_zero_high : str
        J_yZeroHigh for `PhysModelLEB`.
    j_b_zero_high : str
        J_bZeroHigh for `PhysModelLEB`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhysicsCutoff(PhysicsCutoffBase, PhysicsSetting):
    """
    A representation of the model object `PhysicsCutoff`.
    
    Parameters
    ----------
    particles : iterable of mcnpy.Particle
        Particles for `PhysicsCutoff`.
    time : float
        Time for `PhysicsCutoff`.
    min_energy : float
        MinEnergy for `PhysicsCutoff`.
    restore_weight : float
        RestoreWeight for `PhysicsCutoff`.
    min_weight : float
        MinWeight for `PhysicsCutoff`.
    min_source_weight : float
        MinSourceWeight for `PhysicsCutoff`.
    j_time : str
        J_time for `PhysicsCutoff`.
    j_min_energy : str
        J_minEnergy for `PhysicsCutoff`.
    j_restore_weight : str
        J_restoreWeight for `PhysicsCutoff`.
    j_min_weight : str
        J_minWeight for `PhysicsCutoff`.
    j_min_source_weight : str
        J_minSourceWeight for `PhysicsCutoff`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CosyMap(CosyMapBase, PhysicsSetting):
    """
    A representation of the model object `CosyMap`.
    
    Parameters
    ----------
    map_file_prefix : int
        MapFilePrefix for `CosyMap`.
    horizontal : str
        Horizontal for `CosyMap`.
    vertical : str
        Vertical for `CosyMap`.
    energies : iterable of float
        Energies for `CosyMap`.
    map_number : iterable of int
        MapNumber for `CosyMap`.
    
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