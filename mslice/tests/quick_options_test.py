from mock import MagicMock, PropertyMock, Mock, patch
import unittest


from matplotlib import text
from matplotlib.lines import Line2D
from matplotlib.container import ErrorbarContainer
from mslice.plotting.plot_window.slice_plot import SlicePlot
from mslice.plotting.plot_window.cut_plot import CutPlot
from mslice.presenters.quick_options_presenter import quick_options, quick_axis_options
from mslice.plotting.plot_window.quick_options import QuickAxisOptions, QuickLabelOptions, QuickLineOptions


def setup_line_values(qlo_mock):
    quick_line_options = MagicMock()
    qlo_mock.return_value = quick_line_options
    type(quick_line_options).marker = PropertyMock(return_value='.')
    type(quick_line_options).color = PropertyMock(return_value='blue')
    type(quick_line_options).style = PropertyMock(return_value='--')
    type(quick_line_options).width = PropertyMock(return_value='5')
    type(quick_line_options).label = PropertyMock(return_value='label2')
    type(quick_line_options).shown = PropertyMock(return_value=True)
    target = Line2D([], [], 3, '-', 'red', 'o', label='label1')
    return qlo_mock, target


class QuickOptionsTest(unittest.TestCase):

    def setUp(self):
        self.model = MagicMock()

    @patch.object(QuickLabelOptions, '__init__', lambda x, y: None)
    @patch.object(QuickLabelOptions, 'exec_', lambda x: None)
    @patch('mslice.presenters.quick_options_presenter.quick_label_options')
    def test_label(self, label_options_mock):
        target = Mock(spec=text.Text)
        quick_options(target, self.model)
        label_options_mock.assert_called_once_with(target)

    @patch.object(QuickLineOptions, '__init__', lambda x, y: None)
    @patch.object(QuickLineOptions, 'exec_', lambda x: None)
    @patch('mslice.presenters.quick_options_presenter.quick_line_options')
    def test_line(self, line_options_mock):
        target = Line2D([], [], 3, '-', 'red', 'o', label='label1')
        quick_options(target, self.model)
        line_options_mock.assert_called_once_with(target, self.model)

    @patch.object(QuickLineOptions, '__init__', lambda x, y: None)
    @patch.object(QuickLineOptions, 'exec_', lambda x: None)
    @patch('mslice.presenters.quick_options_presenter.quick_axis_options')
    def test_axis(self, axis_options_mock):
        target = "x_axis"
        quick_options(target, self.model)
        axis_options_mock.assert_called_once_with(target, self.model, None)

    @patch('mslice.presenters.quick_options_presenter.QuickLineOptions')
    def test_line_slice(self, qlo_mock):
        plot_figure = MagicMock()
        window = MagicMock()
        plot_figure.window = window
        canvas = MagicMock()
        window.canvas = canvas
        slice_plotter = MagicMock()
        model = SlicePlot(plot_figure, slice_plotter, 'workspace')
        qlo_mock, target = setup_line_values(qlo_mock)
        quick_options(target, model)
        # check view is called with existing line parameters
        qlo_mock.assert_called_with(
            {'shown': None, 'color': '#ff0000', 'label': u'label1', 'style': '-', 'width': '3',
             'marker': 'o', 'legend': None, 'error_bar': None})
        # check model is updated with parameters from view
        self.assertDictEqual(model.get_line_options(target),
                             {'shown': None, 'color': '#0000ff', 'label': u'label2',
                              'style': '--', 'width': '5', 'marker': '.', 'legend': None,
                              'error_bar': None})

    @patch('mslice.presenters.quick_options_presenter.QuickLineOptions')
    def test_line_cut(self, qlo_mock):
        plot_figure = MagicMock()
        window = MagicMock()
        plot_figure.window = window
        canvas = MagicMock()
        window.canvas = canvas
        cut_plotter = MagicMock()
        model = CutPlot(plot_figure, cut_plotter, 'workspace')
        qlo_mock, target = setup_line_values(qlo_mock)

        container = ErrorbarContainer([target], has_yerr=True, label='label1')
        model._lines[target] = container
        container_mock = MagicMock()
        container_mock.containers = [container]
        canvas.figure.gca = MagicMock(return_value=container_mock)

        quick_options(target, model)
        # check view is called with existing line parameters
        qlo_mock.assert_called_with(
            {'shown': True, 'color': '#ff0000', 'label': u'label1', 'style': '-', 'width': '3',
             'marker': 'o', 'legend': True, 'error_bar': False})
        # check model is updated with parameters from view
        self.assertDictEqual(model.get_line_options(target),
                             {'shown': True, 'color': '#0000ff', 'label': u'label2',
                              'style': '--', 'width': '5', 'marker': '.', 'legend': True, 'error_bar': False})

    @patch.object(QuickAxisOptions, '__init__', lambda v, w, x, y, z: None)
    @patch.object(QuickAxisOptions, 'exec_', lambda x: True)
    @patch.object(QuickAxisOptions, 'range_min', PropertyMock(return_value='0'))
    @patch.object(QuickAxisOptions, 'range_max', PropertyMock(return_value='10'))
    @patch.object(QuickAxisOptions, 'grid_state', PropertyMock(return_value=True))
    def test_axis_with_grid(self):
        self.target = 'y_range'
        quick_options(self.target, self.model)
        self.assertEquals(self.model.y_grid, True)


