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

color = aocutils.display.color.color(0, 0, 1)
fp_dark_blue = aocutils.display.color.color(34 / 255, 45 / 255, 90 / 255)
fp_intermediate_blue = aocutils.display.color.color(61 / 255, 79 / 255, 153 / 255)
fp_neon_blue = aocutils.display.color.color(0, 184 / 255, 1)
fp_light_orange = aocutils.display.color.color(1, 136 / 255, 164 / 255)
fp_dark_orange = aocutils.display.color.color(204 / 255, 63 / 255, 20 / 255)
