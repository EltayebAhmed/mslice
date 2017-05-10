"""Package defining top-level MSlice application
and entry points.
"""
from IPython import start_ipython
from PyQt4.QtGui import QApplication

# Module-level reference to keep main window alive after show_gui has returned
MAIN_WINDOW = None
QAPP_REF = None
MPL_COMPAT = False

def check_mpl():
    from distutils.version import LooseVersion
    import matplotlib
    if LooseVersion(matplotlib.__version__) < LooseVersion("1.5.0"):
        import warnings
        warnings.warn('A version of Matplotlib older than 1.5.0 has been detected.')
        warnings.warn('Some features of MSlice may not work correctly.')
        global MPL_COMPAT
        MPL_COMPAT = True

def main():
    """Start the application. Detects the current environment and
    runs accordingly:
      - if an existing QApplication is detected then this is used and IPython
      - is not started, otherwise  a application is created.
      - if an existing IPython shell is detected this instance is used
        and matplotlib support is enabled otherwise a new one is created
    """
    check_mpl()
    global QAPP_REF
    if QApplication.instance():
        # We must be embedded in some other application that has already started the event loop
        # just show the UI...
        show_gui()
        return

    # We're doing our own startup. Are we already running IPython?
    try:
        ip = get_ipython()
        ip_running = True
    except NameError:
        ip_running = False

    if ip_running:
        # IPython handles the Qt event loop exec so we can return control to the ipython terminal
        ip.enable_matplotlib('qt4') # selects the backend
        # Older IPython versions would start this automatically but the newer ones do not
        if QApplication.instance() is None:
            QAPP_REF = QApplication([])
        show_gui()
    else:
        QAPP_REF = QApplication([])
        start_ipython(["--matplotlib=qt4", "-i",
                       "-c from mslice.app import show_gui; show_gui()"])
        # IPython will call EventLoop.exec when required

def show_gui():
    """Display the top-level main window.
    If this is the first call then an instance of the Windows is cached to ensure it
    survives for the duration of the application
    """
    global MAIN_WINDOW
    if MAIN_WINDOW is None:
        from mslice.app.mainwindow import MainWindow
        MAIN_WINDOW = MainWindow()
    MAIN_WINDOW.show()
