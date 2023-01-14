from abc import ABC
from .wrap import wrappers, overrides, subclass_overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class VarianceReductionSetting(ABC):
    """
    """

class CellImportances(CellImportancesBase, VarianceReductionSetting):
    """
    A representation of the model object `CellImportances`.
    
    Parameters
    ----------
    importances : iterable of float
        Importances for `CellImportances`.
    particles : iterable of mcnpy.Particle
        Particles for `CellImportances`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class RussianRoulette(RussianRouletteBase, VarianceReductionSetting):
    """
    A representation of the model object `RussianRoulette`.
    
    Parameters
    ----------
    enabled : mcnpy.EBoolean
        Enabled for `RussianRoulette`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class WeightWindow():
    """"""
    class Energies(WeightWindowEnergiesBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindow.Energies`.
        
        Parameters
        ----------
        max_energies : iterable of float
            MaxEnergies for `WeightWindow.Energies`.
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindow.Energies`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Times(WeightWindowTimesBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindow.Times`.
        
        Parameters
        ----------
        max_times : iterable of float
            MaxTimes for `WeightWindow.Times`.
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindow.Times`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Bounds(WeightWindowBoundsBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindow.Bounds`.
        
        Parameters
        ----------
        name : int
            Name for `WeightWindow.Bounds`.
        bounds : iterable of float
            Bounds for `WeightWindow.Bounds`.
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindow.Bounds`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Parameters(WeightWindowParametersBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindow.Parameters`.
        
        Parameters
        ----------
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindow.Parameters`.
        split_above : float
            SplitAbove for `WeightWindow.Parameters`.
        max_survival : float
            MaxSurvival for `WeightWindow.Parameters`.
        max_integer_splits : int
            MaxintSplits for `WeightWindow.Parameters`.
        where : int
            Where for `WeightWindow.Parameters`.
        lower_weight_bounds : float
            LowerWeightBounds for `WeightWindow.Parameters`.
        energy_is_time : int
            EnergyIsTime for `WeightWindow.Parameters`.
        normalization : float
            Normalization for `WeightWindow.Parameters`.
        roulette_on_splits : int
            RouletteOnSplits for `WeightWindow.Parameters`.
        max_lower_bound : float
            MaxLowerBound for `WeightWindow.Parameters`.
        mfp_travel : int
            MfpTravel for `WeightWindow.Parameters`.
        j_split_above : str
            J_splitAbove for `WeightWindow.Parameters`.
        j_max_survival : str
            J_maxSurvival for `WeightWindow.Parameters`.
        j_max_integer_splits : str
            J_maxintSplits for `WeightWindow.Parameters`.
        j_where : str
            J_where for `WeightWindow.Parameters`.
        j_lower_weight_bounds : str
            J_lowerWeightBounds for `WeightWindow.Parameters`.
        j_energy_is_time : str
            J_energyIsTime for `WeightWindow.Parameters`.
        j_normalization : str
            J_normalization for `WeightWindow.Parameters`.
        j_roulette_on_splits : str
            J_rouletteOnSplits for `WeightWindow.Parameters`.
        j_max_lower_bound : str
            J_maxLowerBound for `WeightWindow.Parameters`.
        j_mfp_travel : str
            J_mfpTravel for `WeightWindow.Parameters`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class WeightWindowGenerator(WeightWindowGeneratorBase, VarianceReductionSetting):
    """
    A representation of the model object `WeightWindowGenerator`.
    
    Parameters
    ----------
    tally : mcnpy.Tally
        Tally for `WeightWindowGenerator`.
    cell : mcnpy.Cell
        Cell for `WeightWindowGenerator`.
    cell_bound : float
        CellBound for `WeightWindowGenerator`.
    un_used1 : str
        UnUsed1 for `WeightWindowGenerator`.
    un_used2 : str
        UnUsed2 for `WeightWindowGenerator`.
    un_used3 : str
        UnUsed3 for `WeightWindowGenerator`.
    energy_is_time : int
        EnergyIsTime for `WeightWindowGenerator`.
    j_cell : str
        J_cell for `WeightWindowGenerator`.
    j_cell_bound : str
        J_cellBound for `WeightWindowGenerator`.
    j_energy_is_time : str
        J_energyIsTime for `WeightWindowGenerator`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class Energies(WeightWindowGeneratorEnergiesBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindowGenerator.Energies`.
        
        Parameters
        ----------
        max_energies : iterable of float
            MaxEnergies for `WeightWindowGenerator.Energies`.
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindowGenerator.Energies`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Times(WeightWindowGeneratorTimesBase, VarianceReductionSetting):
        """
        A representation of the model object `WeightWindowGenerator.Times`.
        
        Parameters
        ----------
        max_times : iterable of float
            MaxTimes for `WeightWindowGenerator.Times`.
        particles : iterable of mcnpy.Particle
            Particles for `WeightWindowGenerator.Times`.
        
        """
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class Mesh(MeshBase, VarianceReductionSetting):
    """
    A representation of the model object `Mesh`.
    
    Parameters
    ----------
    geometry : mcnpy.MeshGeometry
        Geometry for `Mesh`.
    reference : mcnpy.Point
        Reference for `Mesh`.
    origin : mcnpy.Point
        Origin for `Mesh`.
    axis : mcnpy.Point
        Axis for `Mesh`.
    vector : mcnpy.Point
        Vector for `Mesh`.
    i_nodes : iterable of float
        INodes for `Mesh`.
    i_subdivisions : iterable of int
        ISubdivisions for `Mesh`.
    j_nodes : iterable of float
        JNodes for `Mesh`.
    j_subdivisions : iterable of int
        JSubdivisions for `Mesh`.
    k_nodes : iterable of float
        KNodes for `Mesh`.
    k_subdivisions : iterable of int
        KSubdivisions for `Mesh`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EnergySplitting(EnergySplittingBase, VarianceReductionSetting):
    """
    A representation of the model object `EnergySplitting`.
    
    Parameters
    ----------
    factors : iterable of float
        Factors for `EnergySplitting`.
    energies : iterable of float
        Energies for `EnergySplitting`.
    particles : iterable of mcnpy.Particle
        Particles for `EnergySplitting`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class TimeSplitting(TimeSplittingBase, VarianceReductionSetting):
    """
    A representation of the model object `TimeSplitting`.
    
    Parameters
    ----------
    factors : iterable of float
        Factors for `TimeSplitting`.
    times : iterable of float
        Times for `TimeSplitting`.
    particles : iterable of mcnpy.Particle
        Particles for `TimeSplitting`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellExponentialTransforms(CellExponentialTransformsBase, VarianceReductionSetting):
    """
    A representation of the model object `CellExponentialTransforms`.
    
    Parameters
    ----------
    exponential_transforms : iterable of mcnpy.ExponentialTransform
        ExponentialTransforms for `CellExponentialTransforms`.
    particles : iterable of mcnpy.Particle
        Particles for `CellExponentialTransforms`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Vectors(VectorsBase, VarianceReductionSetting):
    """
    A representation of the model object `Vectors`.
    
    Parameters
    ----------
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellForcedCollisions(CellForcedCollisionsBase, VarianceReductionSetting):
    """
    A representation of the model object `CellForcedCollisions`.
    
    Parameters
    ----------
    which_particles : iterable of str
        WhichParticles for `CellForcedCollisions`.
    particles : iterable of mcnpy.Particle
        Particles for `CellForcedCollisions`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicTransport(DeterministicTransportBase, VarianceReductionSetting):
    """
    A representation of the model object `DeterministicTransport`.
    
    Parameters
    ----------
    spheres : mcnpy.DXTSpheres
        Spheres for `DeterministicTransport`.
    cutoff : mcnpy.CutoffParams
        Cutoff for `DeterministicTransport`.
    particles : iterable of mcnpy.Particle
        Particles for `DeterministicTransport`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
    class Sphere(DeterministicTransportSphereBase):
        """
        A representation of the model object `DeterministicTransport.Sphere`.
        
        Parameters
        ----------
        x : float
            X for `DeterministicTransport.Sphere`.
        y : float
            Y for `DeterministicTransport.Sphere`.
        z : float
            Z for `DeterministicTransport.Sphere`.
        ri : float
            Ri for `DeterministicTransport.Sphere`.
        ro : float
            Ro for `DeterministicTransport.Sphere`.
        
        """
        
        def _init(self, x, y, z, ri, ro):
            self.x = x
            self.y = y
            self.z = z
            self.ri = ri
            self.ro = ro

        def __str__(self):
            string = ('(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) 
                    + str(self.ri) + ', ' + str(self.ro) + ')')
            return string

        def __repr__(self):
            return str(self)

class DetectorDiagnostics(DetectorDiagnosticsBase, VarianceReductionSetting):
    """
    A representation of the model object `DetectorDiagnostics`.
    
    Parameters
    ----------
    detector_diagnostic_criteria : iterable of float
        DetectorDiagnosticCriteria for `DetectorDiagnostics`.
    tally : int
        Tally for `DetectorDiagnostics`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDetectorContributions(CellDetectorContributionsBase, VarianceReductionSetting):
    """
    A representation of the model object `CellDetectorContributions`.
    
    Parameters
    ----------
    probabilities : iterable of float
        Probabilities for `CellDetectorContributions`.
    tally : mcnpy.Tally
        Tally for `CellDetectorContributions`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellDeterministicContributions(CellDeterministicContributionsBase, VarianceReductionSetting):
    """
    A representation of the model object `CellDeterministicContributions`.
    
    Parameters
    ----------
    sphere : int
        Sphere for `CellDeterministicContributions`.
    probabilities : iterable of float
        Probabilities for `CellDeterministicContributions`.
    particles : iterable of mcnpy.Particle
        Particles for `CellDeterministicContributions`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])
class BremsstrahlungBiasing(BremsstrahlungBiasingBase, VarianceReductionSetting):
    """
    A representation of the model object `BremsstrahlungBiasing`.
    
    Parameters
    ----------
    bias_factor1 : float
        BiasFactor1 for `BremsstrahlungBiasing`.
    bias_factor2 : float
        BiasFactor2 for `BremsstrahlungBiasing`.
    bias_factor3 : float
        BiasFactor3 for `BremsstrahlungBiasing`.
    bias_factor4 : float
        BiasFactor4 for `BremsstrahlungBiasing`.
    bias_factor5 : float
        BiasFactor5 for `BremsstrahlungBiasing`.
    bias_factor6 : float
        BiasFactor6 for `BremsstrahlungBiasing`.
    bias_factor7 : float
        BiasFactor7 for `BremsstrahlungBiasing`.
    bias_factor8 : float
        BiasFactor8 for `BremsstrahlungBiasing`.
    bias_factor9 : float
        BiasFactor9 for `BremsstrahlungBiasing`.
    bias_factor10 : float
        BiasFactor10 for `BremsstrahlungBiasing`.
    bias_factor11 : float
        BiasFactor11 for `BremsstrahlungBiasing`.
    bias_factor12 : float
        BiasFactor12 for `BremsstrahlungBiasing`.
    bias_factor13 : float
        BiasFactor13 for `BremsstrahlungBiasing`.
    bias_factor14 : float
        BiasFactor14 for `BremsstrahlungBiasing`.
    bias_factor15 : float
        BiasFactor15 for `BremsstrahlungBiasing`.
    bias_factor16 : float
        BiasFactor16 for `BremsstrahlungBiasing`.
    bias_factor17 : float
        BiasFactor17 for `BremsstrahlungBiasing`.
    bias_factor18 : float
        BiasFactor18 for `BremsstrahlungBiasing`.
    bias_factor19 : float
        BiasFactor19 for `BremsstrahlungBiasing`.
    bias_factor20 : float
        BiasFactor20 for `BremsstrahlungBiasing`.
    bias_factor21 : float
        BiasFactor21 for `BremsstrahlungBiasing`.
    bias_factor22 : float
        BiasFactor22 for `BremsstrahlungBiasing`.
    bias_factor23 : float
        BiasFactor23 for `BremsstrahlungBiasing`.
    bias_factor24 : float
        BiasFactor24 for `BremsstrahlungBiasing`.
    bias_factor25 : float
        BiasFactor25 for `BremsstrahlungBiasing`.
    bias_factor26 : float
        BiasFactor26 for `BremsstrahlungBiasing`.
    bias_factor27 : float
        BiasFactor27 for `BremsstrahlungBiasing`.
    bias_factor28 : float
        BiasFactor28 for `BremsstrahlungBiasing`.
    bias_factor29 : float
        BiasFactor29 for `BremsstrahlungBiasing`.
    bias_factor30 : float
        BiasFactor30 for `BremsstrahlungBiasing`.
    bias_factor31 : float
        BiasFactor31 for `BremsstrahlungBiasing`.
    bias_factor32 : float
        BiasFactor32 for `BremsstrahlungBiasing`.
    bias_factor33 : float
        BiasFactor33 for `BremsstrahlungBiasing`.
    bias_factor34 : float
        BiasFactor34 for `BremsstrahlungBiasing`.
    bias_factor35 : float
        BiasFactor35 for `BremsstrahlungBiasing`.
    bias_factor36 : float
        BiasFactor36 for `BremsstrahlungBiasing`.
    bias_factor37 : float
        BiasFactor37 for `BremsstrahlungBiasing`.
    bias_factor38 : float
        BiasFactor38 for `BremsstrahlungBiasing`.
    bias_factor39 : float
        BiasFactor39 for `BremsstrahlungBiasing`.
    bias_factor40 : float
        BiasFactor40 for `BremsstrahlungBiasing`.
    bias_factor41 : float
        BiasFactor41 for `BremsstrahlungBiasing`.
    bias_factor42 : float
        BiasFactor42 for `BremsstrahlungBiasing`.
    bias_factor43 : float
        BiasFactor43 for `BremsstrahlungBiasing`.
    bias_factor44 : float
        BiasFactor44 for `BremsstrahlungBiasing`.
    bias_factor45 : float
        BiasFactor45 for `BremsstrahlungBiasing`.
    bias_factor46 : float
        BiasFactor46 for `BremsstrahlungBiasing`.
    bias_factor47 : float
        BiasFactor47 for `BremsstrahlungBiasing`.
    bias_factor48 : float
        BiasFactor48 for `BremsstrahlungBiasing`.
    bias_factor49 : float
        BiasFactor49 for `BremsstrahlungBiasing`.
    materials : iterable of mcnpy.Material
        Materials for `BremsstrahlungBiasing`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class SecondaryParticleBiasing(SecondaryParticleBiasingBase, VarianceReductionSetting):
    """
    A representation of the model object `SecondaryParticleBiasing`.
    
    Parameters
    ----------
    secondaries : str
        Secondaries for `SecondaryParticleBiasing`.
    pairs : iterable of float
        Pairs for `SecondaryParticleBiasing`.
    particles : iterable of mcnpy.Particle
        Particles for `SecondaryParticleBiasing`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class CellPhotonWeights(CellPhotonWeightsBase, VarianceReductionSetting):
    """
    A representation of the model object `CellPhotonWeights`.
    
    Parameters
    ----------
    photon_weights : iterable of float
        PhotonWeights for `CellPhotonWeights`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class PhotonBias(PhotonBiasBase, VarianceReductionSetting):
    """
    A representation of the model object `PhotonBias`.
    
    Parameters
    ----------
    photon_zaid : iterable of str
        PhotonZaid for `PhotonBias`.
    bias_control : iterable of int
        BiasControl for `PhotonBias`.
    prod_pairs : iterable of mcnpy.PhotonBias.ReacPairs
        ProdPairs for `PhotonBias`.
    
    """
    
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class ReacPairs(ReacPairsBase):
        """
        A representation of the model object `PhotonBias.ReacPairs`.
        
        Parameters
        ----------
        m_treaction_i_d : float
            MTreactionID for `PhotonBias.ReacPairs`.
        control : int
            Control for `PhotonBias.ReacPairs`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class CutoffParams(CutoffParamsBase):
    """
    A representation of the model object `CutoffParams`.
    
    Parameters
    ----------
    upper_weight_cutoff : float
        UpperWeightCutoff for `CutoffParams`.
    lower_weight_cutoff : float
        LowerWeightCutoff for `CutoffParams`.
    min_photon_weight : float
        MinPhotonWeight for `CutoffParams`.
    j_upper_weight_cutoff : str
        J_upperWeightCutoff for `CutoffParams`.
    j_lower_weight_cutoff : str
        J_lowerWeightCutoff for `CutoffParams`.
    j_min_photon_weight : str
        J_minPhotonWeight for `CutoffParams`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class DXTSpheres(DXTSpheresBase):
    """
    A representation of the model object `DXTSpheres`.
    
    Parameters
    ----------
    sphere1 : mcnpy.DeterministicTransport.Sphere
        Sphere1 for `DXTSpheres`.
    sphere2 : mcnpy.DeterministicTransport.Sphere
        Sphere2 for `DXTSpheres`.
    sphere3 : mcnpy.DeterministicTransport.Sphere
        Sphere3 for `DXTSpheres`.
    sphere4 : mcnpy.DeterministicTransport.Sphere
        Sphere4 for `DXTSpheres`.
    sphere5 : mcnpy.DeterministicTransport.Sphere
        Sphere5 for `DXTSpheres`.
    sphere6 : mcnpy.DeterministicTransport.Sphere
        Sphere6 for `DXTSpheres`.
    sphere7 : mcnpy.DeterministicTransport.Sphere
        Sphere7 for `DXTSpheres`.
    sphere8 : mcnpy.DeterministicTransport.Sphere
        Sphere8 for `DXTSpheres`.
    sphere9 : mcnpy.DeterministicTransport.Sphere
        Sphere9 for `DXTSpheres`.
    sphere10 : mcnpy.DeterministicTransport.Sphere
        Sphere10 for `DXTSpheres`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class ExponentialTransform(ExponentialTransformBase):
    """
    A representation of the model object `ExponentialTransform`.
    
    Parameters
    ----------
    sign : str
        Sign for `ExponentialTransform`.
    magnitude : float
        Magnitude for `ExponentialTransform`.
    q : str
        Q for `ExponentialTransform`.
    axis : mcnpy.Axis
        Axis for `ExponentialTransform`.
    vector : mcnpy.Vector
        Vector for `ExponentialTransform`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override

subclass_overrides(PhotonBias)
subclass_overrides(WeightWindow)
subclass_overrides(WeightWindowGenerator)
subclass_overrides(DeterministicTransport)