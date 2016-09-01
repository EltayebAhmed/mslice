def get_figure_class():
    """Check <something> to see where to get figure class from """

    # <somehting should be something easily configurable, e.g. >
    # The figure class should (subclass matplotlib.figure/ implement gca)
    print "Warning :: Using MSlice Figures because get_figure_class is still not implemented"
    from plotting.plot_window.plot_figure import PlotFigureManager
    return PlotFigureManager
