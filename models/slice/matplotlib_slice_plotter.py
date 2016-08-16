from slice_plotter import SlicePlotter
from presenters.slice_plotter_presenter import INVALID_INTENSITY,INVALID_PARAMS,INVALID_SMOOTHING,INVALID_X_PARAMS,\
    INVALID_X_UNITS,INVALID_Y_PARAMS,INVALID_Y_UNITS
from models.workspacemanager.mantid_workspace_provider import MantidWorkspaceProvider
from mantid.simpleapi import BinMD
from mantid.api import IMDEventWorkspace
from math import floor
import numpy as np
from plotting import pyplot as plt


def get_aspect_ratio(workspace):
    return 'auto'

class MatplotlibSlicePlotter(SlicePlotter):
    def __init__(self):
        self._workspace_provider = MantidWorkspaceProvider()
    def display_slice(self, selected_workspace, x_axis, y_axis, smoothing, intensity_start, intensity_end, norm_to_one,
                      colourmap):
        try:
            x_axis.step = float(x_axis.step)
            x_axis.start = float(x_axis.start)
            x_axis.end = float(x_axis.end)
        except ValueError:
            return INVALID_X_PARAMS
        try:
            y_axis.step = float(x_axis.step)
            y_axis.start = float(y_axis.start)
            y_axis.end = float(y_axis.end)
        except ValueError:
            return  INVALID_Y_PARAMS
        workspace = self._workspace_provider.get_workspace_handle(selected_workspace)
        if isinstance(workspace,IMDEventWorkspace):
            # TODO ask if this slice should live in ADS after plotting?
            # TODO implement axis swapping
            # TODO implement input validation and return appropriate error codes
            # Deduct values not supplied by user from workspace
            self._fill_in_missing_input(x_axis, workspace)
            self._fill_in_missing_input(y_axis, workspace)
            error_code = self._validate_input(x_axis,y_axis,intensity_start,intensity_end)
            if error_code:
                return error_code
            # TODO make shown workspaces refresh after this is called
            n_x_bins = self._get_number_of_steps(x_axis)
            n_y_bins = self._get_number_of_steps(y_axis)
            x_dim = workspace.getDimension(0)
            y_dim = workspace.getDimension(1)
            xbinning = x_dim.getName() + "," + str(x_axis.start) + "," + str(x_axis.end) + "," + str(n_x_bins)
            ybinning = y_dim.getName() + "," + str(y_axis.start) + "," + str(y_axis.end) + "," + str(n_y_bins)
            slice = BinMD(InputWorkspace=workspace, AxisAligned="1", AlignedDim0=xbinning, AlignedDim1=ybinning)
            plot_data = slice.getSignalArray() / slice.getNumEventsArray()
            plot_data = np.ma.masked_where(np.isnan(plot_data), plot_data)
            # The flipud is because mantid plots first row of array at top of plot
            # rot90 switches the x and y axis to to plot what user expected.
            plot_data = np.rot90(plot_data)
            plot_data = np.flipud(plot_data)
            x_step = x_dim.getX(1) - x_dim.getX(0)
            x = np.arange(x_axis.start, x_axis.end +x_axis.step/2, x_axis.step)
            y_step = y_dim.getX(1) - y_dim.getX(0)
            y = np.arange(y_axis.start, y_axis.end + x_axis.step/2 , y_axis.step)
            #TODO check maths to see if x and y align properly with plot or are off by half bin/ off by one
            xx, yy = np.meshgrid(x, y, indexing='xy')
            plt.pcolormesh(xx, yy, plot_data)
            plt.xlabel(x_dim.getName())
            plt.ylabel(y_dim.getName())
        else:
            ydata = []
            for i in range(workspace.getNumberHistograms()-1,-1,-1):
                ydata.append(workspace.readY(i))
            x_left = workspace.readX(0)[0]
            x_right = workspace.readX(0)[-1]
            y_top = workspace.getNumberHistograms() - 1
            y_bottom = 0
            plt.imshow(ydata,extent=[x_left, x_right, y_bottom, y_top], aspect=get_aspect_ratio(workspace))

    def _get_number_of_steps(self, axis):
        return int(max(1, floor(axis.end - axis.start)/axis.step))

    def _fill_in_missing_input(self,axis,workspace):
        """Deduct Values not supplied by user from workspace"""
        pass


    def _validate_input(self,x_axis, y_axis, intensity_start, intensity_end):
        return 0