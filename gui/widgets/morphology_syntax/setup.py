import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui import config
from gui.models.roles import Roles
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.models.proxy.text_files import TextFilesProxyModel
from gui.widgets import style
from gui.widgets.common.file_path_select import FilePathSelect
from gui.widgets.common.note_button import NoteButton
from gui.widgets.common.hseparator import HSeparator


class MorphSyntaxSetup(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        texts_model = TextFilesModel()
        nltk_file = FilePath()

        texts_proxy_model = TextFilesProxyModel()
        texts_proxy_model.setSourceModel(texts_model)

        # widgets

        text_lbl = qw.QLabel('Текст для анализа:')
        text_cbx = qw.QComboBox()
        text_cbx.setModel(texts_proxy_model)

        nltk_fps = FilePathSelect()
        nltk_fps.file = nltk_file
        nltk_fps.label.setText('NLTK-модель подкорпуса:')
        nltk_fps.dialog.setNameFilters(['NLTK-модель подкорпуса (*.tab)', 'Все файлы (*.*)'])

        separator_hs = HSeparator()
        analysis_btn = qw.QPushButton(style.icons.play_circle, 'Анализ')
        note_btn = NoteButton()

        # connect

        analysis_btn.clicked.connect(self._on_analysis_click)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(note_btn, 1)
        hbox.addWidget(analysis_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(text_lbl)
        vbox.addWidget(text_cbx)
        vbox.addWidget(nltk_fps)
        vbox.addWidget(separator_hs)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # fields

        self._texts_model = texts_model
        self._texts_proxy_model = texts_proxy_model
        self._nltk_file = nltk_file

        self._nltk_fps = nltk_fps
        self._text_cbx = text_cbx

        self._note_btn = note_btn

    @property
    def texts_model(self) -> TextFilesModel:
        return self._texts_model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._texts_model = value
        self._texts_proxy_model.setSourceModel(value)

    def nltk_file(self) -> FilePath:
        return self._nltk_file

    def set_nltk_file(self, value: FilePath, as_default: bool):
        self._nltk_file = value
        self._nltk_fps.file = value
        if as_default:
            self._nltk_fps.default_path = value.path

    def _on_analysis_click(self):
        try:
            text_file: pl.Path = self._text_cbx.currentData(Roles.SourceDataRole)
            if not text_file or not text_file.exists():
                raise ValueError('Текст недоступен')

            nltk_path = self._nltk_file.path
            if not nltk_path.exists():
                raise ValueError('Файл NLTK-модели недоступен')
        except ValueError as v:
            self._note_btn.show_warn(v.args[0])
            return

        self._note_btn.hide()

        # TODO temp void
        print(f'TEXT: {text_file}')
        print(f'NLTK: {nltk_path}')
