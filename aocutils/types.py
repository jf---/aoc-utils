# coding: utf-8

r"""types.py module of aocutils"""

import sys
import logging
import itertools

import OCC.BRepCheck
import OCC.GeomAbs
import OCC.TopoDS
import OCC.BRep
import OCC.TopAbs
import OCC.Geom

import aocutils.exceptions

logger = logging.getLogger(__name__)

PY3 = not (int(sys.version.split('.')[0]) <= 2)


curve_types_dict = {OCC.GeomAbs.GeomAbs_Line: "line", OCC.GeomAbs.GeomAbs_Circle: "circle",
                    OCC.GeomAbs.GeomAbs_Ellipse: "ellipse", OCC.GeomAbs.GeomAbs_Hyperbola: "hyperbola",
                    OCC.GeomAbs.GeomAbs_Parabola: "parabola", OCC.GeomAbs.GeomAbs_BezierCurve: "bezier",
                    OCC.GeomAbs.GeomAbs_BSplineCurve: "spline", OCC.GeomAbs.GeomAbs_OtherCurve: "other"}

surface_types_dict = {OCC.GeomAbs.GeomAbs_Plane: "plane", OCC.GeomAbs.GeomAbs_Cylinder: "cylinder",
                      OCC.GeomAbs.GeomAbs_Cone: "cone",  OCC.GeomAbs.GeomAbs_Sphere: "sphere",
                      OCC.GeomAbs.GeomAbs_Torus: "torus", OCC.GeomAbs.GeomAbs_BezierSurface: "bezier",
                      OCC.GeomAbs.GeomAbs_BSplineSurface: "spline",
                      OCC.GeomAbs.GeomAbs_SurfaceOfRevolution: "revolution",
                      OCC.GeomAbs.GeomAbs_SurfaceOfExtrusion: "extrusion", OCC.GeomAbs.GeomAbs_OffsetSurface: "offset",
                      OCC.GeomAbs.GeomAbs_OtherSurface: "other"}

state_dict = {OCC.TopAbs.TopAbs_IN: "in", OCC.TopAbs.TopAbs_OUT: "out", OCC.TopAbs.TopAbs_ON: "on",
              OCC.TopAbs.TopAbs_UNKNOWN: "unknown"}

orient_dict = {OCC.TopAbs.TopAbs_FORWARD: "TopAbs_FORWARD", OCC.TopAbs.TopAbs_REVERSED: "TopAbs_REVERSED",
               OCC.TopAbs.TopAbs_INTERNAL: "TopAbs_INTERNAL", OCC.TopAbs.TopAbs_EXTERNAL: "TopAbs_EXTERNAL"}

topo_types_dict = {OCC.TopAbs.TopAbs_VERTEX: "vertex", OCC.TopAbs.TopAbs_EDGE: "edge", OCC.TopAbs.TopAbs_WIRE: "wire",
                   OCC.TopAbs.TopAbs_FACE: "face", OCC.TopAbs.TopAbs_SHELL: "shell", OCC.TopAbs.TopAbs_SOLID: "solid",
                   OCC.TopAbs.TopAbs_COMPSOLID: "compsolid", OCC.TopAbs.TopAbs_COMPOUND: "compound",
                   OCC.TopAbs.TopAbs_SHAPE: "shape"}

geom_types_dict = {OCC.GeomAbs.GeomAbs_Line: "line", OCC.GeomAbs.GeomAbs_Circle: "circle",
                   OCC.GeomAbs.GeomAbs_Ellipse: "ellipse", OCC.GeomAbs.GeomAbs_Hyperbola: "hyperbola",
                   OCC.GeomAbs.GeomAbs_Parabola: "parabola", OCC.GeomAbs.GeomAbs_BezierCurve: "beziercurve",
                   OCC.GeomAbs.GeomAbs_BSplineCurve: "bsplinecurve", OCC.GeomAbs.GeomAbs_OtherCurve: "othercurve"}


