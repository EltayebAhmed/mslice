import unittest
import mock
import numpy as np
from mantid.simpleapi import (AddSampleLog, CreateSampleWorkspace, CreateMDHistoWorkspace, CreateSimulationWorkspace,
                              ConvertToMD)

from mslice.cli._mslice_commands import (Load, MakeProjection, Slice, Cut, PlotCut, PlotSlice, KeepFigure, MakeCurrent,
                                         ConvertToChi, ConvertToChiMag, ConvertToCrossSection, SymmetriseSQE,
                                         ConvertToGDOS)
from mslice.plotting.plot_window.slice_plot import SlicePlot
from mslice.models.projection.powder.mantid_projection_calculator import MantidProjectionCalculator
from mslice.presenters.powder_projection_presenter import PowderProjectionPresenter
from mslice.presenters.slice_plotter_presenter import SlicePlotterPresenter
from mslice.presenters.cut_plotter_presenter import CutPlotterPresenter
from mslice.views.interfaces.powder_projection_view import PowderView
from mslice.presenters.interfaces.main_presenter import MainPresenterInterface
from mslice.workspace import wrap_workspace
from mslice.workspace.histogram_workspace import HistogramWorkspace
from mslice.workspace.pixel_workspace import PixelWorkspace
from mslice.workspace.workspace import Workspace
from mslice.models.cmap import DEFAULT_CMAP


