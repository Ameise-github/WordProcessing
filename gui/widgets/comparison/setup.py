import typing as t
import pathlib as pl
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from gui.widgets.common import NoteButton
from gui.widgets.comparison.file_manager import FileManager
from gui import settings
from gui.widgets.comparison.process import ComparisonProcess
from gui.models.comparison import ComparisonAlgorithmsModel, AlgorithmList
from gui.logic.comparison import ComparisonCombinator


class ComparisonSetup(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models

        algorithms_model = ComparisonAlgorithmsModel()

        # dialogs

        dialog_set_udp = qw.QFileDialog(self)
        dialog_set_udp.setFileMode(qw.QFileDialog.ExistingFile)
        dialog_set_udp.setWindowTitle('Выберите файл UDPipe модели')
        dialog_set_udp.setNameFilters(
            ['UDPipe модель (*.udpipe)', 'Все файлы (*.*)']
        )

        # widgets

        file_man_gbx = qw.QGroupBox('Файлы текстов')
        file_man = FileManager()

        alg_gbx = qw.QGroupBox('Алгоритмы сравнений')
        algorithms_lv = qw.QListView()
        algorithms_lv.setModel(algorithms_model)

        udp_lbl = qw.QLabel('UDPipe файл:')
        udp_file_lned = qw.QLineEdit()
        udp_file_lned.setReadOnly(True)
        udp_file_lned.setPlaceholderText(settings.DEFAULT_UDPIPE_FILE.name)
        udp_add_btn = qw.QPushButton('Обзор...')
        udp_add_btn.setIcon(qg.QIcon.fromTheme('document-open'))

        actions_gbx = qw.QGroupBox('Операции')
        act_define_topic_btn = qw.QPushButton('Определить тематику')
        act_define_topic_btn.setIcon(qg.QIcon.fromTheme('system-run'))
        act_compare_btn = qw.QPushButton('Выполнить сравнение')
        act_compare_btn.setIcon(qg.QIcon.fromTheme('system-run'))

        note_btn = NoteButton()

        # connections

        udp_add_btn.clicked.connect(self._on_choose_udp_file)
        act_compare_btn.clicked.connect(self._on_run_comparison)

        # layout

        file_man_vbox = qw.QVBoxLayout()
        file_man_vbox.addWidget(file_man)
        file_man_gbx.setLayout(file_man_vbox)

        udp_file_hbox = qw.QHBoxLayout()
        udp_file_hbox.addWidget(udp_file_lned, 1)
        udp_file_hbox.addWidget(udp_add_btn)

        alg_vbox = qw.QVBoxLayout()
        alg_vbox.addWidget(algorithms_lv)
        alg_vbox.addWidget(udp_lbl)
        alg_vbox.addLayout(udp_file_hbox)
        alg_vbox.addStretch(1)
        alg_gbx.setLayout(alg_vbox)

        actions_hbox = qw.QHBoxLayout()
        actions_hbox.addWidget(act_define_topic_btn)
        actions_hbox.addWidget(act_compare_btn)
        actions_gbx.setLayout(actions_hbox)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(file_man_gbx)
        vbox.addWidget(alg_gbx)
        vbox.addWidget(actions_gbx)
        vbox.addWidget(note_btn)
        self.setLayout(vbox)

        # fields

        self.dialog_set_udp = dialog_set_udp
        self.file_man = file_man
        self.alg_gbx = alg_gbx
        self.algorithms_lv = algorithms_lv
        self.udp_file_lned = udp_file_lned
        self.act_compare_btn = act_compare_btn
        self.note_btn = note_btn

        # setup

        self.setWindowTitle('Анализ и сравнение текстов')

    @property
    def algorithms(self) -> AlgorithmList:
        model: ComparisonAlgorithmsModel = self.algorithms_lv.model()
        return model.algorithms

    @algorithms.setter
    def algorithms(self, value: AlgorithmList):
        model: ComparisonAlgorithmsModel = self.algorithms_lv.model()
        model.algorithms = value

        # check
        empty = not bool(value)
        if empty:
            qw.QMessageBox.warning(
                self,
                'Список алгоритмов',
                'Алгоритмы сравнения текстов не заданы, сравнение невозможно')
        # setup
        self.act_compare_btn.setEnabled(not empty)
        self.alg_gbx.setEnabled(not empty)

    def _on_choose_udp_file(self):
        if self.dialog_set_udp.exec_():
            file = self.dialog_set_udp.selectedFiles()[0]
            self.udp_file_lned.setText(file)

    def _on_run_comparison(self):
        ref_file = self.file_man.model.exist_ref_file
        other_files = self.file_man.model.exist_other_files

        alg_model: ComparisonAlgorithmsModel = self.algorithms_lv.model()
        checked_algs = alg_model.checked_algorithms()

        udp_file = self.udp_file_lned.text()
        if not udp_file:
            udp_file = settings.DEFAULT_UDPIPE_FILE
        else:
            udp_file = pl.Path(udp_file)

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
