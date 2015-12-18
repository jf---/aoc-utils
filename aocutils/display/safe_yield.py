#!/usr/bin/python
# coding: utf-8

r"""safe_yield.py

Functions
---------
safe_yield()

"""

from __future__ import print_function

import OCC.Display.SimpleGui


def available_backends():
    r"""List of available backends"""
    backends = list()
    try:
        import wx
        backends.append("wx")
    except ImportError:
        print("No wx backend")
    try:
        import PySide
        backends.append("qt-pyside")
    except ImportError:
        print("No PySide backend")
    try:
        import PyQt4
        backends.append("qt-pyqt4")
    except ImportError:
        print("No PyQt4 backend")

    return backends


def safe_yield():
    r"""Reimplementation of a function that once existed in OCC.Display.SimpleGui"""
    if OCC.Display.SimpleGui.get_backend() == 'wx':
        # This function (SafeYield) is similar to `wx.Yield`, except that it disables the
        # user input to all program windows before calling `wx.Yield` and
        # re-enables it again afterwards. If ``win`` is not None, this window
        # will remain enabled, allowing the implementation of some limited user
        # interaction.
        import wx
        wx.SafeYield()
    elif OCC.Display.SimpleGui.get_backend() == 'qt-pyqt4':
        # QtCore.processEvents()
        import PyQt4
        PyQt4.QtGui.QApplication.processEvents()
    elif OCC.Display.SimpleGui.get_backend() == 'qt-pyside':
        import PySide
        PySide.QtGui.QApplication.processEvents()
    else:
        raise RuntimeError("Could not determine the UI backend")
