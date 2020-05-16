import typing as t
import pathlib as pl
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.models.comparison.process import ComparisonProcessModel, ComparisonResult


class ComparisionThread(qc.QThread):
    process_started = qc.Signal(BaseAlgorithm, pl.Path)
    process_finished = qc.Signal(BaseAlgorithm, pl.Path, float)
    error = qc.Signal(BaseAlgorithm, pl.Path, str)

    def __init__(self, model: ComparisonProcessModel, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._model = model
        self._pool = mp.Pool()

        self.process_started.connect(self.on_process_stated)
        self.finished.connect(self.on_finished)

    def run(self):
        with self._pool as pool:
            receivers = {}

            for udpipe, alg, ref, other in self._model.combinator.combine():
                # funcs
                process_func = ft.partial(
                    self._pre_wrapper,
                    udpipe, alg, ref, other)
                callback = ft.partial(
                    self.on_process_finished,
                    alg, other)
                error_callback = ft.partial(
                    self.on_process_error,
                    alg, other)

                # process
                receiver, sender = mp.Pipe(False)
                pool.apply_async(
                    process_func,
                    [sender], {},
                    callback, error_callback)

                # add
                receivers[receiver] = (alg, other)

            self._pre_loop(receivers)

            pool.close()
            pool.join()

    @staticmethod
    def _pre_wrapper(udpipe: pl.Path, alg: BaseAlgorithm, ref: pl.Path, other: pl.Path,
                     sender: mp.connection.PipeConnection) -> float:
        sender.send(object())  # send start signal
        result = alg.process(str(udpipe), str(ref), str(other))
        return result

    def _pre_loop(self, receivers: dict):
        while receivers:
            for_delete = []
            # handle
            for rec, (alg, other) in receivers.items():
                if rec.closed:
                    for_delete.append(rec)
                    continue
                try:
                    rec.recv()
                except EOFError:
                    continue

                for_delete.append(rec)
                self.process_started.emit(alg, other)
            # clean
            for rec in for_delete:
                del receivers[rec]

    def on_process_stated(self, alg: BaseAlgorithm, other: pl.Path):
        result = ComparisonResult(ComparisonResult.WORKING, None)
        self._model.assign_result(other, alg, result)

    def on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: float):
        result = ComparisonResult(ComparisonResult.SUCCESS, result)
        self._model.assign_result(other, alg, result)
        self.process_finished.emit(alg, other, result)

    def on_process_error(self, alg: BaseAlgorithm, other: pl.Path, exception: BaseException):
        result = ComparisonResult(ComparisonResult.ERROR, repr(exception))
        self._model.assign_result(other, alg, result)
        self.error.emit(alg, other, exception.args[0])

    def on_finished(self):
        self._pool.terminate()
