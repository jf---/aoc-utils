#!/usr/bin/python
# coding: utf-8

r"""

Functions
---------
translate
scale_uniform
mirror_pnt_dir
mirror_axe2
rotate

"""

import math

import OCC.BRepBuilderAPI
import OCC.gp
import OCC.TopoDS

import aocutils.common
import aocutils.topology


def translate(brep_or_iterable, vec, copy=False):
    r"""Translate a TopoDS_* using a vector

    Parameters
    ----------
    brep_or_iterable : TopoDS_Shape or iterable[TopoDS_Shape]
        the Topo_DS to translate
    vec
        the vector defining the translation
    copy
        copies to brep if True

    Returns
    -------
    list[OCC.TopoDS.TopoDS_*]

    """
    # st = occutils.types_lut.ShapeToTopology()
    gp_trsf = OCC.gp.gp_Trsf()
    gp_trsf.SetTranslation(vec)
    if issubclass(brep_or_iterable.__class__, OCC.TopoDS.TopoDS_Shape):
        brep_transform = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(brep_or_iterable, gp_trsf, copy)
        brep_transform.Build()
        return aocutils.topology.shape_to_topology(brep_transform.Shape())
    else:
        return [translate(brep_or_iterable, vec, copy) for _ in brep_or_iterable]


def rotate(brep, axe, degree, copy=False):
    r"""Rotate around an axis

    Parameters
    ----------
    brep : OCC.TopoDS.TopoDS_*
    axe : OCC.gp.gp_Ax1
    degree : float
        Rotation angle
    copy : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_*

    """
    gp_trsf = OCC.gp.gp_Trsf()
    gp_trsf.SetRotation(axe, math.radians(degree))
    brep_transform = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(brep, gp_trsf, copy)
    with aocutils.common.AssertIsDone(brep_transform, 'could not produce rotation'):
        brep_transform.Build()
        return aocutils.topology.shape_to_topology(brep_transform.Shape())


def scale_uniform(brep, pnt, factor, copy=False):
    r"""Scale a brep

    Parameters
    ----------
    brep
        the Topo_DS to scale
    pnt : OCC.gp.gp_Pnt
        a gp_Pnt
    factor : float
        scaling factor
    copy : bool
        copies to brep if True

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    trns = OCC.gp.gp_Trsf()
    trns.SetScale(pnt, factor)
    brep_trns = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(brep, trns, copy)
    brep_trns.Build()
    return brep_trns.Shape()


def mirror_pnt_dir(brep, pnt, direction, copy=False):
    r"""Mirror ...

    Parameters
    ----------
    brep
    pnt : OCC.gp.gp_Pnt
    direction : OCC.gp.gp_Dir
    copy : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    trns = OCC.gp.gp_Trsf()
    trns.SetMirror(OCC.gp.gp_Ax1(pnt, direction))
    brep_trns = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(brep, trns, copy)
    with aocutils.common.AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()


def mirror_axe2(brep, axe2, copy=False):
    r"""

    Parameters
    ----------
    brep : OCC.TopoDS.TopoDS_*
    axe2 : OCC.gp.gp_Ax2
    copy : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    trns = OCC.gp.gp_Trsf()
    trns.SetMirror(axe2)
    brep_trns = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(brep, trns, copy)
    with aocutils.common.AssertIsDone(brep_trns, 'could not produce mirror'):
        brep_trns.Build()
        return brep_trns.Shape()
