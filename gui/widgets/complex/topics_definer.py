import typing as t

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.roles import Roles
from gui.models.text_files import TextFilesModel
from gui.widgets import style


class TopicDefiner(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = TextFilesModel()

        # widgets

        optimal_chk = qw.QCheckBox('Согласованность тем')

        define_btn = qw.QPushButton('Выполнить')

        # connect

        define_btn.clicked.connect(self._on_define_click)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(optimal_chk)
        hbox.addStretch(1)
        hbox.addWidget(define_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # fields

        self._model = model

    @property
    def model(self) -> TextFilesModel:
        return self._model

    @model.setter
    def model(self, value: TextFilesModel):
        self._model = value

    def _on_define_click(self):
        pass