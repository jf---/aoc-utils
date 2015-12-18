#!/usr/bin/python
# coding: utf-8

r"""exceptions module for occutils"""


class OccUtilsException(Exception):
    r"""Base exception"""
    pass


class BooleanCutException(OccUtilsException):
    r"""Something went wrong with a boolean cur"""
    pass


class OffsetShapeException(OccUtilsException):
    r"""Something went wrong with an offset shape"""
    pass


class FindPlaneException(OccUtilsException):
    r"""Something went wrong with a find plane operation"""
    pass


class InterpolationException(OccUtilsException):
    r"""Something went wrong with an interpolation"""
    pass


class WrongTopologicalType(OccUtilsException):
    r"""The topological geom_type is wrong"""
    pass


class UniformAbscissaException(OccUtilsException):
    r"""Uniform abscissa exception"""
    pass


class CurveHandleException(OccUtilsException):
    r"""Curve handle exception"""
    pass


class SurfaceHandleException(OccUtilsException):
    r"""Surface handle exception"""
    pass


class TangentException(OccUtilsException):
    r"""Tangent exception"""
    pass


class NoCommonVertexException(OccUtilsException):
    r"""No common vertex exception"""
    pass


class BRepBuildingException(OccUtilsException):
    r"""Something went wrong while building a BRep"""
    pass
