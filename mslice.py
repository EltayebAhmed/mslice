from PyQt4.QtGui import QMainWindow,QApplication

from mainview import MainView
from mslice_ui import Ui_MainWindow
from presenters.main_presenter import MainPresenter


class MsliceGui(QMainWindow,Ui_MainWindow,MainView):

    def __init__(self):
        super(MsliceGui,self).__init__()
        self.setupUi(self)

        workspace_presenter = self.wgtWorkspacemanager.get_presenter()
        slice_presenter = self.wgtSlice.get_presenter()
        powder_presenter = self.wgtPowder.get_presenter()
        self._presenter = MainPresenter(self, workspace_presenter, slice_presenter, powder_presenter)

        self.wgtSlice.error_occurred.connect(self.show_error)

    def show_error(self, error):
        self.statusbar.showMessage(error, 2000)

    def get_presenter(self):
        return self._presenter

if __name__ == "__main__":
    qapp = QApplication([])
    mslice = MsliceGui()
    mslice.show()
    qapp.exec_()