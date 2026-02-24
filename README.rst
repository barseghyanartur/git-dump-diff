=============
git-dump-diff
=============
.. External references

.. _git-dump-diff: https://github.com/barseghyanartur/git-dump-diff/

Git diff tool that shows a tree of changed files followed by their full 
content.

.. image:: https://img.shields.io/pypi/v/git-dump-diff.svg
   :target: https://pypi.python.org/pypi/git-dump-diff
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/git-dump-diff.svg
    :target: https://pypi.python.org/pypi/git-dump-diff/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/git-dump-diff/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/git-dump-diff/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/git-dump-diff/badge/?version=latest
    :target: http://git-dump-diff.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/docs-llms.txt-blue
    :target: http://git-dump-diff.readthedocs.io/en/latest/llms.txt
    :alt: llms.txt - documentation for LLMs

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/git-dump-diff/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/git-dump-diff/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/git-dump-diff?branch=main
    :alt: Coverage

``git-dump-diff`` is a verbose Git diagnostic tool. It shows a directory tree
of changed files and the full content of added or updated files.

Unlike a standard diff that shows only line changes, this tool lets you see the
entire file context.
It is ideal for code reviews and auditing feature branches.

Features
========
- **Visual Tree**: Shows affected files in a clear directory structure.
- **Full Content**: Displays the complete final state of new or modified files.
- **Binary Safe**: Detects and skips binary files to keep your terminal clean.
- **Pager Support**: Works with ``less`` automatically for easy scrolling.
- **No Dependencies**: Uses only standard Python libraries.

Prerequisites
=============
Python 3.10+

Installation
============
uv tool (recommended)
---------------------

.. code-block:: sh

    uv tool install git-dump-diff

pipx
----

.. code-block:: sh

    pipx install git-dump-diff

Usage
=====
Once installed, use the standard Git range syntax (``base..target``).

Compare branches
----------------
.. code-block:: sh

    git dump-diff main..feature-branch

Compare commits
---------------
.. code-block:: sh

    git dump-diff HEAD~3..HEAD

Options
-------
- ``--version``: Show current version.
- ``--help``: Show help message.

How it works
============
Git recognizes any executable in your ``PATH`` starting with ``git-`` as a
subcommand. This package installs a ``git-dump-diff`` entry point, making it
available as ``git dump-diff``.

Tests
=====
Run the tests with pytest:

.. code-block:: sh

    pytest

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
MIT

Support
=======
For issues, visit `GitHub <https://github.com/barseghyanartur/git-dump-diff/issues>`_.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
