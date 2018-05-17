from mock import MagicMock, PropertyMock, Mock, patch
import unittest

from matplotlib import text
from matplotlib.lines import Line2D
from matplotlib.container import Container

from mslice.plotting.plot_window.slice_plot import SlicePlot
from mslice.plotting.plot_window.cut_plot import CutPlot
from mslice.presenters.quick_options_presenter import (quick_options, QuickLinePresenter, QuickAxisPresenter,
                                                       QuickLabelPresenter)
from mslice.plotting.plot_window.quick_options import QuickAxisOptions, QuickLabelOptions, QuickLineOptions


def setup_line_values(qlo_mock):
    quick_line_options = MagicMock()
    qlo_mock.return_value = quick_line_options
    type(quick_line_options).marker = PropertyMock(return_value='.')
    type(quick_line_options).color = PropertyMock(return_value='blue')
    type(quick_line_options).style = PropertyMock(return_value='--')
    type(quick_line_options).width = PropertyMock(return_value='5')
    type(quick_line_options).label = PropertyMock(return_value='label2')
    target = Line2D([], [], 3, '-', 'red', 'o', label='label1')
    return qlo_mock, target


class QuickOptionsTest(unittest.TestCase):

    def setUp(self):
        self.model = MagicMock()

    @patch.object(QuickLabelOptions, '__init__', lambda x, y: None)
    @patch.object(QuickLabelOptions, 'exec_', lambda x: None)
    def test_label(self):
        self.target = Mock(spec=text.Text)
        self.presenter = quick_options(self.target, self.model)
        assert type(self.presenter) is QuickLabelPresenter

    @patch.object(QuickLineOptions, '__init__', lambda x, y: None)
    @patch.object(QuickLineOptions, 'exec_', lambda x: None)
    def test_line(self):
        self.target = 1
        self.presenter = quick_options(self.target, self.model)
        assert type(self.presenter) is QuickLinePresenter

    @patch('mslice.presenters.quick_options_presenter.QuickLineOptions')
    def test_line_slice(self, qlo_mock):
        plot_figure = MagicMock()
        canvas = MagicMock()
        slice_plotter = MagicMock()
        model = SlicePlot(plot_figure, canvas, slice_plotter, 'workspace')
        qlo_mock, target = setup_line_values(qlo_mock)

        self.presenter = quick_options(target, model)
        assert type(self.presenter) is QuickLinePresenter
        # check view is called with existing line parameters
        qlo_mock.assert_called_with(
            {'shown': None, 'color': 'red', 'label': u'label1', 'style': '-', 'width': '3',
             'marker': 'o', 'legend': None})
        # check model is updated with parameters from view
        self.assertDictEqual(model.get_line_data(target),
                             {'shown': None, 'color': 'blue', 'label': u'label2',
                              'style': '--', 'width': '5', 'marker': '.', 'legend': None})

    @patch('mslice.presenters.quick_options_presenter.QuickLineOptions')
    def test_line_cut(self, qlo_mock):
        plot_figure = MagicMock()
        canvas = MagicMock()
        cut_plotter = MagicMock()
        model = CutPlot(plot_figure, canvas, cut_plotter, 'workspace')
        qlo_mock, target = setup_line_values(qlo_mock)

        container = Container([target], label='label1')
        model._lines[target] = container
        container_mock = MagicMock()
        container_mock.containers = [container]
        canvas.figure.gca = MagicMock(return_value=container_mock)

        self.presenter = quick_options(model.get_line_index(target), model)
        assert type(self.presenter) is QuickLinePresenter
        # check view is called with existing line parameters
        qlo_mock.assert_called_with(
            {'shown': True, 'color': 'red', 'label': u'label1', 'style': '-', 'width': '3',
             'marker': 'o', 'legend': True})
        # check model is updated with parameters from view
        self.assertDictEqual(model.get_line_data(model.get_line_index(target)),
                             {'shown': True, 'color': 'blue', 'label': u'label2',
                              'style': '--', 'width': '5', 'marker': '.', 'legend': True})

    @patch.object(QuickAxisOptions, '__init__', lambda v, w, x, y, z: None)
    @patch.object(QuickAxisOptions, 'exec_', lambda x: True)
    @patch.object(QuickAxisOptions, 'range_min', PropertyMock(return_value='0'))
    @patch.object(QuickAxisOptions, 'range_max', PropertyMock(return_value='10'))
    @patch.object(QuickAxisOptions, 'grid_state', PropertyMock(return_value=True))
    def test_axis_with_grid(self):
        self.target = 'y_range'
        self.presenter = quick_options(self.target, self.model)
        assert type(self.presenter) is QuickAxisPresenter
        self.assertEquals(self.model.y_grid, True)

    @patch.object(QuickAxisOptions, '__init__', lambda v, w, x, y, z: None)
    @patch.object(QuickAxisOptions, 'exec_', lambda x: True)
    @patch.object(QuickAxisOptions, 'range_min', PropertyMock(return_value='0'))
    @patch.object(QuickAxisOptions, 'range_max', PropertyMock(return_value='10'))
    def test_axis_no_grid(self):
        self.target = 'colorbar_range'
        self.presenter = quick_options(self.target, self.model)
        assert type(self.presenter) is QuickAxisPresenter


