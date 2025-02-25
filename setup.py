import os.path
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext
import sys
import warnings

from Cython.Build import cythonize
USE_CYTHON = True

# numpy path is needed for building with and without cython:
import numpy
numpy_includes = [numpy.get_include()]
HAVE_NUMPY = True

classifiers = [
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Topic :: Scientific/Engineering'
]


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


ext = '.pyx'

extensions = [Extension(
        'fastdtw._fastdtw',
        [os.path.join('fastdtw', '_fastdtw' + ext)],
        language="c++",
        include_dirs=numpy_includes,
        libraries=["stdc++"]
    )]

extensions = cythonize(extensions)    

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'README.rst')) as f:
    long_description = f.read()

needs_pytest = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

kwargs = {
    'name': 'fastdtw',
    'version': '0.3.4',
    'author': 'Kazuaki Tanida',
    'url': 'https://github.com/slaypni/fastdtw',
    'description': 'Dynamic Time Warping (DTW) algorithm with an O(N) time and memory complexity.',
    'long_description': long_description,
    'license': 'MIT',
    'keywords': ['dtw'],
    'install_requires': ['numpy', 'cython'],
    'packages': find_packages(),
    'ext_modules':  extensions,
    'test_suite': 'tests',
    'setup_requires': pytest_runner,
    'tests_require': ['pytest'],
    'classifiers': classifiers
}

setup(**kwargs)
