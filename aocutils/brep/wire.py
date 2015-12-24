# coding: utf-8

r"""wire module of occutils

Classes
-------
Wire
    check()"""

import logging

import OCC.BRepBuilderAPI
import OCC.TopoDS
import OCC.Approx
import OCC.BRepAdaptor
import OCC.GeomAbs
import OCC.GeomConvert
import OCC.BRepCheck

import aocutils.brep.base
import aocutils.common
import aocutils.tolerance
import aocutils.exceptions

logger = logging.getLogger(__name__)


class Wire(aocutils.brep.base.BaseObject):
    r"""Wire class

    Parameters
    ----------
        wire : OCC.TopoDS.TopoDS_Wire

    """

    def __init__(self, topods_wire):
        if not isinstance(topods_wire, OCC.TopoDS.TopoDS_Wire):
            msg = 'Wire.__init__() needs a TopoDS_Wire, got a %s' % topods_wire.__class__
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        assert not topods_wire.IsNull()

        aocutils.brep.base.BaseObject.__init__(self, topods_wire, name='topods_wire')

    @property
    def topods_wire(self):
        return self._wrapped_instance

    def check(self):
        r"""Super class abstract method implementation"""
        wire_check = OCC.BRepCheck.BRepCheck_Wire(self._wrapped_instance)
        check_orientation = wire_check.Orientation(OCC.TopoDS.TopoDS_Face())  # call with Null face

        # Buggy SelfIntersect ?
        # edge_1 = OCC.TopoDS.TopoDS_Edge()
        # edge_2 = OCC.TopoDS.TopoDS_Edge()
        # check_self_intersect = wire_check.SelfIntersect(OCC.TopoDS.TopoDS_Face(), edge_1, edge_2)

        if check_orientation != OCC.BRepCheck.BRepCheck_NoError:
            # check_self_intersect != OCC.BRepCheck.BRepCheck_NoError):
            return False
        else:
            return True

    def to_curve(self, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE, order=OCC.GeomAbs.GeomAbs_C2,
                 max_segment=200, max_order=12):
        r"""A wire can consist of many edges.

        These edges are merged given a tolerance and a curve

        Parameters
        ----------
        wire : OCC.TopoDS.TopoDS_Wire
        tolerance : float, optional
        order : OCC.GeomAbs.GeomAbs_C*, optional
        max_segment : int, optional
        max_order : int, optional

        Returns
        -------
        OCC.Geom.Geom_BSplineCurve

        """
        adap = OCC.BRepAdaptor.BRepAdaptor_CompCurve(self._wrapped_instance)
        hadap = OCC.BRepAdaptor.BRepAdaptor_HCompCurve(adap)
        approx = OCC.Approx.Approx_Curve3d(hadap.GetHandle(), tolerance, order, max_segment, max_order)
        with aocutils.common.AssertIsDone(approx, 'not able to compute approximation from wire'):
            return approx.Curve().GetObject()

    def to_adaptor_3d(self):
        r"""Abstract curve like geom_type into an adaptor3d

        Parameters
        ----------
        curve

        Returns
        -------

        """
        return OCC.BRepAdaptor.BRepAdaptor_CompCurve(self._wrapped_instance)
