from py4j.protocol import Py4JError, register_output_converter, register_input_converter, REFERENCE_TYPE
from py4j.java_gateway import JavaObject

from .gateway import gateway, is_instance_of
from .util import camel_to_snake_case


overrides = {}
# Used as a function in the output converter.
def wrap_e_object(target_id, gateway_client, wrappers=overrides):
    object = JavaObject(target_id, gateway_client)
    # Use string to avoid infinite loop.
    cls = str(object)
    cls = cls[cls.find('impl.')+5:cls.find('Impl')]
    if cls in wrappers:
        wrapped = wrappers[cls]()
        wrapped._e_object = object
        return wrapped
    return object

class WrapperConverter(object):
    def can_convert(self, object):
        return type(object).__name__ in overrides

    def convert(self, object, gateway_client):
        return object._e_object


register_input_converter(WrapperConverter(), prepend=True)

# Start with the auto-wrapping turned on.
register_output_converter(REFERENCE_TYPE, 
    (lambda target_id, 
    gateway_client: wrap_e_object(target_id, gateway_client)))


# Object meaning java.lang.Object
_OBJECT_METHODS = ('clone', 
                   'equals', 
                   'finalize', 
                   'getClass', 
                   'hashCode', 
                   'notify', 
                   'notifyAll', 
                   'toString', 
                   'wait')
_NOTIFIER_METHODS = ('eAdapters', 'eDeliver', 'eNotify', 'eSetDeliver')
_E_OBJECT_METHODS = ('eResource', 
                     'eContainer', 
                     'eContainingFeature', 
                     'eContainmentFeature', 
                     'eContents',
                     'eAllContents',
                     'eCrossReferences',
                     'eClass',
                     'eGet',
                     'eSet',
                     'eIsSet',
                     'eUnset',
                     'eIsProxy')
_INTERNAL_E_OBJECT_METHODS = ('eBaseStructuralFeatureID',
                              'eBasicRemoveFromContainer',
                              'eBasicSetContainer',
                              'eContainerFeatureID',
                              'eDerivedOperationID',
                              'eDerivedStructuralFeatureID',
                              'eDirectResource',
                              'eGet',
                              'eInternalContainer',
                              'eInternalResource',
                              'eInverseAdd',
                              'eInverseRemove',
                              'eInvoke',
                              'eIsSet',
                              'eNotificationRequired',
                              'eObjectForURIFragmentSegment',
                              'eProxyURI',
                              'eResolveProxy',
                              'eSet',
                              'eSetClass',
                              'eSetProxyURI',
                              'eSetResource',
                              'eSetStore',
                              'eSetting',
                              'eStore',
                              'eUnset',
                              'eURIFragmentSegment')


def delegate_methods(methods):
    """Delegate methods to `self._e_object`."""
    delegated_methods = {}
    for method in methods:
        def delegate_method(method=method):
            def delegated_method(self, *args, **kwargs):
                return getattr(self._e_object, method)(*args, **kwargs)
            return delegated_method
        delegated_methods[method] = delegate_method(method)
    return delegated_methods


# These classes do nothing but delegate methods to self._e_object
Object = type('Object', (object,), delegate_methods(_OBJECT_METHODS))
Notifier = type('Notifier', (Object,), delegate_methods(_NOTIFIER_METHODS))
_e_object_body = delegate_methods(_E_OBJECT_METHODS)
_e_object_body['_e_object'] = None
EObject = type('EObject', (Notifier,), _e_object_body)
InternalEObject = type('InternalEObject', (EObject,), 
                        delegate_methods(_INTERNAL_E_OBJECT_METHODS))


