from setuptools import setup

NAME = 'mcnpy'

setup(
    name=NAME,
    version='0.0.4',
    packages=[NAME],
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    author='Peter J. Kowal',
    author_email='kowalp@rpi.edu',
    description='API to read, write, and edit MCNP decks',
    license='MIT',
    install_requires=['py4j', 'numpy', 'metapy'],
    platforms=['Windows', 'Linux']
)
