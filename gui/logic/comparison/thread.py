import typing as t
import pathlib as pl
import multiprocessing as mp
import functools as ft
import PySide2.QtCore as qc
from gui.models.comparison.algorithms import BaseAlgorithm
from gui.logic.comparison.combinator import ComparisonCombinator


class ComparisionThread(qc.QThread):
    processed = qc.Signal(BaseAlgorithm, pl.Path, float)
    error = qc.Signal(BaseAlgorithm, pl.Path, str)

    def __init__(self, combinator: ComparisonCombinator, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self.finished.connect(self.on_finished)

        self.combinator = combinator
        self._pool = mp.Pool()

    def run(self):
        with self._pool as pool:
            for udpipe, alg, ref, other in self.combinator.combine():
                pool.apply_async(
                    alg.process,
                    (str(udpipe), str(ref), str(other)),
                    callback=ft.partial(self.on_process_finished, alg, other),
                    error_callback=ft.partial(self.on_process_error, alg, other)
                )

            pool.close()
            pool.join()

    def on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: float):
        self.processed.emit(alg, other, result)

    def on_process_error(self, alg: BaseAlgorithm, other: pl.Path, exception: BaseException):
        self.error.emit(alg, other, exception.args[0])

    def on_finished(self):
        self._pool.terminate()