# Setter decorators applied to all properties
def replace_if_contained(feature):
    """Replace previous containing reference with a copy of the value."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if is_instance_of(feature, EReference) and feature.isContainment():
                """Avoids error with lists and tuples not having containing features."""
                """if isinstance(value, tuple) or isinstance(value, list) or value is None:
                    containing_feature = None #value[0].eContainingFeature()
                else:
                    containing_feature = value.eContainingFeature()"""
                try:
                    containing_feature = value.eContainingFeature()
                except:
                    containing_feature = None
                if containing_feature is not None:
                    value_copy = gateway.copier.copy(value._e_object)
                    gateway.copier.copyReferences()
                    value.eContainer().eSet(containing_feature, value_copy._e_object)
            return setter(self, value)
        return setter_decorated
    return decorator

def is_enum(value, feature):
    """Originally within string_or_int_to_enum.
    Serparate so it can be used by set_e_list."""
    EAttribute = gateway.jvm.org.eclipse.emf.ecore.EAttribute
    if is_instance_of(feature, EAttribute):
        EEnum = gateway.jvm.org.eclipse.emf.ecore.EEnum
        data_type = feature.getEAttributeType()
        str_or_int = isinstance(value, str) or isinstance(value, int)
        if is_instance_of(data_type, EEnum) and str_or_int:
            # String enums require upper case.
            if isinstance(value, str):
                value = value.upper()
            literal = data_type.getEEnumLiteral(value)
            if literal is None:
                literal = data_type.getEEnumLiteralByLiteral(value)
            if literal is not None:
                value = literal.getInstance()
    return value

def string_or_int_to_enum(feature):
    """Replace string or int with enum if applicable."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            value = is_enum(value, feature)
            return setter(self, value)
        return setter_decorated
    return decorator

def set_e_list(setter, feature, value):
    e_list = setter.eGet(feature, True)
    EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
    #print('HERE', feature)
    for i in range(len(value)):
        # Special treatment for universes on lattices.
        # TODO: see if there are other special cases like this.
        if type(value[i]).__name__ == 'Universe':
            e_list.addUnique(value[i]._e_object)
        elif type(value[i]).__name__ in overrides:
            value_copy = gateway.copier.copy(value[i]._e_object)
            gateway.copier.copyReferences()
            e_list.addUnique(value_copy._e_object)
        else:
            value[i] = is_enum(value[i], feature)
            try:
                e_list.addUnique(value[i])
            except:
                if isinstance(value[i], int):
                    e_list.addUnique(float(value[i]))
                elif isinstance(value[i], float):
                    e_list.addUnique(int(value[i]))
                else:
                    raise Exception('"' + str(value[i]) + '" of type '
                + str(type(value[i])) + ' is invalid for feature "'
                + str(feature.getName()) + '"')

def value_converter(setter, feature, value):
    """Provides type conversions when using setters."""
    try:
        # Because somehow the API allows any string as an ID... 
        # Now ID/name must be numeric.
        if isinstance(value, str) and feature.getName() == 'name':
            try:
                int(value)
            except:
                raise Exception('"' + value + '" is an invalid ID number')
        elif isinstance(value, str) and feature.getName() == 'comment':
            if value[0] != '$':
                value = '$ ' + value
        setter.eSet(feature, value)
    except:
        if isinstance(value, int):
            try:
                setter.eSet(feature, float(value))
            except:
                setter.eSet(feature, str(value))
        elif isinstance(value, float):
            # Only for round numbers.
            if value%1 == 0:
                try:
                    setter.eSet(feature, int(value))
                except:
                    setter.eSet(feature, str(value))
            else:
                raise Exception('"' + str(value) + '" of type '
            + str(type(value)) + ' is invalid for feature "'
            + str(feature.getName()) + '"')
        else:
                raise Exception('"' + str(value) + '" of type '
            + str(type(value)) + ' is invalid for feature "'
            + str(feature.getName()) + '"')


def set_wrapped_reference(feature):
    """Set references to Python wrappers of EObjects."""
    def decorator(setter, feature=feature):
        def setter_decorated(self, value):
            returned = setter(self, value)  # this should be None anyways
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if (is_instance_of(feature, EReference) and 
                    isinstance(value, EObject)):
                setattr(self, '_'+camel_to_snake_case(feature.getName()), value)
                if feature.isContainment():
                    value._eContainer = self  # needed in replace_if_contained
            return returned
        return setter_decorated
    return decorator


# Getter decorator applied to all properties
def get_wrapped_reference(feature):
    """Get references to Python wrappers of EObjects."""
    def decorator(getter, feature=feature):
        def getter_decorated(self):
            got = getter(self)
            EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
            if is_instance_of(feature, EReference) and got is not None:
                wrapped_reference = getattr(
                    self, '_'+camel_to_snake_case(feature.getName()), None)
                if (wrapped_reference is not None and
                        got.equals(wrapped_reference._e_object)):
                    return wrapped_reference
            return got
        return getter_decorated
    return decorator
            

