=========
metatable
=========

Extensible table data structure that supports the introduction of user-defined workflow combinators and the use of these combinators in concise workflow descriptions.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/metatable.svg
   :target: https://badge.fury.io/py/metatable
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/metatable/badge/?version=latest
   :target: https://metatable.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/reity/metatable/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/reity/metatable/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/metatable/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/metatable?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/metatable>`__::

    python -m pip install metatable

The library can be imported in the usual ways::

    import metatable
    from metatable import *

Examples
^^^^^^^^
This library makes it possible to work with tabular data that is represented as a list of lists (*i.e.*, each row is a list of column values and a table is a list of rows)::

    >>> from metatable import *
    >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
    >>> list(iter(t))
    [['a', 0], ['b', 1], ['c', 2]]

.. |metatable| replace:: ``metatable``
.. _metatable: https://metatable.readthedocs.io/en/latest/_source/metatable.html#metatable.metatable.metatable

All rows in a |metatable|_ instance can be updated in-place using a symbolic representation (implemented using the `symbolism <https://pypi.org/project/symbolism>`__ library) of the transformation that must be applied to each row. For example, the transformation ``{1: column(0)}`` indicates that the value in the column having index ``1`` (*i.e.*, the right-hand column) should be replaced with the value in the column having index ``0`` (*i.e.*, the left-hand column)::

    >>> t.update({1: column(0)})
    [['a', 'a'], ['b', 'b'], ['c', 'c']]

It is also possible to perform an update that removes rows based on a condition. The condition in the example below is the symbolic expression ``column(1) > symbol(0)`` (constructed using the `symbolism <https://pypi.org/project/symbolism>`__ library)::

    >>> from symbolism import symbol
    >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
    >>> t.update_filter({0: column(1)}, column(1) > symbol(0))
    [[1, 1], [2, 2]]

There is also support for working with a tabular data set in which there is a header row containing column names::

    >>> t = metatable([['char', 'num'], ['a', 0], ['b', 1]], header=True)
    >>> t.update({1: column(0)})
    [['char', 'num'], ['a', 'a'], ['b', 'b']]

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/metatable/metatable.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org>`__::

    python -m pip install .[lint]
    python -m pylint src/metatable

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/metatable>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/metatable>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Remove any old build/distribution files and package the source into a distribution archive::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__ using the `twine <https://pypi.org/project/twine>`__ package::

    python -m twine upload dist/*
