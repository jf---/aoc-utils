#!/usr/bin/python
# coding: utf-8

r"""core/compound_make.py
"""

import OCC.TopoDS


def compound(topo):
    r"""Accumulate a bunch of TopoDS_* in list `topo` to a OCC.TopoDS.TopoDS_Compound

    Parameters
    ----------
    topo : list[TopoDS_*]

    Returns
    -------
    OCC.TopoDS.TopoDS_Compound

    """
    bd = OCC.TopoDS.TopoDS_Builder()
    comp = OCC.TopoDS.TopoDS_Compound()
    bd.MakeCompound(comp)
    for i in topo:
        bd.Add(comp, i)
    return comp
