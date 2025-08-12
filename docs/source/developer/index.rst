.. _developer-overview:

Developer Overview
==================

This section provides a high level look at the ``hckr`` project for new contributors.

Repository Structure
--------------------

``hckr`` is organized as a Python package with the command line interface under
``src/hckr`` and Sphinx documentation under ``docs``.  The most important
directories are:

* ``src/hckr/cli`` - Click command definitions
* ``src/hckr/utils`` - shared helper modules
* ``tests`` - unit tests using ``pytest``
* ``docs`` - documentation sources

Entry Point
-----------

The CLI entry point is implemented in ``src/hckr/cli/__init__.py``.  Each
subcommand (``config``, ``cron``, ``crypto`` and others) is defined in its own
module within ``src/hckr/cli`` and added to the top level ``cli`` group.

Next Steps
----------

* Run ``hckr --help`` to explore available commands.
* Browse the source files in ``src/hckr`` to see how commands and utilities are
  implemented.
* Read tests in ``tests`` for examples of expected behaviour.
* Review this documentation under ``docs`` to learn about individual commands.