@patch('mslice.presenters.quick_options_presenter.QuickAxisOptions')
class QuickAxisTest(unittest.TestCase):

    def setUp(self):
        self.view = MagicMock()
        self.model = MagicMock()
        self.model.canvas.draw = MagicMock()
        x_grid = PropertyMock(return_value=False)
        self.model.x_grid = x_grid

        range_min = PropertyMock(return_value=5)
        type(self.view).range_min = range_min
        range_max = PropertyMock(return_value=10)
        type(self.view).range_max = range_max
        grid_state = PropertyMock(return_value=True)
        type(self.view).grid_state = grid_state

    def test_accept(self, quick_axis_options_view):
        quick_axis_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=True)
        quick_axis_options('x_range', self.model)
        self.assertEquals(self.model.x_range, (5, 10))
        self.assertEquals(self.model.x_grid, True)

    def test_reject(self, quick_axis_options_view):
        quick_axis_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=False)
        self.view.set_range = Mock()
        quick_axis_options('x_range', self.model)
        self.view.set_range.assert_not_called()
        self.view.set_grid.assert_not_called()

    def test_colorbar(self, quick_axis_options_view):
        quick_axis_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=True)
        colorbar_log = PropertyMock()
        type(self.model).colorbar_log = colorbar_log
        self.view.log_scale.isChecked = Mock()
        quick_axis_options('colorbar_range', self.model, True)
        self.view.log_scale.isChecked.assert_called_once()
        colorbar_log.assert_called_once()


@patch('mslice.presenters.quick_options_presenter.QuickLabelOptions')
class QuickLabelTest(unittest.TestCase):

    def setUp(self):
        self.view = MagicMock()
        self.model = MagicMock()
        self.target = text.Text()
        label = PropertyMock(return_value="label")
        type(self.view).label = label
        self.target.set_text = MagicMock()

    def test_accept(self, quick_label_options_view):
        quick_label_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=True)
        quick_options(self.target, self.model)
        self.target.set_text.assert_called_once_with("label")

    def test_reject(self, quick_label_options_view):
        quick_label_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=False)
        quick_options(self.target, self.model)
        self.target.set_text.assert_not_called()


@patch('mslice.presenters.quick_options_presenter.QuickLineOptions')
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
        error_bar = PropertyMock(return_value=True)
        type(self.view).error_bar = error_bar

    def test_accept(self, quick_line_options_view):
        quick_line_options_view.return_value = self.view
        shown = PropertyMock(return_value=True)
        type(self.view).shown = shown
        legend = PropertyMock(return_value=True)
        type(self.view).legend = legend
        error_bar = PropertyMock(return_value=True)
        type(self.view).error_bar = error_bar
        self.view.exec_ = MagicMock(return_value=True)
        quick_options(self.target, self.model)

    def test_accept_legend_shown(self, quick_line_options_view):
        quick_line_options_view.return_value = self.view
        shown = PropertyMock(return_value=False)
        type(self.view).shown = shown
        legend = PropertyMock(return_value=False)
        type(self.view).legend = legend
        self.view.exec_ = MagicMock(return_value=True)
        quick_options(self.target, self.model)
        values = {'color': 1, 'style': 2, 'width': 3, 'marker': 4, 'label': 5, 'shown': False, 'legend': False,
                  'error_bar': True}
        self.model.set_line_options.assert_called_once_with(self.target, values)

    def test_reject(self, quick_line_options_view):
        quick_line_options_view.return_value = self.view
        self.view.exec_ = MagicMock(return_value=False)
        quick_options(self.target, self.model)
        self.model.set_line_options_by_index.assert_not_called()
