#!/usr/bin/python
# coding: utf-8

r"""memory.py

Summary
-------
Memory measurement functions

Functions
---------
mem()
rss()
print_consumed_memory()


"""

from __future__ import print_function

import psutil
import sys
import os
import logging

logger = logging.getLogger(__name__)


def mem(size="rss"):
    """Generalization; memory sizes: rss, rsz, vsz.

    rss stands for Resident Set Size
    vsz is the Virtual Memory Size

    Parameters
    ----------
    size

    """
    process = psutil.Process(os.getpid())
    if size == "rss":
        return process.memory_info().rss  # cross-platform
    else:
        if sys.platform == "linux" or sys.platform == "linux2":
            return int(os.popen('ps -p %d -o %s | tail -1' % (os.getpid(), size)).read())
        else:
            raise NotImplementedError


def rss():
    """Return ps -o rss (resident) memory in kB."""
    return float(mem("rss")) / 1024


def print_consumed_memory():
    r"""Print consumed memory to the console"""
    msg = "memory consumption for current pid: %f Mb" % (rss() - initial_memory)
    logger.info(msg)
    print(msg)


initial_memory = rss()
msg = "Initial memory : %i" % initial_memory
logger.info(msg)
print(initial_memory)
