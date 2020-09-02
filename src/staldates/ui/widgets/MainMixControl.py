from PySide.QtCore import Signal, Qt
from PySide.QtGui import QFrame, QGridLayout, QLabel
from staldates.ui.widgets.Buttons import ExpandingButton


class MainMixControl(QFrame):
    cut = Signal()
    take = Signal()

    def __init__(self, parent=None):
        super(MainMixControl, self).__init__(parent)
        layout = QGridLayout()

        label = QLabel('Main mix', None)
        label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(label, 0, 0, 1, 2)

        btnTake = ExpandingButton()
        btnTake.setProperty("class", "mainMix")
        btnTake.setText("Cut")
        btnTake.clicked.connect(self.cut.emit)
        layout.addWidget(btnTake, 1, 0)

        btnFade = ExpandingButton()
        btnFade.setProperty("class", "mainMix")
        btnFade.setText("Fade")
        btnFade.clicked.connect(self.take.emit)
        layout.addWidget(btnFade, 1, 1)

        self.setLayout(layout)
