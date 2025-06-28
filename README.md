# MCNPy: The Python API for MCNP
![logo](https://github.rpi.edu/NuCoMP/mcnpy/blob/master/mcnpy_dark_text.png)

Latest version of MCNPy along with assorted test and example files. All source files are found in the `mcnpy` directory. For the installable wheel file, look in `dist`.


# Install Information
Read the [MCNPy Docs](https://pages.github.rpi.edu/NuCoMP/mcnpy_docs/build/html/getting_started.install.html)!

# More Information
Read the [MCNPy Docs](https://pages.github.rpi.edu/NuCoMP/mcnpy_docs/build/html/index.html)!

# Development Team & Contact Information
MCNPy and related work was developed by the [NuCoMP](nucomp.mane.rpi.edu) Research Group at Rensselaer Polytechnic Institute. This work started with the [MCNP Language Server](https://code.ornl.gov/neams-workbench/mcnp-language-server) and became intermingled with similar projects for the Serpent and KENO Monte Carlo codes. The following people have made significant contributions to this work during their time with NuCoMP:

- Peter Kowal
- Kurt Dominesey
- Joseph McPherson
- Jonathan Eugenio
- Camden Blake
- Wei Ji

## Contact
- Peter Kowal (mcnpy@rpi.slmail.me)
- Wei Ji (jiw2@rpi.edu)

# Technical Details for Developers

## Before You Get Started
Some guidelines so that future developers know what they might be getting into with this work:
1. Proficient in Python
    - If you can handle making classes and aren't scared off by reading source code, then you're probably fine
2. Familiarity with MCNP. Understand what features are available and know how to write input decks.
    - You need to understand the context in which the API classes can be used
3. Comfortable with Java
    - There is not a lot of Java code involved, but adding to or updating it is possible
    - Primarily, you'll have to debug Java error messages 

## Relationship Between Python and Java Components
The user-facing portion of MCNPy is written in Python, but internally calls are made to the Java classes from the metamodel implementation (the API we get starting with the MCNP grammar in Xtext). This is achieved by wrapping the Java classes with Python. Thus, MCNPy is essentially a collection of Python wrappers. This has a few key implications:
1. Java is required to run MCNPy
    - Somewhat obvious, but still important
2. Communication must be established between Python and Java
    - This is facilitated by the `Py4j` Python package. A Java server must be running which makes the desired Java code accessible to Python. This is handled by our `metapy` package (an MCNPy dependency).
3. Java classes must be wrapped
    - `Py4j` provides communication, but does not inherently provide wrappers. The wrapping process is handled dynamically by `metapy`. When MCNPy is imported, it will point `metapy` to the MCNP Java classes and request that they are wrapped. This means that any updates to the Java classes available to `metapy` will be inherited by MCNPy.
4. Wrappers can be customized
    - A basic wrapper will essentially be a "pythonic" version of the wrapped Java class. Custom wrappers can inherit the basic ones and add additional functionality.
    - Currently, all MCNPy wrappers have been at least lightly customized. The following shows one such wrapper:

            class Events(EventsBase):
            """
            A representation of the model object `Events`.
            
            Parameters
            ----------
            event : mcnpy.ParticleTrackEvent
                Event for `Events`.
            
            """

            def _init(self, **kwargs):
                """
                """
                for k in kwargs:
                    setattr(self, k, kwargs[k])

    - We see that `Events` inherits the `EventsBase` class and has a customized `_init` method and docstring. While basic, these customizations provide
        1. A more intuitive class name
        2. A class description for documentation
        3. Method overloading by keyword arguments
    - All source files providing wrappers also have the following header and footer:

            # HEADER
            from mcnpy.wrap import wrappers, overrides
            globals().update({name+'Base': wrapper for name, wrapper in wrappers.items()})

            # FOOTER
            for name, wrapper in overrides.items():
                override = globals().get(name, None)
                if override is not None:
                    overrides[name] = override

    - These ensure that the customized wrappers are correctly treated as replacements for the basic wrappers.
    - For better organization, certain wrappers appear as nested classes. E.g. `SourceInfo.Cells` instead of the default `SourceInfoCells`. To support this deviation from the Java class names, use the following:

            from mcnpy.wrap import subclass_overrides
            subclass_overrides(SourceInfo)

    - This ensures that the nested class wraps the intended Java class and that its wrapper overrides the default one. 

5. Wrapping, type conversions, and Python-Java communications can cause convoluted bugs
    - Because multiple languages are involved, debugging is more complex. A bug may actually be rooted in a different language than it manifests in. Or an operation may succeed for the wrapper class, but later breaks the Java classes.

## Custom Getters and Setters
A basic wrapper will include all necessary setter and getter methods for the class. These setters and getters benefit from automated type conversions included in the wrapping functions. Consequently, they will accept and return Python wrappers appropriately. To improve a class, overriding the default setters and getters can be desirable. This is done in the following fashion:

    # CUSTOM GETTER
    @property
    def name(self):
        value = self._e_object.getName()
        # Do things
        return value

    # CUSTOM SETTER
    @name.setter
    def name(self, value):
        # Do things
        self._e_object.setName(value)

where `name`, `getName`, and `setName` are the authentic names of the existing methods (or the literal names for any class with a `name` attribute). For any customizations, it is critical to always update the wrapped Java class (accessible through `._e_object`). Only storing information at the Python-level will cause information to be lost when serializing. Customize setters/getters as needed, but keep in mind that your custom functionality **replaces** any generated features. 

## Serialization Errors
Certain operations will appear to work just fine up until serialization is invoked. This is because only a valid model can be serialized. Most failures are from when required data is missing, misplaced, or conflicting options are present. 

### Missing Data
If the serializer can't find the required information, then it can't print it out. Since most class parameters are assigned a default value, this usually is not a problem. However, if something remains `null` while a value was expected, the simple solution is to assign a value. If you think a value should be there, but isn't, then debugging is in order. Using some print statements like

    print(my_python_object._e_object.toString())

throughout your code will narrow down when any parameters erroneously changed. The `._e_object` syntax accesses the underlying Java object. Since the serializer interacts with the Java, it's best to directly check the Java itself. 

### Misplaced Data
These errors are more confusing. Error messages along the lines of `Object does not exist for this Java gateway` indicate that a valid Java object exists, but it is owned by a different in-memory Java model. This is akin to one MCNP deck trying to reference cards from an entirely separate deck (without using special features like a READ card). These errors are most likely from incorrectly applied copying operations. To better understand copying nuances, consider the following CSG region definitions:

    region1 = -surf1 & -surf2

Regions are not their own MCNP cards and cannot be referenced directly. A single region definition can be freely reused across multiple cells (standalone or as part of a more complex region). However, each region is a unique Java object which can only appear in one place. Thus, by default, the following would produce an invalid model:

    cell1.region = region1
    cell2.region = region1

The result would be a `cell1` with an empty `region`. Since forcing the user to define multiple duplicate regions is nonsensical, region objects will instead be copied internally. So under the current implementation, `cell1` and `cell2` are both assigned regions semantically identical to `region1`, but each region is its own unique Java object. Such scenarios are why automated copy operations are implemented. 

Just as certain objects must be copied, others should not. Consider cells which are commonly referenced by other cards/classes. When referencing an object, the reference must point to the original object that is associated with the current deck/Java model. Overzealous copy operations can lead to references to objects that are not associated with the deck. If such an issue is suspected, look for calls to `.__copy__()` which is the copy function included in all wrapper classes. A related issue may be that the parent object was copied correctly, but its contained references were not. 

### Conflicting Options
Many classes contain options which are mutually exclusive. For instance, the `SourceParticle` class has the `particle` and `ion` attributes to support MCNP's built-in particle types along with the ZAID specification for heavy ions. Via the API, it is possible to create an object that has its `particle` and `ion` attributes set. This is not typically an issue when creating new objects, but can easily be overlooked when editing existing decks. By default, setting an attribute will not unset its mutually exclusive counterparts. 

This can be corrected inside custom setters. First, we need an additional import:

    from .wrap import package as ePackage

This gives us access to the MCNP Java package. To unset certain attributes, we'll use `eUnset` like in the following example:

    self._e_object.eUnset(ePackage.SOURCE_PARTICLE__ION)

Here `SOURCE_PARTICLE__ION` is the name of the Java object attribute that is being unset. Finding 



Although, to use this function, you need to know the attribute names found in the chosen `ePackage`. The most definitive way to find this is to use Eclipse to view the Java classes. Or you can follow the naming conventions. 
- All letters are capitalized
- `_` between capitalized words in Java class name
    - E.g. `SourceParticle` -> `SOURCE_PARTICLE`
- `__` between class name and attribute name
    - E.g. `__ION` for the `ion` attribute