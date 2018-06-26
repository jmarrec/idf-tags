"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from idftags import __version__


THIS_DIR = abspath(dirname(__file__))
with open(join(THIS_DIR, 'README.rst'), encoding='utf-8') as file:
    LONG_DESCRIPTION = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=idftags', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='idf-tags',
    version=__version__,
    description='A ViM-usable tags file generator for EnergyPlus IDF files.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/jmarrec/idf-tags',
    author='Julien Marrec',
    author_email='julien@effibem.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='energyplus,tags,vim,vi,cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['eppy', 'docopt'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov', 'pytest-pep8', 'tox'],
    },
    entry_points={
        'console_scripts': [
            'idf-tags=idftags.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