class CommandLineTest(unittest.TestCase):

    def create_workspace(self, name):
        workspace = CreateSampleWorkspace(OutputWorkspace=name, NumBanks=1, BankPixelWidth=5, XMin=0.1,
                                          XMax=3.1, BinWidth=0.1, XUnit='DeltaE')
        AddSampleLog(Workspace=workspace, LogName='Ei', LogText='3.', LogType='Number')
        sim_scattering_data = np.arange(0, 1.5, 0.002).reshape(30, 25).transpose()
        for i in range(workspace.getNumberHistograms()):
            workspace.setY(i, sim_scattering_data[i])
        workspace = wrap_workspace(workspace, name)
        workspace.is_PSD = False
        workspace.limits['MomentumTransfer'] = [0.1, 3.1, 0.1]
        workspace.limits['|Q|'] = [0.1, 3.1, 0.1]
        workspace.limits['DeltaE'] = [-10, 15, 1]
        workspace.e_fixed = 10
        return workspace

    def create_pixel_workspace(self, name):
        sim_workspace = CreateSimulationWorkspace(Instrument='MAR', BinParams=[-10, 1, 10],
                                                  UnitX='DeltaE', OutputWorkspace=name)
        AddSampleLog(sim_workspace, LogName='Ei', LogText='3.', LogType='Number')
        sim_workspace = ConvertToMD(InputWorkspace=sim_workspace, OutputWorkspace=name, QDimensions='|Q|',
                                    dEAnalysisMode='Direct', MinValues='-10,0,0', MaxValues='10,6,500',
                                    SplitInto='50,50')
        workspace = wrap_workspace(sim_workspace, name)
        workspace.is_PSD = True
        workspace.limits['MomentumTransfer'] = [0.1, 3.1, 0.1]
        workspace.limits['|Q|'] = [0.1, 3.1, 0.1]
        workspace.limits['DeltaE'] = [-10, 15, 1]
        workspace.e_fixed = 10
        workspace.ef_defined = True
        return workspace

    def create_histo_workspace(self, name):
        signal = list(range(0, 100))
        error = np.zeros(100) + 2
        workspace = CreateMDHistoWorkspace(Dimensionality=2, Extents='0,100,0,100',
                                           SignalInput=signal, ErrorInput=error,
                                           NumberOfBins='10,10', Names='Dim1,Dim2',
                                           Units='U,U', OutputWorkspace=name)
        workspace = wrap_workspace(workspace, name)
        workspace.is_PSD = True
        return workspace

    @mock.patch('mslice.cli._mslice_commands.get_workspace_handle')
    @mock.patch('mslice.cli._mslice_commands.get_dataloader_presenter')
    @mock.patch('mslice.cli._mslice_commands.ospath.exists')
    def test_load(self, ospath_mock, get_dlp, get_workspace_mock):
        ospath_mock.exists.return_value = True
        path = 'made_up_path'
        Load(path)

        get_dlp().load_workspace.assert_called_once_with([path])
        get_workspace_mock.assert_called_with(path)

    @mock.patch('mslice.cli._mslice_commands.get_powder_presenter')
    def test_projection(self,  get_pp):
        get_pp.return_value = PowderProjectionPresenter(mock.create_autospec(PowderView), MantidProjectionCalculator())
        get_pp().register_master(mock.create_autospec(MainPresenterInterface))
        workspace = self.create_workspace('test_projection_cli')
        workspace.is_PSD = True
        result = MakeProjection(workspace, '|Q|', 'DeltaE')
        signal = result.get_signal()
        self.assertEqual(type(result), PixelWorkspace)
        self.assertAlmostEqual(signal[0][0], 0, 4)
        self.assertAlmostEqual(signal[0][11], 0.1753, 4)
        self.assertAlmostEqual(signal[0][28], 0.4248, 4)

    @mock.patch('mslice.cli._mslice_commands.get_powder_presenter')
    def test_projection_fail_non_PSD(self, get_pp):
        get_pp.return_value = PowderProjectionPresenter(mock.create_autospec(PowderView), MantidProjectionCalculator())
        workspace = self.create_workspace('test_projection_cli')
        with self.assertRaises(RuntimeError):
            MakeProjection(workspace, '|Q|', 'DeltaE')

    @mock.patch('mslice.cli._mslice_commands.get_slice_plotter_presenter')
    def test_slice_non_psd(self, get_spp):
        get_spp.return_value = SlicePlotterPresenter()
        workspace = self.create_workspace('test_slice_cli')
        result = Slice(workspace)
        signal = result.get_signal()
        self.assertEqual(type(result), Workspace)
        self.assertAlmostEqual(0.4250, signal[1][10], 4)
        self.assertAlmostEqual(0.9250, signal[4][11], 4)

    @mock.patch('mslice.cli._mslice_commands.get_slice_plotter_presenter')
    def test_slice_non_psd_axes_specified(self, get_spp):
        get_spp.return_value = SlicePlotterPresenter()
        workspace = self.create_workspace('test_slice_cli_axes')
        result = Slice(workspace, 'DeltaE,0,15,1', '|Q|,0,3,0.1')
        signal = result.get_signal()
        self.assertEqual(type(result), Workspace)
        self.assertAlmostEqual(0.4250, signal[2][0], 4)
        self.assertAlmostEqual(0.9250, signal[5][1], 4)

    @mock.patch('mslice.cli._mslice_commands.get_cut_plotter_presenter')
    def test_cut_non_psd(self, get_cpp):
        get_cpp.return_value = CutPlotterPresenter()
        workspace = self.create_workspace('test_workspace_cut_cli')
        result = Cut(workspace)
        signal = result.get_signal()
        self.assertEqual(type(result), HistogramWorkspace)
        self.assertAlmostEqual(1.1299, signal[5], 4)
        self.assertAlmostEqual(1.375, signal[8], 4)

    @mock.patch('mslice.cli._mslice_commands.get_slice_plotter_presenter')
    def test_slice_psd(self, get_spp):
        get_spp.return_value = SlicePlotterPresenter()
        workspace = self.create_pixel_workspace('test_slice_psd_cli')
        result = Slice(workspace)
        signal = result.get_signal()
        self.assertEqual(type(result), HistogramWorkspace)
        self.assertEqual(60, signal[0][9])
        self.assertEqual(110, signal[3][7])
        self.assertEqual(105, signal[5][6])

    @mock.patch('mslice.cli._mslice_commands.get_cut_plotter_presenter')
    def test_cut_psd(self, get_cpp):
        get_cpp.return_value = CutPlotterPresenter()
        workspace = self.create_pixel_workspace('test_workspace_cut_psd_cli')
        result = Cut(workspace)
        signal = result.get_signal()
        self.assertEqual(type(result), HistogramWorkspace)
        self.assertEqual(128, signal[0])
        self.assertEqual(192, signal[29])
        self.assertEqual(429, signal[15])

    @mock.patch('mslice.cli._mslice_commands.get_slice_plotter_presenter')
    def test_slice_fail_workspace_type(self, get_spp):
        get_spp.return_value = SlicePlotterPresenter()
        workspace = self.create_histo_workspace('test_slice_fail_type_cli')
        with self.assertRaises(RuntimeError):
            Slice(workspace)

    @mock.patch('mslice.cli._mslice_commands.get_cut_plotter_presenter')
    def test_cut_fail_workspace_type(self, get_cpp):
        get_cpp.return_value = CutPlotterPresenter()
        workspace = self.create_histo_workspace('test_cut_fail_type_cli')
        with self.assertRaises(RuntimeError):
            Cut(workspace)

    @mock.patch('mslice.cli._mslice_commands.PlotSliceMsliceProjection')
    def test_plot_slice(self, plot_slice):
        slice_ws = Slice(self.create_pixel_workspace('test_plot_slice_cli'))
        PlotSlice(slice_ws)
        plot_slice.assert_called_once_with(slice_ws, "", "", DEFAULT_CMAP)

    @mock.patch('mslice.cli._mslice_commands.PlotSliceMsliceProjection')
    def test_plot_slice_non_psd(self, plot_slice):
        slice_ws = Slice(self.create_workspace('test_plot_slice_non_psd_cli'))
        PlotSlice(slice_ws)
        plot_slice.assert_called_once_with(slice_ws, "", "", DEFAULT_CMAP)

    @mock.patch('mslice.cli._mslice_commands.PlotCutMsliceProjection')
    def test_plot_cut(self, plot_cut):
        cut = Cut(self.create_pixel_workspace('test_plot_cut_cli'))
        PlotCut(cut)
        plot_cut.assert_called_once_with(cut, 0, 0, False)

    @mock.patch('mslice.cli._mslice_commands.PlotCutMsliceProjection')
    def test_plot_cut_non_psd(self, plot_cut):
        workspace = self.create_workspace('test_plot_cut_non_psd_cli')
        cut = Cut(workspace)
        PlotCut(cut)
        plot_cut.assert_called_once_with(cut, 0, 0, False)

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_keep_figure_works_for_last_figure_number(self, gfm):
        gfm.set_figure_as_kept = mock.Mock()
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        PlotSlice(slice_ws)

        KeepFigure()

        gfm.set_figure_as_kept.assert_called_with(None)

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_keep_figure_works_on_figure_number(self, gfm):
        gfm.set_figure_as_kept = mock.Mock()
        workspace = self.create_workspace('test_keep_figure')
        cut_ws = Cut(workspace)
        figure_number = PlotCut(cut_ws)

        KeepFigure(figure_number)

        gfm.set_figure_as_kept.assert_called_with(figure_number)

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_make_current_works_on_last_figure_number(self, gfm):
        gfm.set_figure_as_current = mock.Mock()
        workspace = self.create_workspace('test_make_current')
        slice_ws = Slice(workspace)
        PlotSlice(slice_ws)

        MakeCurrent()

        gfm.set_figure_as_current.assert_called_with(None)

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_make_current_works_on_figure_number(self, gfm):
        gfm.set_figure_as_current = mock.Mock()
        workspace = self.create_workspace('test_make_current')
        cut_ws = Cut(workspace)
        figure_number = PlotCut(cut_ws)

        MakeCurrent(figure_number)

        gfm.set_figure_as_current.assert_called_with(figure_number)

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_convert_to_chi_is_called_correctly(self, gfm):
        figure_mock = mock.MagicMock()
        plot_handler_mock = mock.MagicMock(spec=SlicePlot)
        plot_handler_mock.plot_window = mock.MagicMock()
        figure_mock._plot_handler = plot_handler_mock
        gfm.get_figure_by_number = mock.Mock(return_value=figure_mock)
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        figure_number = PlotSlice(slice_ws)

        ConvertToChi(figure_number)

        plot_handler_mock.plot_window.action_chi_qe.trigger.assert_called_once_with()

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_convert_to_chi_mag_is_called_correctly(self, gfm):
        figure_mock = mock.MagicMock()
        plot_handler_mock = mock.MagicMock(spec=SlicePlot)
        plot_handler_mock.plot_window = mock.MagicMock()
        figure_mock._plot_handler = plot_handler_mock
        gfm.get_figure_by_number = mock.Mock(return_value=figure_mock)
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        figure_number = PlotSlice(slice_ws)

        ConvertToChiMag(figure_number)

        plot_handler_mock.plot_window.action_chi_qe_magnetic.trigger.assert_called_once_with()

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_convert_to_cross_section_is_called_correctly(self, gfm):
        figure_mock = mock.MagicMock()
        plot_handler_mock = mock.MagicMock(spec=SlicePlot)
        plot_handler_mock.plot_window = mock.MagicMock()
        figure_mock._plot_handler = plot_handler_mock
        gfm.get_figure_by_number = mock.Mock(return_value=figure_mock)
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        figure_number = PlotSlice(slice_ws)

        ConvertToCrossSection(figure_number)

        plot_handler_mock.plot_window.action_d2sig_dw_de.trigger.assert_called_once_with()

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_convert_to_symmetrise_sqe_is_called_correctly(self, gfm):
        figure_mock = mock.MagicMock()
        plot_handler_mock = mock.MagicMock(spec=SlicePlot)
        plot_handler_mock.plot_window = mock.MagicMock()
        figure_mock._plot_handler = plot_handler_mock
        gfm.get_figure_by_number = mock.Mock(return_value=figure_mock)
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        figure_number = PlotSlice(slice_ws)

        SymmetriseSQE(figure_number)

        plot_handler_mock.plot_window.action_symmetrised_sqe.trigger.assert_called_once_with()

    @mock.patch('mslice.cli._mslice_commands.GlobalFigureManager')
    def test_that_convert_to_gdos_is_called_correctly(self, gfm):
        figure_mock = mock.MagicMock()
        plot_handler_mock = mock.MagicMock(spec=SlicePlot)
        plot_handler_mock.plot_window = mock.MagicMock()
        figure_mock._plot_handler = plot_handler_mock
        gfm.get_figure_by_number = mock.Mock(return_value=figure_mock)
        workspace = self.create_workspace('test_keep_figure')
        slice_ws = Slice(workspace)
        figure_number = PlotSlice(slice_ws)

        ConvertToGDOS(figure_number)

        plot_handler_mock.plot_window.action_gdos.trigger.assert_called_once_with()
