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
            self.cell = node
            # I think this will decompose cell complements.
            # Sort of works, probably doesn't comply for nested complements.
            #self.node = node.region
        else:
            self.node = node

    def __str__(self):
        if self.node is not None:
            if isinstance(self.node, mcnpy.surfaces.Halfspace):
                return str(~self.node)
            else:
                return ('~' + str(self.node)).replace('~~', '')
        else:
            return ('~' + self.cell.name).replace('~~', '')

for name, wrapper in overrides.items():
    override = globals().get(name, None)
    if override is not None:
        overrides[name] = override