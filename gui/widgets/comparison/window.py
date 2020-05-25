import sys
import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.thread import ComparisionThread, ComparisionPair
from gui.models.comparison.process import ComparisonProcessModel, ComparisonResult
from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets.common.process_dialog import BaseProcessDialog


class ComparisonWindow(BaseProcessDialog):
    def __init__(self,
                 udpipe: t.Optional[pl.Path], algorithms: AlgorithmList,
                 reference: t.Optional[pl.Path], others: t.List[pl.Path],
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = ComparisonProcessModel()
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

    def on_show(self):
        self._thread.start()

    def on_abort(self) -> bool:
        self._thread.abort()
        return True

    def _increment_progress(self, inc=1):
        value = self.progress_bar.value() + inc
        self.progress_bar.setValue(value)

    def _on_prepared(self, combination: t.List[ComparisionPair]):
        self._model.set_source(self._algorithms, self._others, combination)
        self.progress_bar.setMaximum(len(combination))
        self.update()

    def _on_process_started(self, pair: ComparisionPair):
        algorithm, file = pair
        self._model.assign_result(
            algorithm, file,
            ComparisonResult(ComparisonResult.WORKING)
        )

    def _on_process_finished(self, pair: ComparisionPair, result: float):
        algorithm, file = pair
        self._model.assign_result(
            algorithm, file,
            ComparisonResult(ComparisonResult.SUCCESS, result)
        )
        self._increment_progress()

    def _on_process_error(self, pair: ComparisionPair, text: str):
        algorithm, file = pair
        print(f'[ERROR] {file} => [{algorithm}] => {text}', file=sys.stderr, flush=True)
        self._model.assign_result(
            algorithm, file,
            ComparisonResult(ComparisonResult.ERROR, text)
        )
        self._increment_progress()

    def _on_finished(self):
        self.finish_him()
