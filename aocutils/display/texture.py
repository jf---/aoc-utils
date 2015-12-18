# coding: utf-8

r"""texture.py module of occutils

Classes
-------
    Texture
        texture_scale()
        texture_repeat()
        texture_origin()

"""

import os
import os.path


class Texture(object):
    """This class encapsulates the necessary texture properties: Filename, toScaleU, etc.

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise IOError("File %s not found.\n" % filename)
        self._filename = filename
        self._toScaleU = 1.0
        self._toScaleV = 1.0
        self._toRepeatU = 1.0
        self._toRepeatV = 1.0
        self._originU = 0.0
        self._originV = 0.0

    def texture_scale(self, to_scale_u, to_scale_v):
        r"""

        Parameters
        ----------
        to_scale_u
        to_scale_v

        Returns
        -------

        """
        self._toScaleU = to_scale_u
        self._toScaleV = to_scale_v

    def texture_repeat(self, to_repeat_u, to_repeat_v):
        r"""

        Parameters
        ----------
        to_repeat_u
        to_repeat_v

        Returns
        -------

        """
        self._toRepeatU = to_repeat_u
        self._toRepeatV = to_repeat_v

    def texture_origin(self, origin_u, origin_v):
        r"""

        Parameters
        ----------
        origin_u
        origin_v

        Returns
        -------

        """
        self._originU = origin_u
        self._originV = origin_v

    # def get_properties(self):
    def GetProperties(self):  # OCC viewer needs texture.GetProperties()
        r"""Properties

        Returns
        -------
        tuple

        """
        return (self._filename, self._toScaleU, self._toScaleV, self._toRepeatU, self._toRepeatV, self._originU,
                self._originV)
