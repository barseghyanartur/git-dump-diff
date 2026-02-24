Contributor guidelines
======================

.. _git-dump-diff: https://git-dump-diff.readthedocs.io
.. _documentation: https://git-dump-diff.readthedocs.io/#writing-documentation
.. _testing: https://git-dump-diff.readthedocs.io/#testing
.. _pre-commit: https://pre-commit.com/#installation
.. _doc8: https://doc8.readthedocs.io/
.. _ruff: https://beta.ruff.rs/docs/
.. _uv: https://docs.astral.sh/uv/
.. _issues: https://github.com/barseghyanartur/git-dump-diff/issues
.. _discussions: https://github.com/barseghyanartur/git-dump-diff/discussions
.. _pull request: https://github.com/barseghyanartur/git-dump-diff/pulls
.. _support: https://git-dump-diff.readthedocs.io/#support
.. _installation: https://git-dump-diff.readthedocs.io/#installation
.. _features: https://git-dump-diff.readthedocs.io/#features
.. _prerequisites: https://git-dump-diff.readthedocs.io/#prerequisites
.. _versions manifest: https://github.com/actions/python-versions/blob/main/versions-manifest.json

Developer prerequisites
-----------------------
pre-commit
~~~~~~~~~~
Refer to `pre-commit`_ for installation instructions.

TL;DR:

.. code-block:: sh

    curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv
    uv tool install pre-commit  # Install pre-commit
    pre-commit install  # Install pre-commit hooks

Installing `pre-commit`_ will ensure you adhere to the project code quality
standards.

Code standards
--------------
`ruff`_ and `doc8`_ will be automatically triggered by `pre-commit`_.

`ruff`_ is configured to do the job of ``black`` and ``isort`` as well.

Still, if you want to run checks manually:

.. code-block:: sh

    make doc8
    make ruff

Requirements
------------
Requirements are compiled using `uv`_.

.. code-block:: sh

    make compile-requirements

Virtual environment
-------------------
You are advised to work in virtual environment.

TL;DR:

.. code-block:: sh

    make install

Documentation
-------------
Check the `documentation`_.

Testing
-------
Check `testing`_.

If you introduce changes or fixes, make sure to test them locally:

.. code-block:: sh

    make test

In any case, GitHub Actions will catch potential errors, but testing locally
catches things upfront.

Releasing
---------
**Sequence of steps:**

#. Clean and build

    .. code-block:: sh

        make clean
        make build

#. Check the build

    .. code-block:: sh

        make check-build

#. Test release on test.pypi.org. Make sure to check it before moving forward.

    .. code-block:: sh

        make test-release

#. Release

    .. code-block:: sh

        make release

Pull requests
-------------
You can contribute to the project by making a `pull request`_.

For example:

- To fix documentation typos.
- To improve documentation (for instance, to add new recipe or fix
  an existing recipe that doesn't seem to work).
- To introduce a new feature (for instance, add support for a non-supported
  file type).

**Good to know:**

- This library consists of a single ``git_dump_diff.py`` module. That module is
  dependency free.
  Do not submit pull requests splitting the ``git_dump_diff.py`` module into
  small parts. Pull requests with external dependencies in ``git-dump-diff``
  module will not be accepted either.
- Currently, all integration tests are running in the CI against the latest
  version of Python.

**General list to go through:**

- Does your change require documentation update?
- Does your change require update to tests?

**When fixing bugs (in addition to the general list):**

- Make sure to add regression tests.

**When adding a new feature (in addition to the general list):**

- Make sure to update the documentation (check whether the `installation`_ and
  `features`_ require changes).

GitHub Actions
--------------
Only non-EOL versions of Python and software `git-dump-diff`_ aims to
integrate with are supported.

On GitHub Actions includes tests for more than 40 different variations of
Python versions and integration packages. Future, non-stable versions
of Python are being tested too, so that new features/incompatibilities
could be seen and adopted early.

For the list of Python versions supported by GitHub, see GitHub Actions
`versions manifest`_.

Questions
---------
Questions can be asked on GitHub `discussions`_.

Issues
------
For reporting a bug or filing a feature request, use GitHub `issues`_.

**Do not report security issues on GitHub**. Check the `support`_ section.
