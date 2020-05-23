import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.common.text_files import TextFilesModel
from gui.models.common.udpipe import UDPipeFile
from gui.widgets import style
from gui.widgets.topics_definition.window import TopicsDefinitionWindow
from gui.widgets.common.note_button import NoteButton
from gui.widgets.common.hseparator import HSeparator


class PragmaticAdequacySetup(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = TextFilesModel()
        udpipe = UDPipeFile()

        # widgets

        reverse_chb = qw.QCheckBox('Обратное сравнение')
        interlace_chb = qw.QCheckBox('Чересстрочное сравнение')

        separator_hs = HSeparator()

        run_btn = qw.QPushButton(style.icons.play_circle, 'Расчитать прагматическую адекватность')

        # layout

        vbox = qw.QVBoxLayout()
        vbox.addWidget(reverse_chb)
        vbox.addWidget(interlace_chb)
        vbox.addWidget(separator_hs)
        vbox.addWidget(run_btn, 0, qq.AlignRight)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # fields

        self._model = model
        self._udpipe = udpipe

    @property
    def texts_model(self) -> TextFilesModel:
        return self._model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._model = value

    @property
    def udpipe_file(self) -> UDPipeFile:
        return self._udpipe

    @udpipe_file.setter
    def udpipe_file(self, value: UDPipeFile):
        self._udpipe = value
