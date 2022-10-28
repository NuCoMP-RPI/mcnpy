# Rebuild wheel
cd ~/mcnp_api
python setup.py bdist_wheel

# Uninstall mcnpy
printf "y" | pip uninstall mcnpy

# Install new wheel
pip install ./dist/mcnpy-0.0.0-py3-none-any.whl
