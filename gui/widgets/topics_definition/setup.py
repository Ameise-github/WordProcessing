import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.common.text_files import TextFilesModel
from gui.models.common.udpipe import UDPipeFile
from gui.widgets import style
from gui.widgets.topics_definition.window import TopicsDefinitionWindow
from gui.widgets.common.note_button import NoteButton
from gui.widgets.common.hseparator import HSeparator


class TopicsDefinitionSetup(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = TextFilesModel()
        udpipe = UDPipeFile()

        # widgets

        optimal_chb = qw.QCheckBox('Согласованность тем')

        separator_hs = HSeparator()

        define_btn = qw.QPushButton(style.icons.play_circle, 'Определить тематику')
        note_btn = NoteButton()

        # connect

        define_btn.clicked.connect(self._on_define_click)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(note_btn, 1)
        hbox.addWidget(define_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(optimal_chb)
        vbox.addWidget(separator_hs)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # fields

        self._model = model
        self._udpipe = udpipe

        self._optimal_chk = optimal_chb
        self._note_btn = note_btn

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

    def _on_define_click(self):
        try:
            files = self._model.checked(exists_only=True)
            if len(files) <= 1:
                raise ValueError('Нет файлов для определения')
            udpipe_path = self._udpipe.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as v:
            self._note_btn.show_warn(v.args[0])
            return

        self._note_btn.hide()

        dialog = TopicsDefinitionWindow(files, self._udpipe, self._optimal_chk.isChecked(), self)
        dialog.exec_()
