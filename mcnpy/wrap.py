from py4j.protocol import register_output_converter, register_input_converter, REFERENCE_TYPE
from metapy.gateway import ePackage
from metapy.wrap import wrap_e_object, wrap_e_package, e_class_body, _subclass_overrides

overrides = {}
package_name = 'mcnpy'
numeric_ids = True

# Apply overrides to nested subclasses.
# Can provide a custom naming prefix and classes to ignore.
def subclass_overrides(klass, prefix=None, ignore=[], package_name=package_name, overrides=overrides):
    _subclass_overrides(klass, prefix, ignore, package_name, overrides)

class WrapperConverter(object):
    def can_convert(self, object):
        return type(object).__bases__[0].__name__ in overrides

    def convert(self, object, gateway_client):
        return object._e_object

# Defined per package to ensure proper wrapper ownership.
def wrap_e_class(e_class, e_factory, InternalEObject, overrides):
    """Return a Python class which wraps and implements an EClass."""

    return type(e_class.getName(), (InternalEObject,), 
                e_class_body(e_class, e_factory, overrides, numeric_ids))

register_input_converter(WrapperConverter(), prepend=True)

# Start with the auto-wrapping turned on.
register_output_converter(REFERENCE_TYPE, 
    (lambda target_id, 
    gateway_client: wrap_e_object(target_id, gateway_client, overrides)))

wrappers = wrap_e_package(ePackage(package_name), overrides, wrap_e_class)
overrides.update(wrappers)