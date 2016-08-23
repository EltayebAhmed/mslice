from models.slice.slice_plotter import SlicePlotter
from views.slice_plotter_view import SlicePlotterView
from widgets.slice.command import Command
from validation_decorators import require_main_presenter
from interfaces.slice_plotter_presenter import SlicePlotterPresenterInterface
from interfaces.main_presenter import MainPresenterInterface


class Axis(object):
    def __init__(self, units, start, end, step):
        self.units = units
        self.start = start
        self.end = end
        self.step = step

    def __eq__(self, other):
        # This is required for Unit testing
        return self.units == other.units and self.start == other.start and self.end == other.end \
               and self.step == other.step and isinstance(other, Axis)

    def __repr__(self):
        info = (self.units, self.start, self.end, self.step)
        return "Axis(" + " ,".join(map(str, info)) + ")"


INVALID_PARAMS = 1
INVALID_X_PARAMS = 2
INVALID_Y_PARAMS = 3
INVALID_INTENSITY = 4
INVALID_SMOOTHING = 5
INVALID_X_UNITS = 6
INVALID_Y_UNITS = 7


class SlicePlotterPresenter(SlicePlotterPresenterInterface):
    def __init__(self, slice_view, slice_plotter, plot_module):
        if not isinstance(slice_view, SlicePlotterView):
            raise TypeError("Parameter slice_view is not of type SlicePlotterView")
        if not isinstance(slice_plotter, SlicePlotter):
            raise TypeError("Parameter slice_plotter is not of type SlicePlotter")
        self._slice_view = slice_view
        self._main_presenter = None
        self._slice_plotter = slice_plotter
        colormaps = self._slice_plotter.get_available_colormaps()
        self._slice_view.populate_colormap_options(colormaps)
        self._plot_module = plot_module

    def register_master(self, main_presenter):
        assert (isinstance(main_presenter, MainPresenterInterface))
        self._main_presenter = main_presenter
        self._main_presenter.subscribe_to_workspace_selection_monitor(self)

    def notify(self, command):
        if command == Command.DisplaySlice:
            self._display_slice()
        else:
            raise ValueError("Slice Plotter Presenter received an unrecognised command")

    def _display_slice(self):
        selected_workspaces = self._get_main_presenter().get_selected_workspaces()
        if not selected_workspaces or len(selected_workspaces) > 1:
            self._slice_view.error_select_one_workspace()
            return

        selected_workspace = selected_workspaces[0]
        x_axis = Axis(self._slice_view.get_slice_x_axis(), self._slice_view.get_slice_x_start(),
                      self._slice_view.get_slice_x_end(), self._slice_view.get_slice_x_step())
        y_axis = Axis(self._slice_view.get_slice_y_axis(), self._slice_view.get_slice_y_start(),
                      self._slice_view.get_slice_y_end(), self._slice_view.get_slice_y_step())
        status = self._process_axis(x_axis, y_axis)
        if status == INVALID_Y_PARAMS:
            self._slice_view.error_invalid_y_params()
            return
        elif status == INVALID_X_PARAMS:
            self._slice_view.error_invalid_x_params()
            return
        elif status == INVALID_PARAMS:
            self._slice_view.error_invalid_plot_parameters()
            return

        intensity_start = self._slice_view.get_slice_intensity_start()
        intensity_end = self._slice_view.get_slice_intensity_end()
        norm_to_one = bool(self._slice_view.get_slice_is_norm_to_one())
        smoothing = self._slice_view.get_slice_smoothing()
        colourmap = self._slice_view.get_slice_colourmap()
        try:
            intensity_start = self._to_float(intensity_start)
            intensity_end = self._to_float(intensity_end)
        except ValueError:
            self._slice_view.error_invalid_intensity_params()
            return

        if intensity_start is not None and intensity_end is not None and intensity_start > intensity_end:
            self._slice_view.error_invalid_intensity_params()
            return
        try:
            smoothing = self._to_int(smoothing)
        except ValueError:
            self._slice_view.error_invalid_smoothing_params()

        try:
            plot_data, boundaries, colormap, norm = self._slice_plotter.display_slice(selected_workspace, x_axis,
                                                                                      y_axis,
                                                                                      smoothing, intensity_start,
                                                                                      intensity_end, norm_to_one,
                                                                                      colourmap)
        except NotImplementedError as e:
            self._slice_view.error(e.message)
            return
        try:
            self._plot_module.imshow(plot_data, extent=boundaries, cmap=colourmap, aspect='auto', norm=norm,
                                interpolation='none')
        except ValueError:
            # This gets thrown by matplotlib if the supplied intensity_min > data_max_value or vise versa
            self._slice_view.error_invalid_intensity_params()
            return
        self._plot_module.xlabel(x_axis.units)
        self._plot_module.ylabel(y_axis.units)

    @require_main_presenter
    def _get_main_presenter(self):
        return self._main_presenter

    def _process_axis(self, x, y):
        if x.units == y.units:
            return INVALID_PARAMS
        try:
            x.start = self._to_float(x.start)
            x.step = self._to_float(x.step)
            x.end = self._to_float(x.end)
        except ValueError:
            return INVALID_X_PARAMS

        try:
            y.start = self._to_float(y.start)
            y.step = self._to_float(y.step)
            y.end = self._to_float(y.end)
        except ValueError:
            return INVALID_Y_PARAMS

        if x.start and x.end:
            if x.start > x.end:
                return INVALID_X_PARAMS

        if y.start is not None and y.end is not None:
            if y.start > y.end:
                return INVALID_Y_PARAMS

    def _to_float(self, x):
        x = x.strip()
        if x is None or x == "":
            return None
        return float(x)

    def _to_int(self, x):
        x.strip()
        if x is None or x == "":
            return None
        return int(x)

    def workspace_selection_changed(self):
        workspace_selection = self._get_main_presenter().get_selected_workspaces()
        if len(workspace_selection) != 1:
            self._slice_view.populate_slice_x_options([])
            self._slice_view.populate_slice_y_options([])
            return
        workspace_selection = workspace_selection[0]
        axis = self._slice_plotter.get_available_axis(workspace_selection)
        self._slice_view.populate_slice_x_options(axis)
        self._slice_view.populate_slice_y_options(axis[::-1])
