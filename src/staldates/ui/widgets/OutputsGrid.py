from PySide.QtGui import QFrame, QGridLayout, QLabel
from staldates.ui.widgets.Buttons import OutputButton, ExpandingButton
from PySide.QtCore import Signal, QSignalMapper, Qt
from avx.devices.net.atem.constants import VideoSource


class OutputsGrid(QFrame):

    mainToAll = Signal()
    all = Signal()
    selected = Signal(int)
    sendMain = Signal(int)

    def __init__(self, switcherState, me=1, parent=None):
        super(OutputsGrid, self).__init__(parent)
        me_name = 'ME_{}_PROGRAM'.format(me)
        self.me = getattr(VideoSource, me_name)

        self.signalMapper = QSignalMapper(self)
        self.longPressSignalMapper = QSignalMapper(self)

        layout = QGridLayout()

        self.aux_buttons = []

        for idx, output in switcherState.outputs.iteritems():
            ob = OutputButton(output, self.me)
            layout.addWidget(ob, idx / 2, idx % 2)
            ob.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(ob, idx)

            ob.longpress.connect(self.longPressSignalMapper.map)
            self.longPressSignalMapper.setMapping(ob, idx)
            self.aux_buttons.append(ob)

        self.signalMapper.mapped.connect(self.registerClick)
        self.longPressSignalMapper.mapped.connect(self.longPress)

        btnAll = ExpandingButton()
        btnAll.setProperty("class", "mainMix")
        btnAll.setText("Mix to all")
        btnAll.clicked.connect(self.mainToAll.emit)
        layout.addWidget(btnAll, 3, 0)

        self.btnAll = ExpandingButton()
        self.btnAll.setText("All")
        self.btnAll.clicked.connect(self.all.emit)
        layout.addWidget(self.btnAll, 3, 1)

        layout.setColumnMinimumWidth(0, 100)
        layout.setColumnMinimumWidth(1, 100)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        for i in range(4):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

    def registerClick(self, idx):
        self.selected.emit(idx)

    def longPress(self, idx):
        self.sendMain.emit(idx)

    def setAuxesEnabled(self, enabled):
        for button in self.aux_buttons:
            button.setEnabled(enabled)
        self.btnAll.setEnabled(enabled)
