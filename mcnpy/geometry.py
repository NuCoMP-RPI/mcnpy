import numpy as np
from abc import ABC
from random import random
from .tally import Tally
from .region import Complement
from .points import Vector
from .mixin import IDManagerMixin
from .variance_reduction import DeterministicTransport as Dt
from .wrap import wrappers, overrides, subclass_overrides
from .wrap import package as ePackage
from mcnpy.enum_keywords import DensityUnit

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class GeometrySetting(ABC):
    """
    """

class Cell(IDManagerMixin, CellBase):
    """
    A representation of the model object `Cell`.
    
    Parameters
    ----------
    name : int
        Name for `Cell`.
    material : mcnpy.Material
        Material for `Cell`.
    density_unit : mcnpy.DensityUnit
        DensityUnit for `Cell`.
    density : float
        Density for `Cell`.
    region : mcnpy.Region
        Region for `Cell`.
    like : mcnpy.Cell
        Like for `Cell`.
    volume : float
        Volume for `Cell`.
    photon_weight : float
        PhotonWeight for `Cell`.
    no_fission : int
        NoFission for `Cell`.
    tmp_i_d : iterable of int
        TmpID for `Cell`.
    temperature : iterable of float
        Temperature for `Cell`.
    universe : mcnpy.Universe
        Universe for `Cell`.
    transform_angle_unit : mcnpy.AngleUnit
        TransformAngleUnit for `Cell`.
    transformation : mcnpy.Transformation
        Transformation for `Cell`.
    transform : mcnpy.Transform
        Transform for `Cell`.
    lattice : str
        Lattice for `Cell`.
    cosy_map : int
        CosyMap for `Cell`.
    magnetic_field : mcnpy.MagneticField
        MagneticField for `Cell`.
    fill : mcnpy.Cell.Fill
        Fill for `Cell`.
    importances : iterable of mcnpy.Cell.Importance
        Importances for `Cell`.
    exponential_transforms : iterable of mcnpy.Cell.ExponentialTransform
        ExponentialTransforms for `Cell`.
    forced_collisions : iterable of mcnpy.Cell.ForcedCollision
        ForcedCollisions for `Cell`.
    weight_windows : iterable of mcnpy.Cell.WeightWindow
        WeightWindows for `Cell`.
    deterministic_contributions : iterable of mcnpy.Cell.DeterministicContribution
        DeterministicContributions for `Cell`.
    detector_contributions : iterable of mcnpy.Cell.DetectorContribution
        DetectorContributions for `Cell`.
    energy_cutoffs : iterable of mcnpy.Cell.EnergyCutoff
        EnergyCutoffs for `Cell`.
    uncollided_secondaries : iterable of mcnpy.Cell.UncollidedSecondaries
        UncollidedSecondaries for `Cell`.
    comment : str
        Comment for `Cell`.
    
    """

    next_id = 1
    used_ids = set()

    def _init(self, name=None, region=None, material=None, density=0.0, universe=None, 
              comment=None, **kwargs):
        """Define a `Cell`."""
        self.name = name
        self.region = region
        self.universe = universe
        self.material = material
        if self.material is not None:
            if material.density is None:
                self.density = abs(density)
                if density < 0:
                    self.density_unit = 'G_CM3'
        if comment is not None:
            self.comment = comment

        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    @property
    def region(self):
        return self._e_object.getRegion()

    @property
    def density(self):
        return self._e_object.getDensity()

    @property
    def no_fission(self):
        return self._e_object.getNoFission()

    @property
    def importances(self):
        imp = self._e_object.getImportances()
        _importances = {}
        for i in imp:
            for p in i.particles:
                _importances[p] = i.importance
        return _importances

    @property
    def temperature(self):
        return (self._e_object.getTemperature(), self.tmp_id)

    @property
    def fill(self):
        _fill = self._e_object.getFill()
        if self.lattice is not None:
            lattice = Lattice(i=_fill.i, j=_fill.j, k=_fill.k, 
                              type=self.lattice)
            lat = np.array(_fill.lattice)
            dims = []
            dims.append(_fill.i[1]-_fill.i[0]+1)
            dims.append(_fill.j[1]-_fill.j[0]+1)
            dims.append(_fill.k[1]-_fill.k[0]+1)
            lat = lat.reshape(dims[2], dims[1], dims[0])
            lattice.lattice = lat

            return lattice
        else:
            return _fill

    @property
    def material(self):
        return self._e_object.getMaterial()

    @material.setter
    def material(self, material):
        if material is not None:
            self._e_object.setMaterial(material._e_object)
            if material.density is not None:
                self.density = material.density
                self.density_unit = material.density_unit
        else:
            self._e_object.setMaterial(material)
    
    @region.setter
    def region(self, region):
        if region is not None:
            # Should let us reuse regions on different cells.
            self._e_object.setRegion(region.__copy__())
            #self._e_object.setRegion(region)

    @density.setter
    def density(self, density):
        if density is None:
            density = 0
        if density < 0:
            self.density_unit = 'G_CM3'
        self._e_object.setDensity(abs(float(density)))

    @no_fission.setter
    def no_fission(self, nonu):
        if nonu <= 0:
            self._e_object.setNoFission(0)
        else:
            self._e_object.setNoFission(1)

    @temperature.setter
    def temperature(self, temp):
        _tmp = self._e_object.getTemperature()
        del _tmp[:]
        _tmp_id = self._e_object.getTmpID()
        del _tmp_id[:]
        if isinstance(temp, (list, tuple)):
            if isinstance(temp[0], (list, tuple)):
                for i in range(len(temp[0])):
                    _tmp.append(temp[0][i])
                    _tmp_id.append(temp[1][i])
            else:
                for i in range(len(temp)):
                    _tmp.append(temp[i])
        else:
            _tmp.append(temp)

    @fill.setter
    def fill(self, fills):
        if isinstance(fills, (list, tuple)):
            fill = fills[0]
            if isinstance(fills[1], Transformation):
                transform = None
                transformation = fills[1]
            elif isinstance(fills[1], Transform):
                transform = fills[1]
                transformation = None
        else:
            fill = fills
            transform = None
            transformation = None
        _fill = Cell.Fill()
        if isinstance(fill, Lattice):
            _fill.lattice = fill.flatten()
            _fill.i = fill.i
            _fill.j = fill.j
            _fill.k = fill.k
            if fill.type == 'REC':
                self.lattice = '1'
            else:
                self.lattice = '2'
        else:
            if type(fill).__name__ == 'UniverseList':
                _fill.fill = fill._e_object
            else:
                _fill.fill = fill
            if transform is not None:
                _fill.transform = transform
            if transformation is not None:
                _fill.transformation = transformation
        
        self._e_object.setFill(_fill)

    @importances.setter
    def importances(self, importances):
        imp = self._e_object.getImportances()
        del imp[:]
        _imps = {}
        for i in importances:
            if  importances[i] in _imps:
                _imps[importances[i]].append(i)
            else:
                _imps[importances[i]] = [i]
        for i in _imps:
            imp.append(Cell.Importance(i, _imps[i]))
            
    """@property
    def universe(self):
        return self._e_object.getUniverse()

    @universe.setter
    def universe(self, universe):"""


    def __invert__(self):
        return Complement(self)

    def __or__(self, other):
        if isinstance(other, Tally.Bin.CellUnion):
            return Tally.Bin.CellUnion([Tally.Bin.UnaryCellBin(self)] 
                                         + [Tally.Bin.UnaryCellBin(other[:])])
        else:
            return Tally.Bin.CellUnion([Tally.Bin.UnaryCellBin(self)] 
                                         + [Tally.Bin.UnaryCellBin(other)])

    def __and__(self, other):
        if isinstance(other, Tally.Bin.CellLevel):
            return Tally.Bin.CellLevel([Tally.Bin.UnaryCellBin(self)] 
                                         + Tally.Bin.UnaryCellBin(other[:]))
        else:
            return Tally.Bin.CellLevel([Tally.Bin.UnaryCellBin(self)] 
                                         + [Tally.Bin.UnaryCellBin(other)])

    def __getitem__(self, index):
        _index = Lattice.Index(index=index)
        unary = Tally.Bin.UnaryCellBin(self)
        unary.index = _index
        return unary

    def __lshift__(self, other):
        if isinstance(other, Tally.Bin.CellLevel):
            return Tally.Bin.CellLevels([Tally.Bin.CellLevel(
                                          Tally.Bin.UnaryCellBin(self))] 
                                          + Tally.Bin.CellLevel(other[:]))
        else:#elif isinstance(other, (Cell, Universe)):
            return Tally.Bin.CellLevels([Tally.Bin.CellLevel(
                                          Tally.Bin.UnaryCellBin(self))] 
                                          + [Tally.Bin.CellLevel(other.__copy__())])

    def __str__(self):
            string = 'Cell\n'
            string += '{: <16}=\t{}\n'.format('\tName', str(self.name))
            string += '{: <16}=\t{}\n'.format('\tComment', self.comment)
            string += '{: <16}=\t{}\n'.format('\tRegion', self.region)
            if (self.material != 0 and self.material is not None):
                string += '{: <16}=\t{}\n'.format('\tMaterial', 
                                                  str(self.material.name))
            else:
                string += '{: <16}=\t{}\n'.format('\tMaterial', self.material)
            string += '{: <16}=\t{}\n'.format('\tDensity', self.density)
            string += '{: <16}=\t{}\n'.format('\tDensity Unit', 
                                              DensityUnit(self.density_unit).name)
            #string += '{: <16}=\t{}\n'.format('\tUniverse', self.universe)

            return string

    def __repr__(self):
        return '(Cell ' + str(self.name) + ')'

    #TODO: Would be nice if particles were automatically added to mode from here.
    class Importance(CellImportanceBase):
        """
        A representation of the model object `Cell.Importance`.
        
        Parameters
        ----------
        particles : iterable of mcnpy.Particle
            Particles for `Cell.Importance`.
        importance : float
            Importance for `Cell.Importance`.
        
        """

        def _init(self, importance, particles):
            self.importance = importance
            self.particles = particles

        def __str__(self):
            string = ('IMP=' + str(self.importance) + ' for ' 
                      + str(self.particles))
            return string

        def __repr__(self) -> str:
            return str(self)


    class Fill(CellFillBase):
        """
        A representation of the model object `Cell.Fill`.
        
        Parameters
        ----------
        unit : mcnpy.AngleUnit
            Unit for `Cell.Fill`.
        fill : Object
            Fill for `Cell.Fill`.
        transform : mcnpy.Transform
            Transform for `Cell.Fill`.
        transformation : mcnpy.Transformation
            Transformation for `Cell.Fill`.
        i : iterable of int
            I for `Cell.Fill`.
        j : iterable of int
            J for `Cell.Fill`.
        k : iterable of int
            K for `Cell.Fill`.
        lattice : iterable of Object
            Lattice for `Cell.Fill`.
        transforms : iterable of mcnpy.Transform
            Transforms for `Cell.Fill`.
        transformations : iterable of mcnpy.Transformation
            Transformations for `Cell.Fill`.
        
        """

        def _init(self, fill, unit, transformation, transform, lattice, 
                  i, j, k):
            self.fill = fill
            self.unit = unit
            self.lattice = lattice
            self.transformation = transformation
            self.transform = transform
            self.i = i
            self.j = j
            self.k = k

        def universe_fill(self, universe, cell, transform=None, 
                        transformation=None):
            """`Cell.Fill` using a `UniverseList`, `UniverseBase`, or 
            `UniversesBase`.
            """
            if type(universe).__name__ == 'UniverseList':
                self.fill = universe._e_object
            else:
                self.fill = universe
            if transform is not None:
                self.transform = transform
            if transformation is not None:
                self.transformation = transformation
            cell.fill = self

        def lattice_fill(self, lattice, cell):
            """`Cell.Fill` using a `Lattice`.
            """
            self.lattice = lattice.flatten()
            self.i = lattice.i
            self.j = lattice.j
            self.k = lattice.k
            cell.fill = self
            if (lattice.type == 'REC'):
                cell.lattice = '1'
            else:
                cell.lattice = '2'


    class ExponentialTransform(CellExponentialTransformBase):
        """
        A representation of the model object `Cell.ExponentialTransform`.
        
        Parameters
        ----------
        magnitude : float
            Magnitude for `Cell.ExponentialTransform`.
        axis : mcnpy.Axis
            Axis for `Cell.ExponentialTransform`.
        vector : mcnpy.Vector
            Vector for `Cell.ExponentialTransform`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.ExponentialTransform`.
        
        """
        
        def _init(self, particles, magnitude, axis=None, vector=None):
            """
            """
            self.particles = particles
            self.magnitiude = magnitude
            self.axis = axis
            self.vector = vector

        @property
        def vector(self):
            _v = self._e_object.getVector()
            if _v is None:
                return None
            else:
                return (_v.name, _v.x, _v.y, _v.z)

        @vector.setter
        def vector(self, v):
            if isinstance(v, Vector):
                self._e_object.setVector(v)
            else:
                self._e_object.setVector(Vector(str(v[0]), v[1], v[2], v[3]))

    class ForcedCollision(CellForcedCollisionBase):
        """
        A representation of the model object `Cell.ForcedCollision`.
        
        Parameters
        ----------
        which_particles : iterable of float
            WhichParticles for `Cell.ForcedCollision`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.ForcedCollision`.
        
        """
        
        def _init(self, particles, which_particles):
            """
            """
            self.particles = particles
            self.which_particles = which_particles

    class WeightWindow(CellWeightWindowBase):
        """
        A representation of the model object `Cell.WeightWindow`.
        
        Parameters
        ----------
        index : int
            Index for `Cell.WeightWindow`.
        weight_window : float
            WeightWindow for `Cell.WeightWindow`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.WeightWindow`.
        
        """
        
        def _init(self, particles, weight_window, index=None):
            """
            """
            self.particles = particles
            self.weight_window = weight_window
            self.index = index

    class DeterministicContribution(CellDeterministicContributionBase):
        """
        A representation of the model object `Cell.DeterministicContribution`.
        
        Parameters
        ----------
        sphere : mcnpy.DeterministicTransport.Sphere
            Sphere for `Cell.DeterministicContribution`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.DeterministicContribution`.
        
        """
        
        def _init(self, particles, sphere):
            """
            """
            self.particles = particles
            self.sphere = sphere

        @property
        def sphere(self):
            _s = self._e_object.getSphere()
            if _s is None:
                return None
            else:
                return (_s.x, _s.y, _s.z, _s.ri, _s.ro)

        @sphere.setter
        def sphere(self, s):
            if isinstance(s, ):
                self._e_object.setSphere(s)
            else:
                self._e_object.setSphere(Dt.Sphere(str(s[0]), s[1], s[2], s[3], 
                                                      s[4]))

    class DetectorContribution(CellDetectorContributionBase):
        """
        A representation of the model object `Cell.DetectorContribution`.
        
        Parameters
        ----------
        tally : mcnpy.Tally
            Tally for `Cell.DetectorContribution`.
        probability : float
            Probability for `Cell.DetectorContribution`.
        
        """
        
        def _init(self, tally, probability):
            """
            """
            self.tally = tally
            self.probability = probability

    class EnergyCutoff(CellEnergyCutoffBase):
        """
        A representation of the model object `Cell.EnergyCutoff`.
        
        Parameters
        ----------
        lower_cutoff : float
            LowerCutoff for `Cell.EnergyCutoff`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.EnergyCutoff`.
        
        """
        
        def _init(self, particles, lower_cutoff):
            """
            """
            self.particles = particles
            self.lower_cutoff = lower_cutoff

    class UncollidedSecondaries(CellUncollidedSecondariesBase):
        """
        A representation of the model object `Cell.UncollidedSecondaries`.
        
        Parameters
        ----------
        uncollided : int
            Uncollided for `Cell.UncollidedSecondaries`.
        particles : iterable of mcnpy.Particle
            Particles for `Cell.UncollidedSecondaries`.
        
        """
        
        def _init(self, particles, uncollided):
            """
            """
            self.particles = particles
            self.uncollided = uncollided

