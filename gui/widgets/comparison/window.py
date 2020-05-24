import sys
import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.combinator import ComparisonCombinator
from gui.logic.comparison.thread import ComparisionThread
from gui.models.comparison.process import ComparisonProcessModel
from gui.widgets.common.process_dialog import BaseProcessDialog


class ComparisonWindow(BaseProcessDialog):
    def __init__(self, combinator: ComparisonCombinator,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = ComparisonProcessModel(combinator)
        thread = ComparisionThread(model, self)

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel(str(combinator.reference))

        result_tv = qw.QTableView()
        result_tv.setModel(model)
        result_tv.setSelectionMode(result_tv.SelectionMode.SingleSelection)

        # connect

        thread.prepared.connect(self._on_prepared)
        thread.process_finished.connect(self._on_process_finished)
        thread.error.connect(self._on_error)
        thread.finished.connect(self._on_finished)

        # layout

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_lbl)
        ref_hbox.addWidget(ref_value_lbl, 1)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(ref_hbox)
        vbox.addWidget(result_tv)

        self.content_layout = vbox

        # fields

        self._thread = thread

        # setup

        self.setMinimumWidth(650)
        self.setWindowTitle('Сравнение')
        self.progress_bar.setFormat('  %v из %m')

    def on_show(self):
        self._thread.start()

    def on_abort(self) -> bool:
        self._thread.terminate()
        return True

    def _increment_progress(self, inc=1):
        value = self.progress_bar.value() + inc
        self.progress_bar.setValue(value)

    def _on_prepared(self, count: int):
        self.progress_bar.setMaximum(count)
        self.update()

    def _on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: int):
        self._increment_progress()

    def _on_finished(self):
        self.finish_him()

    def _on_error(self, alg: BaseAlgorithm, other: pl.Path, text: str):
        self._increment_progress()
        print(f'[ERROR] {other} => [{alg}] => {text}', file=sys.stderr, flush=True)
