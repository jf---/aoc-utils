#!/usr/bin/python
# coding: utf-8

r"""geometry/plane.py
"""

import logging

import OCC.BRepBuilderAPI
import OCC.GeomPlate
import OCC.gp
import OCC.TColgp

import aocutils.exceptions
import aocutils.common
import aocutils.brep.vertex
import aocutils.convert.collections
import aocutils.topology
import aocutils.geom.vector


logger = logging.getLogger(__name__)


class Plane(object):
    r"""Wrapper for Geom_Plane

    """
    def __init__(self, geom_plane):
        self._geom_plane = geom_plane

    @property
    def geom_plane(self):
        return self._geom_plane

    @classmethod
    def from_shape(cls, shape, tolerance=-1):
        r"""Find a plane from a shape

        Parameters
        ----------
        shape : OCC.TopoDS.TopoDS_Shape
        tolerance : float

        Returns
        -------
        OCC.Geom.Geom_Plane

        """
        try:
            fpl = OCC.BRepBuilderAPI.BRepBuilderAPI_FindPlane(shape, tolerance)
            if fpl.Found():
                return cls(fpl.Plane().GetObject())
            else:
                msg = 'Plane not found in %s' % shape
                logger.error(msg)
                raise aocutils.exceptions.FindPlaneException(msg)
        except:
            msg = 'Could not find plane in %s' % shape
            logger.error(msg)
            raise aocutils.exceptions.FindPlaneException(msg)

    @classmethod
    def through_face_vertices(cls, _face):
        r"""Fit a plane through face vertices

        Parameters
        ----------
        _face : occutils.core.face.Face

        Returns
        -------
        Geom_Plane

        """
        uvs_from_vertices = [_face.project_vertex(aocutils.brep.vertex.Vertex.to_pnt(i))
                             for i in aocutils.topology.Topo(_face).vertices()]
        normals = [OCC.gp.gp_Vec(_face.DiffGeom.normal(*uv[0])) for uv in uvs_from_vertices]
        points = [i[1] for i in uvs_from_vertices]

        NORMALS = OCC.TColgp.TColgp_SequenceOfVec()
        [NORMALS.Append(i) for i in normals]
        POINTS = aocutils.convert.collections.to_tcol_(points, OCC.TColgp.TColgp_HArray1OfPnt)

        pl = OCC.GeomPlate.GeomPlate_BuildAveragePlane(NORMALS, POINTS).Plane().GetObject()
        vec = OCC.gp.gp_Vec(pl.Location(), _face.GlobalProperties.centre())
        pt = (pl.Location().as_vec() + vec).as_pnt()
        pl.SetLocation(pt)
        return cls(pl)

    def normal_vector(self, vec_length=1.):
        r"""Vector normal to the plane of length vec_length

        Parameters
        ----------
        plane
        vec_length

        Returns
        -------
        OCC.gp.gp_Vec

        """
        trns = OCC.gp.gp_Vec(self._geom_plane.Axis().Direction())
        return aocutils.geom.vector.Vector(trns.Normalized() * vec_length)