brep_check_dict = {OCC.BRepCheck.BRepCheck_NoError: "NoError",
                   OCC.BRepCheck.BRepCheck_InvalidPointOnCurve: "InvalidPointOnCurve",
                   OCC.BRepCheck.BRepCheck_InvalidPointOnCurveOnSurface: "InvalidPointOnCurveOnSurface",
                   OCC.BRepCheck.BRepCheck_InvalidPointOnSurface: "InvalidPointOnSurface",
                   OCC.BRepCheck.BRepCheck_No3DCurve: "No3DCurve",
                   OCC.BRepCheck.BRepCheck_Multiple3DCurve: "Multiple3DCurve",
                   OCC.BRepCheck.BRepCheck_Invalid3DCurve: "Invalid3DCurve",
                   OCC.BRepCheck.BRepCheck_NoCurveOnSurface: "NoCurveOnSurface",
                   OCC.BRepCheck.BRepCheck_InvalidCurveOnSurface: "InvalidCurveOnSurface",
                   OCC.BRepCheck.BRepCheck_InvalidCurveOnClosedSurface: "InvalidCurveOnClosedSurface",
                   OCC.BRepCheck.BRepCheck_InvalidSameRangeFlag: "InvalidSameRangeFlag",
                   OCC.BRepCheck.BRepCheck_InvalidSameParameterFlag: "InvalidSameParameterFlag",
                   OCC.BRepCheck.BRepCheck_InvalidDegeneratedFlag: "InvalidDegeneratedFlag",
                   OCC.BRepCheck.BRepCheck_FreeEdge: "FreeEdge",
                   OCC.BRepCheck.BRepCheck_InvalidMultiConnexity: "InvalidMultiConnexity",
                   OCC.BRepCheck.BRepCheck_InvalidRange: "InvalidRange",
                   OCC.BRepCheck.BRepCheck_EmptyWire: "EmptyWire",
                   OCC.BRepCheck.BRepCheck_RedundantEdge: "RedundantEdge",
                   OCC.BRepCheck.BRepCheck_SelfIntersectingWire: "SelfIntersectingWire",
                   OCC.BRepCheck.BRepCheck_NoSurface: "NoSurface",
                   OCC.BRepCheck.BRepCheck_InvalidWire: "InvalidWire",
                   OCC.BRepCheck.BRepCheck_RedundantWire: "RedundantWire",
                   OCC.BRepCheck.BRepCheck_IntersectingWires: "IntersectingWires",
                   OCC.BRepCheck.BRepCheck_InvalidImbricationOfWires: "InvalidImbricationOfWires",
                   OCC.BRepCheck.BRepCheck_EmptyShell: "EmptyShell",
                   OCC.BRepCheck.BRepCheck_RedundantFace: "RedundantFace",
                   OCC.BRepCheck.BRepCheck_UnorientableShape: "UnorientableShape",
                   OCC.BRepCheck.BRepCheck_NotClosed: "NotClosed",
                   OCC.BRepCheck.BRepCheck_NotConnected: "NotConnected",
                   OCC.BRepCheck.BRepCheck_SubshapeNotInShape: "SubshapeNotInShape",
                   OCC.BRepCheck.BRepCheck_BadOrientation: "BadOrientation",
                   OCC.BRepCheck.BRepCheck_BadOrientationOfSubshape: "BadOrientationOfSubshape",
                   OCC.BRepCheck.BRepCheck_InvalidToleranceValue: "InvalidToleranceValue",
                   OCC.BRepCheck.BRepCheck_CheckFail: "CheckFail"}


class BidirDict(dict):
    """Bi-directional dictionnary

    Parameters
    ----------
    iterable
    kwargs

    Raises
    ------
    KeyError if a duplicate value exists (as values must also be able to behave as keys)

    """
    def __init__(self, iterable=(), **kwargs):
        self.update(iterable, **kwargs)

    def update(self, iterable=(), **kwargs):
        if hasattr(iterable, 'items'):
            iterable = iterable.items()
        for (key, value) in itertools.chain(iterable, kwargs.items()):
            self[key] = value

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        value = self[key]
        dict.__delitem__(self, key)
        dict.__delitem__(self, value)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, dict.__repr__(self))


brepcheck_lut = BidirDict(brep_check_dict)
curve_lut = BidirDict(curve_types_dict)
surface_lut = BidirDict(surface_types_dict)
state_lut = BidirDict(state_dict)
orient_lut = BidirDict(orient_dict)
topo_lut = BidirDict(topo_types_dict)
geom_lut = BidirDict(geom_types_dict)

# classes = dir()
# geom_classes = list()
# for elem in classes:
#     if elem.startswith('Geom') and 'swig' not in elem:
#         geom_classes.append(elem)


# def what_is_face(face):
#     """Returns all class names for which this class can be downcasted
#
#     Parameters
#     ----------
#     face : OCC.TopoDS_Shape of type OCC.TopAbs.TopAbs_FACE
#
#     Returns
#     -------
#     list
#
#     """
#     if not face.ShapeType() == OCC.TopAbs.TopAbs_FACE:
#         msg = '%s type is not TopAbs_FACE. Conversion impossible' % str(face)
#         logger.error(msg)
#         raise aocutils.exceptions.WrongTopologicalType(msg)
#
#     # BRep_Tool.Surface() signatures
#     # ------------------------------
#     # static const Handle< Geom_Surface > & 	Surface (const TopoDS_Face &F, TopLoc_Location &L)
#     #         static Handle< Geom_Surface > 	Surface (const TopoDS_Face &F)
#     handle_geom_surface = OCC.BRep.BRep_Tool_Surface(face)
#     geom_surface = handle_geom_surface.GetObject()
#
#     result = list()
#
#     for elem in classes:
#         if elem.startswith('Geom') and 'swig' not in elem:
#             geom_classes.append(elem)
#
#     for geom_class in geom_classes:
#         if geom_surface.IsKind(geom_class) and geom_class not in result:
#             result.append(geom_class)
#     return result


# def shape_is_cylinder(face):
#     r"""
#
#     Parameters
#     ----------
#     face : OCC.TopoDS.TopoDS_Face
#
#     Returns
#     -------
#     bool
#         True is the TopoDS_Shape is a cylinder, False otherwise
#
#     """
#     hs = OCC.BRep.BRep_Tool_Surface(face)
#     downcast_result = OCC.Geom.Handle_Geom_CylindricalSurface().DownCast(hs)
#     if downcast_result.IsNull():
#         return False
#     else:
#         return True
