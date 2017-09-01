import unittest
import numpy as np
from mantid.simpleapi import CreateWorkspace, CreateMDHistoWorkspace, CreateSimulationWorkspace, ConvertToMD, AddSampleLog

from mslice.workspace.workspace import Workspace
from mslice.workspace.pixel_workspace import PixelWorkspace
from mslice.workspace.histogram_workspace import HistogramWorkspace


class BaseWorkspaceTest(unittest.TestCase):

    def check_signal(self):
        expected_values = np.arange(0, 100)
        result = np.array(self.workspace.get_signal().flatten())
        result.sort()
        self.assertTrue((result == expected_values).all())

    def check_error(self):
        expected = np.zeros(100) + 2
        self.assertTrue((expected == self.workspace.get_error().flatten()).all())

    def check_variance(self):
        expected = np.zeros(100) + 4
        self.assertTrue((expected == self.workspace.get_variance().flatten()).all())

    def check_add_workspace(self):
        two_workspace = self.workspace + self.workspace
        expected_values = np.linspace(0, 198, 100)
        result = np.array(two_workspace.get_signal().flatten())
        result.sort()
        self.assertTrue((result == expected_values).all())

    def check_mul_workspace(self):
        two_workspace = self.workspace * 2
        expected_values = np.linspace(0, 198, 100)
        result = np.array(two_workspace.get_signal().flatten())
        result.sort()
        self.assertTrue((result == expected_values).all())


class WorkspaceTest(BaseWorkspaceTest):

    @classmethod
    def setUpClass(self):
        x = np.linspace(0, 99, 100)
        y = x * 1
        e = y * 0 + 2
        self.workspace = Workspace(CreateWorkspace(x, y, e, OutputWorkspace="testBaseWorkspace"))

    def test_get_coordinates(self):
        expected_values = np.linspace(0, 99, 100)
        self.assertTrue((expected_values == self.workspace.get_coordinates()['']).all())

    def test_get_signal(self):
        expected_values = range(0, 100)
        result = np.array(self.workspace.get_signal().flatten())
        self.assertTrue((result == expected_values).all())

    def test_get_error(self):
        self.check_error()

    def test_get_variance(self):
        self.check_variance()

    def test_add_workspace(self):
        self.check_add_workspace()

    def test_mul_workspace_number(self):
        self.check_mul_workspace()

class HistogramWorkspaceTest(BaseWorkspaceTest):

    @classmethod
    def setUpClass(self):
        signal = range(0, 100)
        error = np.zeros(100) + 2
        self.workspace = HistogramWorkspace(CreateMDHistoWorkspace(Dimensionality=2, Extents='0,100,0,100',
                                                                   SignalInput=signal, ErrorInput=error,
                                                                   NumberOfBins='10,10', Names='Dim1,Dim2',
                                                                   Units='U,U', OutputWorkspace='testHistoWorkspace'))

    def test_get_coordinates(self):
        expected = np.linspace(0, 100, 10)
        self.assertTrue((self.workspace.get_coordinates()['Dim1'] == expected).all())

    def test_get_signal(self):
        self.check_signal()

    def test_get_error(self):
        self.check_error()

    def test_get_variance(self):
        self.check_variance()

    def test_add_workspace(self):
        self.check_add_workspace()

    def test_mul_workspace_number(self):
        self.check_mul_workspace()
        
class PixelWorkspaceTest(BaseWorkspaceTest):

    @classmethod
    def setUpClass(self): #create non-zero test data
        sim_workspace = CreateSimulationWorkspace(Instrument='MAR', BinParams=[-10, 1, 10], UnitX='DeltaE', OutputWorkspace='simws')
        AddSampleLog(sim_workspace, LogName='Ei', LogText='3.', LogType='Number')
        self.workspace = ConvertToMD(InputWorkspace=sim_workspace, OutputWorkspace="Convertspace", QDimensions='|Q|', dEAnalysisMode='Direct',
                                     MinValues='-10,0,0', MaxValues='10,6,500', SplitInto='50,50')
        self.workspace = PixelWorkspace(self.workspace)


    def test_get_coordinates(self):
        np.set_printoptions(threshold=np.nan)
        coords = self.workspace.get_coordinates()
        self.assertEqual(set(coords), {'|Q|', 'DeltaE'})
        self.assertEqual(coords['|Q|'][2], 0.20996594809147776)

    def test_get_signal(self):
        signal = self.workspace.get_signal()
        self.assertEqual(0, signal[0][0])
        self.assertEqual(12, signal[1][47])
        self.assertEqual(32, signal[3][52])

    def test_get_error(self):
        expected = np.zeros((100, 100))
        self.assertTrue((self.workspace.get_error() == expected).all())

    def test_get_variance(self):
        expected = np.zeros((100, 100))
        self.assertTrue((self.workspace.get_variance() == expected).all())

    def test_add_workspace(self):
        np.set_printoptions(threshold=np.nan)
        two_workspace = self.workspace + self.workspace
        signal = two_workspace.get_signal()
        self.assertEqual(0, signal[0][0])
        self.assertEqual(24, signal[1][47])
        self.assertEqual(64, signal[3][52])

    def test_mul_workspace_number(self):
        np.set_printoptions(threshold=np.nan)
        three_workspace = self.workspace * 3
        signal = three_workspace.get_signal()
        self.assertEqual(0, signal[0][0])
        self.assertEqual(36, signal[1][47])
        self.assertEqual(96, signal[3][52])