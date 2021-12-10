from collections import OrderedDict
from collections.abc import MutableSequence
from abc import ABC

from mcnpy.wrap import wrappers, overrides
import mcnpy
#from mcnpy.surfaces import Halfspace
#from mcnpy.cells import Cell

globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

class Region(RegionBase, ABC):
    #My custom region class.

    def __and__(self, other):
        return Intersection((self, other))

    def __or__(self, other):
        return Union((self, other))

    def __invert__(self):
        return Complement(self)

    def get_surfaces(self, surfaces=None):
        """Recursively find all surfaces referenced by a region and return them

        Parameters
        ----------
        surfaces: collections.OrderedDict, optional
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        Returns
        -------
        surfaces: collections.OrderedDict
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        """
        if surfaces is None:
            surfaces = OrderedDict()
        for region in self:
            surfaces = region.get_surfaces(surfaces)
        return surfaces

    def remove_redundant_surfaces(self, redundant_surfaces):
        """Recursively remove all redundant surfaces referenced by this region

        .. versionadded:: 0.12

        Parameters
        ----------
        redundant_surfaces : dict
            Dictionary mapping redundant surface IDs to class:`mcnpy.Surface`
            instances that should replace them.

        """
        for region in self:
            region.remove_redundant_surfaces(redundant_surfaces)

class Intersection(IntersectionBase, Region, MutableSequence):
    """My custom intersection class."""

    def _init(self, nodes):
        self.nodes = nodes

    def __and__(self, other):
        new = Intersection(self)
        new &= other
        return new

    def __iand__(self, other):
        if isinstance(other, Intersection):
            self.extend(other)
        else:
            self.nodes.addUnique(other._e_object)
            #self.append(other)
        return self

    # Implement mutable sequence protocol by delegating to list
    def __getitem__(self, key):
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __delitem__(self, key):
        del self.nodes[key]

    def __len__(self):
        return len(self.nodes)

    def insert(self, index, value):
        self.nodes.insert(index, value)

    def __str__(self):
        return '(' + ' '.join(map(str, self)) + ')'

class Union(UnionBase, Region, MutableSequence):
    """My custom union class."""

    def _init(self, nodes):
        self.nodes = nodes

    def __or__(self, other):
        new = Union(self)
        new |= other
        return new

    def __ior__(self, other):
        if isinstance(other, Union):
            self.extend(other)
        else:
            self.nodes.addUnique(other._e_object)
            #self.append(other)
        return self

    # Implement mutable sequence protocol by delegating to list
    def __getitem__(self, key):
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __delitem__(self, key):
        del self.nodes[key]

    def __len__(self):
        return len(self.nodes)

    def insert(self, index, value):
        self.nodes.insert(index, value)

    def __str__(self):
        return '(' + ' | '.join(map(str, self)) + ')'

class Complement(ComplementBase, Region):
    def _init(self, node):
        if isinstance(node, mcnpy.cells.Cell):
            #self.cell = node
            # I think this will decompose cell complements.
            # Sort of works, probably doesn't comply for nested complements.
            self.node = node.region
        else:
            self.node = node

    def __str__(self):
        if self.node is not None:
            if isinstance(self.node, mcnpy.surfaces.Halfspace):
                return str(~self.node)
            else:
                return ('~' + str(self.node)).replace('~~', '')
        else:
            return ('~' + str(self.cell.region)).replace('~~', '')

    def get_surfaces(self, surfaces=None):
        """Recursively find and return all the surfaces referenced by the node

        Parameters
        ----------
        surfaces: collections.OrderedDict, optional
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        Returns
        -------
        surfaces: collections.OrderedDict
            Dictionary mapping surface IDs to :class:`mcnpy.Surface` instances

        """
        if surfaces is None:
            surfaces = OrderedDict()
        #print('\nNode:', self.node)
        #if isinstance(self.node, mcnpy.surfaces.Halfspace):
        #    surfaces = self.node.get_surfaces(surfaces)
        try:
            for region in self.node:
                surfaces = region.get_surfaces(surfaces)
        except:
            surfaces = self.node.get_surfaces(surfaces)
        return surfaces

    def remove_redundant_surfaces(self, redundant_surfaces):
        """Recursively remove all redundant surfaces referenced by this region

        .. versionadded:: 0.12

        Parameters
        ----------
        redundant_surfaces : dict
            Dictionary mapping redundant surface IDs to class:`mcnpy.Surface`
            instances that should replace them.

        """
        for region in self.node:
            region.remove_redundant_surfaces(redundant_surfaces)

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override