from os.path import abspath, dirname, join
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from shutil import copyfile

HERE = abspath(dirname(__file__))
NAME = 'mcnpy'

def copy_files (target_path):
    source_path = join(HERE, 'mcnpy')
    for fn in ['EntryPoint.jar', 'EntryPoint.class', 'EntryPoint.java', 
               'manifest.mf', 'server_delay']:
        copyfile(join(source_path, fn), join(target_path,fn))
    
    """lib_path = os.path.join(source_path, 'lib')
    lib_target = os.path.join(target_path, 'lib')
    copytree(lib_path, target_path)
    onlyfiles = [f for f in listdir(lib_path) if isfile(join(lib_path, f))]
    for f in onlyfiles:
        copyfile(os.path.join(lib_path, f), os.path.join(lib_target, f))"""

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        copy_files (abspath(NAME))

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        copy_files (abspath(join(self.install_lib, NAME)))

setup(
    name=NAME,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    version='0.0.0',
    packages=[NAME],
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    author='Peter J. Kowal',
    author_email='kowalp@rpi.edu',
    description='API to read, write, and edit MCNP decks',
    license='MIT',
    install_requires=['py4j', 'psutil', 'h5py', 'numpy'],
    platforms=['Windows', 'Linux']
)