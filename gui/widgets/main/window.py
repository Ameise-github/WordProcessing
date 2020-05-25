import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui import config
from gui.models.comparison.algorithms import ComparisonAlgorithmsModel, AlgorithmList
from gui.models.common.text_files import TextFilesModel
from gui.models.common.udpipe import UDPipeFile
from gui.widgets.main.text_files_list import TextFilesList
from gui.widgets.comparison.setup import ComparisonSetup
from gui.widgets.topics_definition.setup import TopicsDefinitionSetup
from gui.widgets.pragmatic_adequacy.setup import PragmaticAdequacySetup


class MainWindow(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models

        texts_model = TextFilesModel()
        algorithms_model = ComparisonAlgorithmsModel()
        udpipe_file = UDPipeFile(config.DEFAULT_UDPIPE_FILE)

        # dialogs

        dialog_set_udp = qw.QFileDialog(self)
        dialog_set_udp.setFileMode(qw.QFileDialog.ExistingFile)
        dialog_set_udp.setWindowTitle('Выберите файл UDPipe модели')
        dialog_set_udp.setNameFilters(
            ['UDPipe модель (*.udpipe)', 'Все файлы (*.*)']
        )

        # widgets

        udpipe_lbl = qw.QLabel('UDPipe файл:')
        udpipe_lned = qw.QLineEdit()
        udpipe_lned.setReadOnly(True)
        udpipe_lned.setPlaceholderText(config.DEFAULT_UDPIPE_FILE.name)
        udpipe_btn = qw.QPushButton('Обзор...')

        text_lbl = qw.QLabel('Файлы текстов:')
        text_man = TextFilesList()
        text_man.layout().setMargin(0)
        text_man.model = texts_model

        comparator_w = ComparisonSetup()
        comparator_w.algorithms_model = algorithms_model
        comparator_w.texts_model = texts_model
        comparator_w.udpipe_file = udpipe_file

        topics_definer_w = TopicsDefinitionSetup()
        topics_definer_w.texts_model = texts_model
        topics_definer_w.udpipe_file = udpipe_file

        pragmatic_w = PragmaticAdequacySetup()
        pragmatic_w.texts_model = texts_model
        pragmatic_w.udpipe_file = udpipe_file

        analysis_tw = qw.QTabWidget()
        analysis_tw.addTab(comparator_w, 'Сравнение')
        analysis_tw.addTab(topics_definer_w, 'Тематика')
        analysis_tw.addTab(pragmatic_w, 'Прагматическая адекватность')

        # connections

        udpipe_btn.clicked.connect(self._on_choose_udp_file)

        # layout

        udpipe_hbox = qw.QHBoxLayout()
        udpipe_hbox.addWidget(udpipe_lned, 1)
        udpipe_hbox.addWidget(udpipe_btn)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(udpipe_lbl)
        vbox.addLayout(udpipe_hbox)
        vbox.addWidget(text_lbl)
        vbox.addWidget(text_man)
        vbox.addWidget(analysis_tw)
        self.setLayout(vbox)

        # fields

        self.texts_model = texts_model
        self.algorithms_model = algorithms_model
        self.udpipe_file = udpipe_file

        self.dialog_set_udp = dialog_set_udp
        self.udp_file_lned = udpipe_lned

        # setup

        self.setWindowTitle('Анализ и сравнение текстов')
        self.setMinimumSize(500, 500)

    @property
    def algorithms(self) -> AlgorithmList:
        return self.algorithms_model.algorithms

    @algorithms.setter
    def algorithms(self, value: AlgorithmList):
        self.algorithms_model.algorithms = value

    def _on_choose_udp_file(self):
        if self.dialog_set_udp.exec_():
            file = self.dialog_set_udp.selectedFiles()[0]
            self.udp_file_lned.setText(file)
            self.udpipe_file.path = pl.Path(file)
