import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

import gui.widgets.notification_server as ns
from gui.models.roles import Roles
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.models.proxy.text_files import TextFilesProxyModel
from gui.widgets.common.setup import BaseSetup
from gui.widgets.common.file_path_select import FilePathSelect
from gui.widgets.morphology_syntax.dialog import MorphSyntaxDialog


class MorphSyntaxSetup(BaseSetup):
    def __init__(self, parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__('Морфология и Синтаксис', 'Анализ', parent, f)

        # [other]

        texts_model = TextFilesModel()
        nltk_file = FilePath()
        udpipe_file = FilePath()

        texts_proxy_model = TextFilesProxyModel()
        texts_proxy_model.setSourceModel(texts_model)

        # [widgets]

        text_lbl = qw.QLabel('Текст для анализа:')
        text_cbx = qw.QComboBox()
        text_cbx.setModel(texts_proxy_model)

        nltk_fps = FilePathSelect()
        nltk_fps.file = nltk_file
        nltk_fps.label.setText('NLTK-модель подкорпуса:')
        nltk_fps.dialog.setNameFilters(['NLTK-модель подкорпуса (*.tab)', 'Все файлы (*.*)'])

        rus_chb = qw.QCheckBox('Части речи и теги на русском')

        # [layout]

        vbox = qw.QVBoxLayout()
        vbox.addWidget(text_lbl)
        vbox.addWidget(text_cbx)
        vbox.addWidget(nltk_fps)
        vbox.addWidget(rus_chb)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # [fields]

        self._texts_model = texts_model
        self._texts_proxy_model = texts_proxy_model
        self._nltk_file = nltk_file
        self._udpipe_file = udpipe_file

        self._nltk_fps = nltk_fps
        self._text_cbx = text_cbx
        self._rus_chb = rus_chb

    @property
    def texts_model(self) -> TextFilesModel:
        return self._texts_model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._texts_model = value
        self._texts_proxy_model.setSourceModel(value)

    @property
    def udpipe_file(self) -> FilePath:
        return self._udpipe_file

    @udpipe_file.setter
    def udpipe_file(self, value: FilePath):
        self._udpipe_file = value

    def nltk_file(self) -> FilePath:
        return self._nltk_file

    def set_nltk_file(self, value: FilePath, as_default: bool):
        self._nltk_file = value
        self._nltk_fps.file = value
        if as_default:
            self._nltk_fps.default_path = value.path

    def analysis(self):
        try:
            text_file: pl.Path = self._text_cbx.currentData(Roles.SourceDataRole)
            if not text_file or not text_file.exists():
                raise ValueError('Текст недоступен')

            nltk_path = self._nltk_file.path
            if not nltk_path.exists():
                raise ValueError('Файл NLTK-модели недоступен')

            udpipe_path = self._udpipe_file.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')

        except ValueError as v:
            ns.global_server.notify(v.args[0])

        else:
            ns.global_server.clear()

            dialog = MorphSyntaxDialog(nltk_path, udpipe_path, text_file, self._rus_chb.isChecked())
            dialog.exec_()
