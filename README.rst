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

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!
