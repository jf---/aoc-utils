# coding: utf-8

r"""face.py module of occutils
"""

import logging
# import functools

import OCC.BRepBuilderAPI
import OCC.BRep
import OCC.BRepTopAdaptor
import OCC.BRepFill
import OCC.Geom
import OCC.GeomAbs
import OCC.GeomAPI
import OCC.GeomLib
import OCC.TopAbs
import OCC.TopExp
import OCC.TopoDS
import OCC.GeomLProp
import OCC.BRepTools
import OCC.BRepAdaptor
import OCC.ShapeAnalysis
import OCC.GeomProjLib
import OCC.Adaptor3d
import OCC.gp
import OCC.BRepCheck

import aocutils.brep.base
import aocutils.common
import aocutils.brep.edge
import aocutils.topology
import aocutils.exceptions
import aocutils.tolerance
import aocutils.types

logger = logging.getLogger(__name__)


class Face(aocutils.brep.base.BaseObject):
    r"""High level surface API
    object is a Face if part of a Solid
    otherwise the same methods do apply, apart from the topology obviously

    Parameters
    ----------
    face

    """
    def __init__(self, topods_face):
        if not isinstance(topods_face, OCC.TopoDS.TopoDS_Face):
            msg = 'need a TopoDS_Face, got a %s' % topods_face.__class__
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)

        assert not topods_face.IsNull()

        aocutils.brep.base.BaseObject.__init__(self, topods_face, 'face')

        self._surface_handle = None
        self._adaptor = None
        self._adaptor_handle = None
        self._classify_uv = None

    @property
    def topods_face(self):
        return self._wrapped_instance

    def check(self):
        r"""Check the face"""
        # super(Face, self).check()
        # todo : call BRepCheck_Face methods
        return OCC.BRepCheck.BRepCheck_Face(self._wrapped_instance)

    # aliasing of useful methods
    @property
    def is_u_periodic(self):
        r"""Is U periodic ?

        Returns
        -------
        bool

        """
        return self.adaptor.IsUPeriodic()

    @property
    def is_v_periodic(self):
        r"""Is V periodic ?

        Returns
        -------
        bool
        """
        return self.adaptor.IsVPeriodic()

    @property
    def is_u_closed(self):
        r"""Is U closed ?

        Returns
        -------
        bool

        """
        return self.adaptor.IsUClosed()

    @property
    def is_v_closed(self):
        r"""Is V closed ?

        Returns
        -------
        bool

        """
        return self.adaptor.IsVClosed()

    @property
    def is_u_rational(self):
        r"""Is U rational ?

        Returns
        -------
        bool

        """
        return self.adaptor.IsURational()

    @property
    def is_v_rational(self):
        r"""Is V rational ?

        Returns
        -------
        bool

        """
        return self.adaptor.IsVRational()

    @property
    def u_degree(self):
        r"""Degree of U

        Returns
        -------
        int

        """
        return self.adaptor.UDegree()

    @property
    def v_degree(self):
        r"""Degree of V

        Returns
        -------
        int

        """
        return self.adaptor.VDegree()

    @staticmethod
    def _continuities():
        return ["GeomAbs_C0", "GeomAbs_G1", "GeomAbs_C1", "GeomAbs_G2", "GeomAbs_C2", "GeomAbs_C3", "GeomAbs_CN"]

    @property
    def u_continuity(self):
        r"""U continuity

        Returns
        -------
        int

        """
        return self._continuities()[self.adaptor.UContinuity()]

    @property
    def v_continuity(self):
        r"""V continuity

        Returns
        -------
        int

        """
        return self._continuities()[self.adaptor.VContinuity()]

    @property
    def domain(self):
        r"""The u,v domain of the curve

        Returns
        -------
        UMin, UMax, VMin, VMax : tuple of float

        """
        return OCC.BRepTools.breptools_UVBounds(self._wrapped_instance)

    def _midpoint(self):
        """u, v parameters at the mid point of the face, and its corresponding gp_Pnt

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        u_min, u_max, v_min, v_max = self.domain
        u_mid = (u_min + u_max) / 2.
        v_mid = (v_min + v_max) / 2.
        return (u_mid, v_mid), self.adaptor.Value(u_mid, v_mid)

    @property
    def midpoint(self):
        r"""Midpoint

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        return self._midpoint()[1]

    @property
    def midpoint_parameters(self):
        r"""Values of u and v at midpoint

        Returns
        -------
        tuple[float]
            u and v values at midpoint

        """
        return self._midpoint()[0]

    @property
    def surface(self):
        r"""Surface

        Returns
        -------
        OCC.Geom.Geom_Surface or subclass

        """
        return self.surface_handle.GetObject()

    @property
    def surface_handle(self):
        r"""Surface handle

        Returns
        -------
        Handle <Geom_Surface>

        """
        if self._surface_handle is None:
            self._surface_handle = OCC.BRep.BRep_Tool_Surface(self._wrapped_instance)
        return self._surface_handle

    @property
    def adaptor(self):
        r"""Adaptor

        Returns
        -------
        OCC.BRepAdaptor.BRepAdaptor_Surface

        """
        if self._adaptor is None:
            self._adaptor = OCC.BRepAdaptor.BRepAdaptor_Surface(self._wrapped_instance)
        return self._adaptor

    @property
    def adaptor_handle(self):
        r"""Adaptor handle

        Returns
        -------
        OCC.BRepAdaptor.BRepAdaptor_HSurface

        """
        if self._adaptor_handle is None:
            self._adaptor_handle = OCC.BRepAdaptor.BRepAdaptor_HSurface()
            self._adaptor_handle.Set(self.adaptor)
        return self._adaptor_handle

    @property
    def is_closed(self):
        r""" Is the face closed ?

        Returns
        -------
        tuple[bool]

        """
        sa = OCC.ShapeAnalysis.ShapeAnalysis_Surface(self.surface_handle)
        # sa.GetBoxUF()
        return sa.IsUClosed(), sa.IsVClosed()

    def is_planar(self, tol=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
        """Checks if the surface is planar within a tolerance

        Parameters
        ----------
        tol : float

        Returns
        -------
        bool

        """
        # logger.debug(str(self.surface_handle))
        # is_planar_surface = OCC.GeomLib.GeomLib_IsPlanarSurface(self.surface_handle, tol)
        return OCC.GeomLib.GeomLib_IsPlanarSurface(self.surface_handle, tol).IsPlanar()

    @property
    def is_plane(self):
        r"""Is plane?

        Returns
        -------
        bool
            True if the TopoDS_Shape is a plane, False otherwise

        See Also
        --------
        face.py's Face.is_planar()

        """

        hs = OCC.BRep.BRep_Tool_Surface(self._wrapped_instance)
        downcast_result = OCC.Geom.Handle_Geom_Plane().DownCast(hs)
        # the handle is null if downcast failed or is not possible,
        # that is to say the face is not a plane
        if downcast_result.IsNull():
            return False
        else:
            return True

    @property
    def is_trimmed(self):
        r"""Is the face trimmed?

        Returns
        -------
        bool
            True if the Wire delimiting the Face lies on the bounds of the surface
            if this is not the case, the wire represents a contour that delimits the face [ think cookie cutter ]
            and implies that the surface is trimmed
        """
        a = list(map(lambda x: round(x, 3), OCC.BRepTools.breptools_UVBounds(self._wrapped_instance)))
        b = list(map(lambda x: round(x, 3), self.adaptor.Surface().Surface().GetObject().Bounds()))
        if a != b:
            logger.info('%s, %s' % (str(a), str(b)))
            return True
        return False

    def on_trimmed(self, u, v):
        r"""Tests whether the surface at the u,v parameter has been trimmed

        Parameters
        ----------
        u
        v

        Returns
        -------
        bool

        """
        if self._classify_uv is None:
            self._classify_uv = OCC.BRepTopAdaptor.BRepTopAdaptor_FClass2d(self._wrapped_instance, 1e-9)
        uv = OCC.gp.gp_Pnt2d(u, v)
        if self._classify_uv.Perform(uv) == OCC.TopAbs.TopAbs_IN:
            return True
        else:
            return False

    def parameter_to_point(self, u, v):
        r"""Coordinate at u,v

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        return self.surface.Value(u, v)

    def point_to_parameter(self, pt):
        r"""uv value of a point on a surface

        Parameters
        ----------
        pt : OCC.gp.gp_Pnt

        Returns
        -------
        tuple[float]
            u, v coordinates

        """
        sas = OCC.ShapeAnalysis.ShapeAnalysis_Surface(self.surface_handle)
        uv = sas.ValueOfUV(pt, self.tolerance)
        return uv.X(), uv.Y()

    def continuity_edge_face(self, edge, face):
        r"""compute the continuity between two faces at edge

        Parameters
        ----------
        edge :
            an occutils.edge.Edge or OCC.TopoDS.TopoDS_Edge from :face:
        face : Face or OCC.TopoDS.TopoDS_Face

        Returns
        -------
        bool, GeomAbs_Shape
            bool, GeomAbs_Shape if it has continuity, otherwise False, None

        """
        bt = OCC.BRep.BRep_Tool()
        if bt.HasContinuity(edge, self._wrapped_instance, face):
            continuity = bt.Continuity(edge, self._wrapped_instance, face)
            return True, continuity
        else:
            return False, None

# ===========================================================================
#    Surface.project
#    project curve, point on face
# ===========================================================================

    def project_vertex(self, pnt, tol=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
        r"""Projects self with a point, curve, edge, face, solid method wraps dealing with the various topologies

        Parameters
        ----------
        pnt : OCC.TopoDS.TopoDS_Vertex or OCC.gp.gp_Pnt
        tol : float

        Returns
        -------
        uv, point

        """
        if isinstance(pnt, OCC.TopoDS.TopoDS_Vertex):
            pnt = OCC.BRep.BRep_Tool.Pnt(pnt)

        proj = OCC.GeomAPI.GeomAPI_ProjectPointOnSurf(pnt, self.surface_handle, tol)
        # uv = proj.LowerDistanceParameters()
        proj_pnt = proj.NearestPoint()

        return proj.LowerDistanceParameters(), proj_pnt

    def project_curve(self, other):
        r"""Project a curve on face(self)

        Parameters
        ----------
        other : OCC.TopoDS.TopoDS_Edge or OCC.Geom.Geom_Curve (or subclass)

        Returns
        -------
        Handle< Geom_Curve >

        """
        # this way Geom_Circle and alike are valid too
        if isinstance(other, OCC.TopoDS.TopoDS_Edge) or isinstance(other, OCC.Geom.Geom_Curve) \
                or issubclass(other, OCC.Geom.Geom_Curve):
                # convert edge to curve
                first, last = OCC.TopExp.topexp.FirstVertex(other), OCC.TopExp.topexp.LastVertex(other)
                lbound, ubound = OCC.BRep.BRep_Tool().Parameter(first, other), OCC.BRep.BRep_Tool().Parameter(last,
                                                                                                              other)
                other = OCC.BRep.BRep_Tool.Curve(other, lbound, ubound).GetObject()

                # Project (const Handle< Geom_Curve > &C, const Handle< Geom_Surface > &S)
                return OCC.GeomProjLib.geomprojlib.Project(other, self.surface_handle)

    def project_edge(self, edg):
        r"""Project edge

        Parameters
        ----------
        edg : occutils.brep.edge.Edge

        Returns
        -------
        Handle< Geom_Curve >

        """
        if hasattr(edg, 'adaptor'):
            return self.project_curve(self.adaptor)
        return self.project_curve(aocutils.brep.edge.Edge(edg).adaptor())

    def iso_curve(self, u_or_v, param):
        r"""Get the iso curve from a u,v + parameter

        Parameters
        ----------
        u_or_v : str
            'u' or 'v'
        param : float

        Returns
        -------
        OCC.Adaptor3d.Adaptor3d_IsoCurve

        """
        uv = 0 if u_or_v == 'u' else 1
        return OCC.Adaptor3d.Adaptor3d_IsoCurve(self.adaptor_handle.GetHandle(), uv, param)

    @property
    def edges(self):
        r"""Edges of the face

        Returns
        -------
        list[occutils.brep.edge.Edge]

        """
        return [aocutils.brep.edge.Edge(i)
                for i in aocutils.topology.WireExplorer(next(self.topo.wires)).ordered_edges]

    def local_props(self, u, v):
        r"""Curvature at the u parameter
        the local_props object can be returned too using curvatureType == curvatureType
        curvatureTypes are:
            gaussian
            minimum
            maximum
            mean
            curvatureType

        Parameters
        ----------
        u
        v

        Returns
        -------
        OCC.GeomLProp.GeomLProp_SLProps

        """
        _local_props = OCC.GeomLProp.GeomLProp_SLProps(self.surface_handle, u, v, 1, 1e-6)

        _domain = self.domain
        if u in _domain or v in _domain:
            logger.info('<<<CORRECTING DOMAIN...>>>')
            div = 1000
            delta_u, delta_v = (_domain[0] - _domain[1])/div, (_domain[2] - _domain[3])/div

            if u in _domain:
                low, hi = u-_domain[0], u-_domain[1]
                if low < hi:
                    u -= delta_u
                else:
                    u += delta_u

            if v in _domain:
                low, hi = v-_domain[2], v-_domain[3]
                if low < hi:
                    v -= delta_v
                else:
                    v += delta_v

        _local_props.SetParameters(u, v)

        return _local_props

    def gaussian_curvature(self, u, v):
        r"""Gaussian local_props

        Parameters
        ----------
        u
        v

        Returns
        -------
        float

        """
        return self.local_props(u, v).GaussianCurvature()

    def min_curvature(self, u, v):
        r"""Minimum local_props

        Parameters
        ----------
        u
        v

        Returns
        -------
        float

        """
        return self.local_props(u, v).MinCurvature()

    def mean_curvature(self, u, v):
        r"""Mean local_props

        Parameters
        ----------
        u
        v

        Returns
        -------
        float

        """
        return self.local_props(u, v).MeanCurvature()

    def max_curvature(self, u, v):
        r"""Maximum local_props

        Parameters
        ----------
        u
        v

        Returns
        -------
        float

        """
        return self.local_props(u, v).MaxCurvature()

    def normal(self, u, v):
        r"""Normal

        Parameters
        ----------
        u
        v

        Returns
        -------
        OCC.gp.gp_Vec

        """
        curv = self.local_props(u, v)
        if curv.IsNormalDefined():
            norm = curv.Normal()
            if self.orientation == OCC.TopAbs.TopAbs_REVERSED:
                norm.Reverse()
            return OCC.gp.gp_Vec(norm.X(), norm.Y(), norm.Z())
        else:
            msg = "normal is not defined at u,v: {0}, {1}".format(u, v)
            logger.error(msg)
            raise ValueError(msg)

    def tangent(self, u, v):
        r"""Tangent

        Parameters
        ----------
        u
        v

        Returns
        -------
        tuple[OCC.gp.gp_Vec]
            U tangent, V tangent

        """
        du, dv = OCC.gp.gp_Dir(), OCC.gp.gp_Dir()
        curv = self.local_props(u, v)
        if curv.IsTangentUDefined() and curv.IsTangentVDefined():
            curv.TangentU(du), curv.TangentV(dv)
            return OCC.gp.gp_Vec(du.X(), du.Y(), du.Z()), OCC.gp.gp_Vec(dv.X(), dv.Y(), dv.Z())
        else:
            msg = 'Tangent not defined in U or V'
            logger.error(msg)
            raise aocutils.exceptions.TangentException(msg)

    def radius(self, u, v):
        r"""Radius at u

        Parameters
        ----------
        u
        v

        Returns
        -------
        float

        """
        # TODO: SHOULD WE RETURN A SIGNED RADIUS? ( get rid of abs() )?
        try:
            _crv_min = 1. / self.min_curvature(u, v)
        except ZeroDivisionError:
            return float('inf')

        try:
            _crv_max = 1. / self.max_curvature(u, v)
        except ZeroDivisionError:
            return float('inf')

        return abs((_crv_min + _crv_max)/2.)

    @property
    def geom_type(self):
        r"""Geometrical geom_type"""
        return aocutils.types.surface_lut[self.adaptor.GetType()]

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()