class QuickAxisTest(unittest.TestCase):

    def setUp(self):
        self.view = MagicMock()
        self.model = MagicMock()
        self.model.canvas.draw = MagicMock()
        range_min = PropertyMock(return_value=5)
        type(self.view).range_min = range_min
        range_max = PropertyMock(return_value=10)
        type(self.view).range_max = range_max
        grid_state = PropertyMock(return_value=True)
        type(self.view).grid_state = grid_state

    def test_accept(self):
        self.view.exec_ = MagicMock(return_value=True)
        QuickAxisPresenter(self.view, 'x_range', self.model, False, None)
        self.assertEquals(self.model.x_range, (5, 10))
        self.assertEquals(self.model.x_grid, True)

    def test_reject(self):
        self.view.exec_ = MagicMock(return_value=False)
        self.view.set_range = Mock()
        QuickAxisPresenter(self.view, 'x_range', self.model, False, None)
        self.view.set_range.assert_not_called()
        self.view.set_grid.assert_not_called()

    def test_colorbar(self):
        self.view.exec_ = MagicMock(return_value=True)
        colorbar_log = PropertyMock()
        type(self.model).colorbar_log = colorbar_log
        self.view.log_scale.isChecked = Mock()
        QuickAxisPresenter(self.view, 'colorbar_range', self.model, None, True)
        self.view.log_scale.isChecked.assert_called_once()
        colorbar_log.assert_called_once()


class QuickLabelTest(unittest.TestCase):

    def setUp(self):
        self.view = MagicMock()
        self.model = MagicMock()
        self.target = MagicMock()
        label = PropertyMock(return_value="label")
        type(self.view).label = label
        self.target.set_text = MagicMock()

    def test_accept(self):
        self.view.exec_ = MagicMock(return_value=True)
        QuickLabelPresenter(self.view, self.target, self.model)
        self.target.set_text.assert_called_once_with("label")

    def test_reject(self):
        self.view.exec_ = MagicMock(return_value=False)
        QuickLabelPresenter(self.view, self.target, self.model)
        self.target.set_text.assert_not_called()


class QuickLineTest(unittest.TestCase):

    def setUp(self):
        self.view = MagicMock()
        self.model = MagicMock()
        self.target = MagicMock()
        self.model.canvas.draw = MagicMock()
        self.target.set_color = MagicMock()
        self.target.set_linestyle = MagicMock()
        self.target.set_linewidth = MagicMock()
        self.target.set_marker = MagicMock()
        self.target.set_label = MagicMock()
        color = PropertyMock(return_value=1)
        type(self.view).color = color
        style = PropertyMock(return_value=2)
        type(self.view).style = style
        width = PropertyMock(return_value=3)
        type(self.view).width = width
        marker = PropertyMock(return_value=4)
        type(self.view).marker = marker
        label = PropertyMock(return_value=5)
        type(self.view).label = label

    def test_accept(self):
        shown = PropertyMock(return_value=True)
        type(self.view).shown = shown
        legend = PropertyMock(return_value=True)
        type(self.view).legend = legend
        self.view.exec_ = MagicMock(return_value=True)
        QuickLinePresenter(self.view, self.target, self.model)

    def test_accept_legend_shown(self):
        shown = PropertyMock(return_value=False)
        type(self.view).shown = shown
        legend = PropertyMock(return_value=False)
        type(self.view).legend = legend
        self.view.exec_ = MagicMock(return_value=True)
        QuickLinePresenter(self.view, self.target, self.model)
        values = {'color': 1, 'style': 2, 'width': 3, 'marker': 4, 'label': 5, 'shown': False, 'legend': False}
        self.model.set_line_data.assert_called_once_with(self.target, values)

    def test_reject(self):
        self.view.exec_ = MagicMock(return_value=False)
        QuickLinePresenter(self.view, self.target, self.model)
        self.model.set_line_data.assert_not_called()
