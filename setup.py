from __future__ import print_function

import os, sys

from setuptools import (setup, find_packages)

def get_scripts(scripts_dir='bin'):
    """Get relative file paths for all files under the ``scripts_dir``
    """
    scripts = []
    for (dirname, _, filenames) in os.walk(scripts_dir):
        scripts.extend([os.path.join(dirname, fn) for fn in filenames])
    return scripts

# package dependencies
install_requires = [
    'numpy',
    'scipy',
    'astropy',
    'h5py',
    'pandas',
    'george',
    'h5py',
    'scikit-learn>=0.18',
    'matplotlib',
    'sncosmo',
    'requests',
    'penquins',
    'afterglowpy',
    'Cython',
    'extinction',
]

# test dependencies
tests_require = [
    'pytest>=3.1',
    'pytest-runner',
    'freezegun',
    'sqlparse',
    'bs4',
]
if sys.version < '3':
    tests_require.append('mock')

# -- run setup ----------------------------------------------------------------

setup(name='kilonova_lightcurves',
    provides=['kilonova_lightcurves'],
    version='0.1',
    description="A python package for kilonova lightcurves",
    long_description=("A redback friendly module for computing kilonova models"),
    author='Nikhil Sarin',
    author_email='nsarin.astro@gmail.com',
    license='MIT',
    url='https://github.com/nikhil-sarin/kilonova_lightcurves',
    # package content
    packages=find_packages(),
    scripts=get_scripts(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require)
