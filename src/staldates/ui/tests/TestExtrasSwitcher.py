'''
Created on 20 Feb 2015

@author: jrem
'''
import unittest
from avx.devices.Device import Device
from mock import MagicMock
from staldates.ui.ExtrasSwitcher import ExtrasSwitcher
from staldates.ui.tests.GuiTest import GuiTest
from staldates.ui.tests.TestUtils import MockController


class Test(GuiTest):

    def setUp(self):
        GuiTest.setUp(self)
        self.mockController = MockController()

        self.main = Device("Main")
        self.mockController.addDevice(self.main)
        self.main.sendInputToOutput = MagicMock(return_value=1)

        self.extras = Device("Extras")
        self.mockController.addDevice(self.extras)
        self.extras.sendInputToOutput = MagicMock(return_value=1)

        self.es = ExtrasSwitcher(self.mockController)

    def testDoesntSwitchMinusOne(self):
        self.es.takePreview()
        self.assertFalse(self.extras.sendInputToOutput.called, "Switcher was called but it shouldn't have been")
        self.es.inputs.buttons()[0].click()
        self.es.takePreview()
        self.assert_(self.extras.sendInputToOutput.called, "Switcher was not called but it should have been")

if __name__ == "__main__":
    unittest.main()
