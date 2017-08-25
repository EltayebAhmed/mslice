import numpy as np
import operator
from mantid.simpleapi import BinMD, CreateMDHistoWorkspace, ReplicateMD

class Workspace(object):

    def __init__(self, matrix_workspace):
        self.inner_workspace = matrix_workspace

    def get_coordinates(self):
        coords = {}
        for i in range(self.inner_workspace.getNumDims()):
            dim = self.inner_workspace.getDimension(i)
            coords[dim.getName()] = np.linspace(dim.getMinimum(), dim.getMaximum(), dim.getNBins())
        return coords

    def get_signal(self):
        return self.inner_workspace.extractY()

    def get_error(self):
        return self.inner_workspace.extractE()

    def get_variance(self):
        return np.square(self.get_error())

    def _binary_op(self, operator, other):
        if isinstance(other, list):
            other = np.asarray(other)
        if isinstance(other, Workspace):
            inner_res = operator(self.inner_workspace, other.inner_workspace) #dimensionality/binning checks?
        elif isinstance(other, np.ndarray):
            inner_res = self._binary_op_list(operator, other)
        else:
            inner_res = operator(self.inner_workspace, other)
        workspace_type = type(self)
        return workspace_type(inner_res)

    def _binary_op_list(self, operator, other): #Does not work, seek help
        min = np.amin(other)
        max = np.amax(other)
        size = other.size
        try:
            ws = CreateMDHistoWorkspace(Dimensionality=1, Extents='' + str(min) + ',' + str(max),
                                        SignalInput=other, ErrorInput=other, NumberOfBins=str(size), Names='Dim1',
                                        Units='MomentumTransfer')
            print self.inner_workspace.getNumDims()
            print ws.getNumDims()
            replicated = ReplicateMD(self.inner_workspace, ws)
            inner_res = operator(self.inner_workspace, replicated)
        except RuntimeError:
            raise RuntimeError("List or array must have same number of elements as an axis of the workspace")

    def __add__(self, other):
        return self._binary_op(operator.add, other)

    def __sub__(self, other):
        return self._binary_op(operator.sub, other)

    def __mul__(self, other):
        return self._binary_op(operator.mul, other)

    def __div__(self, other):
        return self._binary_op(operator.div, other)

    def __pow__(self, other):
        orig = self
        new = self
        while other > 1:
            new = new * orig
            other-=1
        return new

    def __neg__(self):
        return self * -1
