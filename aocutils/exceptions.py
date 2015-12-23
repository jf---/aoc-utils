#!/usr/bin/python
# coding: utf-8

r"""exceptions module for aocutils"""


class AocUtilsException(Exception):
    r"""Base exception"""
    pass


class ParameterOutOfDomainException(AocUtilsException):
    r"""A function was invoked with a parameter outside of the object parameter domain"""
    pass


class BooleanCutException(AocUtilsException):
    r"""Something went wrong with a boolean cut"""
    pass


class OffsetShapeException(AocUtilsException):
    r"""Something went wrong with an offset shape"""
    pass


class FindPlaneException(AocUtilsException):
    r"""Something went wrong with a find plane operation"""
    pass


class InterpolationException(AocUtilsException):
    r"""Something went wrong with an interpolation"""
    pass


class WrongTopologicalType(AocUtilsException):
    r"""The topological geom_type is wrong"""
    pass


class UniformAbscissaException(AocUtilsException):
    r"""Uniform abscissa exception"""
    pass


class CurveHandleException(AocUtilsException):
    r"""Curve handle exception"""
    pass


class SurfaceHandleException(AocUtilsException):
    r"""Surface handle exception"""
    pass


class TangentException(AocUtilsException):
    r"""Tangent exception"""
    pass


class NoCommonVertexException(AocUtilsException):
    r"""No common vertex exception"""
    pass


class BRepBuildingException(AocUtilsException):
    r"""Something went wrong while building a BRep"""
    pass