class Transformation(IDManagerMixin, TransformationBase, GeometrySetting):
    """TR Card
    
    Parameters
    ----------
    name : str
        Unique ID for the transformation.
    transformation : mcnpy.geometry.Transform or nested list
        The transformation itself described as a Transform or a list. The list may contain up to 3 items. First a list of displacements, second a 3x3 array describing the rotation matrix, and third the 'm' value specifiying the rotation reference frame.
    """
    next_id = 1
    used_ids = set()

    def _init(self, name=None, transformation=None, unit=None):
        """`transformation` must be a `Transform` or a list containing at least a displacement.
        """
        self.name = name
        self.transformation = transformation
        if unit is not None:
            self.unit = unit

    @property
    def transformation(self):
        return self._e_object.getTransformation()

    @transformation.setter
    def transformation(self, tr):
        if isinstance(tr, (tuple, list)):
            if len(tr) == 1:
                self._e_object.setTransformation(Transform(tr[0]))
            elif len(tr) == 2:
                self._e_object.setTransformation(Transform(tr[0], tr[1]))
            else:
                self._e_object.setTransformation(Transform(tr[0], tr[1], tr[2]))
        else:
            self._e_object.setTransformation(tr)

class Transform(TransformBase):
    """
    A representation of the model object `Transform`.
    
    Parameters
    ----------
    disp1 : float
        Disp1 for `Transform`.
    j_disp1 : str
        J_disp1 for `Transform`.
    disp2 : float
        Disp2 for `Transform`.
    j_disp2 : str
        J_disp2 for `Transform`.
    disp3 : float
        Disp3 for `Transform`.
    j_disp3 : str
        J_disp3 for `Transform`.
    rotation : mcnpy.Transform.RotMatrix
        Rotation for `Transform`.
    
    """

    def _init(self, displacement, rotation=None, m=None):
        """
        """

        self.displacement = displacement

        if rotation is not None:
            if isinstance(rotation, Transform.RotMatrix):
                self.rotation = rotation
            else:
                self.rotation = Transform.RotMatrix(rotation, m)

    @property
    def displacement(self):
        return [self.disp1, self.disp2, self.disp3]

    @displacement.setter
    def displacement(self, disp):
        self.disp1 = disp[0]
        self.disp2 = disp[1]
        self.disp3 = disp[2]

    class RotMatrix(RotMatrixBase):
        """
        A representation of the model object `Transform.RotMatrix`.
        
        Parameters
        ----------
        xx : float
            Xx for `Transform.RotMatrix`.
        j_xx : str
            J_xx for `Transform.RotMatrix`.
        yx : float
            Yx for `Transform.RotMatrix`.
        j_yx : str
            J_yx for `Transform.RotMatrix`.
        zx : float
            Zx for `Transform.RotMatrix`.
        j_zx : str
            J_zx for `Transform.RotMatrix`.
        xy : float
            Xy for `Transform.RotMatrix`.
        j_xy : str
            J_xy for `Transform.RotMatrix`.
        yy : float
            Yy for `Transform.RotMatrix`.
        j_yy : str
            J_yy for `Transform.RotMatrix`.
        zy : float
            Zy for `Transform.RotMatrix`.
        j_zy : str
            J_zy for `Transform.RotMatrix`.
        xz : float
            Xz for `Transform.RotMatrix`.
        j_xz : str
            J_xz for `Transform.RotMatrix`.
        yz : float
            Yz for `Transform.RotMatrix`.
        j_yz : str
            J_yz for `Transform.RotMatrix`.
        zz : float
            Zz for `Transform.RotMatrix`.
        j_zz : str
            J_zz for `Transform.RotMatrix`.
        m : float
            M for `Transform.RotMatrix`.
        j_m : str
            J_m for `Transform.RotMatrix`.
        
        """

        def _init(self, matrix, m=None):
            """`matrix` is a 3x3 numpy array in the form
            `[[xx, yx, zx], [xy, yy, zy], [xz, yz, zz]]` 
            """

            self.matrix = matrix

            if m is not None:
                self.m = m

        @property
        def matrix(self):
            matrix = np.array([[self.xx, self.yx, self.zx], 
                            [self.xy, self.yy, self.zy], 
                            [self.xz, self.yz, self.zz]], dtype=float)
            return matrix

        @matrix.setter
        def matrix(self, _matrix):
            if (_matrix[0,0] == 0 and _matrix[0,1] == 0 and _matrix[0,2] == 0 and
                _matrix[1,0] == 0 and _matrix[1,1] == 0 and _matrix[1,2] == 0 and
                _matrix[2,0] == 0 and _matrix[2,1] == 0 and _matrix[2,2] == 0):
                self._e_object.eUnset(ePackage.ROT_MATRIX__XX)
                self._e_object.eUnset(ePackage.ROT_MATRIX__YX)
                self._e_object.eUnset(ePackage.ROT_MATRIX__ZX)
                self._e_object.eUnset(ePackage.ROT_MATRIX__XY)
                self._e_object.eUnset(ePackage.ROT_MATRIX__YY)
                self._e_object.eUnset(ePackage.ROT_MATRIX__ZY)
                self._e_object.eUnset(ePackage.ROT_MATRIX__XZ)
                self._e_object.eUnset(ePackage.ROT_MATRIX__YZ)
                self._e_object.eUnset(ePackage.ROT_MATRIX__ZZ)
            else:
                self.xx = _matrix[0, 0]
                self.yx = _matrix[0, 1]
                self.zx = _matrix[0, 2]

                self.xy = _matrix[1, 0]
                self.yy = _matrix[1, 1]
                self.zy = _matrix[1, 2]

                self.xz = _matrix[2, 0]
                self.yz = _matrix[2, 1]
                self.zz = _matrix[2, 2]

