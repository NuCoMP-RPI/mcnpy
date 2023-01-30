# MCNPy: The Python API for MCNP
Newer version of `mcnpy` with dynamic wrapping.

# Dependencies
- `py4j`.
- `h5py`
- `psutil`
- `numpy`
- `metapy`
- Everything should come with a standard Python install

# How to Install
1. Clone the repository: `git clone https://github.rpi.edu/NuCoMP/mcnpy.git`.
2. Ensure you are running the desired Python environment.
    - Try `conda activate ENV_NAME` to switch.
3. Run `pip install /path/to/cloned/repo/dist/mcnpy-X.whl` where `X` is the version.
    - All dependencies *except* `metapy` will be downloaded if needed.
    - `metapy` must be installed from the [metapy repository](https://github.rpi.edu/NuCoMP/metapy).
4. Done!

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
