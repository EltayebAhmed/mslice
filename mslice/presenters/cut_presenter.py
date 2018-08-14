from __future__ import (absolute_import, division, print_function)

from mslice.models.cut.cut_cache import CutCache
from .busy import show_busy
from mslice.models.alg_workspace_ops import get_available_axes, get_axis_range
from mslice.models.axis import Axis
from mslice.models.cut.cut_functions import compute_cut, get_arrays_from_workspace, is_cuttable
from mslice.models.cut.cut_plotter import CutPlotter
from mslice.models.workspacemanager.workspace_provider import get_workspace_handle
from mslice.presenters.presenter_utility import PresenterUtility

from mslice.views.cut_view import CutView
from mslice.widgets.cut.command import Command
from .validation_decorators import require_main_presenter
import warnings


class CutPresenter(PresenterUtility):
    def __init__(self, cut_view, cut_plotter):
        self._cut_view = cut_view
        assert isinstance(cut_view, CutView)
        assert isinstance(cut_plotter, CutPlotter)
        self._main_presenter = None
        self._cut_plotter = cut_plotter
        self._acting_on = None
        self._cut_view.disable()
        self._previous_cut = None
        self._previous_axis = None
        self._minimumStep = dict()

    @require_main_presenter
    def notify(self, command):
        self._clear_displayed_error(self._cut_view)
        with show_busy(self._cut_view):
            if command == Command.Plot:
                self._cut(output_method=self._plot_cut)
            elif command == Command.PlotOver:
                self._cut(output_method=self._plot_cut, plot_over=True)
            elif command == Command.PlotFromWorkspace:
                self._plot_cut_from_workspace(plot_over=False)
            elif command == Command.PlotOverFromWorkspace:
                self._plot_cut_from_workspace(plot_over=True)
            elif command == Command.SaveToWorkspace:
                self._cut(output_method=self._save_cut_to_workspace)
            elif command == Command.AxisChanged:
                self._cut_axis_changed()


    def _cut(self, output_method, plot_over=False):
        selected_workspaces = self._main_presenter.get_selected_workspaces()
        try:
            self._parse_step()
            parsed_params = self._parse_input()
        except ValueError as e:
            self._cut_view.display_error(str(e))
            return
        for workspace in selected_workspaces:
            params = (workspace,) + parsed_params.unpack()
            self._run_cut_method(params, output_method, plot_over)
            plot_over = True # The first plot will respect which button the user pressed. The rest will over plot

    def _run_cut_method(self, params, output_method, plot_over=False):
            width = params[-1]
            params = params[:-1]
            if width is not None:
                self._plot_with_width(params, output_method, width, plot_over)
            else:
                output_method(params, plot_over)

    def _plot_with_width(self, params, output_method, width, plot_over):
        """This function handles the width parameter."""
        integration_start = params[2].start
        integration_end = params[2].end
        cut_start, cut_end = integration_start, min(integration_start + width, integration_end)
        index = 0
        while cut_start != cut_end:
            params = params[:2] + (Axis(params[2].units, cut_start, cut_end, 0.),) + params[3:]
            output_method(params, plot_over)
            index += 1
            cut_start, cut_end = cut_end, min(cut_end + width, integration_end)
            # The first plot will respect which button the user pressed. The rest will over plot
            plot_over = True

    def _plot_cut(self, params, plot_over):
        self._cut_plotter.plot_cut(*params, plot_over=plot_over)
        self._cut_plotter.set_icut(False)
        self._main_presenter.highlight_ws_tab(2)
        self._main_presenter.update_displayed_workspaces()

    def _save_cut_to_workspace(self, params, _):
        cut_params = params[:4]
        compute_cut(*cut_params)
        self._main_presenter.update_displayed_workspaces()

    def _plot_cut_from_workspace(self, plot_over):
        selected_workspaces = self._main_presenter.get_selected_workspaces()
        self._cut_plotter.set_icut(False)

        for workspace in selected_workspaces:
            x, y, e, units = get_arrays_from_workspace(workspace)
            self._cut_plotter.plot_cut_from_xye(x, y, e, units, workspace, plot_over=plot_over)
            plot_over = True  # plot over if multiple workspaces selected

    def _parse_step(self):
        step = self._cut_view.get_cut_axis_step()
        try:
            step = float(step)
        except ValueError:
            step = self._cut_view.get_minimum_step()
            if step is not None:
                self._cut_view.populate_cut_params(self._cut_view.get_cut_axis_start(),
                                                   self._cut_view.get_cut_axis_end(),
                                                   "%0.5f" % step)
                self._cut_view.display_error("Invalid cut step parameter, using default.")
                warnings.warn("Invalid cut step, using default value")

    def _parse_input(self):
        '''Gets values entered by user. Validation is performed by the CutParams object.'''
        cut_params = CutCache()
        cut_params.cut_axis = Axis(self._cut_view.get_cut_axis(), self._cut_view.get_cut_axis_start(),
                                   self._cut_view.get_cut_axis_end(), self._cut_view.get_cut_axis_step())

        cut_params.integration_axis = Axis(self._cut_view.get_integration_axis(), self._cut_view.get_integration_start(),
                                           self._cut_view.get_integration_end(), 0.)

        cut_params.intensity_start = self._cut_view.get_intensity_start()
        cut_params.intensity_end = self._cut_view.get_intensity_end()

        cut_params.norm_to_one = bool(self._cut_view.get_intensity_is_norm_to_one())
        cut_params.width = self._cut_view.get_integration_width()
        return cut_params

    def _set_minimum_step(self, workspace, axis):
        """Gets axes limits and then sets the minimumStep dictionary with those values"""
        for ax in axis:
            try:
                self._minimumStep[ax] = get_axis_range(workspace, ax)[2]
            except (KeyError, RuntimeError):
                self._minimumStep[ax] = None
        self._cut_view.set_minimum_step(self._minimumStep[axis[0]])

    def workspace_selection_changed(self):
        if self._previous_cut is not None and self._previous_axis is not None:
            if not self._cut_view.is_fields_cleared():
                previous_cut_workspace = get_workspace_handle(self._previous_cut)
                previous_cut_workspace.set_saved_cut_parameters(self._previous_axis, self._cut_view.get_input_fields())
            else:
                self._previous_cut = None
                self._previous_axis = None
        workspace_selection = self._main_presenter.get_selected_workspaces()
        if len(workspace_selection) == 0 or not all([is_cuttable(ws) for ws in workspace_selection]):
            self._cut_view.clear_input_fields()
            self._cut_view.disable()
            self._previous_cut = None
            self._previous_axis = None
        else:
            non_psd = all([not get_workspace_handle(ws).is_PSD for ws in workspace_selection])
            self._cut_view.enable_integration_axis(non_psd)
            self._populate_fields_using_workspace(workspace_selection[0])

    def _populate_fields_using_workspace(self, workspace_name, plotting=False):

        workspace = get_workspace_handle(workspace_name)
        axes = get_available_axes(workspace_name)

        chosen_axis, saved_parameters = self._get_axis_to_populate_fields(workspace, axes)

        self._cut_view.clear_input_fields()
        self._cut_view.populate_cut_axis_options(axes)
        self._cut_view.enable()
        self._cut_view.set_cut_axis(chosen_axis)
        self.update_integration_axis()
        if not plotting and saved_parameters is not None:
            self._cut_view.populate_input_fields(saved_parameters)
        self._previous_cut = workspace
        self._previous_axis = chosen_axis
        self._set_minimum_step(workspace, axes)

    def _get_axis_to_populate_fields(self, workspace, available_axes):
        # There are three choices for which axes to select:
        #   1. If the current cut is of the same type (e.g. QE), and parameters for the current
        #      axis in the new cut has not been defined by the user, use the current axis
        #   2. If the user has looked at this cut _and_ this axis before, use that
        #   3. Otherwise use the first available axis

        prev_cut_par = self._get_current_axis_parameters_if_chosen(workspace, available_axes)
        if prev_cut_par:
            chosen_axis = self._cut_view.get_cut_axis()
            saved_parameters = prev_cut_par
        else:
            this_cut_par, prev_selected_axis = workspace.get_saved_cut_parameters()
            if this_cut_par is not None:
                chosen_axis = prev_selected_axis
                saved_parameters = this_cut_par
            else:
                chosen_axis = available_axes[0]
                saved_parameters = None
        return chosen_axis, saved_parameters

    def _get_current_axis_parameters_if_chosen(self, workspace, available_axes):
        if self._previous_cut is not None:
            previous_cut_workspace = get_workspace_handle(self._previous_cut)
            prev_cut_par, _ = previous_cut_workspace.get_saved_cut_parameters(self._previous_axis)
            if available_axes == prev_cut_par['axes'] and not workspace.is_axis_saved(self._previous_axis):
                return prev_cut_par
        return False

    def update_integration_axis(self):
        workspace = get_workspace_handle(self._main_presenter.get_selected_workspaces()[0])
        axes = get_available_axes(workspace)
        if self._cut_view.get_cut_axis() == 'DeltaE':
            axes.remove('DeltaE')
            self._cut_view.populate_integration_axis_options(axes)
        else:
            self._cut_view.populate_integration_axis_options(['DeltaE'])

    def _cut_axis_changed(self):
        previous_cut_workspace = get_workspace_handle(self._previous_cut)
        if self._previous_axis is not None and not self._cut_view.is_fields_cleared():
            previous_cut_workspace.set_saved_cut_parameters(self._previous_axis, self._cut_view.get_input_fields())
        self._cut_view.clear_input_fields(keep_axes=True)
        if self._previous_cut is not None:
            self._previous_axis = self._cut_view.get_cut_axis()
            saved_parameters, _ = previous_cut_workspace.get_saved_cut_parameters(self._previous_axis)
            if saved_parameters is not None:
                self._cut_view.populate_input_fields(saved_parameters)
        min_step = self._minimumStep[self._cut_view.get_cut_axis()]
        self._cut_view.set_minimum_step(min_step)
        self.update_integration_axis()
