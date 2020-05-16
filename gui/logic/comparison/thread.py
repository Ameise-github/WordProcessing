import typing as t
import pathlib as pl
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.models.comparison.process import ComparisonProcessModel, ComparisonResult


class ComparisionThread(qc.QThread):
    processed = qc.Signal(BaseAlgorithm, pl.Path, float)
    error = qc.Signal(BaseAlgorithm, pl.Path, str)

    def __init__(self, model: ComparisonProcessModel, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._model = model
        self._pool = mp.Pool()

        self.finished.connect(self.on_finished)

    def run(self):
        with self._pool as pool:
            for udpipe, alg, ref, other in self._model.combinator.combine():
                pool.apply_async(
                    alg.process,
                    (str(udpipe), str(ref), str(other)),
                    callback=ft.partial(self.on_process_finished, alg, other),
                    error_callback=ft.partial(self.on_process_error, alg, other)
                )

            pool.close()
            pool.join()

    def on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: float):
        result = ComparisonResult(ComparisonResult.SUCCESS, result)
        self._model.assign_result(other, alg, result)
        self.processed.emit(alg, other, result)

    def on_process_error(self, alg: BaseAlgorithm, other: pl.Path, exception: BaseException):
        result = ComparisonResult(ComparisonResult.ERROR, repr(exception))
        self._model.assign_result(other, alg, result)
        self.error.emit(alg, other, exception.args[0])

    def on_finished(self):
        self._pool.terminate()
