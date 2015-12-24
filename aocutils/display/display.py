#!/usr/bin/python
# coding: utf-8

r"""Display related utility functions"""

import functools
import logging

import OCC.Display.SimpleGui
import OCC.AIS
import OCC.Quantity

logger = logging.getLogger(__name__)


def colored_and_transparent(display, object, color=OCC.Quantity.Quantity_NOC_AQUAMARINE4, transparency=0.5):
    r"""Display an object with color and transparency using AIS

    Parameters
    ----------
    display
    object
    color
    transparency

    """
    ais_shp = OCC.AIS.AIS_Shape(object)
    ais_shp.SetTransparency(transparency)
    ais_shp.SetColor(color)
    ais_context = display.GetContext().GetObject()
    ais_context.Display(ais_shp.GetHandle())


def show(shape, backend=None):
    r"""Quick and dirty shape display, mostly aimed at quickly looking at a shape during the development workflow

    Parameters
    ----------
    shape : TopoDS_Shape
        The shape to display
    backend : str
    """
    if backend is None:
        display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display()
    else:
        display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    display.DisplayShape(shape, update=True)
    display.FitAll()
    display.View_Iso()
    start_display()


class Singleton(object):
    r"""Singleton pattern implementation - Decorator

    Parameters
    ----------
    cls : object
        The class decorated as a Singleton

    """
    def __init__(self, cls):
        self.cls = cls
        self.instance_container = []

    def __call__(self, *args, **kwargs):
        if not len(self.instance_container):
            cls = functools.partial(self.cls, *args, **kwargs)
            self.instance_container.append(cls())
        return self.instance_container[0]


@Singleton
class Display(object):
    """Display objectization"""
    def __init__(self, backend=None):
        if backend is None:
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = \
                OCC.Display.SimpleGui.init_display()
        else:
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = \
                OCC.Display.SimpleGui.init_display(backend)

    def display_shape(self, *args, **kwargs):
        r"""Display a shape

        Parameters
        ----------
        args
        kwargs

        """
        self.display.DisplayShape(*args, **kwargs)
        self.display.FitAll()
        self.display.View_Iso()
        self.start_display()
