import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

import gui.widgets.notification_server as ns
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.widgets.common.setup import BaseSetup
from gui.widgets.common.hseparator import HSeparator
from gui.widgets.topics_definition.window import TopicsDefinitionWindow


class TopicsDefinitionSetup(BaseSetup):
    def __init__(self, parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__('Тематика', 'Определить тематику', parent, f)

        # [other]

        model = TextFilesModel()
        udpipe = FilePath()

        # [widgets]

        optimal_chb = qw.QCheckBox('Согласованность тем')

        # [layout]

        vbox = qw.QVBoxLayout()
        vbox.addWidget(optimal_chb)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # [fields]

        self._model = model
        self._udpipe = udpipe

        self._optimal_chk = optimal_chb

    @property
    def texts_model(self) -> TextFilesModel:
        return self._model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._model = value

    @property
    def udpipe_file(self) -> FilePath:
        return self._udpipe

    @udpipe_file.setter
    def udpipe_file(self, value: FilePath):
        self._udpipe = value

    def analysis(self):
        try:
            files = self._model.checked(exists_only=True)
            if len(files) <= 1:
                raise ValueError('Нет файлов для определения')
            udpipe_path = self._udpipe.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')

        except ValueError as v:
            ns.global_server.notify(v.args[0])

        else:
            ns.global_server.clear()

            dialog = TopicsDefinitionWindow(files, self._udpipe, self._optimal_chk.isChecked(), self)
            dialog.exec_()
