#!/usr/bin/python
# coding: utf-8

r"""default display options"""

from __future__ import division

import logging

import aocutils.display.backends
import aocutils.display.color

logger = logging.getLogger(__name__)

backend = "wx"

if backend not in aocutils.display.backends.available_backends():
    msg = "%s backend is not available" % backend
    logger.error(msg)
    raise ValueError(msg)


