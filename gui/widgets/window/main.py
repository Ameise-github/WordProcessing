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
from gui.widgets.common.note_button import NoteButton
from gui.widgets.common.hseparator import HSeparator
from gui.widgets.complex.text_manager import TextManager
from gui.widgets.complex.comparison_manager import ComparisonManager
from gui.widgets.window.process import ComparisonProcess


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
        text_man = TextManager()
        text_man.model = texts_model

        udpipe_lbl = qw.QLabel('UDPipe файл:')
        udpipe_lned = qw.QLineEdit()
        udpipe_lned.setReadOnly(True)
        udpipe_lned.setPlaceholderText(config.DEFAULT_UDPIPE_FILE.name)
        udpipe_btn = qw.QPushButton('Обзор...')

        alg_gbx = qw.QGroupBox('Сравнение')
        comparison_cm = ComparisonManager()
        comparison_cm.algorithms_model = algorithms_model
        comparison_cm.texts_model = texts_model
        comparison_cm.udpipe_file = udpipe_file

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

        alg_vbox = qw.QVBoxLayout()
        alg_vbox.addWidget(comparison_cm)
        alg_gbx.setLayout(alg_vbox)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(files_gbx)
        vbox.addWidget(alg_gbx)
        self.setLayout(vbox)

        # fields

        self.texts_model = texts_model
        self.algorithms_model = algorithms_model
        self.udpipe_file = udpipe_file

        self.dialog_set_udp = dialog_set_udp
        self.file_man = text_man
        self.alg_gbx = alg_gbx
        self.comparison_cm = comparison_cm
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

    def _on_run_comparison(self):
        ref_file = self.file_man.model.exist_ref_file
        other_files = self.file_man.model.exist_other_files

        alg_model: ComparisonAlgorithmsModel = self.algorithms_lv.model()
        checked_algs = alg_model.checked_algorithms()

        udp_file = self.udpipe_file.path

        try:
            if not ref_file:
                if len(other_files) <= 1:
                    raise ValueError('Доступно менее двух текстов')
                raise ValueError('Эталонный текст недоступен')
            if not checked_algs:
                raise ValueError('Не выбран алгоритм сравнения')
            if not udp_file.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as v:
            self.note_btn.show_warn(v.args[0])
            return

        self.note_btn.hide()

        combinator = ComparisonCombinator()
        combinator.udpipe = udp_file
        combinator.algorithms = checked_algs
        combinator.reference = ref_file
        combinator.others = other_files

        proc_w = ComparisonProcess(combinator, self)
        proc_w.exec_()
