import numpy as np
from abc import ABC
from .wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class GeometrySetting(ABC):
    """
    """

class Transformation(TransformationBase, GeometrySetting):
    """TR Card
    
    Parameters
    ----------
    name : str
        Unique ID for the transformation.
    transformation : mcnpy.geometry.Transform or nested list
        The transformation itself descriped as a Transform or a list. The list may contain up to 3 items. First a list of displacements, second a 3x3 array describing the rotation matrix, and third the 'm' value specifiying the rotation reference frame.
    """
    def _init(self, name, transformation, unit=None):
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
    __doc__ = TransformBase().__doc__

    def _init(self, displacement, rotation=None, m=None):
        """
        """

        self.displacement = displacement

        if rotation is not None:
            if isinstance(rotation, RotMatrix):
                self.rotation = rotation
            else:
                self.rotation = RotMatrix(rotation, m)

    @property
    def displacement(self):
        return [self.disp1, self.disp2, self.disp3]

    @displacement.setter
    def displacement(self, disp):
        self.disp1 = disp[0]
        self.disp2 = disp[1]
        self.disp3 = disp[2]

class RotMatrix(RotMatrixBase):
    __doc__ = RotMatrixBase().__doc__

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
    __doc__ = VolumesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Areas(AreasBase, GeometrySetting):
    __doc__ = AreasBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Fills(FillsBase, GeometrySetting):
    __doc__ = FillsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class StochasticGeometry(StochasticGeometryBase, GeometrySetting):
    __doc__ = StochasticGeometryBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicMaterials(DeterministicMaterialsBase, GeometrySetting):
    __doc__ = DeterministicMaterialsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicWeightWindowGenerator(DeterministicWeightWindowGeneratorBase, GeometrySetting):
    __doc__ = DeterministicWeightWindowGeneratorBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedGeometry(EmbeddedGeometryBase, GeometrySetting):
    __doc__ = EmbeddedGeometryBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEdit(EmbeddedEditBase, GeometrySetting):
    __doc__ = EmbeddedEditBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditEnergyBins(EmbeddedEditEnergyBinsBase, GeometrySetting):
    __doc__ = EmbeddedEditEnergyBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditEnergyBinMultipliers(EmbeddedEditEnergyBinMultipliersBase, GeometrySetting):
    __doc__ = EmbeddedEditEnergyBinMultipliersBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditTimeBins(EmbeddedEditTimeBinsBase, GeometrySetting):
    __doc__ = EmbeddedEditTimeBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditTimeBinMultipliers(EmbeddedEditTimeBinMultipliersBase, GeometrySetting):
    __doc__ = EmbeddedEditTimeBinMultipliersBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditDoseBins(EmbeddedEditDoseBinsBase, GeometrySetting):
    __doc__ = EmbeddedEditDoseBinsBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditDoseBinMultipliers(EmbeddedEditDoseBinMultipliersBase, GeometrySetting):
    __doc__ = EmbeddedEditDoseBinMultipliersBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Lattices(LatticesBase):
    __doc__ = LatticesBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class StochasticGeometryTransformation(StochasticGeometryTransformationBase):
    __doc__ = StochasticGeometryTransformationBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class PartisnBlockOne(PartisnBlockOneBase):
    __doc__ = PartisnBlockOneBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class PartisnBlockThree(PartisnBlockThreeBase):
    __doc__ = PartisnBlockThreeBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class PartisnBlockFive(PartisnBlockFiveBase):
    __doc__ = PartisnBlockFiveBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

class PartisnBlockSix(PartisnBlockSixBase):
    __doc__ = PartisnBlockSixBase().__doc__

    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k, kwargs[k])

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override