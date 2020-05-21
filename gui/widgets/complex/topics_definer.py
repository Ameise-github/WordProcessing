import typing as t

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.roles import Roles
from gui.models.text_files import TextFilesModel
from gui.models.udpipe import UDPipeFile
from gui.widgets import style
from gui.widgets.window.topics_definition import TopicsDefinition
from gui.widgets.common.note_button import NoteButton


class TopicDefiner(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = TextFilesModel()
        udpipe = UDPipeFile()

        # widgets

        optimal_chk = qw.QCheckBox('Согласованность тем')
        define_btn = qw.QPushButton('Выполнить')
        note_btn = NoteButton()

        # connect

        define_btn.clicked.connect(self._on_define_click)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(optimal_chk)
        hbox.addStretch(1)
        hbox.addWidget(define_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(note_btn)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # fields

        self._model = model
        self._udpipe = udpipe

        self._optimal_chk = optimal_chk
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
            files = self._model.files(exists_only=True)
            if not files:
                raise ValueError('Нет файлов для определения')
            udpipe_path = self._udpipe.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as v:
            self._note_btn.show_warn(v.args[0])
            return

        self._note_btn.hide()

        dialog = TopicsDefinition(files, self._udpipe, self._optimal_chk.isChecked())
        dialog.setWindowModality(qq.WindowModality.WindowModal)
        dialog.exec_()
