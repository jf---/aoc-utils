.. -*- coding: utf-8 -*-

aoc-utils
=========

.. image:: http://img.shields.io/badge/Status-development-ff3300.svg
   :alt: Development
.. image:: https://img.shields.io/pypi/dm/aocutils.svg
   :alt: Downloads
.. image:: https://travis-ci.org/floatingpointstack/aoc-utils.svg
   :alt: Build Status
.. image:: https://coveralls.io/repos/floatingpointstack/aoc-utils/badge.svg?branch=master&service=github
   :alt: Coverage Status
.. image:: http://img.shields.io/badge/license-GPL_v3-blue.svg
   :target: https://www.gnu.org/copyleft/gpl.html
   :alt: GPL v3
.. image:: http://img.shields.io/badge/Python-2.7_3.*-ff3366.svg
   :target: https://www.python.org/downloads/
   :alt: Python 2.7 3.*

The **aoc-utils** project provides a Python package named **aocutils** with
useful modules/classes/methods for `PythonOCC <http://github.com/tpaviot/pythonocc-core>`_. It is a high level API for PythonOCC.

PythonOCC is a set of Python wrappers for the OpenCascade Community Edition (an industrial strength 3D CAD modeling kernel)

install
-------

.. code-block:: shell

  pip install aocutils

Dependencies
~~~~~~~~~~~~

*aocutils* depends on OCC >=0.16 and scipy. The examples require wx>=2.8 (or another backend (minor code modifications required)).
These requirements cannot be satisfied through pip.
Please see the table below for instructions on how to satisfy the requirements.

+---------+----------+----------------------------------------------------------------------------+
| package | version  | Comment                                                                    |
+=========+==========+============================================================================+
| OCC     | >=0.16.  | | See pythonocc.org or github.com.tpaviot/pythonocc-core for instructions  |
|         |          | | or `conda install -c https://conda.anaconda.org/dlr-sc pythonocc-core`   |
+---------+----------+----------------------------------------------------------------------------+
| scipy   | latest   | | Simplest solution is `conda install scipy`                               |
|         |          | | or a full Anaconda distribution                                          |
+---------+----------+----------------------------------------------------------------------------+
| wx      | >=2.8    | See wxpython.org for instructions                                          |
+---------+----------+----------------------------------------------------------------------------+

Goal
----

The goal of the **aocutils** package is to simplify some frequently used operations made in PythonOCC.

Versions
--------

aocutils version and target PythonOCC version

+------------------+-------------------+
| aocutils version | PythonOCC version |
+==================+===================+
| 0.1.*            | 0.16.2            |
+------------------+-------------------+

Examples
--------

The examples are in the *examples* folder at the Github repository (https://github.com/floatingpointstack/aoc-utils).

The wx backend (wxPython) backend is used for the examples that display a UI.
You may easily change this behaviour to use pyqt4 or PySide by changing the backend in the call to init_display().

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-utils/master/img/geomplate.jpg
   :alt: geomplate

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-utils/master/img/surfaces.jpg
   :alt: surfaces
