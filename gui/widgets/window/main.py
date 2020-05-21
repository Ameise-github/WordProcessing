import typing as t
import pathlib as pl

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui import config
from gui.logic.comparison.combinator import ComparisonCombinator
from gui.models.algorithms import ComparisonAlgorithmsModel, AlgorithmList
from gui.models.text_files import TextFilesModel
from gui.models.udpipe import UDPipeFile
from gui.widgets.complex.text_list import TextList
from gui.widgets.complex.comparator import Comparator
from gui.widgets.complex.topics_definer import TopicDefiner
from gui.widgets.window.comparison import ComparisonProcess


class Main(qw.QWidget):
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

        files_gbx = qw.QGroupBox('Файлы')

        text_lbl = qw.QLabel('Тексты:')
        text_man = TextList()
        text_man.layout().setMargin(0)
        text_man.model = texts_model

        udpipe_lbl = qw.QLabel('UDPipe файл:')
        udpipe_lned = qw.QLineEdit()
        udpipe_lned.setReadOnly(True)
        udpipe_lned.setPlaceholderText(config.DEFAULT_UDPIPE_FILE.name)
        udpipe_btn = qw.QPushButton('Обзор...')

        comparator_w = Comparator()
        comparator_w.algorithms_model = algorithms_model
        comparator_w.texts_model = texts_model
        comparator_w.udpipe_file = udpipe_file

        topics_definer_w = TopicDefiner()
        topics_definer_w.model = texts_model

        tabs_tw = qw.QTabWidget()
        tabs_tw.addTab(comparator_w, 'Сравнение')
        tabs_tw.addTab(topics_definer_w, 'Определение тематики')

        # connections

        udpipe_btn.clicked.connect(self._on_choose_udp_file)

        # layout

        udpipe_hbox = qw.QHBoxLayout()
        udpipe_hbox.addWidget(udpipe_lned, 1)
        udpipe_hbox.addWidget(udpipe_btn)

        files_vbox = qw.QVBoxLayout()
        files_vbox.addWidget(udpipe_lbl)
        files_vbox.addLayout(udpipe_hbox)
        files_vbox.addWidget(text_lbl)
        files_vbox.addWidget(text_man)
        files_gbx.setLayout(files_vbox)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(files_gbx, 1)
        vbox.addWidget(tabs_tw)
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
