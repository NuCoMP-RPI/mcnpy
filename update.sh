eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"
# Rebuild wheel
cd ~/Research/mcnp_api
python setup.py bdist_wheel

# Uninstall mcnpy
printf "y" | pip uninstall mcnpy

# Install new wheel
pip install ./dist/mcnpy-0.0.0-py3-none-any.whl

# Install for openmc-env
conda activate openmc-env
# Uninstall metapy
printf "y" | pip uninstall mcnpy

# Install new wheel
pip install ./dist/mcnpy-0.0.0-py3-none-any.whl

# Return to base env
conda activate base