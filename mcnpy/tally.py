import mcnpy as mp
from abc import ABC
from collections.abc import MutableSequence
from .mixin import IDManagerMixin, NoIDMixin
from .wrap import wrappers, overrides, subclass_overrides
import mcnpy

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

def str_name(obj):
    if isinstance(obj, mp.Surface):
        return str(obj.name)
    elif isinstance(obj, mp.SurfaceFacet):
        return str(obj.surface.name)
    else:
        return str(obj)

# The cell and surface bins run into issues when they are reused. e.g. the same 
# bin object cannot appear on 2 different tallies. To get around this, we can 
# make copies so that each tally gets a unique object with the same semantics.
# The exception is that proper cells and surfaces should not be copied because
# they can be referenced freely throughout the input. The bins themselves
# cannot be referenced. Conceptually, the copying is just like the user typing
# out the same bins for multiple tallies.
def copy_inputs(obj, other):
    cp = obj.__copy__()
    if isinstance(other, (mp.Cell, mp.Universe, mp.UniverseList, mp.Surface, 
                          mp.SurfaceFacet)) is False:
        return cp, other.__copy__()
    else:
        return cp, other

class TallyABC(IDManagerMixin, ABC):
    """
    """
    used_ids = set()

    @property
    def bins(self):
        return self._e_object.getBins()

    @bins.setter
    def bins(self, bins):
        if bins is None:
            pass
        else:
            try:
                if isinstance(bins, (list, mcnpy.Cell)):
                    self._e_object.setBins(Tally.Bin.CellBins(bins))
                else:
                    self._e_object.setBins(Tally.Bin.CellBins(bins.__copy__()))
            except:
                if isinstance(bins, (list, mcnpy.Surface)):
                    self._e_object.setBins(Tally.Bin.SurfaceBins(bins))
                else:
                    self._e_object.setBins(Tally.Bin.SurfaceBins(bins.__copy__()))
                
class TMeshABC(TallyABC):
    """For tracking TMESH 1, 2, 4 IDs"""
    @property
    def bins(self):
        pass

    @bins.setter
    def bins(self, bins):
        pass

class FTallyABC(TallyABC):
    """General class for F1, F2, F4, F6, F7, and F8 tallies.
    """
    def _init(self, name=None, particles=None, bins=None, unit=None, 
              total=None):
        """
        """
        self.name = name
        self.bins = bins
        self.particles = particles
        self.unit = unit
        self.total = total

class DetTallyABC(TallyABC):
    """F5 point and ring flux tallies.
    """
    def _init(self, name=None, particles=None, detectors=None, unit=None, 
              no_direct=None):
        """
        """
        self.name = name
        self.detectors = detectors
        self.particles = particles
        self.unit = unit
        self.no_direct = no_direct

class RadTallyABC(TallyABC):
    """F5 radiography image tallies.
    """
    def _init(self, name=None, particles=None, center=None, r0=None, 
              reference=None, unit=None, no_direct=None):
        """
        """
        self.name = name
        self.center = center
        self.r0 = r0
        self.reference = reference
        self.particles = particles
        self.unit = unit
        self.no_direct = no_direct

class TallySettingABC(ABC):
    pass

class TallyRef(TallySettingABC):
    @property
    def tally(self):
        return self._e_object.getTally()

    @tally.setter
    def tally(self, tally):
        if tally == 0:
            self._e_object.setTally(None)
        else:
            self._e_object.setTally(tally)