def wrap_e_class(e_class, e_factory):
    """Return a Python class which wraps and implements an EClass."""
    def __init__(self, *args, **kwargs):
        """This might be a little sketchy, but the output converter for 
        automatic-wrapping is turned off and on. EObjects need to be 
        unwrapped for self._e_object = e_factory.create(e_class). Otherwise,
        we create an infinite loop of wrappers. In this case, we actually 
        want the unwrapped EObject. After this, we can turn the auto-wrapping
        back on. Not sure if there's a more elegant way to handle this."""
        register_output_converter(REFERENCE_TYPE, 
                (lambda target_id, 
                gateway_client: JavaObject(target_id, gateway_client)))
        self._e_object = e_factory.create(e_class)
        #print(self._e_object)
        register_output_converter(REFERENCE_TYPE, 
            (lambda target_id, 
            gateway_client: wrap_e_object(target_id, gateway_client)))
        if args or kwargs:
            self._init(*args, **kwargs)
    def _init(self):
        raise NotImplementedError  # this should be unreachable
    def __str__(self):
        return self.toString()
    def __hash__(self):
        return self.hashCode()
    def __eq__(self, other):
        # Tests structural equality, not identity
        equals = gateway.equalityHelper.equals
        if isinstance(other, EObject):
            return equals(self._e_object, other._e_object)
        try:
            return equals(self._e_object, other)
        except Py4JError:
            return False
    #class Java:
    #    implements = ['gov.lanl.mcnp.mcnp.'+e_class.getName(),
    #                  'org.eclipse.emf.ecore.InternalEObject']
    body = {attr.__name__: attr for attr in 
            (__init__, _init, __str__, __hash__, __eq__)}
    e_classes = [e_class]
    for e_cls in e_classes:
        for e_super_class in e_cls.getESuperTypes():
            e_classes.append(e_super_class)
        for feature in e_cls.getEStructuralFeatures():
            def make_property(feature=feature):
                #@get_wrapped_reference(feature)
                def getter(self):
                    #print('GETTER RETURN TYPE:', self._e_object.eGet(feature, True))
                    return self._e_object.eGet(feature, True)
                @replace_if_contained(feature)
                #@set_wrapped_reference(feature)
                @string_or_int_to_enum(feature)
                def setter(self, value):
                    if type(value).__name__ in overrides:
                        EReference = gateway.jvm.org.eclipse.emf.ecore.EReference
                        if is_instance_of(feature, EReference):
                            # This makes intersections with 3+ nodes work.
                            # TODO: make sure this is a real fix.
                            try:
                                self.eSet(feature, value._e_object)
                            except:
                                set_e_list(self, feature, value)
                        else:
                            value_copy = gateway.copier.copy(value._e_object)
                            gateway.copier.copyReferences()
                            self.eSet(feature, value_copy._e_object)
                    elif isinstance(value, tuple) or isinstance(value, list):
                        set_e_list(self, feature, value)
                    else:
                        value_converter(self, feature, value)
                            
                return property(getter, setter)
            snake_name = camel_to_snake_case(feature.getName())
            body[snake_name] = make_property(feature)
            cap_name = feature.getName().capitalize()
            body['get'+cap_name] = body[snake_name].fget
            body['set'+cap_name] = body[snake_name].fset
    return type(e_class.getName(), (InternalEObject,), body)


def wrap_e_package(e_package):
    """Wrap every EClass contained in an EPackage."""
    wrappers = {}
    e_factory = e_package.getEFactoryInstance()
    for classifier in e_package.getEClassifiers():
        EClass = gateway.jvm.org.eclipse.emf.ecore.EClass
        if not is_instance_of(classifier, EClass):
            continue
        wrappers[classifier.getName()] = wrap_e_class(classifier, e_factory)
    return wrappers


wrappers = wrap_e_package(gateway.ePackage)
overrides.update(wrappers)


_E_MODEL_ELEMENT_METHODS = ('getEAnnotation', 'getEAnnotations')
_E_FACTORY_METHODS = ('convertToString',
                      'create',
                      'createFromString',
                      'getEPackage',
                      'setEPackage')

EModelElement = type('EModelElement', (InternalEObject,), 
                      delegate_methods(_E_MODEL_ELEMENT_METHODS))
EFactory = type('EFactory', (EModelElement,), 
                 delegate_methods(_E_FACTORY_METHODS))


def wrap_e_factory(e_factory):
    pass  # TODO

