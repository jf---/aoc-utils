#!/usr/bin/python
# coding: utf-8

r"""operations/section
"""


import OCC.BRepFill
import OCC.TopTools


def n_sections(edges):
    r"""

    Parameters
    ----------
    edges : list[OCC.TopoDS.TopoDS_Edge]

    Returns
    -------
    OCC.BRepFill.BRepFill_NSections

    """
    seq = OCC.TopTools.TopTools_SequenceOfShape()
    for i in edges:
        seq.Append(i)
    n_sec = OCC.BRepFill.BRepFill_NSections(seq, True)
    return n_sec