class Tally():
    """
    """
    class SurfaceCurrent(FTallyABC, TallySurfaceCurrentBase):
        """
        A representation of the model object `Tally.SurfaceCurrent`.
        
        Parameters
        ----------
        unit : mcnpy.CurrentUnit
            Unit for `Tally.SurfaceCurrent`.
        name : int
            Name for `Tally.SurfaceCurrent`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.SurfaceCurrent`.
        bins : mcnpy.Tally.Bin.SurfaceBins
            Bins for `Tally.SurfaceCurrent`.
        total : str
            Total for `Tally.SurfaceCurrent`.
        
        """
        
        next_id = 1
        increment = 10

    class SurfaceFlux(FTallyABC, TallySurfaceFluxBase):
        """
        A representation of the model object `Tally.SurfaceFlux`.
        
        Parameters
        ----------
        unit : mcnpy.FluxUnit
            Unit for `Tally.SurfaceFlux`.
        name : int
            Name for `Tally.SurfaceFlux`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.SurfaceFlux`.
        bins : mcnpy.Tally.Bin.SurfaceBins
            Bins for `Tally.SurfaceFlux`.
        total : str
            Total for `Tally.SurfaceFlux`.
        
        """
        
        next_id = 2
        increment = 10

    class CellFlux(FTallyABC, TallyCellFluxBase):
        """
        A representation of the model object `Tally.CellFlux`.
        
        Parameters
        ----------
        unit : mcnpy.FluxUnit
            Unit for `Tally.CellFlux`.
        name : int
            Name for `Tally.CellFlux`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.CellFlux`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.CellFlux`.
        total : str
            Total for `Tally.CellFlux`.
        
        """
        
        next_id = 4
        increment = 10

    class EnergyDeposition(FTallyABC, TallyEnergyDepositionBase):
        """
        A representation of the model object `Tally.EnergyDeposition`.
        
        Parameters
        ----------
        unit : mcnpy.FluxUnit
            Unit for `Tally.EnergyDeposition`.
        name : int
            Name for `Tally.EnergyDeposition`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.EnergyDeposition`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.EnergyDeposition`.
        total : str
            Total for `Tally.EnergyDeposition`.
        
        """
        
        next_id = 6
        increment = 10

    class CollisionHeating(FTallyABC, TallyCollisionHeatingBase):
        """
        A representation of the model object `Tally.CollisionHeating`.
        
        Parameters
        ----------
        name : int
            Name for `Tally.CollisionHeating`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.CollisionHeating`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.CollisionHeating`.
        total : str
            Total for `Tally.CollisionHeating`.
        
        """
        
        next_id = 6
        increment = 10

    class FissionHeating(FTallyABC, TallyFissionHeatingBase):
        """
        A representation of the model object `Tally.FissionHeating`.
        
        Parameters
        ----------
        unit : mcnpy.DepositionUnit
            Unit for `Tally.FissionHeating`.
        name : int
            Name for `Tally.FissionHeating`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.FissionHeating`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.FissionHeating`.
        total : str
            Total for `Tally.FissionHeating`.
        
        """
        
        next_id = 7
        increment = 10
        
    class PulseHeight(FTallyABC, TallyPulseHeightBase):
        """
        A representation of the model object `Tally.PulseHeight`.
        
        Parameters
        ----------
        unit : mcnpy.PulseUnit
            Unit for `Tally.PulseHeight`.
        name : int
            Name for `Tally.PulseHeight`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.PulseHeight`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.PulseHeight`.
        total : str
            Total for `Tally.PulseHeight`.
        
        """
        
        next_id = 8
        increment = 10
        
    class ChargeDeposition(FTallyABC, TallyChargeDepositionBase):
        """
        A representation of the model object `Tally.ChargeDeposition`.
        
        Parameters
        ----------
        name : int
            Name for `Tally.ChargeDeposition`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.ChargeDeposition`.
        bins : mcnpy.Tally.Bin.CellBins
            Bins for `Tally.ChargeDeposition`.
        total : str
            Total for `Tally.ChargeDeposition`.
        
        """
        
        next_id = 8
        increment = 10

    class PointFlux(DetTallyABC, TallyPointFluxBase):
        """
        A representation of the model object `Tally.PointFlux`.
        
        Parameters
        ----------
        detectors : iterable of mcnpy.Tally.PointFluxDetector
            Detectors for `Tally.PointFlux`.
        no_direct : str
            NoDirect for `Tally.PointFlux`.
        
        """
        
        next_id = 5
        increment = 10

        class Detector(TallyPointFluxDetectorBase):
            """
            A representation of the model object `Tally.PointFlux.Detector`.
            
            Parameters
            ----------
            x0 : float
                X0 for `Tally.PointFlux.Detector`.
            y0 : float
                Y0 for `Tally.PointFlux.Detector`.
            z0 : float
                Z0 for `Tally.PointFlux.Detector`.
            mean_free_paths : mcnpy.Boolean
                MeanFreePaths for `Tally.PointFlux.Detector`.
            exclusion : float
                Exclusion for `Tally.PointFlux.Detector`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class RingFlux(DetTallyABC, TallyRingFluxBase):
        """
        A representation of the model object `Tally.RingFlux`.
        
        Parameters
        ----------
        axis : mcnpy.Axis
            Axis for `Tally.RingFlux`.
        detectors : iterable of mcnpy.Tally.RingFluxDetector
            Detectors for `Tally.RingFlux`.
        no_direct : str
            NoDirect for `Tally.RingFlux`.
        faxis : mcnpy.fAxis
            Faxis for `Tally.RingFlux`.
        
        """
        
        next_id = 5
        increment = 10

        class Detector(TallyRingFluxDetectorBase):
            """
            A representation of the model object `Tally.RingFlux.Detector`.
            
            Parameters
            ----------
            distance : float
                Distance for `Tally.RingFlux.Detector`.
            radius : float
                Radius for `Tally.RingFlux.Detector`.
            mean_free_paths : mcnpy.Boolean
                MeanFreePaths for `Tally.RingFlux.Detector`.
            exclusion : float
                Exclusion for `Tally.RingFlux.Detector`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    class PinholeImageFlux(RadTallyABC, TallyPinholeImageFluxBase):
        """
        A representation of the model object `Tally.PinholeImageFlux`.
        
        Parameters
        ----------
        collimator_radius : float
            CollimatorRadius for `Tally.PinholeImageFlux`.
        pinhole_radius : float
            PinholeRadius for `Tally.PinholeImageFlux`.
        distance : float
            Distance for `Tally.PinholeImageFlux`.
        
        """
        
        next_id = 5
        increment = 10
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class PlanarImageFlux(RadTallyABC, TallyPlanarImageFluxBase):
        """
        A representation of the model object `Tally.PlanarImageFlux`.
        
        Parameters
        ----------
        scattered_only : mcnpy.Boolean
            ScatteredOnly for `Tally.PlanarImageFlux`.
        scattered_value : int
            ScatteredValue for `Tally.PlanarImageFlux`.
        field_of_view : float
            FieldOfView for `Tally.PlanarImageFlux`.
        centered : mcnpy.Boolean
            Centered for `Tally.PlanarImageFlux`.
        centered_value : int
            CenteredValue for `Tally.PlanarImageFlux`.
        
        """
        
        next_id = 5
        increment = 10
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class CylindricalImageFlux(RadTallyABC, TallyCylindricalImageFluxBase):
        """
        A representation of the model object `Tally.CylindricalImageFlux`.
        
        Parameters
        ----------
        scattered_only : mcnpy.Boolean
            ScatteredOnly for `Tally.CylindricalImageFlux`.
        scattered_value : int
            ScatteredValue for `Tally.CylindricalImageFlux`.
        field_of_view : float
            FieldOfView for `Tally.CylindricalImageFlux`.
        centered : mcnpy.Boolean
            Centered for `Tally.CylindricalImageFlux`.
        centered_value : int
            CenteredValue for `Tally.CylindricalImageFlux`.
        
        """
        
        next_id = 5
        increment = 10
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class FMESH(TallyABC, TallyMeshBase):
        """
        A representation of the model object `Tally.FMESH`.
        
        Parameters
        ----------
        name : int
            Name for `Tally.FMESH`.
        geometry : mcnpy.Tally.FMESHGeometry
            Geometry for `Tally.FMESH`.
        origin : mcnpy.Point
            Origin for `Tally.FMESH`.
        axis : mcnpy.Point
            Axis for `Tally.FMESH`.
        vector : mcnpy.Point
            Vector for `Tally.FMESH`.
        i_nodes : iterable of float
            INodes for `Tally.FMESH`.
        i_subdivisions : iterable of int
            ISubdivisions for `Tally.FMESH`.
        j_nodes : iterable of float
            JNodes for `Tally.FMESH`.
        j_subdivisions : iterable of int
            JSubdivisions for `Tally.FMESH`.
        k_nodes : iterable of float
            KNodes for `Tally.FMESH`.
        k_subdivisions : iterable of int
            KSubdivisions for `Tally.FMESH`.
        energy_nodes : iterable of float
            EnergyNodes for `Tally.FMESH`.
        energy_subdivisions : iterable of int
            EnergySubdivisions for `Tally.FMESH`.
        energy_normalization : mcnpy.YesNo
            EnergyNormalization for `Tally.FMESH`.
        time_node : iterable of float
            TimeNode for `Tally.FMESH`.
        time_subdivisions : iterable of int
            TimeSubdivisions for `Tally.FMESH`.
        time_normalization : mcnpy.YesNo
            TimeNormalization for `Tally.FMESH`.
        factor : float
            Factor for `Tally.FMESH`.
        format : mcnpy.Tally.FMESHFormat
            Format for `Tally.FMESH`.
        transformation : mcnpy.Transformation
            Transformation for `Tally.FMESH`.
        collision_l : float
            CollisionL for `Tally.FMESH`.
        collision_u : float
            CollisionU for `Tally.FMESH`.
        type_quantity : mcnpy.TallyQuantityType
            TypeQuantity for `Tally.FMESH`.
        kcode_cycles : float
            KcodeCycles for `Tally.FMESH`.
        particles : iterable of mcnpy.Particle
            Particles for `Tally.FMESH`.
        
        """
        
        next_id = 4
        increment = 10
        
        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    # This is really just the container around a TMESH block.
    # All of the numbered meshes are their own set of cards/classes.
    #TODO: Work on better combining these cards.
    class SuperimposedTallyMesh(SuperimposedTallyMeshBase):
        """
        A representation of the model object `Tally.SuperimposedTallyMesh`.
        
        Parameters
        ----------
        meshes : iterable of mcnpy.Tally.TMESH
            Meshes for `Tally.SuperimposedTallyMesh`.
        
        """
        
        def _init(self, meshes=[]):
            """
            """
            self.meshes = meshes

    class TMESH(TMESHBase):
        """
        A representation of the model object `Tally.TMESH`.
        
        Parameters
        ----------
        mesh : mcnpy.Tally.TMESHType
            Mesh for `Tally.TMESH`.
        mesh_data : mcnpy.Tally.TMESH.Data
            MeshData for `Tally.TMESH`.
        
        """

        def _init(self, mesh=None, mesh_data=None):
            """
            """
            self.mesh = mesh
            self.mesh_data = mesh_data

        @property
        def mesh(self):
            return self._e_object.getMesh()

        @mesh.setter
        def mesh(self, mesh):
            self._e_object.setMesh(mesh._e_object)

        class Data(MeshDataBase):
            """
            A representation of the model object `Tally.TMESH.Data`.
            
            Parameters
            ----------
            options : iterable of mcnpy.Tally.TMESH.Options
                Options for `Tally.TMESH.Data`.
            coord : iterable of Object
                Coord for `Tally.TMESH.Data`.
            
            """

            def _init(self, coord=[], options=[]):
                """
                """
                self.coord = coord
                self.options = options

        class Options(MeshOptionsBase):
            """
            A representation of the model object `Tally.TMESH.Options`.
            
            Parameters
            ----------
            tally : mcnpy.Tally.TMESHType
                Tally for `Tally.TMESH.Options`.
            
            """
            
            class MF(MeshMFBase):
                """
                A representation of the model object `Tally.TMESH.Options.MF`.
                
                Parameters
                ----------
                m_fpairs : iterable of mcnpy.Tally.TMESH.Options.MF.EnergyPairs
                    MFpairs for `Tally.TMESH.Options.MF`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

                class EnergyPairs(energyPairsBase):
                    """
                    A representation of the model object `Tally.TMESH.Options.MF.EnergyPairs`.
                    
                    Parameters
                    ----------
                    energy1 : float
                        Energy1 for `Tally.TMESH.Options.MF.EnergyPairs`.
                    energy2 : float
                        Energy2 for `Tally.TMESH.Options.MF.EnergyPairs`.
                    
                    """

                    def _init(self, **kwargs):
                        """
                        """
                        for k in kwargs:
                            setattr(self, k, kwargs[k])

            class Multiplier(MeshMultiplierBase):
                """
                A representation of the model object `Tally.TMESH.Options.Multiplier`.
                
                Parameters
                ----------
                sign : mcnpy.Boolean
                    Sign for `Tally.TMESH.Options.Multiplier`.
                bins : Object
                    Bins for `Tally.TMESH.Options.Multiplier`.
                total : mcnpy.Boolean
                    Total for `Tally.TMESH.Options.Multiplier`.
                cumulative : mcnpy.Boolean
                    Cumulative for `Tally.TMESH.Options.Multiplier`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class EnergyLimits(EnergyLimitsBase):
                """
                A representation of the model object `Tally.TMESH.Options.EnergyLimits`.
                
                Parameters
                ----------
                lower_limit : float
                    LowerLimit for `Tally.TMESH.Options.EnergyLimits`.
                upper_limit : float
                    UpperLimit for `Tally.TMESH.Options.EnergyLimits`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])


        class CORA(CORABase):
            """
            A representation of the model object `Tally.TMESH.CORA`.
            
            Parameters
            ----------
            i_d : mcnpy.Tally.TMESHType
                ID for `Tally.TMESH.CORA`.
            coord : iterable of float
                Coord for `Tally.TMESH.CORA`.
            
            """

            def _init(self, tmesh=None, coord=None):
                """
                """
                self.tmesh = tmesh
                self.coord = coord
            
            @property
            def tmesh(self):
                return self._e_object.getID()

            @tmesh.setter
            def tmesh(self, tmesh):
                self._e_object.setID(tmesh._e_object)

        class CORB(CORBBase):
            """
            A representation of the model object `Tally.TMESH.CORB`.
            
            Parameters
            ----------
            i_d : mcnpy.Tally.TMESHType
                ID for `Tally.TMESH.CORB`.
            coord : iterable of float
                Coord for `Tally.TMESH.CORB`.
            
            """

            def _init(self, tmesh=None, coord=None):
                """
                """
                self.tmesh = tmesh
                self.coord = coord
            
            @property
            def tmesh(self):
                return self._e_object.getID()

            @tmesh.setter
            def tmesh(self, tmesh):
                self._e_object.setID(tmesh._e_object)

        class CORC(CORCBase):
            """
            A representation of the model object `Tally.TMESH.CORC`.
            
            Parameters
            ----------
            i_d : mcnpy.Tally.TMESHType
                ID for `Tally.TMESH.CORC`.
            coord : iterable of float
                Coord for `Tally.TMESH.CORC`.
            
            """

            def _init(self, tmesh=None, coord=None):
                """
                """
                self.tmesh = tmesh
                self.coord = coord
            
            @property
            def tmesh(self):
                return self._e_object.getID()

            @tmesh.setter
            def tmesh(self, tmesh):
                self._e_object.setID(tmesh._e_object)

        class Type(TMESHTypeBase):
            """
            A representation of the model object `Tally.TMESH.Type`.
            
            Parameters
            ----------
            mesh : mcnpy.MeshType
                Mesh for `Tally.TMESH.Type`.
            name : int
                Name for `Tally.TMESH.Type`.
            
            """


        class TrackAveraged(TMeshABC, TypeOneBase, Type):
            """
            A representation of the model object `Tally.TMESH.TrackAveraged`.
            
            Parameters
            ----------
            keywords : iterable of mcnpy.Tmesh1
                Keywords for `Tally.TMESH.TrackAveraged`.
            dose_params : mcnpy.Tally.TMESH.TrackAveraged.dParams
                DoseParams for `Tally.TMESH.TrackAveraged`.
            mfactinfo : iterable of float
                Mfactinfo for `Tally.TMESH.TrackAveraged`.
            transfomation : mcnpy.Transformation
                Transfomation for `Tally.TMESH.TrackAveraged`.
            particles : iterable of mcnpy.Particle
                Particles for `Tally.TMESH.TrackAveraged`.
            
            """
            
            next_id = 1
            increment = 10

            def _init(self, name=None, mesh_type=None, particles=[], 
                      keywords=[], dose=None, mfact=[], transformation=None):
                self.mesh_type = mesh_type
                self.name = name
                self.particles = particles
                self.keywords = keywords
                self.dose_params = dose
                self.mfactinfo = mfact
                self.transformation = transformation


            class dParams(dParamsBase):
                """
                A representation of the model object `Tally.TMESH.TrackAveraged.dParams`.
                
                Parameters
                ----------
                conv_coeff : int
                    ConvCoeff for `Tally.TMESH.TrackAveraged.dParams`.
                interpolation_method : int
                    InterpolationMethod for `Tally.TMESH.TrackAveraged.dParams`.
                res_units : int
                    ResUnits for `Tally.TMESH.TrackAveraged.dParams`.
                norm_factor : float
                    NormFactor for `Tally.TMESH.TrackAveraged.dParams`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

        class Source(TMeshABC, TypeTwoBase, Type):
            """
            A representation of the model object `Tally.TMESH.Source`.
            
            Parameters
            ----------
            particles : iterable of mcnpy.Particle
                Particles for `Tally.TMESH.Source`.
            transformation : mcnpy.Transformation
                Transformation for `Tally.TMESH.Source`.
            
            """
            
            next_id = 2
            increment = 10

            def _init(self, name=None, mesh_type=None, particles=[], 
                      transformation=None):
                self.mesh_type = mesh_type
                self.name = name
                self.particles = particles
                self.transformation = transformation

        class EnergyDeposition(TypeThreeBase, Type):
            """
            A representation of the model object `Tally.TMESH.EnergyDeposition`.
            
            Parameters
            ----------
            keywords : iterable of mcnpy.Tmesh3
                Keywords for `Tally.TMESH.EnergyDeposition`.
            m_val : iterable of float
                MVal for `Tally.TMESH.EnergyDeposition`.
            transformation : mcnpy.Transformation
                Transformation for `Tally.TMESH.EnergyDeposition`.
            
            """
            
            next_id = 3
            increment = 10
            used_ids = set()

            def _init(self, name=None, mesh_type=None, keywords=[], 
                      mfact=[], transformation=None):
                self.mesh_type = mesh_type
                self.name = name
                self.keywords = keywords
                self.m_val = mfact
                self.transformation = transformation

        class DXTRAN(TMeshABC, TypeFourBase, Type):
            """
            A representation of the model object `Tally.TMESH.DXTRAN`.
            
            Parameters
            ----------
            transformation : mcnpy.Transformation
                Transformation for `Tally.TMESH.DXTRAN`.
            particles : iterable of mcnpy.Particle
                Particles for `Tally.TMESH.DXTRAN`.
            
            """
            
            next_id = 4
            increment = 10

            def _init(self, name=None, mesh_type=None, particles=[], 
                      transformation=None):
                self.mesh_type = mesh_type
                self.name = name
                self.particles = particles
                self.transformation = transformation

    class Bin(ABC):
        """
        """
        class Level(ABC):
            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceLevel((cp, cp2))
                else:
                    return Tally.Bin.CellLevel((cp, cp2))

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceUnion((cp, cp2))
                else:
                    return Tally.Bin.CellUnion((cp, cp2))

            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if 'Surface' in str(type(self)):
                    return Tally.Bin.SurfaceLevels([cp] + [cp2])
                else:
                    return Tally.Bin.CellLevels([cp] + [cp2])

        class CellBins(CellBinsBase):
            """
            A representation of the model object `Tally.Bin.CellBins`.
            
            Parameters
            ----------
            bins : iterable of Object
                Bins for `Tally.Bin.CellBins`.
            
            """

            def _init(self, bins):
                """
                """
                self.bins = bins

            @property
            def bins(self):
                return self._e_object.getBins()

            @bins.setter
            def bins(self, bins):
                _bins = self._e_object.getBins()
                del _bins[:]
                if (isinstance(bins, (MutableSequence, tuple)) is False 
                    or isinstance(bins, Tally.Bin.Level)): 
                    bins = [bins]
                if isinstance(bins, Tally.Bin.CellLevels):
                    _bins.append(bins)
                else:
                    for i in bins:
                        if isinstance(i, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                            _bins.append(Tally.Bin.UnaryCellBin(i))
                        else:
                            if i is not None:
                                _bins.append(i)

        class CellLevel(CellLevelBase, Level, MutableSequence):
            """
            A representation of the model object `Tally.Bin.CellLevel`.
            
            Parameters
            ----------
            level : iterable of Object
                Level for `Tally.Bin.CellLevel`.
            
            """

            def _init(self, level):
                """
                """
                self.level = level

            @property
            def level(self):
                return self._e_object.getLevel()

            @level.setter
            def level(self, level):
                _level = self._e_object.getLevel()
                del _level[:]
                if (isinstance(level, (MutableSequence, tuple)) is False 
                    or isinstance(level, Tally.Bin.Level)):
                    level = [level]
                for i in level:
                    if isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _level.append(Tally.Bin.UnaryCellBin(i))
                    else:
                        _level.append(i)

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellLevel(cp)
                new &= cp2
                return new

            def __iand__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevel):
                    cp.extend(cp2)
                else:
                    cp.level.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.level[key]

            def __setitem__(self, key, value):
                self.level[key] = value

            def __delitem__(self, key):
                del self.level[key]

            def __len__(self):
                return len(self.level)

            def insert(self, index, value):
                self.level.insert(index, value)

            def __str__(self):
                return ' & '.join(map(str_name, self))

            def __repr__(self):
                return str(self)

        class CellLevels(CellLevelsBase, MutableSequence):
            """
            A representation of the model object `Tally.Bin.CellLevels`.
            
            Parameters
            ----------
            levels : iterable of mcnpy.Tally.Bin.CellLevel
                Levels for `Tally.Bin.CellLevels`.
            
            """

            def _init(self, levels):
                """
                """
                self.levels = levels

            @property
            def levels(self):
                return self._e_object.getLevels()

            @levels.setter
            def levels(self, levels):
                _levels = self._e_object.getLevels()
                del _levels[:]
                if (isinstance(levels, (MutableSequence, tuple)) is False 
                    or isinstance(levels, Tally.Bin.Level)):
                    levels = [levels]
                elif isinstance(levels, Tally.Bin.CellLevels):
                    self.extend(levels)
                for i in levels:
                    if isinstance(i, (Tally.Bin.UnaryCellBin, 
                                      Tally.Bin.CellUnion)):
                        _levels.append(Tally.Bin.CellLevel(i))
                    elif isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _levels.append(Tally.Bin.CellLevel(Tally.Bin.
                                                           UnaryCellBin(i)))
                    else:
                        _levels.append(i)


            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellLevels(cp)
                new <<= cp2
                return new

            def __ilshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevels):
                    cp.extend(cp2)
                else:
                    if isinstance(cp2, (Tally.Bin.CellUnion, 
                                        Tally.Bin.UnaryCellBin)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [cp2])._e_object)
                    elif isinstance(cp2, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [Tally.Bin.UnaryCellBin(
                                            cp2)])._e_object)
                    else:
                        cp.levels.addUnique(cp2._e_object)
                return cp

            def __getitem__(self, key):
                return self.levels[key]

            def __setitem__(self, key, value):
                self.levels[key] = value

            def __delitem__(self, key):
                del self.levels[key]

            def __len__(self):
                return len(self.levels)

            def insert(self, index, value):
                self.levels.insert(index, value)

            def __str__(self):
                return '(' + ' << '.join(map(str, self)) + ')'
            
            def __repr__(self):
                return str(self)

        class CellUnion(CellUnionBase, Level, MutableSequence):
            """
            A representation of the model object `Tally.Bin.CellUnion`.
            
            Parameters
            ----------
            union : iterable of mcnpy.Tally.Bin.UnaryCellBin
                Union for `Tally.Bin.CellUnion`.
            
            """

            def _init(self, union):
                """
                """
                if isinstance(union, Tally.Bin.CellUnion):
                    self.union = union.union
                else:
                    self.union = union

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.CellUnion(cp)
                new |= cp2
                return new

            def __ior__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellUnion):
                    cp.extend(cp2)
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    cp.union.addUnique(Tally.Bin.UnaryCellBin(cp2)._e_object)
                else:
                    cp.union.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.union[key]

            def __setitem__(self, key, value):
                self.union[key] = value

            def __delitem__(self, key):
                del self.union[key]

            def __len__(self):
                return len(self.union)

            def insert(self, index, value):
                self.union.insert(index, value)

            def __str__(self):
                return '(' + ' | '.join(map(str, self)) + ')'

        class FS_halfspace(FS_halfspaceBase):
            """
            A representation of the model object `Tally.Bin.FS_halfspace`.
            
            Parameters
            ----------
            bin : float
                Bin for `Tally.Bin.FS_halfspace`.
            hs : mcnpy.Halfspace
                Hs for `Tally.Bin.FS_halfspace`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class ROCBin(ROCBinBase):
            """
            A representation of the model object `Tally.Bin.ROCBin`.
            
            Parameters
            ----------
            bins : iterable of mcnpy.Tally.Bin.ROCBinRange
                Bins for `Tally.Bin.ROCBin`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class ROCBinRange(ROCBinRangeBase):
            """
            A representation of the model object `Tally.Bin.ROCBinRange`.
            
            Parameters
            ----------
            lower : int
                Lower for `Tally.Bin.ROCBinRange`.
            upper : int
                Upper for `Tally.Bin.ROCBinRange`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        class SurfaceBins(SurfaceBinsBase):
            """
            A representation of the model object `Tally.Bin.SurfaceBins`.
            
            Parameters
            ----------
            bins : iterable of Object
                Bins for `Tally.Bin.SurfaceBins`.
            
            """

            def _init(self, bins):
                """
                """
                self.bins = bins

            @property
            def bins(self):
                return self._e_object.getBins()

            @bins.setter
            def bins(self, bins):
                _bins = self._e_object.getBins()
                del _bins[:]
                if (isinstance(bins, (MutableSequence, tuple)) is False 
                    or isinstance(bins, Tally.Bin.Level)): 
                    bins = [bins]
                if isinstance(bins, Tally.Bin.SurfaceLevels):
                    _bins.append(bins)
                else:
                    for i in bins:
                        if isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                            _bins.append(Tally.Bin.UnarySurfaceBin(i))
                        else:
                            if i is not None:
                                _bins.append(i)

        class SurfaceLevel(SurfaceLevelBase, Level, MutableSequence):
            """
            A representation of the model object `Tally.Bin.SurfaceLevel`.
            
            Parameters
            ----------
            level : iterable of Object
                Level for `Tally.Bin.SurfaceLevel`.
            
            """

            def _init(self, level):
                """
                """
                self.level = level

            @property
            def level(self):
                return self._e_object.getLevel()

            @level.setter
            def level(self, level):
                _level = self._e_object.getLevel()
                del _level[:]
                if (isinstance(level, (MutableSequence, tuple)) is False 
                    or isinstance(level, Tally.Bin.Level)):
                    level = [level]
                for i in level:
                    if isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                        _level.append(Tally.Bin.UnarySurfaceBin(i))
                    else:
                        _level.append(i)

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceLevel(cp)
                new &= cp2
                return new

            def __iand__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceLevel):
                    cp.extend(cp2)
                else:
                    cp.level.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.level[key]

            def __setitem__(self, key, value):
                self.level[key] = value

            def __delitem__(self, key):
                del self.level[key]

            def __len__(self):
                return len(self.level)

            def insert(self, index, value):
                self.level.insert(index, value)

            def __str__(self):
                return ' & '.join(map(str_name, self))

            def __repr__(self):
                return str(self)

        class SurfaceLevels(SurfaceLevelsBase, MutableSequence):
            """
            A representation of the model object `Tally.Bin.SurfaceLevels`.
            
            Parameters
            ----------
            surface_levels : mcnpy.Tally.Bin.SurfaceLevel
                Surface_levels for `Tally.Bin.SurfaceLevels`.
            cell_levels : iterable of mcnpy.Tally.Bin.CellLevel
                Cell_levels for `Tally.Bin.SurfaceLevels`.
            
            """

            def _init(self, levels):
                """
                """
                self.levels = levels

            @property
            def levels(self):
                _levels = []
                _levels.append(self._e_object.getSurface_levels())
                for i in range(len(self._e_object.getCell_levels())):
                    _levels.append(_levels[i])

                return _levels 

            @levels.setter
            def levels(self, levels):
                _levels = []
                if (isinstance(levels, (MutableSequence, tuple)) is False 
                    or isinstance(levels, Tally.Bin.Level)):
                    levels = [levels]
                elif isinstance(levels, Tally.Bin.SurfaceLevels):
                    self.extend(levels)
                for i in levels:
                    if isinstance(i, (Tally.Bin.UnarySurfaceBin, 
                                      Tally.Bin.SurfaceUnion)):
                        _levels.append(Tally.Bin.SurfaceLevel(i))
                    elif isinstance(i, (mp.Surface, mp.SurfaceFacet)):
                        _levels.append(Tally.Bin.SurfaceLevel(
                                       Tally.Bin.UnarySurfaceBin(i)))
                    elif isinstance(i, (Tally.Bin.UnaryCellBin, 
                                        Tally.Bin.CellUnion)):
                        _levels.append(Tally.Bin.CellLevel(i))
                    elif isinstance(i, (mp.Cell, mp.Universe, mp.UniverseList)):
                        _levels.append(Tally.Bin.CellLevel(
                                       Tally.Bin.UnaryCellBin(i)))
                    elif isinstance(i, Tally.Bin.SurfaceLevel):
                        _levels.append(i)
                    elif isinstance(i, Tally.Bin.CellLevels):
                        for j in i:
                            _levels.append(j)
                    else:
                        _levels.append(i)
                self._e_object.setSurface_levels(_levels[0].__copy__())
                _cell_levels = self._e_object.getCell_levels()
                del _cell_levels[:]
                for i in range(1, len(_levels)):
                    _cell_levels.append(_levels[i])



            def __lshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceLevels(cp)
                new <<= cp2
                return new

            def __ilshift__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevels):
                    cp.extend(cp2)
                else:
                    if isinstance(cp2, (Tally.Bin.CellUnion, 
                                        Tally.Bin.UnaryCellBin)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [cp2])._e_object)
                    elif isinstance(cp2, (mp.Cell, mp.Universe, 
                                          mp.UniverseList)):
                        cp.levels.addUnique(Tally.Bin.CellLevel(
                                            [Tally.Bin.UnaryCellBin(
                                            cp2)])._e_object)
                    else:
                        cp.levels.addUnique(cp2._e_object)
                return cp

            def __getitem__(self, key):
                return self.levels[key]

            def __setitem__(self, key, value):
                self.levels[key] = value

            def __delitem__(self, key):
                del self.levels[key]

            def __len__(self):
                return len(self.levels)

            def insert(self, index, value):
                self.levels.insert(index, value)

            def __str__(self):
                return '(' + ' << '.join(map(str_name, self)) + ')'

            def __repr__(self):
                return str(self)

        class SurfaceUnion(SurfaceUnionBase, Level, MutableSequence):
            """
            A representation of the model object `Tally.Bin.SurfaceUnion`.
            
            Parameters
            ----------
            union : iterable of mcnpy.Tally.Bin.UnarySurfaceBin
                Union for `Tally.Bin.SurfaceUnion`.
            
            """

            def _init(self, union):
                """
                """
                if isinstance(union, Tally.Bin.SurfaceUnion):
                    self.union = union.union
                else:
                    self.union = union

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                new = Tally.Bin.SurfaceUnion(cp)
                new |= cp2
                return new

            def __ior__(self, other):
                cp, cp2 = copy_inputs(cp, other)
                if isinstance(cp2, Tally.Bin.SurfaceUnion):
                    cp.extend(cp2)
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    cp.union.addUnique(Tally.Bin.UnarySurfaceBin(cp2)._e_object)
                else:
                    cp.union.addUnique(cp2._e_object)
                return cp

            # Implement mutable sequence protocol by delegating to list
            def __getitem__(self, key):
                return self.union[key]

            def __setitem__(self, key, value):
                self.union[key] = value

            def __delitem__(self, key):
                del self.union[key]

            def __len__(self):
                return len(self.union)

            def insert(self, index, value):
                self.union.insert(index, value)

            def __str__(self):
                return '(' + ' | '.join(map(str, self)) + ')'

        class UnaryCellBin(UnaryCellBinBase, Level):
            """
            A representation of the model object `Tally.Bin.UnaryCellBin`.
            
            Parameters
            ----------
            cell : mcnpy.Cell
                Cell for `Tally.Bin.UnaryCellBin`.
            index : mcnpy.Lattice.Index
                Index for `Tally.Bin.UnaryCellBin`.
            universe : mcnpy.Universe
                Universe for `Tally.Bin.UnaryCellBin`.
            
            """

            def _init(self, unary_cell, index=None):
                """
                """
                if isinstance(unary_cell, mp.Cell):
                    self.cell = unary_cell
                    self.universe = None
                else:
                    self.cell = None
                    self.universe = unary_cell
                if index is not None:
                    if isinstance(index, mp.Lattice.Index):
                        self.index = index
                    else:
                        self.index = mp.Lattice.Index(index)

            def __str__(self):
                if self.cell is None and self.universe is None:
                    return None
                elif self.universe is not None:
                    string = 'U=' + str(self.universe.name)
                else:
                    string = str(self.cell.name)

                if self.index is not None:
                    string += str(self.index)

                return string

            def __repr__(self):
                return str(self)

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellUnion):
                    return Tally.Bin.CellUnion([cp] + cp2[:])
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    return (Tally.Bin.CellUnion([cp] 
                            + [Tally.Bin.UnaryCellBin(cp2)]))
                else:
                    return Tally.Bin.CellUnion([cp, cp2])

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.CellLevel):
                    return Tally.Bin.CellLevel([cp] + cp2[:])
                elif isinstance(cp2, (mp.Cell, mp.Universe, mp.UniverseList)):
                    return (Tally.Bin.CellLevel([cp] 
                            + [Tally.Bin.UnaryCellBin(cp2)]))
                else:
                    return Tally.Bin.CellLevel([cp, cp2])

            def __getitem__(self, index):
                _index = mp.Lattice.Index(index)
                self.index = _index
                return self

        class UnarySurfaceBin(UnarySurfaceBinBase, Level):
            """
            A representation of the model object `Tally.Bin.UnarySurfaceBin`.
            
            Parameters
            ----------
            surface : mcnpy.Surface
                Surface for `Tally.Bin.UnarySurfaceBin`.
            facets : str
                Facets for `Tally.Bin.UnarySurfaceBin`.
            
            """

            def _init(self, surface, facet=None):
                """
                """
                self.surface = surface
                if facet is not None:
                    self.facets = '.' + str(facet)

            def __str__(self):
                string = str(self.surface.name)
                if self.facets is not None:
                    string = '{}.{}'.format(string, int(self.facets))
                return string

            def __repr__(self):
                return str(self)

            def __or__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceUnion):
                    return Tally.Bin.SurfaceUnion([cp] + cp2[:])
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    return (Tally.Bin.SurfaceUnion([cp] 
                            + [Tally.Bin.UnarySurfaceBin(cp2)]))
                else:
                    return Tally.Bin.SurfaceUnion((self, cp2))

            def __and__(self, other):
                cp, cp2 = copy_inputs(self, other)
                if isinstance(cp2, Tally.Bin.SurfaceLevel):
                    return Tally.Bin.SurfaceLevel([cp] + cp2[:])
                elif isinstance(cp2, (mp.Surface, mp.SurfaceFacet)):
                    return (Tally.Bin.SurfaceLevel([cp] 
                            + [Tally.Bin.UnarySurfaceBin(cp2)]))
                else:
                    return Tally.Bin.SurfaceLevel((cp, cp2))

            @property
            def surface(self):
                return self._e_object.getSurface()
            
            @surface.setter
            def surface(self, surface):
                if isinstance(surface, mp.Surface):
                    self._e_object.setSurface(surface._e_object)
                else:
                    self._e_object.setSurface(surface.surface._e_object)
                    self._e_object.setFacets('.' + str(surface.facet))

    class Bins(ABC):
        """
        """
        class Energies(TallyRef, TallyEnergiesBase):
            """
            A representation of the model object `Tally.Bins.Energies`.
            
            Parameters
            ----------
            particles : iterable of mcnpy.Particle
                Particles for `Tally.Bins.Energies`.
            max_energies : iterable of float
                MaxEnergies for `Tally.Bins.Energies`.
            no_total : mcnpy.Boolean
                NoTotal for `Tally.Bins.Energies`.
            cumulative : mcnpy.Boolean
                Cumulative for `Tally.Bins.Energies`.
            tally : mcnpy.Tally
                Tally for `Tally.Bins.Energies`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Times(TallyRef, TallyTimesBase):
            """
            A representation of the model object `Tally.Bins.Times`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.Times`.
            max_times : iterable of float
                MaxTimes for `Tally.Bins.Times`.
            no_total : mcnpy.Boolean
                NoTotal for `Tally.Bins.Times`.
            cumulative : mcnpy.Boolean
                Cumulative for `Tally.Bins.Times`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class TimesCyclic(TallyRef, TallyTimesCyclicBase):
            """
            A representation of the model object `Tally.Bins.TimesCyclic`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.TimesCyclic`.
            start : float
                Start for `Tally.Bins.TimesCyclic`.
            frequency : float
                Frequency for `Tally.Bins.TimesCyclic`.
            dead_time : float
                DeadTime for `Tally.Bins.TimesCyclic`.
            alive_time : float
                AliveTime for `Tally.Bins.TimesCyclic`.
            subdivisions : float
                Subdivisions for `Tally.Bins.TimesCyclic`.
            end : float
                End for `Tally.Bins.TimesCyclic`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Angles(TallyRef, TallyAnglesBase):
            """
            A representation of the model object `Tally.Bins.Angles`.
            
            Parameters
            ----------
            unit : mcnpy.AngleUnit
                Unit for `Tally.Bins.Angles`.
            tally : mcnpy.Tally
                Tally for `Tally.Bins.Angles`.
            max_angles : iterable of float
                MaxAngles for `Tally.Bins.Angles`.
            total : mcnpy.Boolean
                Total for `Tally.Bins.Angles`.
            cumulative : mcnpy.Boolean
                Cumulative for `Tally.Bins.Angles`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class User(TallyRef, TallyUserBase):
            """
            A representation of the model object `Tally.Bins.User`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.User`.
            parameters : iterable of float
                Parameters for `Tally.Bins.User`.
            no_total : mcnpy.Boolean
                NoTotal for `Tally.Bins.User`.
            cumulative : mcnpy.Boolean
                Cumulative for `Tally.Bins.User`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        
        class Multiplier(TallyRef, TallyMultiplierBase):
            """
            A representation of the model object `Tally.Bins.Multiplier`.
            
            Parameters
            ----------
            sign : str
                Sign for `Tally.Bins.Multiplier`.
            tally : mcnpy.Tally
                Tally for `Tally.Bins.Multiplier`.
            bins : Object
                Bins for `Tally.Bins.Multiplier`.
            total : mcnpy.Boolean
                Total for `Tally.Bins.Multiplier`.
            cumulative : mcnpy.Boolean
                Cumulative for `Tally.Bins.Multiplier`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class AttnMatSet(AttnMatSetBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.AttnMatSet`.
                
                Parameters
                ----------
                m : mcnpy.Material
                    M for `Tally.Bins.Multiplier.AttnMatSet`.
                sign : mcnpy.Boolean
                    Sign for `Tally.Bins.Multiplier.AttnMatSet`.
                px : float
                    Px for `Tally.Bins.Multiplier.AttnMatSet`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class AttnSet(AttnSetBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.AttnSet`.
                
                Parameters
                ----------
                c : float
                    C for `Tally.Bins.Multiplier.AttnSet`.
                attenuator : iterable of mcnpy.Tally.Bins.Multiplier.AttnMatSet
                    Attenuator for `Tally.Bins.Multiplier.AttnSet`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBin(MultBinBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.MultBin`.
                
                Parameters
                ----------
                bin : Object
                    Bin for `Tally.Bins.Multiplier.MultBin`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBinSet(MultBinSetBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.MultBinSet`.
                
                Parameters
                ----------
                set : iterable of mcnpy.Tally.Bins.Multiplier.MultBin
                    Set for `Tally.Bins.Multiplier.MultBinSet`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultBinSets(MultBinSetsBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.MultBinSets`.
                
                Parameters
                ----------
                sets : iterable of mcnpy.Tally.Bins.Multiplier.MultBinSet
                    Sets for `Tally.Bins.Multiplier.MultBinSets`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultSet(MultSetBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.MultSet`.
                
                Parameters
                ----------
                c : float
                    C for `Tally.Bins.Multiplier.MultSet`.
                m : mcnpy.Material
                    M for `Tally.Bins.Multiplier.MultSet`.
                reactions : mcnpy.Tally.Bins.Multiplier.RxnLists
                    Reactions for `Tally.Bins.Multiplier.MultSet`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class MultSetSpecial(MultSetSpecialBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.MultSetSpecial`.
                
                Parameters
                ----------
                c : float
                    C for `Tally.Bins.Multiplier.MultSetSpecial`.
                k : str
                    K for `Tally.Bins.Multiplier.MultSetSpecial`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnLists(RxnListsBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.RxnLists`.
                
                Parameters
                ----------
                nodes : iterable of mcnpy.Tally.Bins.Multiplier.Rxns
                    Nodes for `Tally.Bins.Multiplier.RxnLists`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnMult(RxnMultBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.RxnMult`.
                
                Parameters
                ----------
                nodes : iterable of mcnpy.Tally.Bins.Multiplier.RxnNum
                    Nodes for `Tally.Bins.Multiplier.RxnMult`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnNum(RxnNumBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.RxnNum`.
                
                Parameters
                ----------
                sign : mcnpy.PositiveNegative
                    Sign for `Tally.Bins.Multiplier.RxnNum`.
                value : int
                    Value for `Tally.Bins.Multiplier.RxnNum`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class Rxns(RxnsBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.Rxns`.
                
                Parameters
                ----------
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

            class RxnSum(RxnSumBase):
                """
                A representation of the model object `Tally.Bins.Multiplier.RxnSum`.
                
                Parameters
                ----------
                nodes : iterable of mcnpy.Tally.Bins.Multiplier.RxnMult
                    Nodes for `Tally.Bins.Multiplier.RxnSum`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

        class Segments(TallyRef, TallySegmentsBase):
                """
                A representation of the model object `Tally.Bins.Segments`.
                
                Parameters
                ----------
                tally : mcnpy.Tally
                    Tally for `Tally.Bins.Segments`.
                particles : iterable of mcnpy.Particle
                    Particles for `Tally.Bins.Segments`.
                halfspaces : iterable of mcnpy.Tally.Bin.FS_halfspace
                    Halfspaces for `Tally.Bins.Segments`.
                total : mcnpy.Boolean
                    Total for `Tally.Bins.Segments`.
                cumulative : mcnpy.Boolean
                    Cumulative for `Tally.Bins.Segments`.
                
                """
                
                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k.lower(), kwargs[k])

        class AngleMultiplier(TallyRef, AngleMultiplierBase):
            """
            A representation of the model object `Tally.Bins.AngleMultiplier`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.AngleMultiplier`.
            multipliers : iterable of float
                Multipliers for `Tally.Bins.AngleMultiplier`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FlagCells(TallyRef, FlagCellsBase):
            """
            A representation of the model object `Tally.Bins.FlagCells`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.FlagCells`.
            cells : iterable of mcnpy.Cell
                Cells for `Tally.Bins.FlagCells`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Fluctuation(TallyRef, TallyFluctuationBase):
            """
            A representation of the model object `Tally.Bins.Fluctuation`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.Fluctuation`.
            geometry : int
                Geometry for `Tally.Bins.Fluctuation`.
            direct : int
                Direct for `Tally.Bins.Fluctuation`.
            user : int
                User for `Tally.Bins.Fluctuation`.
            segment : int
                Segment for `Tally.Bins.Fluctuation`.
            multiplier : int
                Multiplier for `Tally.Bins.Fluctuation`.
            angle : int
                Angle for `Tally.Bins.Fluctuation`.
            energy : int
                Energy for `Tally.Bins.Fluctuation`.
            time : int
                Time for `Tally.Bins.Fluctuation`.
            j_geometry : str
                J_geometry for `Tally.Bins.Fluctuation`.
            j_direct : str
                J_direct for `Tally.Bins.Fluctuation`.
            j_user : str
                J_user for `Tally.Bins.Fluctuation`.
            j_segment : str
                J_segment for `Tally.Bins.Fluctuation`.
            j_multiplier : str
                J_multiplier for `Tally.Bins.Fluctuation`.
            j_angle : str
                J_angle for `Tally.Bins.Fluctuation`.
            j_energy : str
                J_energy for `Tally.Bins.Fluctuation`.
            j_time : str
                J_time for `Tally.Bins.Fluctuation`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FluctuationROC(TallyRef, TallyFluctuationROCBase):
            """
            A representation of the model object `Tally.Bins.FluctuationROC`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.FluctuationROC`.
            geometry1 : mcnpy.Tally.Bin.ROCBin
                Geometry1 for `Tally.Bins.FluctuationROC`.
            direct1 : mcnpy.Tally.Bin.ROCBin
                Direct1 for `Tally.Bins.FluctuationROC`.
            user1 : mcnpy.Tally.Bin.ROCBin
                User1 for `Tally.Bins.FluctuationROC`.
            segment1 : mcnpy.Tally.Bin.ROCBin
                Segment1 for `Tally.Bins.FluctuationROC`.
            multiplier1 : mcnpy.Tally.Bin.ROCBin
                Multiplier1 for `Tally.Bins.FluctuationROC`.
            angle1 : mcnpy.Tally.Bin.ROCBin
                Angle1 for `Tally.Bins.FluctuationROC`.
            energy1 : mcnpy.Tally.Bin.ROCBin
                Energy1 for `Tally.Bins.FluctuationROC`.
            time1 : mcnpy.Tally.Bin.ROCBin
                Time1 for `Tally.Bins.FluctuationROC`.
            geometry2 : mcnpy.Tally.Bin.ROCBin
                Geometry2 for `Tally.Bins.FluctuationROC`.
            direct2 : mcnpy.Tally.Bin.ROCBin
                Direct2 for `Tally.Bins.FluctuationROC`.
            user2 : mcnpy.Tally.Bin.ROCBin
                User2 for `Tally.Bins.FluctuationROC`.
            segment2 : mcnpy.Tally.Bin.ROCBin
                Segment2 for `Tally.Bins.FluctuationROC`.
            multiplier2 : mcnpy.Tally.Bin.ROCBin
                Multiplier2 for `Tally.Bins.FluctuationROC`.
            angle2 : mcnpy.Tally.Bin.ROCBin
                Angle2 for `Tally.Bins.FluctuationROC`.
            energy2 : mcnpy.Tally.Bin.ROCBin
                Energy2 for `Tally.Bins.FluctuationROC`.
            time2 : mcnpy.Tally.Bin.ROCBin
                Time2 for `Tally.Bins.FluctuationROC`.
            j_geometry1 : str
                J_geometry1 for `Tally.Bins.FluctuationROC`.
            j_direct1 : str
                J_direct1 for `Tally.Bins.FluctuationROC`.
            j_user1 : str
                J_user1 for `Tally.Bins.FluctuationROC`.
            j_segment1 : str
                J_segment1 for `Tally.Bins.FluctuationROC`.
            j_multiplier1 : str
                J_multiplier1 for `Tally.Bins.FluctuationROC`.
            j_angle1 : str
                J_angle1 for `Tally.Bins.FluctuationROC`.
            j_energy1 : str
                J_energy1 for `Tally.Bins.FluctuationROC`.
            j_time1 : str
                J_time1 for `Tally.Bins.FluctuationROC`.
            j_geometry2 : str
                J_geometry2 for `Tally.Bins.FluctuationROC`.
            j_direct2 : str
                J_direct2 for `Tally.Bins.FluctuationROC`.
            j_user2 : str
                J_user2 for `Tally.Bins.FluctuationROC`.
            j_segment2 : str
                J_segment2 for `Tally.Bins.FluctuationROC`.
            j_multiplier2 : str
                J_multiplier2 for `Tally.Bins.FluctuationROC`.
            j_angle2 : str
                J_angle2 for `Tally.Bins.FluctuationROC`.
            j_energy2 : str
                J_energy2 for `Tally.Bins.FluctuationROC`.
            j_time2 : str
                J_time2 for `Tally.Bins.FluctuationROC`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Treatments(TallyRef, TallyTreatmentsBase):
                """
                A representation of the model object `Tally.Bins.Treatments`.
                
                Parameters
                ----------
                tally : mcnpy.Tally
                    Tally for `Tally.Bins.Treatments`.
                keyword : mcnpy.TTreatment
                    Keyword for `Tally.Bins.Treatments`.
                treatment_vals : iterable of float
                    TreatmentVals for `Tally.Bins.Treatments`.
                
                """
                
                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k.lower(), kwargs[k])

        class DoseEnergy(TallyRef, DoseEnergyBase):
            """
            A representation of the model object `Tally.Bins.DoseEnergy`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.DoseEnergy`.
            interpolation : mcnpy.Interpolation
                Interpolation for `Tally.Bins.DoseEnergy`.
            energies : iterable of float
                Energies for `Tally.Bins.DoseEnergy`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseTable(TallyRef, DoseTableBase):
            """
            A representation of the model object `Tally.Bins.DoseTable`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.DoseTable`.
            interpolation : mcnpy.Interpolation
                Interpolation for `Tally.Bins.DoseTable`.
            doses : iterable of float
                Doses for `Tally.Bins.DoseTable`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseFunction(TallyRef, DoseFunctionBase):
            """
            A representation of the model object `Tally.Bins.DoseFunction`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.DoseFunction`.
            unit : str
                Unit for `Tally.Bins.DoseFunction`.
            normalize : mcnpy.Tally.Bins.DoseFunction.Normalization
                Normalize for `Tally.Bins.DoseFunction`.
            function : str
                Function for `Tally.Bins.DoseFunction`.
            interpolation : mcnpy.Interpolation
                Interpolation for `Tally.Bins.DoseFunction`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class Normalization(DoseNormalizationBase):
                """
                A representation of the model object `Tally.Bins.DoseFunction.Normalization`.
                
                Parameters
                ----------
                fac : str
                    Fac for `Tally.Bins.DoseFunction.Normalization`.
                user_fac : float
                    UserFac for `Tally.Bins.DoseFunction.Normalization`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

        class TimeMultiplier(TallyRef, TimeMultiplierBase):
            """
            A representation of the model object `Tally.Bins.TimeMultiplier`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.TimeMultiplier`.
            multipliers : iterable of float
                Multipliers for `Tally.Bins.TimeMultiplier`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class EnergyMultiplier(TallyRef, EnergyMultiplierBase):
            """
            A representation of the model object `Tally.Bins.EnergyMultiplier`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.EnergyMultiplier`.
            multipliers : iterable of float
                Multipliers for `Tally.Bins.EnergyMultiplier`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class FlagSurfaces(TallyRef, FlagSurfacesBase):
            """
            A representation of the model object `Tally.Bins.FlagSurfaces`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.FlagSurfaces`.
            surfaces : iterable of mcnpy.Surface
                Surfaces for `Tally.Bins.FlagSurfaces`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])
        
        class SegmentDivisors(TallyRef, TallySegmentDivisorsBase):
            """
            A representation of the model object `Tally.Bins.SegmentDivisors`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Bins.SegmentDivisors`.
            tally_divisors : iterable of mcnpy.Tally.Bins.SegmentDivisors.Divisor
                TallyDivisors for `Tally.Bins.SegmentDivisors`.
            tally_divisor : mcnpy.Tally.Bins.SegmentDivisors.Divisor
                TallyDivisor for `Tally.Bins.SegmentDivisors`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

            class Divisor(TallyDivisorBase):
                """
                A representation of the model object `Tally.Bins.SegmentDivisors.Divisor`.
                
                Parameters
                ----------
                quantities : iterable of float
                    Quantities for `Tally.Bins.SegmentDivisors.Divisor`.
                
                """

                def _init(self, **kwargs):
                    """
                    """
                    for k in kwargs:
                        setattr(self, k, kwargs[k])

    class Setting(ABC):
        class Comment(TallyRef, TallySettingABC, TallyCommentBase):
            """
            A representation of the model object `Tally.Setting.Comment`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Setting.Comment`.
            comment : iterable of str
                Comment for `Tally.Setting.Comment`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Print(TallyRef, TallySettingABC, TallyPrintBase):
            """
            A representation of the model object `Tally.Setting.Print`.
            
            Parameters
            ----------
            tally : mcnpy.Tally
                Tally for `Tally.Setting.Print`.
            order : iterable of mcnpy.TallyQuantity
                Order for `Tally.Setting.Print`.
            
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class NoTransport(NoIDMixin, TallySettingABC, NoTransportBase):
            """NOTRN
            """
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class Perturbation(IDManagerMixin, TallySettingABC, PerturbationBase):
            """
            A representation of the model object `Tally.Setting.Perturbation`.
            
            Parameters
            ----------
            name : int
                Name for `Tally.Setting.Perturbation`.
            cells : iterable of mcnpy.Cell
                Cells for `Tally.Setting.Perturbation`.
            material : mcnpy.Material
                Material for `Tally.Setting.Perturbation`.
            density : float
                Density for `Tally.Setting.Perturbation`.
            method : int
                Method for `Tally.Setting.Perturbation`.
            min_energy : float
                MinEnergy for `Tally.Setting.Perturbation`.
            max_energy : float
                MaxEnergy for `Tally.Setting.Perturbation`.
            sign : iterable of str
                Sign for `Tally.Setting.Perturbation`.
            reactions : iterable of int
                Reactions for `Tally.Setting.Perturbation`.
            particles : iterable of mcnpy.Particle
                Particles for `Tally.Setting.Perturbation`.
            
            """
            
            next_id = 1
            used_ids = set()
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class ReactivityPerturbation(IDManagerMixin, TallySettingABC, 
                                     ReactivityPerturbationBase):
            """
            A representation of the model object `Tally.Setting.ReactivityPerturbation`.
            
            Parameters
            ----------
            name : int
                Name for `Tally.Setting.ReactivityPerturbation`.
            cells : iterable of mcnpy.Cell
                Cells for `Tally.Setting.ReactivityPerturbation`.
            materials : iterable of mcnpy.Material
                Materials for `Tally.Setting.ReactivityPerturbation`.
            densities : iterable of float
                Densities for `Tally.Setting.ReactivityPerturbation`.
            nuclides : iterable of str
                Nuclides for `Tally.Setting.ReactivityPerturbation`.
            sign : iterable of str
                Sign for `Tally.Setting.ReactivityPerturbation`.
            reactions : iterable of int
                Reactions for `Tally.Setting.ReactivityPerturbation`.
            energy_bins : iterable of float
                EnergyBins for `Tally.Setting.ReactivityPerturbation`.
            linear : mcnpy.YesNo
                Linear for `Tally.Setting.ReactivityPerturbation`.
            
            """
            
            next_id = 1
            used_ids = set()
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class CriticalitySensitivity(IDManagerMixin, TallySettingABC, 
                                     CriticalitySensitivityBase):
            
            """
            A representation of the model object `Tally.Setting.CriticalitySensitivity`.
            
            Parameters
            ----------
            name : int
                Name for `Tally.Setting.CriticalitySensitivity`.
            type : mcnpy.Tally.Setting.CriticalitySensitivityType
                Type for `Tally.Setting.CriticalitySensitivity`.
            nuclides : iterable of str
                Nuclides for `Tally.Setting.CriticalitySensitivity`.
            sabnuclides : iterable of mcnpy.SabNuclide
                Sabnuclides for `Tally.Setting.CriticalitySensitivity`.
            sign : iterable of str
                Sign for `Tally.Setting.CriticalitySensitivity`.
            reactions : iterable of int
                Reactions for `Tally.Setting.CriticalitySensitivity`.
            energy_bins : iterable of float
                EnergyBins for `Tally.Setting.CriticalitySensitivity`.
            incoming_energy_bins : iterable of float
                IncomingEnergyBins for `Tally.Setting.CriticalitySensitivity`.
            moment : iterable of int
                Moment for `Tally.Setting.CriticalitySensitivity`.
            angles : iterable of float
                Angles for `Tally.Setting.CriticalitySensitivity`.
            normalize : mcnpy.YesNo
                Normalize for `Tally.Setting.CriticalitySensitivity`.
            
            """
            
            next_id = 1
            used_ids = set()
            
            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class LatticeSpeedTallyEnhancement(NoIDMixin, TallySettingABC, 
                                           LatticeSpeedTallyEnhancementBase):
            """
            A representation of the model object `Tally.Setting.LatticeSpeedTallyEnhancement`.
            
            Parameters
            ----------
            enabled : mcnpy.ForceOff
                Enabled for `Tally.Setting.LatticeSpeedTallyEnhancement`.
            
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

subclass_overrides(Tally, ignore=[Tally.Bin, Tally.Bins, Tally.Setting])
subclass_overrides(Tally.Bin, ignore=[Tally.Bin.Level])
subclass_overrides(Tally.Bins)
subclass_overrides(Tally.Setting)
subclass_overrides(Tally.TMESH)
