import numpy as np
from abc import ABC
from .wrap import wrappers, overrides

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class GeometrySetting(ABC):
    """
    """

class Transformation(TransformationBase, GeometrySetting):
    """TR
    """
    def _init(self, name, transformation, unit=None):
        """`transformation` must be a `Transform` or a list containing at least a displacement.
        """
        self.name = name
        if isinstance(transformation, tuple) or isinstance(transformation, list):
            if len(transformation) == 1:
                self.transformation = Transform(transformation[0])
            elif len(transformation) == 2:
                self.transformation = Transform(transformation[0], transformation[1])
            else:
                self.transformation = Transform(transformation[0], transformation[1], self.transformation[2])
        else:
            self.transformation = transformation
            

        if unit is not None:
            self.unit = unit

class Transform(TransformBase):
    """
    """
    def _init(self, displacement, rotation=None, m=None):
        """
        """
        self.disp1 = displacement[0]
        self.disp2 = displacement[1]
        self.disp3 = displacement[2]

        self.displacement = [self.disp1, self.disp2, self.disp3]

        if rotation is not None:
            if isinstance(rotation, RotMatrix):
                self.rotation = rotation
            else:
                self.rotation = RotMatrix(rotation, m)

class RotMatrix(RotMatrixBase):
    """
    """
    def _init(self, matrix, m=None):
        """`matrix` is a 3x3 numpy array in the form
        `[[xx, yx, zx], [xy, yy, zy], [xz, yz, zz]]` 
        """
        self.xx = matrix[0, 0]
        self.yx = matrix[0, 1]
        self.zx = matrix[0, 2]

        self.xy = matrix[1, 0]
        self.yy = matrix[1, 1]
        self.zy = matrix[1, 2]

        self.xz = matrix[2, 0]
        self.yz = matrix[2, 1]
        self.zz = matrix[2, 2]

        self.matrix = np.array([[self.xx, self.yx, self.zx], [self.xy, self.yy, self.zy], [self.xz, self.yz, self.zz]], dtype=float)

        if m is not None:
            self.m = m

class Volumes(VolumesBase, GeometrySetting):
    """VOL
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Areas(AreasBase, GeometrySetting):
    """AREA
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class Fills(FillsBase, GeometrySetting):
    """FILL
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class StochasticGeometry(StochasticGeometryBase, GeometrySetting):
    """URAN
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicMaterials(DeterministicMaterialsBase, GeometrySetting):
    """DM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class DeterministicWeightWindowGenerator(DeterministicWeightWindowGeneratorBase, GeometrySetting):
    """DAWWG
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedGeometry(EmbeddedGeometryBase, GeometrySetting):
    """EMBED
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEdit(EmbeddedEditBase, GeometrySetting):
    """EMBEE
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditEnergyBins(EmbeddedEditEnergyBinsBase, GeometrySetting):
    """EMBEB
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditEnergyBinMultipliers(EmbeddedEditEnergyBinMultipliersBase, GeometrySetting):
    """EMBEM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditTimeBins(EmbeddedEditTimeBinsBase, GeometrySetting):
    """EMBTB
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditTimeBinMultipliers(EmbeddedEditTimeBinMultipliersBase, GeometrySetting):
    """EMBTM
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditDoseBins(EmbeddedEditDoseBinsBase, GeometrySetting):
    """EMBDE
    """
    def _init(self, **kwargs):
        """
        """
        for k in kwargs:
            setattr(self, k.lower(), kwargs[k])

class EmbeddedEditDoseBinMultipliers(EmbeddedEditDoseBinMultipliersBase, GeometrySetting):
    """EMBDF
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