from PySide.QtGui import QFrame, QGridLayout, QLabel
from staldates.ui.widgets.Buttons import OutputButton
from PySide.QtCore import Signal, QSignalMapper, Qt
from avx.devices.net.atem.constants import VideoSource


class SuperSourceButton(OutputButton):
    def _update_from_output(self):
        super(SuperSourceButton, self)._update_from_output()
        self.setEnabled(self.output.enabled)


class SuperSourceInputsGrid(QFrame):

    setBox = Signal(int)
    setBackground = Signal()

    def __init__(self, super_source, parent=None):
        super(SuperSourceInputsGrid, self).__init__(parent)
        self._super_source = super_source

        self.boxSignalMapper = QSignalMapper(self)

        layout = QGridLayout()

        self.destination_buttons = []

        lbl = QLabel('Super Source inputs')
        lbl.setAlignment(Qt.AlignHCenter)
        layout.addWidget(lbl, 0, 0, 1, 2)

        for i in range(4):
            btn = SuperSourceButton(super_source.boxes[i])
            layout.addWidget(btn, 1 + (i / 2), i % 2)
            btn.clicked.connect(self.boxSignalMapper.map)
            self.boxSignalMapper.setMapping(btn, i)
            self.destination_buttons.append(btn)

        btnBackground = SuperSourceButton(super_source.fill)
        btnBackground.clicked.connect(self.setBackground.emit)
        btnBackground.setProperty("class", "mainMix")
        layout.addWidget(btnBackground, 3, 0, 1, 2)
        self.destination_buttons.append(btnBackground)

        self.setDestinationButtonsEnabled(False)

        self.setLayout(layout)

    def setBoxInput(self, idx):
        self.setBox.emit(idx)

    def setDestinationButtonsEnabled(self, enabled):
        for b in self.destination_buttons:
            b.setEnabled(enabled and b.output.enabled)
