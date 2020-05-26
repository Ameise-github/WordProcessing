import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.common.file_path import FilePath


class FilePathSelect(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [other]

        file = FilePath()

        # [dialogs]

        file_d = qw.QFileDialog(self)
        file_d.setFileMode(qw.QFileDialog.ExistingFile)
        file_d.setWindowTitle('Выберите файл')

        # [widgets]

        label = qw.QLabel('Файл:')
        field = qw.QLineEdit()
        field.setReadOnly(True)
        button = qw.QPushButton('Обзор...')

        # [connect]

        file.path_changed.connect(self._on_path_changed)
        button.clicked.connect(self._on_button_click)

        # [layout]

        hbox = qw.QHBoxLayout()
        hbox.addWidget(field, 1)
        hbox.addWidget(button)

        vbox = qw.QVBoxLayout()
        vbox.setMargin(0)
        vbox.addWidget(label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # [fields]

        self._file = file
        self._file_dialog = file_d

        self._label = label
        self._field = field
        self._button = button

        self._default_path = pl.Path()

    @property
    def file(self) -> FilePath:
        return self._file

    @file.setter
    def file(self, value: FilePath):
        self._file.path_changed.disconnect(self._on_path_changed)
        self._on_path_changed(self._file.path, value.path)
        self._file = value
        value.path_changed.connect(self._on_path_changed)

    @property
    def label(self):
        return self._label

    @property
    def button(self):
        return self._button

    @property
    def default_path(self) -> pl.Path:
        return self._default_path

    @default_path.setter
    def default_path(self, value: pl.Path):
        self._default_path = value
        self._field.setPlaceholderText(value.name)
        self._on_path_changed(self._file.path, self._file.path)

    @property
    def dialog(self):
        return self._file_dialog

    def _on_path_changed(self, old: pl.Path, new: pl.Path):
        if new == self._default_path:
            self._field.clear()
        else:
            self._field.setText(str(new))

    def _on_button_click(self):
        if self._file_dialog.exec_():
            file = self._file_dialog.selectedFiles()[0]
            self._file.path = pl.Path(file)
