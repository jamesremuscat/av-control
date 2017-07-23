from PySide.QtGui import QFrame, QGridLayout
from staldates.ui.widgets.Buttons import OutputButton, ExpandingButton
from PySide.QtCore import Signal, QSignalMapper


class OutputsGrid(QFrame):

    take = Signal()
    mainToAll = Signal()
    all = Signal()
    selected = Signal(int)

    def __init__(self, switcherState, parent=None):
        super(OutputsGrid, self).__init__(parent)

        self.signalMapper = QSignalMapper(self)

        layout = QGridLayout()

        btnMain = ExpandingButton()
        btnMain.setText("Church / Main")
        btnMain.clicked.connect(self.take.emit)
        layout.addWidget(btnMain, 0, 0, 1, 2)

        for idx, output in switcherState.outputs.iteritems():
            ob = OutputButton(output)
            layout.addWidget(ob, 1 + (idx / 2), idx % 2)
            ob.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(ob, idx)

        self.signalMapper.mapped.connect(self.registerClick)

        btnMainToAll = ExpandingButton()
        btnMainToAll.setText("Main to\nall auxes")
        btnMainToAll.clicked.connect(self.mainToAll.emit)
        layout.addWidget(btnMainToAll, 4, 0)

        btnAll = ExpandingButton()
        btnAll.setText("All")
        btnAll.clicked.connect(self.all.emit)
        layout.addWidget(btnAll, 4, 1)

        layout.setColumnMinimumWidth(0, 100)
        layout.setColumnMinimumWidth(1, 100)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    def registerClick(self, idx):
        self.selected.emit(idx)
