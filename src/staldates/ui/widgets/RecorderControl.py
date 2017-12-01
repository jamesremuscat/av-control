from staldates.ui.widgets.Screens import ScreenWithBackButton
from PySide.QtGui import QGridLayout, QIcon, QButtonGroup
from staldates.ui.widgets.Buttons import ExpandingButton
from PySide.QtCore import Qt
from avx.devices.net.hyperdeck import TransportState, TransportMode


def _make_button(caption, icon, onclick):
    b = ExpandingButton()
    b.setIcon(QIcon(icon))
    b.setText(caption)
    b.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    b.clicked.connect(onclick)
    return b


class RecorderControl(ScreenWithBackButton):
    def __init__(self, hyperdeck, state, mainWindow):
        self.hyperdeck = hyperdeck
        self.state = state
        super(RecorderControl, self).__init__("Recorder", mainWindow)
        self.state.transportChange.connect(self.updateState)
        if self.hyperdeck:
            self.updateState(state.transport)

    def makeContent(self):
        layout = QGridLayout()

        self.btnGroupSDCard = QButtonGroup()

        for i in range(2):
            btn = ExpandingButton()
            btn.setCheckable(True)
            btn.setText("SD card {}".format(i + 1))
            self.btnGroupSDCard.addButton(btn, i)
            layout.addWidget(btn, 0, i)

        self.btnSetPreview = ExpandingButton()
        self.btnSetPreview.setText("To preview")
        layout.addWidget(self.btnSetPreview, 0, 4)

        btnClearPeaks = ExpandingButton()
        btnClearPeaks.setText("Clear VU peaks")
        layout.addWidget(btnClearPeaks, 0, 5)

        self.btnGroupTransportMode = QButtonGroup()

        self.btnPlaybackMode = ExpandingButton()
        self.btnPlaybackMode.setCheckable(True)
        self.btnPlaybackMode.setChecked(True)
        self.btnPlaybackMode.setText("Playback mode")
        self.btnGroupTransportMode.addButton(self.btnPlaybackMode)
        self.btnPlaybackMode.clicked.connect(lambda: self._setRecordMode(False))
        layout.addWidget(self.btnPlaybackMode, 1, 1, 1, 2)

        self.btnRecordMode = ExpandingButton()
        self.btnRecordMode.setCheckable(True)
        self.btnRecordMode.setText("Record mode")
        self.btnGroupTransportMode.addButton(self.btnRecordMode)
        self.btnRecordMode.clicked.connect(lambda: self._setRecordMode(True))
        layout.addWidget(self.btnRecordMode, 1, 3, 1, 2)

        self.btnSkipBack = _make_button("Back", ":icons/media-skip-backward", self.hyperdeck.prev)
        layout.addWidget(self.btnSkipBack, 2, 0)

        self.btngroup = QButtonGroup()

        self.btnPlay = _make_button("Play", ":icons/media-playback-start", self.hyperdeck.play)
        self.btnPlay.setCheckable(True)
        self.btngroup.addButton(self.btnPlay)
        layout.addWidget(self.btnPlay, 2, 1)

        self.btnLoopPlay = _make_button("Loop", ":icons/media-playback-start", lambda: self.hyperdeck.play(loop=True))
        layout.addWidget(self.btnLoopPlay, 2, 2)

        self.btnSkipForward = _make_button("Forward", ":icons/media-skip-forward", self.hyperdeck.next)
        layout.addWidget(self.btnSkipForward, 2, 3)

        self.btnStop = _make_button("Stop", ":icons/media-playback-stop", self.hyperdeck.stop)
        self.btnStop.setCheckable(True)
        self.btngroup.addButton(self.btnStop)
        layout.addWidget(self.btnStop, 2, 4)

        self.btnRecord = _make_button("Record", ":icons/media-record", self.hyperdeck.record)
        self.btnRecord.setCheckable(True)
        self.btnRecord.setEnabled(False)
        self.btngroup.addButton(self.btnRecord)
        layout.addWidget(self.btnRecord, 2, 5)

        self.btnChooseClip = ExpandingButton()
        self.btnChooseClip.setText("Select clip")
        self.btnChooseClip.setEnabled(False)
        layout.addWidget(self.btnChooseClip, 3, 1, 1, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 1)

        return layout

    def updateState(self, state):
        if 'status' in state:
            self.btnRecord.setChecked(state['status'] == TransportState.RECORD)
            self.btnPlay.setChecked(state['status'] == TransportState.PLAYING)
            self.btnStop.setChecked(state['status'] != TransportState.RECORD and state['status'] != TransportState.PLAYING)
        currentSlot = state.get('slot id', 1)
        self.btnGroupSDCard.button(currentSlot - 1).setChecked(True)

    def _setRecordMode(self, isRecordMode):
        if isRecordMode:
            self.btnSkipBack.setEnabled(False)
            self.btnSkipForward.setEnabled(False)
            self.btnPlay.setEnabled(False)
            self.btnPlay.setChecked(False)
            self.btnLoopPlay.setEnabled(False)
            self.btnRecord.setEnabled(True)
            self.hyperdeck.setTransportMode(TransportMode.RECORD)
        else:
            self.btnSkipBack.setEnabled(True)
            self.btnSkipForward.setEnabled(True)
            self.btnPlay.setEnabled(True)
            self.btnLoopPlay.setEnabled(True)
            self.btnRecord.setEnabled(False)
            self.btnRecord.setChecked(False)
            self.hyperdeck.setTransportMode(TransportMode.PLAYBACK)
