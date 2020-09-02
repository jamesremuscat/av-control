from PySide.QtGui import QFrame, QGridLayout, QLabel, QSizePolicy
from staldates.ui.widgets.Buttons import ExpandingButton, OutputButton
from PySide.QtCore import Signal, QSignalMapper, Qt
from avx.devices.net.atem.constants import VideoSource


class SuperSourceButton(OutputButton):
    def _update_from_output(self):
        super(SuperSourceButton, self)._update_from_output()
        self.setEnabled(self.output.enabled)


class SuperSourceInputsGrid(QFrame):

    setBox = Signal(int)
    setBackground = Signal()
    sendToPreview = Signal()

    def __init__(self, super_source, parent=None):
        super(SuperSourceInputsGrid, self).__init__(parent)
        self._super_source = super_source

        self.boxSignalMapper = QSignalMapper(self)

        layout = QGridLayout()

        self.destination_buttons = []

        lbl = QLabel('Super Source inputs')
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(lbl, 0, 0, 1, 1)

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

        btnPreview = ExpandingButton()
        btnPreview.setText('Preview SS')
        btnPreview.clicked.connect(self.sendToPreview.emit)
        btnPreview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(btnPreview, 0, 1, alignment=Qt.AlignTop)

        self.setDestinationButtonsEnabled(False)

        self.setLayout(layout)

    def setBoxInput(self, idx):
        self.setBox.emit(idx)

    def setDestinationButtonsEnabled(self, enabled):
        for b in self.destination_buttons:
            b.setEnabled(enabled and b.output.enabled)
