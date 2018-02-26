from __future__ import (absolute_import, division,
                        print_function)

import inspect
import threading
import types
import warnings

from mslice.util.qt import QtWidgets

# Ignore Jupyter/IPython deprecation warnings that we can't do anything about
warnings.filterwarnings('ignore', category=DeprecationWarning, module='IPython.*')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='ipykernel.*')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='jupyter_client.*')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='qtconsole.*')
del warnings

try:
    # Later versions of Qtconsole are part of Jupyter
    from qtconsole.rich_jupyter_widget import RichJupyterWidget as RichIPythonWidget
    from qtconsole.inprocess import QtInProcessKernelManager
except ImportError:
    from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
    from IPython.qt.inprocess import QtInProcessKernelManager

def our_run_code(self, code_obj, result=None):
    """ Method with which we replace the run_code method of IPython's InteractiveShell class.
        It calls the original method (renamed to ipython_run_code) on a separate thread
        so that we can avoid locking up the whole of MantidPlot while a command runs.

        Parameters
        ----------
        code_obj : code object
          A compiled code object, to be executed
        result : ExecutionResult, optional
          An object to store exceptions that occur during execution.
        Returns
        -------
        False : Always, as it doesn't seem to matter.
    """

    t = threading.Thread()
    #ipython 3.0 introduces a third argument named result
    nargs = len(inspect.getargspec(self.ipython_run_code).args)
    if (nargs == 3):
        t = threading.Thread(target=self.ipython_run_code, args=[code_obj,result])
    else:
        t = threading.Thread(target=self.ipython_run_code, args=[code_obj])
    t.start()
    while t.is_alive():
        QtWidgets.QApplication.processEvents()
    # We don't capture the return value of the ipython_run_code method but as far as I can tell
    #   it doesn't make any difference what's returned
    return 0


class IPythonWidget(RichIPythonWidget):
    """ Extends IPython's qt widget to include setting up and in-process kernel,
     plus our trick to avoid blocking the event loop while processing commands.
    """

    def __init__(self, *args, **kw):
        super(IPythonWidget, self).__init__(*args, **kw)

        # Create an in-process kernel
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel = kernel_manager.kernel
        kernel.gui = 'qt'
        shell = kernel.shell

        # These 3 lines replace the run_code method of IPython's InteractiveShell class (of which the
        # shell variable is a derived instance) with our method defined above. The original method
        # is renamed so that we can call it from within the our_run_code method.
        f = shell.run_code
        shell.run_code = types.MethodType(our_run_code, shell)
        shell.ipython_run_code = f

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client