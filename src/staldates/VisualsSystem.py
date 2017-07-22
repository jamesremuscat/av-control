from avx.devices.net.atem import VideoSource, MessageTypes
from PySide.QtCore import QObject, Signal
from PySide.QtGui import QIcon


class Input(QObject):

    changedState = Signal()

    def __init__(self, source, label, icon=None):
        super(Input, self).__init__()
        self.source = source
        self.label = label
        self.icon = icon
        self.isLive = False
        self.isPreview = False

    def set_label(self, new_label):
        if new_label != self.label:
            self.label = new_label
            self.changedState.emit()

    def set_live(self, isLive):
        if isLive != self.isLive:
            self.isLive = isLive
            self.changedState.emit()

    def set_preview(self, isPreview):
        if isPreview != self.isPreview:
            self.isPreview = isPreview
            self.changedState.emit()


def _default_inputs():
    return {source: Input(source, name, icon) for (source, name, icon) in [
        (VideoSource.INPUT_1, "Camera 1", QIcon(":icons/camera-video")),
        (VideoSource.INPUT_2, "Camera 2", QIcon(":icons/camera-video")),
        (VideoSource.INPUT_3, "Camera 3", QIcon(":icons/camera-video")),
        (VideoSource.INPUT_4, "DVD", QIcon(":icons/media-optical")),
        (VideoSource.INPUT_5, "Visuals PC", QIcon(":icons/computer")),
        (VideoSource.INPUT_6, "PC Video", QIcon(":icons/video-display")),
        (VideoSource.BLACK, "Black", None)
    ]}


class SwitcherState(QObject):
    def __init__(self, atem):
        self.inputs = _default_inputs()

        if atem:
            self.updateInputs(atem.getInputs())
            self.updateTally(atem.getTally())

    def updateInputs(self, inputs):
        for source, props in inputs.iteritems():
            if source in self.inputs:
                self.inputs[source].set_label(props['name_long'])
            else:
                self.inputs[source] = Input(source, props['name_long'], None)

    def updateTally(self, tallyMap):
        for source, tally in tallyMap.iteritems():
            if source in self.inputs:
                self.inputs[source].set_preview(tally['prv'])
                self.inputs[source].set_live(tally['pgm'])

    def handleMessage(self, msgType, data):
        if msgType == MessageTypes.TALLY:
            self.updateTally(data)
