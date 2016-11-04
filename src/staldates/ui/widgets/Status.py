from PySide.QtGui import QWidget, QVBoxLayout, QPixmap, QMessageBox, QPushButton
from Pyro4.errors import PyroError
from enum import Enum
from PySide.QtCore import QSize, QTimer


class Status(Enum):
    OK = ("Status OK", QMessageBox.Information, ":icons/status-ok")
    BAD = ("Controller not reachable", QMessageBox.Critical, ":icons/network-offline")
    UNKNOWN = ("Status unknown", QMessageBox.Question, ":icons/status-unknown")

    def __init__(self, message, boxIcon, icon):
        self.message = message
        self.boxIcon = boxIcon
        self.icon = icon


class SystemStatus(QWidget):
    def __init__(self, controller, parent=None):
        super(SystemStatus, self).__init__(parent)
        self.controller = controller
        self.status = Status.UNKNOWN

        layout = QVBoxLayout()

        self.icon = QPushButton(self)
        self.icon.setFlat(True)
        self.icon.setIcon(QPixmap(":icons/status-unknown"))
        self.icon.setIconSize(QSize(32, 32))
        layout.addWidget(self.icon)

        self.icon.clicked.connect(self.showStatusPopup)

        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.checkStatus)
        timer.start(10000)  # Ten seconds
        self.checkStatus()

    def checkStatus(self):
        # NB We deliberately don't use handlePyroErrors here'
        try:
            v = self.controller.getVersion()
            self.status = Status.OK
            self.status.message = "Status OK, controller version {}".format(v)
        except PyroError as e:
            self.status = Status.BAD
            self.status.message = str(e)
        self.icon.setIcon(QPixmap(self.status.icon))

    def showStatusPopup(self):
        msgBox = QMessageBox(
            self.status.boxIcon,
            "System status",
            '<span style="color: white;">' + self.status.message + '</span>'
        )
        msgBox.exec_()