class Volumes(VolumesBase, GeometrySetting):
    """
    A representation of the model object `Volumes`.
    
    Parameters
    ----------
    volumes : iterable of str
        Volumes for `Volumes`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Areas(AreasBase, GeometrySetting):
    """
    A representation of the model object `Areas`.
    
    Parameters
    ----------
    areas : iterable of str
        Areas for `Areas`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Fills(FillsBase, GeometrySetting):
    """
    A representation of the model object `Fills`.
    
    Parameters
    ----------
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class StochasticGeometry(StochasticGeometryBase, GeometrySetting):
    """
    A representation of the model object `StochasticGeometry`.
    
    Parameters
    ----------
    stochastic_transformations : iterable of mcnpy.StochasticGeometry.Transformation
        StochasticTransformations for `StochasticGeometry`.
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

    class Transformation(StochasticGeometryTransformationBase):
        """
        A representation of the model object `StochasticGeometry.Transformation`.
        
        Parameters
        ----------
        universe : Object
            Universe for `StochasticGeometry.Transformation`.
        dx : float
            Dx for `StochasticGeometry.Transformation`.
        dy : float
            Dy for `StochasticGeometry.Transformation`.
        dz : float
            Dz for `StochasticGeometry.Transformation`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class Deterministic(GeometrySetting):
    """
    """
    class Materials(DeterministicMaterialsBase, GeometrySetting):
        """
        A representation of the model object `Deterministic.Materials`.
        
        Parameters
        ----------
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class WeightWindowGenerator(DeterministicWeightWindowGeneratorBase, 
                                GeometrySetting):
        """
        A representation of the model object `Deterministic.WeightWindowGenerator`.
        
        Parameters
        ----------
        points : int
            Points for `Deterministic.WeightWindowGenerator`.
        xsec_library : mcnpy.Library
            XsecLibrary for `Deterministic.WeightWindowGenerator`.
        tally : mcnpy.Tally
            Tally for `Deterministic.WeightWindowGenerator`.
        block_one : mcnpy.Partisn.BlockOne
            BlockOne for `Deterministic.WeightWindowGenerator`.
        block_three : mcnpy.Partisn.BlockThree
            BlockThree for `Deterministic.WeightWindowGenerator`.
        block_five : mcnpy.Partisn.BlockFive
            BlockFive for `Deterministic.WeightWindowGenerator`.
        block_six : mcnpy.Partisn.BlockSix
            BlockSix for `Deterministic.WeightWindowGenerator`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

class Embedded(GeometrySetting):
    """
    """
    class Geometry(EmbeddedGeometryBase, GeometrySetting):
        """
        A representation of the model object `Embedded.Geometry`.
        
        Parameters
        ----------
        name : int
            Name for `Embedded.Geometry`.
        background : mcnpy.Cell
            Background for `Embedded.Geometry`.
        sign : iterable of str
            Sign for `Embedded.Geometry`.
        materials : iterable of int
            Materials for `Embedded.Geometry`.
        cells : iterable of int
            Cells for `Embedded.Geometry`.
        mesh_format : mcnpy.EmbeddedGeometryMeshFormat
            MeshFormat for `Embedded.Geometry`.
        mesh : str
            Mesh for `Embedded.Geometry`.
        eeout : str
            Eeout for `Embedded.Geometry`.
        eeout_res : str
            EeoutRes for `Embedded.Geometry`.
        calculate_volumes : mcnpy.YesNo
            CalculateVolumes for `Embedded.Geometry`.
        debug : mcnpy.EmbeddedGeometryDebug
            Debug for `Embedded.Geometry`.
        filetype : mcnpy.EmbeddedGeometryFiletype
            Filetype for `Embedded.Geometry`.
        gmv_file : str
            GmvFile for `Embedded.Geometry`.
        length_conversion_factor : float
            LengthConversionFactor for `Embedded.Geometry`.
        mcnpum_file : str
            McnpumFile for `Embedded.Geometry`.
        overlap : mcnpy.EmbeddedGeometryOverlap
            Overlap for `Embedded.Geometry`.
        overlap_cell : iterable of mcnpy.EmbeddedGeometryOverlap
            OverlapCell for `Embedded.Geometry`.
        overlap_cells : iterable of mcnpy.Cell
            OverlapCells for `Embedded.Geometry`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

    class Edit(EmbeddedEditBase, GeometrySetting):
        """
        A representation of the model object `Embedded.Edit`.
        
        Parameters
        ----------
        name : int
            Name for `Embedded.Edit`.
        mesh_universe : int
            MeshUniverse for `Embedded.Edit`.
        scale_energy : float
            ScaleEnergy for `Embedded.Edit`.
        scale_time : float
            ScaleTime for `Embedded.Edit`.
        atom_density_flag : mcnpy.YesNo
            AtomDensityFlag for `Embedded.Edit`.
        mult_constant : float
            MultConstant for `Embedded.Edit`.
        rxn_list : mcnpy.Tally.Bins.Multiplier.RxnLists
            RxnList for `Embedded.Edit`.
        material_no : mcnpy.Material
            MaterialNo for `Embedded.Edit`.
        mult_type : mcnpy.MTypeOptions
            MultType for `Embedded.Edit`.
        errors : mcnpy.YesNo
            Errors for `Embedded.Edit`.
        comment : str
            Comment for `Embedded.Edit`.
        particles : iterable of mcnpy.Particle
            Particles for `Embedded.Edit`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k.lower(), kwargs[k])

        class EnergyBins(EmbeddedEditEnergyBinsBase, GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.EnergyBins`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.EnergyBins`.
            bins : iterable of float
                Bins for `Embedded.Edit.EnergyBins`.
            particles : iterable of mcnpy.Particle
                Particles for `Embedded.Edit.EnergyBins`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class EnergyBinMultipliers(EmbeddedEditEnergyBinMultipliersBase, 
                                   GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.EnergyBinMultipliers`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.EnergyBinMultipliers`.
            multipliers : iterable of float
                Multipliers for `Embedded.Edit.EnergyBinMultipliers`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class TimeBins(EmbeddedEditTimeBinsBase, GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.TimeBins`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.TimeBins`.
            bins : iterable of float
                Bins for `Embedded.Edit.TimeBins`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class TimeBinMultipliers(EmbeddedEditTimeBinMultipliersBase, 
                                 GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.TimeBinMultipliers`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.TimeBinMultipliers`.
            multipliers : iterable of float
                Multipliers for `Embedded.Edit.TimeBinMultipliers`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseBins(EmbeddedEditDoseBinsBase, GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.DoseBins`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.DoseBins`.
            bins : iterable of float
                Bins for `Embedded.Edit.DoseBins`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

        class DoseBinMultipliers(EmbeddedEditDoseBinMultipliersBase, 
                                 GeometrySetting):
            """
            A representation of the model object `Embedded.Edit.DoseBinMultipliers`.
            
            Parameters
            ----------
            edit : mcnpy.Embedded.Edit
                Edit for `Embedded.Edit.DoseBinMultipliers`.
            multipliers : iterable of float
                Multipliers for `Embedded.Edit.DoseBinMultipliers`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k.lower(), kwargs[k])

