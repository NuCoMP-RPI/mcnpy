# mcnpy2.0
Newer version of `mcnpy` with dynamic wrapping.

# Dependencies
- `py4j`.
- `h5py`
- `psutil`
- `numpy`
- Everything should come with a standard Python install

# Installing Py4j
1. `pip install py4j`
    - Be aware of which environment it is installed to.
    - Use `conda activate ENV_NAME` to switch.
2. Locate `py4j0.x.jar`. Probable locations:
    - Either `/usr/share/py4j/py4j0.x.jar` or `/usr/local/share/py4j/py4j0.x.jar`  
    for system-wide install on Linux.
    - `{virtual_env_dir}/share/py4j/py4j0.x.jar` for installation in a virtual environment.
    - `C:\python\share\py4j\py4j0.x.jar` for system-wide install on Windows.
3. Copy `py4j.x.jar` to `mcnpy/lib` directory.
    - Note that a version of `py4j.x.jar` is included with `mcnpy` by default.

# How to Use
Even though `mcnpy` is still in development, there's the option to install it from a wheel.  
The wheel was built in `Pop!_OS 21.10 x86_64` with `Python 3.8.8`. It has run  
successfully with newer Python versions, but there has been no extensive testing.
## From Wheel
1. Enter your Python environment of choice.
2. Run `pip install mcnpy-X.whl` where `X` is the version.
3. You can now import `mcnpy` from anywhere.
4. Uninstall with `pip uninstall mcnpy`.
5. To build your own wheel, run `python setup.py bdist_wheel` from within  
the `mcnpy` directory.

## From Repo
1. Place `/mcnpy/` into your working directory.
    - Eventually everything will be packaged for a global install.
2. Import `mcnpy` as a Python package.
    - It will be a local import.
    - The Java gateway will be run automatically.
3. See `mcnpy/example.py` for an example class using the RCF.
4. Files must have the `.mcnp` extension be parsed.

# Recompiling `EntryPoint.jar`
This should be done after:
- Adding new `.jar` files to `/mcnpy/lib`.
- Editing `/mcnpy/EntryPoint.java`.

To recompile:
- Run `/mcnpy/compile.sh`.
    - A very similar batch file can probably be made for Windows.

# MCNP to OpenMC Translation
Using `translate_to_openmc.py`, and OpenMC geometry and material XML files can be  
  generated from an MCNP input. The translation process is not 100% complete, but can  
  handle complex model's such as ORNL's HFIR (`hfir.mcnp`)

## Setup
- `/mcnpy/` must also be located in your working directory or otherwise installed.
- The OpenMC Python API is required by this script. This is most easily achieved by  
  [installing OpenMC](https://docs.openmc.org/en/stable/quickinstall.html). 
    - On Windows, running an Ubuntu Linux subsystem can make the install very  
      painless.
- Also configure [cross sections for OpenMC](https://docs.openmc.org/en/stable/usersguide/cross_sections.html). This allows your plots to be colored by  
  material (as is necessary for OpenMC to run simulations).
- In `translate_to_openmc.py`, under the main function (go to the end of the file),  
  modify the following line of code to reflect your cross-sections file location.

        model[1].cross_sections = '/home/peter/openmc_XS/mcnp_endfb71/cross_sections.xml'

## Running
- `python translate_to_openmc.py .../mcnp_model.mcnp`.