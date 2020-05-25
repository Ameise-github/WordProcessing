import typing as t
import pathlib as pl
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.models.comparison.algorithms import AlgorithmList

ComparisionPair = t.Tuple[BaseAlgorithm, pl.Path]


class ComparisionThread(qc.QThread):
    prepared = qc.Signal(list)
    process_started = qc.Signal(tuple)
    process_finished = qc.Signal(tuple, float)
    process_error = qc.Signal(tuple, str)

    def __init__(self,
                 udpipe: t.Optional[pl.Path], algorithms: AlgorithmList,
                 reference: t.Optional[pl.Path], others: t.List[pl.Path],
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._udpipe = udpipe
        self._algorithms = algorithms
        self._reference = reference
        self._others = others

        self._abort = False

    def _combine(self):
        combination = []
        for other in self._others:
            for alg in self._algorithms:
                combination.append((alg, other))
        return combination

    def run(self):
        with mp.Pool() as pool:
            combination = self._combine()
            self.prepared.emit(combination)

            receivers = {}

            for alg, other in combination:
                # funcs
                process_func = ft.partial(
                    self._pre_wrapper,
                    self._udpipe, alg, self._reference, other)
                callback = ft.partial(
                    self._on_process_finished,
                    alg, other)
                error_callback = ft.partial(
                    self._on_process_error,
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

            if self._abort:
                pool.terminate()
            else:
                pool.close()
            pool.join()

    def abort(self):
        self._abort = True

    @staticmethod
    def _pre_wrapper(udpipe: pl.Path, alg: BaseAlgorithm, ref: pl.Path, other: pl.Path,
                     sender: mp.connection.PipeConnection) -> float:
        sender.send(object())  # send start signal
        result = alg.process(str(udpipe), str(ref), str(other))
        return result

    def _pre_loop(self, receivers: dict):
        while receivers and not self._abort:
            for_delete = []
            # handle
            for rec, (alg, other) in receivers.items():
                rec: mp.connection.PipeConnection = rec
                if rec.closed:
                    for_delete.append(rec)
                    continue
                try:
                    rec.recv()
                except EOFError:
                    continue

                for_delete.append(rec)
                self._on_process_started(alg, other)
            # clean
            for rec in for_delete:
                del receivers[rec]

    def _on_process_started(self, alg: BaseAlgorithm, other: pl.Path):
        if self._abort:
            return
        self.process_started.emit((alg, other))

    def _on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: float):
        if self._abort:
            return
        self.process_finished.emit((alg, other), result)

    def _on_process_error(self, alg: BaseAlgorithm, other: pl.Path, exception: BaseException):
        self.process_error.emit((alg, other), exception.args[0])
