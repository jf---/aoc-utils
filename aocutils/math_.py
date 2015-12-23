#!/usr/bin/python
# coding: utf-8

r"""math_.py

Summary
-------
Mathematical utilities

"""


def roundlist(li, n_decimals=3):
    r"""Round all the elements of a list to n decimals

    Parameters
    ----------
    li : list[float]
        The list with unrounded elements
    n_decimals : int
        The number of decimals to round to

    Returns
    -------
    list[float]
        A list with rounded elements

    """
    # TODO : should we keep a function for such a simple comprehension
    return [round(value, n_decimals) for value in li]


def smooth_pnts(pnts):
    r"""Smooth the values in a list

    Parameters
    ----------
    pnts

    Returns
    -------
    list
        List of smoothed values
    """
    # TODO : make this work for gp_Pnt or Point
    # Initial implementation of occutils probably made this possible, even though addition and division implementation
    # for points was directly on gp_Pnt -> use wrapper instead
    smooth = [pnts[0]]
    for i in range(1, len(pnts)-1):
        prev = pnts[i - 1]
        this = pnts[i]
        next_pnt = pnts[i + 1]
        pt = (prev + this + next_pnt) / 3.0
        smooth.append(pt)
    smooth.append(pnts[-1])
    return smooth
