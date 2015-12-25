#!/usr/bin/python
# coding: utf-8

r"""Boolean operations"""

import logging

import OCC.BRepAlgoAPI

import aocutils.exceptions
import aocutils.tolerance

logger = logging.getLogger(__name__)


def common(shape_1, shape_2):
    r"""Boolean operation : Common

    Parameters
    ----------
    shape_1 : TopoDS_Shape
    shape_2 : TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    algo_common = OCC.BRepAlgoAPI.BRepAlgoAPI_Common(shape_1, shape_2)
    logger.debug("OCC.BRepAlgoAPI.BRepAlgoAPI_Common.BuilderCanWork()? : {answer}"
                 .format(answer=algo_common.BuilderCanWork()))
    _error = {0: '- Ok',
              1: '- The Object is created but Nothing is Done',
              2: '- Null source shapes is not allowed',
              3: '- Check types of the arguments',
              4: '- Can not allocate memory for the DSFiller',
              5: '- The Builder can not work with such types of arguments',
              6: '- Unknown operation is not allowed',
              7: '- Can not allocate memory for the Builder'}

    if algo_common.ErrorStatus() != 0:
        msg = _error[algo_common.ErrorStatus()]
        logger.error(msg)
        raise aocutils.exceptions.BooleanCommonException()
    else:
        logger.debug('BRepAlgoAPI_Common status: {status}'.format(status=_error[algo_common.ErrorStatus()]))

    return algo_common.Shape()


def cut(shape_to_cut_from, cutting_shape):
    r"""Boolean cut

    Parameters
    ----------
    shape_to_cut_from : OCC.TopoDS.TopoDS_Shape
    cutting_shape : OCC.TopoDS.TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    try:
        brep_cut = OCC.BRepAlgoAPI.BRepAlgoAPI_Cut(shape_to_cut_from, cutting_shape)
        logger.info('Can work ? : %s' % str(brep_cut.BuilderCanWork()))
        _error = {0: '- Ok',
                  1: '- The Object is created but Nothing is Done',
                  2: '- Null source shapes is not allowed',
                  3: '- Check types of the arguments',
                  4: '- Can not allocate memory for the DSFiller',
                  5: '- The Builder can not work with such types of arguments',
                  6: '- Unknown operation is not allowed',
                  7: '- Can not allocate memory for the Builder'}
        logger.info('Error status : %s' % str(_error[brep_cut.ErrorStatus()]))
        brep_cut.RefineEdges()
        brep_cut.FuseEdges()
        shp = brep_cut.Shape()
        brep_cut.Destroy()
        return shp
    except:
        msg = "Failed to boolean cut"
        logger.error(msg)
        raise aocutils.exceptions.BooleanCutException(msg)


def fuse(shape_to_cut_from, joining_shape):
    r"""Boolean fuse

    Parameters
    ----------
    shape_to_cut_from : OCC.TopoDS.TopoDS_Shape
    joining_shape : OCC.TopoDS.TopoDS_Shape

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    join = OCC.BRepAlgoAPI.BRepAlgoAPI_Fuse(shape_to_cut_from, joining_shape)
    join.RefineEdges()
    join.FuseEdges()
    shape = join.Shape()
    join.Destroy()
    return shape
