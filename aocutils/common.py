# coding: utf-8

r"""common.py module of occutils

Classes
-------
    AssertIsDone

"""
import logging

logger = logging.getLogger(__name__)


class AssertIsDone(object):
    r"""Raises an assertion error when IsDone() returns false, with the error specified in error_statement

    This is a context manager.

    """
    def __init__(self, to_check, error_statement):
        self.to_check = to_check
        self.error_statement = error_statement

    def __enter__(self, ):
        if self.to_check.IsDone():
            pass
        else:
            msg = self.error_statement
            logger.error(msg)
            raise AssertionError(msg)

    def __exit__(self, assertion_type, value, traceback):
        pass
