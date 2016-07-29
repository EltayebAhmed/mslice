from sliceplotter.command import Command
from mainview import MainView
from sliceplotter.SlicePlotterView import SlicePlotterView
from sliceplotter.SlicePlotter import SlicePlotter
from collections import namedtuple

Axis = namedtuple('Axis', ['units', 'start', 'end', 'step'])

#TODO askOwen ,these constants exist in both sliceplotter and the presenter, where should they be defined?
INVALID_PARAMS = 1
INVALID_X_PARAMS = 2
INVALID_Y_PARAMS = 3
INVALID_INTENSITY = 4
INVALID_SMOOTHING = 5
INVALID_X_UNITS = 6
INVALID_Y_UNITS = 7


class SlicePlotterPresenter:
    def __init__(self, main_view, slice_view,slice_plotter):
        if not isinstance(main_view, MainView):
            raise TypeError("Parameter main_view is not of type MainView")
        if not isinstance(slice_view, SlicePlotterView):
            raise TypeError("Parameter slice_view is not of type SlicePlotterView")
        if not isinstance(slice_plotter, SlicePlotter):
            raise TypeError("Parameter slice_plotter is not of type SlicePlotter")
        self._slice_view = slice_view
        self._main_presenter = main_view.get_presenter()
        self._slice_plotter = slice_plotter

    def notify(self,command):
        if command == Command.DisplaySlice:
            self._display_slice()
        else:
            raise ValueError("Slice Plotter Presenter received an unrecognised command")

    def _display_slice(self):
        selected_workspaces = self._main_presenter.get_selected_workspaces()
        if not selected_workspaces:
            self._slice_view.error_select_one_workspace()
            return
        if len(selected_workspaces) > 1:
            pass
            #TODO is this okay? plot multiple? or error?
        selected_workspace = selected_workspaces[0]
        x_axis = Axis(self._slice_view.get_slice_x_axis(), self._slice_view.get_slice_x_start(),
                      self._slice_view.get_slice_x_end(), self._slice_view.get_slice_x_step())
        y_axis = Axis(self._slice_view.get_slice_y_axis(), self._slice_view.get_slice_y_start(),
                      self._slice_view.get_slice_y_end(), self._slice_view.get_slice_y_step())
        intensity_start = self._slice_view.get_slice_intensity_start()
        intensity_end = self._slice_view.get_slice_intensity_end()
        norm_to_one = self._slice_view.get_slice_is_norm_to_one()
        smoothing = self._slice_view.get_slice_smoothing()
        colourmap = self._slice_view.get_slice_colourmap()
        status = self._slice_plotter.display_slice(x_axis, y_axis, smoothing, intensity_start, intensity_end, norm_to_one,
                                          colourmap)
        if status == INVALID_PARAMS:
            self._slice_view.error_invalid_plot_parameters()

        elif status == INVALID_X_PARAMS:
            self._slice_view.error_invalid_x_params()

        elif status == INVALID_Y_PARAMS:
            self._slice_view.error_invalid_y_params()

        elif status == INVALID_INTENSITY:
            self._slice_view.error_invalid_intensity_params()

        elif status == INVALID_SMOOTHING:
            self._slice_view.error_invalid_smoothing_params()

        elif status == INVALID_X_UNITS:
            self._slice_view.error_invalid_x_units()

        elif status == INVALID_Y_UNITS:
            self._slice_view.error_invalid_y_units()