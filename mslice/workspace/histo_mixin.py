from __future__ import (absolute_import, division, print_function)
import numpy as np
from mslice.util.numpy_helper import apply_with_corrected_shape
from mantid.simpleapi import CloneWorkspace


class HistoMixin(object):

    def get_signal(self):
        """Gets data values (Y axis) from the workspace as a numpy array."""
        return self._raw_ws.getSignalArray().copy()

    def get_error(self):
        """Gets error values (E) from the workspace as a numpy array."""
        return np.sqrt(self.get_variance(False))

    def get_variance(self, copy=True):
        """Gets variance (error^2) from the workspace as a numpy array."""
        variance = self._raw_ws.getErrorSquaredArray()
        return variance.copy() if copy else variance

    def set_signal(self, signal):
        self._raw_ws.setSignalArray(signal)

    def _binary_op_array(self, operator, other):
        """
        Perform binary operation (+,-,*,/) using a 1D numpy array.

        :param operator: binary operator to apply (add/sub/mul/div)
        :param other: 1D numpy array to use with operator.
        :return: new HistogramWorkspace
        """
        signal = self.get_signal()
        new_ws = CloneWorkspace(InputWorkspace=self._raw_ws, StoreInADS=False)
        error = RuntimeError("List or array must have same number of elements as an axis of the workspace")
        new_signal = apply_with_corrected_shape(operator, signal, other, error)
        new_ws.setSignalArray(new_signal)
        return new_ws
