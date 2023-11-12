"""
Copyright (c) 2011-2023 Massachusetts Institute of Technology, UChicago Argonne
LLC, and OpenMC contributors

Copyright (c) 2023 NuCoMP

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from numbers import Integral
from warnings import warn

import numpy as np

import mcnpy.checkvalue as cv


class EqualityMixin:
    """A Class which provides a generic __eq__ method that can be inherited
    by downstream classes.
    """

    def __eq__(self, other):
        if isinstance(other, type(self)):
            for key, value in self.__dict__.items():
                if isinstance(value, np.ndarray):
                    if not np.array_equal(value, other.__dict__.get(key)):
                        return False
                else:
                    return value == other.__dict__.get(key)
        else:
            return False

        return True


class IDWarning(UserWarning):
    pass

class NoIDMixin:
    """Data cards that have no form of ID number."""
    #TODO: Name them by class or keyword for dict storage.
    pass

class IDManagerMixin:
    """A Class which automatically manages unique IDs.
    This mixin gives any subclass the ability to assign unique IDs through a
    'name' property and keeps track of which ones have already been
    assigned. Crucially, each subclass must define class variables 'next_id' and
    'used_ids' as they are used in the 'name' property that is supplied here.
    """

    @property
    def name(self):
        if self._e_object.getName() is None:
            return None
        else:
            return int(self._e_object.getName())

    @name.setter
    def name(self, uid):
        # The first time this is called for a class, we search through the MRO
        # to determine which class actually holds next_id and used_ids. Since
        # next_id is an integer (immutable), we can't modify it directly through
        # the instance without just creating a new attribute
        try:
            cls = self._id_class
        except AttributeError:
            for cls in self.__class__.__mro__:
                if 'next_id' in cls.__dict__:
                    break
        try:
            inc = cls.increment
        except:
            inc = 1
        if uid is None:
            while cls.next_id in cls.used_ids:
                cls.next_id += inc
            self._e_object.setName(str(cls.next_id))
            cls.used_ids.add(cls.next_id)
        else:
            name = cls.__name__
            cv.check_type(f'{name} ID', uid, Integral)
            cv.check_greater_than(f'{name} ID', uid, 0, equality=True)
            if uid in cls.used_ids:
                msg = f'Another {name} instance already exists with id={uid}.'
                warn(msg, IDWarning)
            else:
                cls.used_ids.add(uid)
            self._e_object.setName(str(uid))


def reset_auto_ids():
    """Reset counters for all auto-generated IDs"""
    for cls in IDManagerMixin.__subclasses__():
        cls.used_ids.clear()
        cls.next_id = 1


def reserve_ids(ids, cls=None):
    """Reserve a set of IDs that won't be used for auto-generated IDs.
    Parameters
    ----------
    ids : iterable of int
        IDs to reserve
    cls : type or None
        Class for which IDs should be reserved (e.g., :class:`openmc.Cell`). If
        None, all classes that have auto-generated IDs will be used.
    """
    if cls is None:
        for cls in IDManagerMixin.__subclasses__():
            cls.used_ids |= set(ids)
    else:
        cls.used_ids |= set(ids)


def set_auto_id(next_id):
    """Set the next ID for auto-generated IDs.
    Parameters
    ----------
    next_id : int
        The next ID to assign to objects with auto-generated IDs.
    """
    for cls in IDManagerMixin.__subclasses__():
        cls.next_id = next_id