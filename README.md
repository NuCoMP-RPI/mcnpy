# mcnpy2.0
Newer version of `mcnpy` with dynamic wrapping.

# Dependencies
- `Py4j`.
- Everything else comes with a basic Anaconda3 install.

# Installing Py4j
1. `pip install py4j`
    - Be aware of which environment it is installed to.
    - Use `conda activate ENV_NAME` to switch.
2. Locate `py4j0.x.jar`. Probable locations:
    - Either `/usr/share/py4j/py4j0.x.jar` or `/usr/local/share/py4j/py4j0.x.jar` for system-wide install on Linux.
    - `{virtual_env_dir}/share/py4j/py4j0.x.jar` for installation in a virtual environment.
    - `C:\python\share\py4j\py4j0.x.jar` for system-wide install on Windows.
3. Copy `py4j.x.jar` to `mcnpy/lib` directory.
    - Note that a version of `py4j.x.jar` is included with `mcnpy` by default.

# How to Use
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