class Lattices(LatticesBase, GeometrySetting):
    """
    A representation of the model object `Lattices`.
    
    Parameters
    ----------
    
    """

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class Partisn(GeometrySetting):
    """
    """
    class BlockOne(PartisnBlockOneBase, GeometrySetting):
        """
        A representation of the model object `Partisn.BlockOne`.
        
        Parameters
        ----------
        group_count : int
            GroupCount for `Partisn.BlockOne`.
        sn_order : int
            SnOrder for `Partisn.BlockOne`.
        isotope_count : int
            IsotopeCount for `Partisn.BlockOne`.
        material_count : int
            MaterialCount for `Partisn.BlockOne`.
        quadrature : int
            Quadrature for `Partisn.BlockOne`.
        read_composition : int
            ReadComposition for `Partisn.BlockOne`.
        suppress_solver : int
            SuppressSolver for `Partisn.BlockOne`.
        supress_edit : int
            SupressEdit for `Partisn.BlockOne`.
        print_g_e_o_d_s_t : int
            PrintGEODST for `Partisn.BlockOne`.
        print_mixing : int
            PrintMixing for `Partisn.BlockOne`.
        print_a_s_g_m_a_t : int
            PrintASGMAT for `Partisn.BlockOne`.
        print_m_a_c_r_x_s : int
            PrintMACRXS for `Partisn.BlockOne`.
        print_s_o_l_i_n_p : int
            PrintSOLINP for `Partisn.BlockOne`.
        print_e_d_i_t_i_t : int
            PrintEDITIT for `Partisn.BlockOne`.
        print_a_d_j_m_a_c : int
            PrintADJMAC for `Partisn.BlockOne`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class BlockThree(PartisnBlockThreeBase, GeometrySetting):
        """
        A representation of the model object `Partisn.BlockThree`.
        
        Parameters
        ----------
        xsec_form : str
            XsecForm for `Partisn.BlockThree`.
        xsec_library : str
            XsecLibrary for `Partisn.BlockThree`.
        enable_fission_neutrons : int
            EnableFissionNeutrons for `Partisn.BlockThree`.
        last_neutron_group_index : int
            LastNeutronGroupIndex for `Partisn.BlockThree`.
        xsec_balance : int
            XsecBalance for `Partisn.BlockThree`.
        mendf_fission_fraction : int
            MendfFissionFraction for `Partisn.BlockThree`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class BlockFive(PartisnBlockFiveBase, GeometrySetting):
        """
        A representation of the model object `Partisn.BlockFive`.
        
        Parameters
        ----------
        calculation_type : int
            CalculationType for `Partisn.BlockFive`.
        legendre_order : int
            LegendreOrder for `Partisn.BlockFive`.
        adjoint : int
            Adjoint for `Partisn.BlockFive`.
        trcor : str
            Trcor for `Partisn.BlockFive`.
        left_b_c : int
            LeftBC for `Partisn.BlockFive`.
        right_b_c : int
            RightBC for `Partisn.BlockFive`.
        top_b_c : int
            TopBC for `Partisn.BlockFive`.
        bottom_b_c : int
            BottomBC for `Partisn.BlockFive`.
        convergence_precision : float
            ConvergencePrecision for `Partisn.BlockFive`.
        max_outer_iterations : int
            MaxOuterIterations for `Partisn.BlockFive`.
        inhibit_fission_multiplication : int
            InhibitFissionMultiplication for `Partisn.BlockFive`.
        solver_acceleration : mcnpy.PartisnSolverAcceleration
            SolverAcceleration for `Partisn.BlockFive`.
        diffusion_solver : str
            DiffusionSolver for `Partisn.BlockFive`.
        synthetic_acceleration_sn_order : int
            SyntheticAccelerationSnOrder for `Partisn.BlockFive`.
        synthetic_acceleration_convergence : float
            SyntheticAccelerationConvergence for `Partisn.BlockFive`.
        max_synthetic_acceleration_iterations : float
            MaxSyntheticAccelerationIterations for `Partisn.BlockFive`.
        sytnethic_acceleration_scattering_reduction : float
            SytnethicAccelerationScatteringReduction for `Partisn.BlockFive`.
        special_criticality_convergence : int
            SpecialCriticalityConvergence for `Partisn.BlockFive`.
        norm : float
            Norm for `Partisn.BlockFive`.
        print_xsecs : int
            PrintXsecs for `Partisn.BlockFive`.
        print_fission_source_rate : int
            PrintFissionSourceRate for `Partisn.BlockFive`.
        print_fission_source : int
            PrintFissionSource for `Partisn.BlockFive`.
        print_angular_flux : int
            PrintAngularFlux for `Partisn.BlockFive`.
        print_coarse_mesh_balance : int
            PrintCoarseMeshBalance for `Partisn.BlockFive`.
        prepare_angular_flux : int
            PrepareAngularFlux for `Partisn.BlockFive`.
        prepare_flux_moments : int
            PrepareFluxMoments for `Partisn.BlockFive`.
        prepare_xmfluxa : int
            PrepareXmfluxa for `Partisn.BlockFive`.
        right_flux : int
            RightFlux for `Partisn.BlockFive`.
        left_flux : int
            LeftFlux for `Partisn.BlockFive`.
        top_flux : int
            TopFlux for `Partisn.BlockFive`.
        bottom_flux : int
            BottomFlux for `Partisn.BlockFive`.
        back_flux : int
            BackFlux for `Partisn.BlockFive`.
        front_flux : int
            FrontFlux for `Partisn.BlockFive`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

    class BlockSix(PartisnBlockSixBase, GeometrySetting):
        """
        A representation of the model object `Partisn.BlockSix`.
        
        Parameters
        ----------
        mass_edits : int
            MassEdits for `Partisn.BlockSix`.
        edits_by_fine_mesh : int
            EditsByFineMesh for `Partisn.BlockSix`.
        edits_by_zone : int
            EditsByZone for `Partisn.BlockSix`.
        print_a_flux : int
            PrintAFlux for `Partisn.BlockSix`.
        print_b_flux : int
            PrintBFlux for `Partisn.BlockSix`.
        ascii_output : int
            AsciiOutput for `Partisn.BlockSix`.
        scale_edits_by_volume : int
            ScaleEditsByVolume for `Partisn.BlockSix`.
        adjoint : int
            Adjoint for `Partisn.BlockSix`.
        flux_override : int
            FluxOverride for `Partisn.BlockSix`.
        
        """

        def _init(self, **kwargs):
            """
            """
            for k in kwargs:
                setattr(self, k, kwargs[k])

class Lattice():
    """Class for lattices. Defined by max indicies `i`, `j`, `k`, and a 3D array `lattice`. The array should be defined using `numpy.array()` where `k` indicies are your outermost dimension followed by `j` and `i`. Elements of `lattice` can be `LatticeElement` objects, universe IDs, tuple(universe ID, transformation ID), or 0. When using IDs, `universes` and `transformations` must include the key value pair of ID and object. Using `Transforms` instead of `Transformations` is also allowed.
    
    Parameters
    ----------
    i : iterable of int
        Indices of innermost lattice dimension.
    j : iterable of int
        Indicies of second lattice dimension.
    k : iterable of int
        Indicies of outermost lattice dimension.
    lattice : numpy.array
        Array of universe IDs, `mcnpy.Lattice.Element` objects, or 
        tuple(universe ID, transformation ID). When providing IDs, `universes` 
        and `transformations` must be specified. Use `0` for elements with 
        background fill.
    type : str, optional
        Lattice type, 'REC' or 'HEX'
    universes : dict, optional
        Dictionary mapping universe IDs to `mcnpy.Univese` objects.
    transformations : dict, optional
        Dictionary mapping Transformation IDs to `mcnpy.Transformation` objects.
        Note that that the values can also be `mcnpy.Transforms` if an appropriate
        ID is used when defining `lattice`.

    """
    
    def __init__(self, i=[], j=[], k=[], lattice=None, type='REC', 
                 universes=None, transformations=None):
        """Class for lattices. Defined by max indicies `i`, `j`, `k`, and a 3D array `lattice`. The array should be defined using `numpy.array()` where `k` indicies are your outermost dimension followed by `j` and `i`. Elements of `lattice` can be `LatticeElement` objects, universe IDs, tuple(universe ID, transformation ID), or 0. When using IDs, `universes` and `transformations` must include the key value pair of ID and object. Using `Transforms` instead of `Transformations` is also allowed.
        """
        self._i = i
        self._j = j
        self._k = k
        self._type = type
        self._universes = universes
        self._transformations = transformations
        self._lattice = lattice

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, i):
        self._i = i

    @property
    def j(self):
        return self._j

    @j.setter
    def j(self, j):
        self._j = j

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, k):
        self._k = k

    @property
    def dims(self):
        _dims = []
        _dims.append(self.i[1]-self.i[0]+1)
        _dims.append(self.j[1]-self.j[0]+1)
        _dims.append(self.k[1]-self.k[0]+1)
        return _dims

    @property
    def size(self):
        return int(self.dims[0]*self.dims[1]*self.dims[2])

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if (str(type).upper() == 'REC' or str(type).upper() == 'RECTANGULAR' 
        or str(type) == '1'):
            self._type = 'REC'
        elif (str(type).upper() == 'HEX' or str(type).upper() == 'HEXAGONAL' 
        or str(type) == '2'):
            self._type = 'HEX'
        else:
            self._type = str(type) + ' (INVALID!)'

    @property
    def universes(self):
        return self._universes

    @universes.setter
    def universes(self, universes):
        self._universes = universes

    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, lattice):
        self._lattice = lattice

    @property
    def transformations(self):
        return self._transformations

    @transformations.setter
    def transformations(self, transformations):
        self._transformations = transformations

    def make_element(self, element):
        if isinstance(element, (tuple, list)) is False:
            _element = [element]
        else:
            _element = list(element)
        if _element[0] == 0:
            return Lattice.Element(0)
        elif isinstance(_element[0], Lattice.Element):
            return _element[0]
        else:
            if _element[0] != 0:
                _element[0] = self.universes[int(_element[0])]
            if len(_element) == 1:
                return Lattice.Element(_element[0])
            else:
                if _element[1] != 0:
                    _element[1] = self.transformations[int(_element[1])]
                return Lattice.Element(_element)

    def as_ids(self):
        universes = {}
        transformations = {}
        dim = self.dims[::-1]
        _lattice = np.empty(shape=dim, dtype='object')
        for k in range(dim[0]):
            for j in range(dim[1]):
                for i in range(dim[2]):
                    el = self.lattice[k,j,i].element
                    _el = [0, 0]
                    if el[0] != 0:
                        _el[0] = int(el[0].name)
                        if int(el[0].name) not in universes:
                            universes[int(el[0].name)] = el[0]._e_object
                    if el[1] != 0:
                        if isinstance(el[1], Transform):
                            in_dict = True
                            while in_dict is True:
                                num = random.randint(1, 2147483647)
                                if num not in transformations:
                                    in_dict = False
                                    _el[1] = num
                                    transformations[num] = el[1]._e_object
                        else:
                            _el[1] = int(el[1].name)
                            if int(el[1].name) not in transformations:
                                universes[int(el[1].name)] = el[1]._e_object
                    _lattice[k,j,i] = tuple(_el)
        
        self.universes = universes
        self.transformations = transformations
        self.lattice = _lattice

    def flatten(self):
        """Flattens the provided lattice.
        """
        lattice = self.lattice.flatten()#.astype('int32')
        _lattice = []
        for i in range(self.lattice.size):
            if self.universes is not None:
                _lattice.append(self.make_element(lattice[i]))
            else:
                _lattice.append(lattice[i]._e_object)
        return _lattice
            
    def rings(self):
        """For HEX lattices. Lattice must have equal X and Y dimensions. Returns a list of rings describing the lattice. 
        """
        num_rings = int((self.dims[0]-1) / 2) + 1
        rings = []
        for k in range(self.dims[2]):
            rings.append([])
            for r in range(num_rings - 1):
                ring_a = []
                ring_b = []
                ring_c = []
                for j in range(self.dims[1]):
                    index = num_rings - 1 - j
                    stop = len(self.lattice[k,j]) - r 
                    if index > 0:
                        if r == j:
                            ring_c += list(self.lattice[k, j, index+r:stop])
                        elif r - j < 0:
                            ring_c.append(self.lattice[k, j, stop-1])
                            ring_b.append(self.lattice[k, j, index+r])
                    elif index < 0:
                        if r == 2*index + j:
                            ring_b += list(self.lattice[k, j, r:stop+index])
                        elif r - (2*index + j) < 0:
                            ring_a.append(self.lattice[k, j, stop+index-1])
                            ring_b.append(self.lattice[k, j, r])
                    else:
                        ring_c.append(self.lattice[k, j, stop-1])
                        ring_b.append(self.lattice[k, j, r])
                rings[k].append(ring_c[::-1] + ring_b + ring_a[::-1])

            rings[k].append([self.lattice[k, num_rings-1, num_rings-1]])

        return (rings, num_rings)
        
    def __repr__(self):
            string = 'Lattice\n'
            string += '{: <16}=\t{}\n'.format('\tType', str(self.type))
            string += '{: <16}=\t{}\n'.format('\tI', str(self.i))
            string += '{: <16}=\t{}\n'.format('\tJ', str(self.j))
            string += '{: <16}=\t{}\n'.format('\tK', str(self.k))
            string += '{: <16}=\t{}\n'.format('\tI', str(self.i))
            string += '{: <16}=\t{}\n'.format('\tElements', '\n' 
                                              + np.array2string(self.lattice, 
                                                                separator=' '))

            return string

    class Element(LatticeElementBase):
        """
        
        A representation of the model object `Lattice.Element`.

        Parameters
        ----------
        element : list or tuple
            A `mcnpy.Universe` with optional `mcnpy.Transform` or `mcnpy.Transformation`.
        
        """
        
        def _init(self, element):
            """
            """
            self.element = element

        def __str__(self):
            if self.element[0] == 0:
                string = '(U' + str(self.element[0])
            else:
                string = '(' + str(self.element[0])
            string += ', TR' + str(self.element[1]) + ')'
            return string

        def __repr__(self):
            return str(self)

        @property
        def element(self):
            if self._e_object.getTransformation() is None:
                if self._e_object.getTransform() is None:
                    if self._e_object.getFill() is None:
                        return (0, 0)
                    else:
                        return (self._e_object.getFill(), 0)
                else:
                    if self._e_object.getFill() is None:
                        return (0, self._e_object.getTransform())
                    else:
                        return (self._e_object.getFill(), 
                                self._e_object.getTransform())
            else:
                if self._e_object.getFill() is None:
                    return (0, self._e_object.getTransformation())
                else:
                    return (self._e_object.getFill(), 
                            self._e_object.getTransformation())
        
        @element.setter
        def element(self, element):
            #self._e_object.setBackground(None)
            if isinstance(element, (list, tuple)):
                if element[0] == 0:
                    self._e_object.setBackground(0)
                    #self._e_object.setFill(None)
                else:
                    #self._e_object.setBackground(None)
                    self._e_object.setFill(element[0])
                if element[1] != 0:
                    if isinstance(element[1], Transform):
                        self._e_object.setTransform(element[1])
                        #self._e_object.setTransformation(None)
                    else:
                        #self._e_object.setTransform(None)
                        #if element[1] == 0:
                        #    self._e_object.setTransformation(None)
                        #else:
                        self._e_object.setTransformation(element[1])
            elif element == 0:
                self._e_object.setBackground(0)
                #self._e_object.setFill(None)
                #self._e_object.setTransform(None)
                #self._e_object.setTransformation(None)
            else:
                #self._e_object.setBackground(None)
                self._e_object.setFill(element._e_object)
                #self._e_object.setTransform(None)
                #self._e_object.setTransformation(None)

    class Range(LatticeRangeBase):
        """
        A representation of the model object `Lattice.Range`.
        
        Parameters
        ----------
        i0 : mcnpy.Lattice.Range.Int
            I0 for `Lattice.Range`.
        i1 : mcnpy.Lattice.Range.Int
            I1 for `Lattice.Range`.
        j0 : mcnpy.Lattice.Range.Int
            J0 for `Lattice.Range`.
        j1 : mcnpy.Lattice.Range.Int
            J1 for `Lattice.Range`.
        k0 : mcnpy.Lattice.Range.Int
            K0 for `Lattice.Range`.
        k1 : mcnpy.Lattice.Range.Int
            K1 for `Lattice.Range`.
        
        """

        def _init(self, i0, j0, k0, i1=None, j1=None, k1=None):
            if i0 is not None:
                self.i0 = Lattice.Range.Int(i0)
            if i1 is not None:
                self.i1 = Lattice.Range.Int(i1)
            if j0 is not None:
                self.j0 = Lattice.Range.Int(j0)
            if j1 is not None:
                self.j1 = Lattice.Range.Int(j1)
            if k0 is not None:
                self.k0 = Lattice.Range.Int(k0)
            if k1 is not None:
                self.k1 = Lattice.Range.Int(k1)

        @property
        def rrange(self):
            range = []
            range.append(self._e_object.getI0())
            range.append(self._e_object.getI1())
            range.append(self._e_object.getJ0())
            range.append(self._e_object.getJ1())
            range.append(self._e_object.getK0())
            range.append(self._e_object.getK1())

            return range

        @rrange.setter
        def rrange(self, range):
            if isinstance(range[0], Lattice.Range.Int):
                self._e_object.setI0(range[0])
            else:
                self._e_object.setI0(Lattice.Range.Int(range[0]))

            if isinstance(range[1], Lattice.Range.Int) or range[1] is None:
                self._e_object.setI1(range[1])
            else:
                self._e_object.setI1(Lattice.Range.Int(range[1]))

            if isinstance(range[2], Lattice.Range.Int) or range[2] is None:
                self._e_object.setJ0(range[2])
            else:
                self._e_object.setJ0(Lattice.Range.Int(range[2]))

            if isinstance(range[3], Lattice.Range.Int) or range[3] is None:
                self._e_object.setJ1(range[3])
            else:
                self._e_object.setJ1(Lattice.Range.Int(range[3]))

            if isinstance(range[4], Lattice.Range.Int) or range[4] is None:
                self._e_object.setK0(range[4])
            else:
                self._e_object.setK0(Lattice.Range.Int(range[4]))

            if isinstance(range[5], Lattice.Range.Int) or range[5] is None:
                self._e_object.setK1(range[5])
            else:
                self._e_object.setK1(Lattice.Range.Int(range[5]))

        def __str__(self):
            string = '[ '
            if self.i1 is not None:
                string += str(self.i0) + ':' + str(self.i1) + ' '
            else:
                string += str(self.i0) + ' '

            if self.j1 is not None:
                string += str(self.j0) + ':' + str(self.j1) + ' '
            else:
                string += str(self.j0) + ' '

            if self.k1 is not None:
                string += str(self.k0) + ':' + str(self.k1) + ' ]'
            else:
                string += str(self.k0) + ' ]'

            return string

        class Int(RangeIntBase):
            """
            A representation of the model object `Lattice.Range.Int`.
            
            Parameters
            ----------
            sign : str
                Sign for `Lattice.Range.Int`.
            value : int
                Value for `Lattice.Range.Int`.
            
            """

            def _init(self, value):
                """
                """
                self.value = value
                """if value < 0:
                    self.sign = '-'
                else:
                    self.sign = sign"""

            @property
            def value(self):
                if self._e_object.getSign().toString() == '-':
                    return -1 * self._e_object.getValue()
                else:
                    return self._e_object.value

            @value.setter
            def value(self, value):
                if value < 0:
                    self._e_object.setSign('-')
                self._e_object.setValue(abs(value))

            def __str__(self):
                if self.sign is not None:
                    return str(self.sign) + str(self.value)
                else:
                    return str(self.value)

    class Coordinate(LatticeCoordinateBase):
        """
        A representation of the model object `Lattice.Coordinate`.
        
        Parameters
        ----------
        i : int
            I for `Lattice.Coordinate`.
        j : int
            J for `Lattice.Coordinate`.
        k : int
            K for `Lattice.Coordinate`.
        
        """

        def _init(self, i, j, k):
            self.i = i
            self.j = j
            self.k = k

        @property
        def coordinate(self):
            return (self._e_object.getI(), self._e_object.getJ(), 
                    self._e_object.getK())

        @coordinate.setter
        def coordinate(self, coord):
            self._e_object.setI(coord[0])
            self._e_object.setJ(coord[1])
            self._e_object.setK(coord[2])

        def __str__(self):
            return ('( ' + str(self.i) + ' ' + str(self.j) + ' ' 
                    + str(self.k) + ' )')

    class Coordinates(LatticeCoordinatesBase):
        """
        A representation of the model object `Lattice.Coordinates`.
        
        Parameters
        ----------
        coordinates : iterable of mcnpy.Lattice.Coordinate
            Coordinates for `Lattice.Coordinates`.
        
        """

        def _init(self, coordinates:list):
            self.coordinates = coordinates

        @property
        def coordinates(self):
            _coords = self._e_object.getCoordinates()
            coords = []
            for i in _coords:
                coords.append(i.coordinate)
            return coords

        @coordinates.setter
        def coordinates(self, coords):
            _coords = self._e_object.getCoordinates()
            del _coords[:]
            for i in coords:
                if isinstance(i, Lattice.Coordinate):
                    _coords.append(i)
                else:
                    coord = Lattice.Coordinate()
                    coord.coordinate = i
                    _coords.append(coord)

        def __str__(self):
            string = '[ '
            for i in range(len(self.coordinates)):
                string += str(self.coordinates[i])
                if (i != len(self.coordinates)):
                    string += ', '
            string += ' ]'
            return string

    class FlatIndex(LatticeFlatIndexBase):
        """
        A representation of the model object `Lattice.FlatIndex`.
        
        Parameters
        ----------
        i : int
            I for `Lattice.FlatIndex`.
        
        """

        def _init(self, i):
            self.i = i

        def __str__(self):
            return str(self.i)

    class Index(LatticeIndexBase):
        """
        A representation of the model object `Lattice.Index`.
        
        Parameters
        ----------
        index : Object
            Index for `Lattice.Index`.
        universe : mcnpy.Universe
            Universe for `Lattice.Index`.
        
        """

        def _init(self, index=None, universe=None):
            self.index = index
            self.universe = universe #TODO: check this option

        def __str__(self):
            return str(self.index)

        @property
        def index(self):
            _index = self._e_object.getIndex()
            if isinstance(_index, Lattice.FlatIndex):
                return _index.i
            elif isinstance(_index, Lattice.Coordinates):
                return _index.coordinates
            elif isinstance(_index, Lattice.Range):
                return _index.rrange

        @index.setter
        def index(self, index):
            if isinstance(index, int):
                self._e_object.setIndex(Lattice.FlatIndex(index))
            elif isinstance(index, (list, tuple)):
                if isinstance(index[0], (list, tuple, Lattice.Coordinate)):
                    _index = Lattice.Coordinates()
                    _index.coordinates = index
                    self._e_object.setIndex(_index)
                elif isinstance(index[0], (int, Lattice.Range.Int)):
                    _index = Lattice.Range()
                    _index.rrange = index
                    self._e_object.setIndex(_index)
            else:
                self._e_object.setIndex(index)

class UniverseList():
    """Class to assign `mcnpy.Universe` objects to a list of `mcnpy.Cell` objects.

    Parameters
    ----------
    name : int
        The universe ID number.
    cells : iterable of mcnpy.Cell, optional
        List of cells.
    sign : str, optional
        '-' turns off distance to universe boundary calculations.
    
    Attributes
    ----------
    name : int
        The universe ID number.
    cells : dict
        Dictionary storing all cells in the universe by their IDs.
    sign : str
        '-' turns off distance to universe boundary calculations.
    """
    def __init__(self, name, cells=None, sign=None):
        
        # self._e_object exists because the universe keyword on each cell
        # creates a separate referenceable object. Using self._e_object gives
        # the Universe class a singular reference.
        self._e_object = None
        self.name = name
        self.cells = {}
        self.sign = sign
        if cells is not None:
            if isinstance(cells, list):
                self.add_all(cells)
            else:
                self.add(cells)

    def apply_to_cell(self, cell):
        _universe = Universe(name=self.name)
        #_universe.name = self.name
        if self.sign is not None:
            _universe.sign = self.sign
        cell.universe = _universe

        # self._e_object is set to the reference of the universe keyword of 
        # the first cell listed.
        if self._e_object is None:
            self._e_object = _universe._e_object

        return cell

    def add(self, cell):
        """Add a cell to a `mcnpy.UniverseList`.

        Parameters
        ----------
        cell : mcnpy.Cell
            Cell to be added.
        """

        self.cells[cell.name] = self.apply_to_cell(cell)

    def add_all(self, cells):
        """Add a list of cells to a `mcnpy.UniverseList`.

        Parameters
        ----------
        cells : iterable of mcnpy.Cell
            Cells to be added.
        """

        for cell in cells:
            self.add(cell)

    def remove(self, cell):
        """Remove a cell from a `mcnpy.UniverseList`.

        Parameters
        ----------
        cell : mcnpy.Cell
            Cell to be removed.
        """

        del self.cells[cell.name]
        # This should ensure that references aren't broken when removing cells
        # from the universe. 
        if self._e_object == cell.universe:
            key = list(self.cells.keys())[0]
            #self._e_object = self.cells[key].universe
            self.cells[key].universe = self._e_object
        cell.universe = None

    def remove_all(self, cells):
        """Remove a list of cells from a `mcnpy.UniverseList`.

        Parameters
        ----------
        cells : iterable of mcnpy.Cell
            Cells to be removed.
        """

        for cell in cells:
            self.remove(cell)

    def add_only(self, cell):
        self.cells[cell.name] = cell

class Universe(UniverseBase):
    """
    A representation of the model object `Universe`.
    
    Parameters
    ----------
    sign : str
        Sign for `Universe`.
    name : int
        Name for `Universe`.
    
    """

    def _init(self, name):
        self.name = name

    @property
    def name(self):
        return int(self._e_object.getName())

    @name.setter
    def name(self, name):
        self._e_object.setName(str(name))
        
    def __str__(self):
        return 'U' + str(self.name)

    def __repr__(self):
        return 'U' + str(self.name)

class Universes(UniversesBase):
    """
    A representation of the model object `Universes`.
    
    Parameters
    ----------
    
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

subclass_overrides(Cell)
subclass_overrides(Transform)
subclass_overrides(Embedded)
subclass_overrides(Partisn)
subclass_overrides(StochasticGeometry)
subclass_overrides(Deterministic)
subclass_overrides(Lattice)