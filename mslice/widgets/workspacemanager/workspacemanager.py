from __future__ import (absolute_import, division, print_function)

from mantid.api import IMDEventWorkspace, IMDHistoWorkspace, Workspace

from mslice.util.qt.QtCore import Signal
from mslice.util.qt.QtWidgets import QWidget, QListWidgetItem, QFileDialog, QInputDialog, QMessageBox

from mslice.models.workspacemanager.mantid_workspace_provider import MantidWorkspaceProvider
from mslice.presenters.workspace_manager_presenter import WorkspaceManagerPresenter
from mslice.util.qt import load_ui
from mslice.views.workspace_view import WorkspaceView
from .command import Command

TAB_2D = 0
TAB_EVENT = 1
TAB_HISTO = 2

class WorkspaceManagerWidget(WorkspaceView, QWidget):
    """A Widget that allows user to perform basic workspace save/load/rename/delete operations on workspaces"""

    error_occurred = Signal('QString')
    tab_changed = Signal(int)
    busy = Signal(bool)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        load_ui(__file__, 'workspacemanager.ui', self)
        self.button_mappings = {}
        self._main_window = None
        self.onscreen_workspaces = []
        self.tab_to_list = {TAB_2D: self.listWorkspaces2D,
                            TAB_EVENT: self.listWorkspacesEvent,
                            TAB_HISTO: self.listWorkspacesHisto}
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.listWorkspaces2D.itemSelectionChanged.connect(self.list_item_changed)
        self.listWorkspacesEvent.itemSelectionChanged.connect(self.list_item_changed)
        self.listWorkspacesHisto.itemSelectionChanged.connect(self.list_item_changed)
        self._presenter = WorkspaceManagerPresenter(self, MantidWorkspaceProvider())

    def _display_error(self, error_string):
        self.error_occurred.emit(error_string)

    def current_list(self):
        return self.tab_to_list[self.tabWidget.currentIndex()]

    def change_tab(self, tab):
        self.tabWidget.setCurrentIndex(tab)

    def _btn_clicked(self):
        sender = self.sender()
        try:
            command = self.button_mappings[sender]
        except KeyError:
            raise Exception('Invalid sender')
        self._presenter.notify(command)

    def add_workspace(self, workspace):
        item = QListWidgetItem(workspace)
        self.onscreen_workspaces.append(workspace)
        workspace = self._presenter.get_workspace_provider().get_workspace_handle(workspace)
        if isinstance(workspace, IMDEventWorkspace):
            self.listWorkspacesEvent.addItem(item)
        elif isinstance(workspace, IMDHistoWorkspace):
            self.listWorkspacesHisto.addItem(item)
        elif isinstance(workspace, Workspace):
            self.listWorkspaces2D.addItem(item)
        else:
            raise TypeError("Loaded file is not a valid workspace")

    def display_loaded_workspaces(self, workspaces):
        for workspace in workspaces:
            if workspace not in self.onscreen_workspaces:
                self.add_workspace(workspace)
        for workspace in self.onscreen_workspaces:
            if workspace not in workspaces:
                self.remove_workspace(workspace)

    def remove_workspace(self, workspace):
        """Remove workspace from list.

        Must be done in seperate function because items are removed by index and removing an items may alter the indexes
        of other items"""
        self.onscreen_workspaces.remove(workspace)
        for ws_list in [self.listWorkspaces2D, self.listWorkspacesEvent, self.listWorkspacesHisto]:
            for index in range(ws_list.count()):
                if ws_list.item(index).text() == workspace:
                    ws_list.takeItem(index)
                    return

    def get_workspace_selected(self):
        selected_workspaces = [str(x.text()) for x in self.current_list().selectedItems()]
        return selected_workspaces

    def set_workspace_selected(self, index):
        current_list = self.current_list()
        for item_index in range(current_list.count()):
            self.listWorkspaces2D.setItemSelected(current_list.item(item_index), False)
        for this_index in (index if hasattr(index, "__iter__") else [index]):
            self.listWorkspaces2D.setItemSelected(current_list.item(this_index), True)

    def get_workspace_index(self, ws_name):
        current_list = self.current_list()
        for index in range(current_list.count()):
            if str(current_list.item(index).text()) == ws_name:
                return index
        return -1

    def get_workspace_to_load_path(self):
        paths = QFileDialog.getOpenFileNames()
        return [str(filename) for filename in paths]

    def get_directory_to_save_workspaces(self):
        return QFileDialog.getExistingDirectory()

    def get_workspace_new_name(self):
        name, success = QInputDialog.getText(self,"Workspace New Name","Enter the new name for the workspace :      ")
        # The message above was padded with spaces to allow the whole title to show up
        if not success:
            raise ValueError('No Valid Name supplied')
        return str(name)

    def error_select_only_one_workspace(self):
        self._display_error('Please select only one workspace and then try again')

    def error_select_one_or_more_workspaces(self):
        self._display_error('Please select one or more workspaces the try again')

    def error_select_one_workspace(self):
        self._display_error('Please select a workspace then try again')

    def error_select_more_than_one_workspaces(self):
        self._display_error('Please select more than one projected workspaces then try again')

    def error_invalid_save_path(self):
        self._display_error('No files were saved')

    def get_presenter(self):
        return self._presenter

    def list_item_changed(self):
        self._presenter.notify(Command.SelectionChanged)

    def error_unable_to_save(self):
        self._display_error("Something went wrong while trying to save")

    def clear_displayed_error(self):
        self._display_error("")
