idf-tags
=========

*A ViM-usable tags file generator for EnergyPlus IDF files.*

Purpose
-------


EnergyPlus IDF files can be huge, and you've probably wanted a way to jump to
another object that the object you're looking at references.

For example jump from one object that references a schedule to a schedule itself.

If you use ViM, you've probably been using `tags` files. This utility is a
`tags` generator for EnergyPlus IDF files.

It also comes with a Command Line Interface (CLI) for easy generation of said tags.

Note that because `tags` expects proper variables names, and EnergyPlus doesn't
enforce such rules for the `Name` of objects, we have to create a new IDF file
where the name doesn't include any spaces or other special characters.

Usage
-----

It installs a CLI `idf-tags`. Here's the output of `idf-tags`

    $ idf-tags

    idf-tags

    Usage:
      idf-tags
      idf-tags [--recursive | -r | <idf_path>]
      idf-tags -h | --help
      idf-tags -v | --version

    Options:
      -r --recursive    Search for IDF files is recursive (includes subdirectories)
      -h --help         Show this screen.
      -v --version      Show version.

    Examples:
      idf-tags          Generates a tag file for all files in current directory
      idf-tags -r       Tag file including subdirectories
      idf-tags in.idf   Tag file for a specific IDF file

    Help:
      For help using this tool, please open an issue on the Github repository:
      https://github.com/jmarrec/idf-tags


Developper
-----------

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project, against Python 2.7 and 3.6, I
have implemented tox, and you can just run::

    $ tox

or, for only your current environment::

    $ python setup.py test

Both will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Uploading a new version to PyPi, the Python Package Index
(`PyPI <https://pypi.python.org/pypi>`_)::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*). You need  `twine
<https://pypi.python.org/pypi/twine>`_
