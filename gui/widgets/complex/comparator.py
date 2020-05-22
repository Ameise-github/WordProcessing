import typing as t
import pathlib as pl

import PySide2
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.logic.comparison.combinator import ComparisonCombinator
from gui.models.algorithms import ComparisonAlgorithmsModel, AlgorithmList
from gui.models.text_files import TextFilesModel
from gui.models.roles import Roles
from gui.models.udpipe import UDPipeFile
from gui.widgets import style
from gui.widgets.common.checkable_list import CheckableList
from gui.widgets.common.note_button import NoteButton
from gui.widgets.window.comparison import Comparison


class TextsShortProxyModel(qc.QIdentityProxyModel):
    def data(self, proxy_index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Any:
        text_file: str = super().data(proxy_index, Roles.SourceDataRole)

        if qq.DisplayRole == role:
            return pl.Path(text_file).name
        elif qq.CheckStateRole == role:
            return None
        else:
            return super().data(proxy_index, role)


class Comparator(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models

        algorithms_model = ComparisonAlgorithmsModel()
        texts_model = TextFilesModel()

        texts_proxy_model = TextsShortProxyModel()
        texts_proxy_model.setSourceModel(texts_model)

        # widgets

        reference_lbl = qw.QLabel('Эталонный текст:')
        reference_cbx = qw.QComboBox()
        reference_cbx.setModel(texts_proxy_model)

        algorithms_lbl = qw.QLabel('Алгоритмы:')
        algorithms_chl = CheckableList()
        algorithms_chl.model = algorithms_model

        compare_btn = qw.QPushButton(style.icons.play_circle, 'Выполнить сравнение')

        note_btn = NoteButton()

        # connect

        compare_btn.clicked.connect(self._on_run_comparison)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(note_btn, 1)
        hbox.addWidget(compare_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(reference_lbl)
        vbox.addWidget(reference_cbx)
        vbox.addWidget(algorithms_lbl)
        vbox.addWidget(algorithms_chl)
        vbox.addLayout(hbox, 1)
        self.setLayout(vbox)

        # fields

        self._algorithms_model = algorithms_model
        self._texts_model = texts_model
        self._texts_proxy_model = texts_proxy_model

        self._algorithms_chl = algorithms_chl
        self._reference_cbx = reference_cbx
        self._note_btn = note_btn

        self._udpipe_file = UDPipeFile()

        # setup

    @property
    def algorithms_model(self) -> ComparisonAlgorithmsModel:
        return self._algorithms_model

    @algorithms_model.setter
    def algorithms_model(self, value: ComparisonAlgorithmsModel):
        self._algorithms_model = value
        self._algorithms_chl.model = value

    @property
    def texts_model(self) -> TextFilesModel:
        return self._texts_model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._texts_model = value
        self._texts_proxy_model.setSourceModel(value)

    @property
    def udpipe_file(self) -> UDPipeFile:
        return self._udpipe_file

    @udpipe_file.setter
    def udpipe_file(self, value: UDPipeFile):
        self._udpipe_file = value

    def _on_run_comparison(self):
        try:
            other_files = self._texts_model.checked(exists_only=True)

            ref_file: pl.Path = self._reference_cbx.currentData(Roles.SourceDataRole)
            if not ref_file:
                raise ValueError('Эталонный текст недоступен')

            if ref_file in other_files:
                other_files.remove(ref_file)
            if not other_files:
                raise ValueError('Нечего сравнивать')

            checked_algs = self._algorithms_model.checked()
            if not checked_algs:
                raise ValueError('Не выбран алгоритм сравнения')

            udpipe_path = self.udpipe_file.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as v:
            self._note_btn.show_warn(v.args[0])
            return

        self._note_btn.hide()

        combinator = ComparisonCombinator()
        combinator.udpipe = udpipe_path
        combinator.algorithms = checked_algs
        combinator.reference = ref_file
        combinator.others = other_files

        proc_w = Comparison(combinator, self)
        proc_w.exec_()
