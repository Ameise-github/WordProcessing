import sys
import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.thread import ComparisionThread, ComparisionData
from gui.models.comparison.process import ComparisonProcessModel, ComparisonResult
from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets.common.process_dialog import BaseProcessDialog


class ComparisonDialog(BaseProcessDialog):
    def __init__(self,
                 udpipe: t.Optional[pl.Path], algorithms: AlgorithmList,
                 reference: t.Optional[pl.Path], others: t.List[pl.Path],
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = ComparisonProcessModel()
        model.set_source(algorithms, others)
        thread = ComparisionThread(udpipe, algorithms, reference, others, self)

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel(str(reference))

        result_tv = qw.QTableView()
        result_tv.setModel(model)
        result_tv.setSelectionMode(result_tv.SelectionMode.SingleSelection)

        # connect

        thread.prepared.connect(self._on_prepared)
        thread.process_started.connect(self._on_process_started)
        thread.process_finished.connect(self._on_process_finished)
        thread.process_error.connect(self._on_process_error)
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

        self._model = model
        self._algorithms = algorithms
        self._others = others

        # setup

        self.setMinimumWidth(650)
        self.setWindowTitle('Сравнение')
        self.progress_bar.setFormat('  %v из %m')
        self._thread.start()

    def on_abort(self) -> bool:
        self._thread.abort()
        return True

    def _on_prepared(self, count: int):
        self.progress_bar.setMaximum(count)
        self.update()

    def _on_process_started(self, data: ComparisionData):
        alg, other = data
        self._model.assign_result(
            alg, other,
            ComparisonResult(ComparisonResult.WORKING)
        )

    def _on_process_finished(self, data: ComparisionData, result: float):
        alg, other = data
        self._model.assign_result(
            alg, other,
            ComparisonResult(ComparisonResult.SUCCESS, result)
        )
        self.progress_value += 1

    def _on_process_error(self, data: ComparisionData, text: str):
        alg, other = data
        print(f'[ERROR] {other} => [{alg}] => {text}', file=sys.stderr, flush=True)
        self._model.assign_result(
            alg, other,
            ComparisonResult(ComparisonResult.ERROR, text)
        )
        self.progress_value += 1

    def _on_finished(self):
        self.finish_him()
