from __future__ import (absolute_import, division, print_function)
import mock
from mock import call, patch
import unittest
import warnings

from six import string_types

from mslice.models.axis import Axis
from mslice.models.cut.cut_plotter import CutPlotter
from mslice.models.alg_workspace_ops import get_available_axes
from mslice.presenters.cut_presenter import CutPresenter
from mslice.presenters.interfaces.main_presenter import MainPresenterInterface
from mslice.widgets.cut.command import Command
from mslice.views.interfaces.cut_view import CutView


class CutPresenterTest(unittest.TestCase):

    def setUp(self):
        self.view = mock.create_autospec(CutView)
        self.cut_plotter = mock.create_autospec(CutPlotter)
        self.main_presenter = mock.create_autospec(MainPresenterInterface)

    def test_constructor_success(self):
        self.view.disable = mock.Mock()
        CutPresenter(self.view, self.cut_plotter)
        self.view.disable.assert_called()

    def test_register_master_success(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self.main_presenter.subscribe_to_workspace_selection_monitor.assert_called_with(cut_presenter)

    def test_workspace_selection_changed_multiple_workspaces(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self.main_presenter.get_selected_workspace = mock.Mock(return_value=['a', 'b'])
        for attribute in dir(CutView):
            if not attribute.startswith("__"):
                setattr(self.view, attribute, mock.Mock())
        cut_presenter.workspace_selection_changed()
        # make sure only the attributes in the tuple were called and nothing else
        for attribute in dir(CutView):
            if not attribute.startswith("__"):
                if attribute in ("clear_input_fields", "disable"):
                    getattr(self.view, attribute).assert_called()
                else:
                    getattr(self.view, attribute).assert_not_called()

    def test_notify_presenter_clears_error(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self.view.clear_displayed_error = mock.Mock()
        # This unit test will verify that notifying cut presenter will cause the error to be cleared on the view.
        # The actual subsequent procedure will fail, however this irrelevant to this. Hence the try, except blocks
        for command in [x for x in dir(Command) if x[0] != "_"]:
            cut_presenter.notify(command)
            self.view.clear_displayed_error.assert_called()
            self.view.reset_mock()

    @patch('mslice.presenters.cut_presenter.is_cuttable')
    @patch('mslice.presenters.cut_presenter.get_workspace_handle')
    @patch('mslice.models.alg_workspace_ops.get_workspace_handle')
    def test_workspace_selection_changed_single_cuttable_workspace(self, get_ws_handle_mock2, get_ws_handle_mock,
                                                                   is_cuttable_mock):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        workspace = 'workspace'
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[workspace])
        is_cuttable_mock.return_value=True

        ws_mock = mock.Mock()
        ws_mock.is_PSD = False
        ws_mock.limits = {}
        ws_mock.get_saved_cut_parameters = mock.Mock(return_value=(None, None))

        get_ws_handle_mock.return_value = ws_mock
        get_ws_handle_mock2.return_value = ws_mock
        available_dimensions = get_available_axes(workspace)
        cut_presenter.workspace_selection_changed()
        self.view.populate_cut_axis_options.assert_called_with(available_dimensions)
        self.view.enable.assert_called_with()
        # Change workspace again, to check if cut parameters properly saved
        new_workspace = 'new_workspace'
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[new_workspace])
        fields = dict()
        fields['axes'] = available_dimensions
        self.view.get_input_fields = mock.Mock(return_value=fields)
        self.view.is_fields_cleared = mock.Mock(return_value=False)
        ws_mock.get_saved_cut_parameters.return_value=(fields, available_dimensions[0])
        ws_mock.is_axis_saved = mock.Mock(return_value=False)
        self.view.get_cut_axis = mock.Mock(return_value=available_dimensions[0])
        cut_presenter.workspace_selection_changed()
        ws_mock.set_saved_cut_parameters.assert_called_with(available_dimensions[0], fields)
        self.view.get_cut_axis.assert_called_with()
        # Change back to check that it repopulates the fields
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[workspace])
        cut_presenter.workspace_selection_changed()
        self.view.populate_input_fields.assert_called_with(fields)
        ws_mock.set_saved_cut_parameters.assert_called_with(available_dimensions[0], fields)

    @patch('mslice.presenters.cut_presenter.is_cuttable')
    def test_workspace_selection_changed_single_noncut_workspace(self, is_cuttable_mock):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        workspace = 'workspace'
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[workspace])
        is_cuttable_mock.return_value = False
        cut_presenter.workspace_selection_changed()
        self.view.clear_input_fields.assert_called_with()
        self.view.disable.assert_called_with()

    def _create_cut(self, *args):
        axis, processed_axis = tuple(args[0:2])
        integration_start, integration_end, width = tuple(args[2:5])
        intensity_start, intensity_end, is_norm = tuple(args[5:8])
        workspace, integrated_axis = tuple(args[8:10])
        if isinstance(workspace, string_types):
            workspace = [workspace]
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=workspace)
        self.view.get_cut_axis = mock.Mock(return_value=axis.units)
        self.view.get_cut_axis_start = mock.Mock(return_value=axis.start)
        self.view.get_cut_axis_end = mock.Mock(return_value=axis.end)
        self.view.get_cut_axis.step = mock.Mock(return_value=axis.step)
        self.view.get_integration_axis = mock.Mock(return_value=integrated_axis)
        self.view.get_integration_start = mock.Mock(return_value=integration_start)
        self.view.get_integration_end = mock.Mock(return_value=integration_end)
        self.view.get_intensity_start = mock.Mock(return_value=intensity_start)
        self.view.get_intensity_end = mock.Mock(return_value=intensity_end)
        self.view.get_intensity_is_norm_to_one = mock.Mock(return_value=is_norm)
        self.view.get_integration_width = mock.Mock(return_value=width)

    def test_cut_parse_input_errors(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        # Invalid workspace
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        # Defines good values
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0, 100, 1)
        integration_start = 3
        integration_end = 8
        width = "2"
        intensity_start = 11
        intensity_end = 30
        is_norm = True
        workspace = "workspace"
        integrated_axis = 'integrated axis'
        # Wrong units
        axis = Axis("", "0", "100", "1")
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        # Bad cut axis
        with self.assertRaises(ValueError):
            Axis("units", "a", "100", "1")
        axis = Axis("units", "0", "100", "1")
        # Bad integration
        integration_start = "a"
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        # Invalid integration range
        integration_start = 30
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        integration_start = 3
        # Bad intensity
        intensity_start = "a"
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        # Invalid intensity range
        intensity_start = 100
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)
        intensity_start = 11
        # Wrong width
        width = "a"
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.Plot)
        self.assertRaises(ValueError)

    def test_plot_single_cut_success(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0, 100, 1)
        integration_start = 3
        integration_end = 5
        width = ""
        intensity_start = 11
        intensity_end = 30
        is_norm = True
        workspace = "workspace"
        integrated_axis = 'integrated axis'
        integration_axis = Axis('integrated axis', integration_start, integration_end, 0)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)

        cut_presenter.notify(Command.Plot)
        self.cut_plotter.plot_cut.assert_called_with(workspace, processed_axis, integration_axis,
                                                     is_norm, intensity_start, intensity_end, plot_over=False)

    def test_plot_over_cut_fail(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0, 100, 1)
        integration_start = 3
        integration_end = 5
        width = ""
        intensity_start = ""
        intensity_end = 30
        is_norm = True
        workspace = "workspace"
        integrated_axis = 'integrated axis'
        integration_axis = Axis('integrated axis', integration_start, integration_end, 0)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        cut_presenter.notify(Command.PlotOver)
        self.cut_plotter.plot_cut.assert_called_with(workspace, processed_axis, integration_axis,
                                                     is_norm, None, intensity_end, plot_over=True)

    @patch('mslice.presenters.cut_presenter.compute_cut')
    @patch('mslice.models.cut.cut_functions.get_workspace_handle')
    def test_cut_single_save_to_workspace(self, get_workspace_handle_mock, compute_cut_mock):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0, 100, 1)
        integration_start = 3
        integration_end = 5
        width = ""
        intensity_start = 11
        intensity_end = 30
        is_norm = True
        workspace = "workspace"
        ws_mock = mock.Mock()
        get_workspace_handle_mock.return_value = ws_mock
        integrated_axis = 'integrated axis'
        integration_axis = Axis('integrated axis', integration_start, integration_end, 0)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        self.cut_plotter.plot_cut = mock.Mock()
        cut_presenter.notify(Command.SaveToWorkspace)
        compute_cut_mock.assert_called_with(workspace, processed_axis, integration_axis, is_norm)
        self.cut_plotter.plot_cut.assert_not_called()

    def test_plot_multiple_cuts_with_width(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0.0, 100.0, 1.0)
        integration_start = 3.0
        integration_end = 8.0
        width = "2"
        intensity_start = 11.0
        intensity_end = 30.0
        is_norm = True
        workspace = "workspace"
        integrated_axis = 'integrated axis'
        integration_axis1 = Axis('integrated axis', 3.0, 5.0, 0)
        integration_axis2 = Axis('integrated axis', 5.0, 7.0, 0)
        integration_axis3 = Axis('integrated axis', 7.0, 8.0, 0)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)

        cut_presenter.notify(Command.Plot)
        call_list = [
            call(workspace, processed_axis, integration_axis1, is_norm,
                 intensity_start, intensity_end, plot_over=False),
            call(workspace, processed_axis, integration_axis2,
                 is_norm, intensity_start, intensity_end, plot_over=True),
            call(workspace, processed_axis, integration_axis3,
                 is_norm, intensity_start, intensity_end, plot_over=True)
        ]
        self.cut_plotter.plot_cut.assert_has_calls(call_list)

    def test_plot_multiple_workspaces_cut(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", "1")
        processed_axis = Axis("units", 0, 100, 1)
        integration_start = 3
        integration_end = 8
        width = ""
        intensity_start = 11
        intensity_end = 30
        is_norm = True
        selected_workspaces = ["ws1", "ws2"]
        integrated_axis = 'integrated axis'
        integration_axis = Axis('integrated axis', integration_start, integration_end, 0)
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, selected_workspaces, integrated_axis)
        cut_presenter.notify(Command.Plot)
        call_list = [
            call(selected_workspaces[0], processed_axis, integration_axis, is_norm,
                 intensity_start, intensity_end, plot_over=False),
            call(selected_workspaces[1], processed_axis, integration_axis, is_norm,
                 intensity_start, intensity_end, plot_over=True),
        ]
        self.cut_plotter.plot_cut.assert_has_calls(call_list)

    @patch('mslice.presenters.cut_presenter.is_cuttable')
    @patch('mslice.presenters.cut_presenter.get_workspace_handle')
    @patch('mslice.models.alg_workspace_ops.get_workspace_handle')
    def test_change_axis(self, get_ws_handle_mock, get_ws_handle_mock2, is_cuttable_mock):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        # Set up a mock workspace with two sets of cutable axes, then change to this ws
        workspace = 'workspace'
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[workspace])
        is_cuttable_mock.return_value = True
        ws_mock = mock.Mock()
        ws_mock.is_PSD = False
        ws_mock.limits = {}
        ws_mock.get_saved_cut_parameters = mock.Mock(return_value=(None, None))
        get_ws_handle_mock.return_value = ws_mock
        get_ws_handle_mock2.return_value = ws_mock
        cut_presenter.workspace_selection_changed()
        # Set up a set of input values for this cut, then simulate changing axes.
        fields1 = dict()
        fields1['axes'] = '|Q|'
        fields1['cut_parameters'] = ['0', '10', '0.05']
        fields1['integration_range'] = ['-1', '1']
        fields1['integration_width'] = '2'
        fields1['smoothing'] = ''
        fields1['normtounity'] = False
        self.view.get_input_fields = mock.Mock(return_value=fields1)
        self.view.get_cut_axis = mock.Mock(return_value='DeltaE')
        self.view.is_fields_cleared = mock.Mock(return_value=False)
        self.view.populate_input_fields = mock.Mock()
        cut_presenter.notify(Command.AxisChanged)
        ws_mock.set_saved_cut_parameters.assert_called_with('|Q|', fields1)
        self.view.clear_input_fields.assert_called_with(keep_axes=True)
        self.view.populate_input_fields.assert_not_called()
        # Set up a set of input values for this other cut, then simulate changing axes again.
        fields2 = dict()
        fields2['axes'] = 'DeltaE'
        fields2['cut_parameters'] = ['-5', '5', '0.1']
        fields2['integration_range'] = ['2', '3']
        fields2['integration_width'] = '1'
        fields2['smoothing'] = ''
        fields2['normtounity'] = True
        self.view.get_input_fields = mock.Mock(return_value=fields2)
        self.view.get_cut_axis = mock.Mock(return_value='|Q|')
        ws_mock.get_saved_cut_parameters = mock.Mock(return_value=(fields1, '|Q|'))
        cut_presenter.notify(Command.AxisChanged)
        ws_mock.set_saved_cut_parameters.assert_called_with('DeltaE', fields2)
        ws_mock.get_saved_cut_parameters.assert_called_with('|Q|')
        self.view.populate_input_fields.assert_called_with(fields1)

    @patch('mslice.presenters.cut_presenter.is_cuttable')
    @patch('mslice.presenters.cut_presenter.get_axis_range')
    @patch('mslice.presenters.cut_presenter.get_workspace_handle')
    @patch('mslice.models.alg_workspace_ops.get_workspace_handle')
    def test_cut_step_size(self, get_ws_handle_mock, get_ws_handle_mock2, get_axis_range_mock, is_cuttable_mock):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        workspace = 'workspace'
        self.main_presenter.get_selected_workspaces = mock.Mock(return_value=[workspace])
        is_cuttable_mock.return_value = True
        ws_mock = mock.Mock()
        ws_mock.is_PSD = False
        ws_mock.limits = {}
        ws_mock.get_saved_cut_parameters = mock.Mock(return_value=(None, None))
        get_ws_handle_mock.return_value = ws_mock
        get_ws_handle_mock2.return_value = ws_mock
        cut_presenter.workspace_selection_changed()
        get_axis_range_mock.assert_any_call(ws_mock, '|Q|')
        get_axis_range_mock.assert_any_call(ws_mock, 'DeltaE')
        get_axis_range_mock.side_effect = KeyError
        cut_presenter.workspace_selection_changed()
        self.view.set_minimum_step.assert_called_with(None)

    def test_invalid_step(self):
        cut_presenter = CutPresenter(self.view, self.cut_plotter)
        cut_presenter.register_master(self.main_presenter)
        axis = Axis("units", "0", "100", 0)
        processed_axis = Axis("units", 0, 100, 0)
        integration_start = 3
        integration_end = 5
        width = ""
        intensity_start = 11
        intensity_end = 30
        is_norm = True
        workspace = "workspace"
        integrated_axis = 'integrated axis'
        self._create_cut(axis, processed_axis, integration_start, integration_end, width,
                         intensity_start, intensity_end, is_norm, workspace, integrated_axis)
        self.view.get_cut_axis_step = mock.Mock(return_value="")
        self.view.get_minimum_step = mock.Mock(return_value=1)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cut_presenter.notify(Command.Plot)
        self.view.get_minimum_step.assert_called_with()
        self.view.display_error.assert_any_call('Invalid cut step parameter, using default.')
        self.view.populate_cut_params.assert_called_with(0.0, 100.0, '1.00000')
