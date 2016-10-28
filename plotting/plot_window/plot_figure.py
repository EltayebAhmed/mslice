from base_qt_plot_window import BaseQtPlotWindow
from plotting.plot_window.plot_window_ui import Ui_MainWindow
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from PyQt4.QtCore import Qt
from plot_options import PlotOptionsDialog, LegendDescriptor, PlotConfig
from matplotlib.container import ErrorbarContainer
from itertools import chain


class PlotFigureManager(BaseQtPlotWindow, Ui_MainWindow):
    def __init__(self, number, manager):
        super(PlotFigureManager, self).__init__(number, manager)

        self.actionKeep.triggered.connect(self._report_as_kept_to_manager)
        self.actionMakeCurrent.triggered.connect(self._report_as_current_to_manager)

        self.actionDump_To_Console.triggered.connect(self._dump_script_to_console)

        self.actionDataCursor.toggled.connect(self.toggle_data_cursor)
        self.stock_toolbar = NavigationToolbar2QT(self.canvas, self)
        self.stock_toolbar.hide()

        self.actionZoom_In.triggered.connect(self.stock_toolbar.zoom)
        self.actionZoom_Out.triggered.connect(self.stock_toolbar.back)
        self.action_save_image.triggered.connect(self.stock_toolbar.save_figure)
        self.actionPlotOptions.triggered.connect(self._plot_options)
        self.actionToggleLegends.triggered.connect(self._toggle_legend)

        self.show()  # is not a good idea in non interactive mode

    def toggle_data_cursor(self):
        if self.actionDataCursor.isChecked():
            self.stock_toolbar.message.connect(self.statusbar.showMessage)
            self.canvas.setCursor(Qt.CrossCursor)
        else:
            self.stock_toolbar.message.disconnect()
            self.canvas.setCursor(Qt.ArrowCursor)

    def _display_status(self,status):
        if status == "kept":
            self.actionKeep.setChecked(True)
            self.actionMakeCurrent.setChecked(False)
        elif status == "current":
            self.actionMakeCurrent.setChecked(True)
            self.actionKeep.setChecked(False)

    def _plot_options(self):
        config = self._get_plot_description()
        new_config = PlotOptionsDialog.get_new_config(config)
        if new_config:
            self._apply_config(new_config)

    def _apply_config(self, plot_config):
        current_axis = self.canvas.figure.gca()
        current_axis.set_title(plot_config.title)
        current_axis.set_xlabel(plot_config.xlabel)
        current_axis.set_ylabel(plot_config.ylabel)

        current_axis.set_xlim(*plot_config.x_range)
        current_axis.set_ylim(*plot_config.y_range)

        legend_config = plot_config.legend
        for handle in legend_config.handles:
            handle.set_label(legend_config.get_legend_text(handle))

        # To show/hide errorbars we will just set the alpha to 0
        if plot_config.errorbar is not None:
            self._set_errorbars_shown_state(plot_config.errorbar)

        # The legend must be set after hiding/showing the error bars so the errorbars on the legend are in sync with
        # the plot (in terms of having/not having errorbars)
        if legend_config.visible:
            current_axis.legend()

        else:
            if current_axis.legend_:
                current_axis.legend_.remove()
            current_axis.legend_ = None

        self.canvas.draw()

    def _set_legend_state(self, visible=True):
        """Show legends if true, hide legends is visible is false"""
        current_axes = self.canvas.figure.gca()
        if visible:
            current_axes.legend()
        else:
            if current_axes.legend_:
                current_axes.legend_.remove()
                current_axes.legend_ = None

    def _toggle_legend(self):
        current_axes = self.canvas.figure.gca()
        if not list(current_axes._get_legend_handles()):
            return  # Legends are not appplicable to this plot
        current_state = getattr(current_axes, 'legend_') is not None
        self._set_legend_state(not current_state)
        self.canvas.draw()

    def _has_errorbars(self):
        """True current axes has visible errorbars,
         False if current axes has hidden errorbars
         None if errorbars are not applicable"""
        current_axis = self.canvas.figure.gca()
        if not any(map(lambda x: isinstance(x, ErrorbarContainer),current_axis.containers)):
            has_errorbars = None  # Error bars are not applicable to this plot and will not show up in the config
        else:
            # If all the error bars have alpha= 0 they are all transparent (hidden)
            containers = filter(lambda x: isinstance(x, ErrorbarContainer), current_axis.containers)
            line_components = map(lambda x:x.get_children(), containers)
            # drop the first element of each container because it is the the actual line
            errorbars = map(lambda x: x[1:] , line_components)
            errorbars = chain(*errorbars)
            alpha = map(lambda x: x.get_alpha(), errorbars)
            # replace None with 1(None indicates default which is 1)
            alpha = map(lambda x: x if x is not None else 1, alpha)
            if sum(alpha) == 0:
                has_errorbars = False
            else:
                has_errorbars = True
        return has_errorbars

    def _set_errorbars_shown_state(self,state):
        """Show errrorbar if state = 1, hide if state = 0"""
        current_axis = self.canvas.figure.gca()
        if state:
            alpha = 1
        else:
            alpha = 0
        for container in current_axis.containers:
            if isinstance(container, ErrorbarContainer):
                elements = container.get_children()
                for i in range(len(elements)):
                    # The first component is the actual line so we will not touch it
                    if i != 0:
                        elements[i].set_alpha(alpha)

    def _toggle_errorbars(self):
        state = self._has_errorbars()
        if state is None: # No errorbars in this plot
            return
        self._set_errorbars_shown_state(not state)

    def _get_plot_description(self):
        current_axis = self.canvas.figure.gca()
        title = current_axis.get_title()
        xlabel = current_axis.get_xlabel()
        ylabel = current_axis.get_ylabel()
        x_range = current_axis.get_xlim()
        y_range = current_axis.get_ylim()
        # if a legend has been set to '' or has been hidden (by prefixing with '_)then it will be ignored by
        # axes.get_legend_handles_labels()
        # That is the reason for the use of the private function axes._get_legend_handles
        # This code was written against the 1.5.1 version of matplotlib.
        handles = list(current_axis._get_legend_handles())
        labels = map(lambda x: x.get_label(), handles)
        labels = list(labels)
        if not handles:
            legend = LegendDescriptor(applicable=False)
        else:
            visible = getattr(current_axis, 'legend_') is not None
            legend = LegendDescriptor(visible=visible, handles=handles)
        has_errorbars  = self._has_errorbars()
        return PlotConfig(title=title, x_axis_label=xlabel, y_axis_label=ylabel, legends=legend,
                          errorbars_enabled=has_errorbars,
                          x_range=x_range,
                          y_range=y_range)