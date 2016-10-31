from avx.Sequencer import ControllerEvent, DeviceEvent, LogEvent, SleepEvent
from PySide.QtCore import Qt
from PySide.QtGui import QHBoxLayout
from staldates.ui.widgets.Buttons import SvgButton
from staldates.ui.widgets.Screens import ScreenWithBackButton

import logging


class SystemPowerWidget(ScreenWithBackButton):

    def __init__(self, controller, mainWindow):
        self.controller = controller
        ScreenWithBackButton.__init__(self, "System Power", mainWindow)

    def makeContent(self):

        buttons = QHBoxLayout()

        self.btnOff = SvgButton(":icons/lightbulb_off", 128, 128)
        self.btnOff.setText("Off")
        self.btnOff.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnOff.clicked.connect(self.powerOff)
        buttons.addWidget(self.btnOff)

        self.btnOn = SvgButton(":icons/lightbulb_on", 128, 128)
        self.btnOn.setText("On")
        self.btnOn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnOn.clicked.connect(self.powerOn)
        buttons.addWidget(self.btnOn)

        return buttons

    def powerOn(self):
        self.controller.sequence(
            ControllerEvent("showPowerOnDialogOnClients"),
            LogEvent(logging.INFO, "Turning system power on"),
            DeviceEvent("Power", "on", 1),
            SleepEvent(3),
            DeviceEvent("Power", "on", 2),
            SleepEvent(3),
            DeviceEvent("Power", "on", 3),
            SleepEvent(3),
            DeviceEvent("Power", "on", 4),
            ControllerEvent("initialise"),  # By this time all things we care about to initialise will have been switched on
            ControllerEvent("hidePowerDialogOnClients"),
            LogEvent(logging.INFO, "Power on sequence complete")
        )

    def powerOff(self):
        self.controller.sequence(
            ControllerEvent("showPowerOffDialogOnClients"),
            LogEvent(logging.INFO, "Turning system power off"),
            DeviceEvent("Power", "off", 4),
            SleepEvent(3),
            DeviceEvent("Power", "off", 3),
            SleepEvent(3),
            DeviceEvent("Power", "off", 2),
            SleepEvent(3),
            DeviceEvent("Power", "off", 1),
            ControllerEvent("hidePowerDialogOnClients"),
            LogEvent(logging.INFO, "Power off sequence complete")
        )
