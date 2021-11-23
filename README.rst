=========
metatable
=========

Extensible table data structure that supports the introduction of user-defined workflow combinators and the use of these combinators in concise workflow descriptions.

|pypi| |readthedocs| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/metatable.svg
   :target: https://badge.fury.io/py/metatable
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/metatable/badge/?version=latest
   :target: https://metatable.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |travis| image:: https://app.travis-ci.com/reity/metatable.svg?branch=main
   :target: https://app.travis-ci.com/reity/metatable
   :alt: Travis CI build status.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/metatable/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/metatable?branch=main
   :alt: Coveralls test coverage summary.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/metatable/>`_::

    python -m pip install metatable

The library can be imported in the usual ways::

    import metatable
    from metatable import *

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    python -m pip install nose coverage
    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python metatable/metatable.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    pylint metatable

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/metatable>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
