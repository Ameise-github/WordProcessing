import typing as t
import pathlib as pl
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.logic.common.pool_tread import BasePoolThread
from gui.models.comparison.algorithms import AlgorithmList


class ComparisionData:
    def __init__(self, algorithm: BaseAlgorithm = None, other: pl.Path = None):
        self.algorithm = algorithm
        self.other = other

    def __iter__(self):
        return iter((self.algorithm, self.other))


class ComparisionThread(BasePoolThread):
    def __init__(self,
                 udpipe: t.Optional[pl.Path], algorithms: AlgorithmList,
                 reference: t.Optional[pl.Path], others: t.List[pl.Path],
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._udpipe = udpipe
        self._algorithms = algorithms
        self._reference = reference
        self._others = others

    def combine(self):
        combination = []
        for other in self._others:
            for alg in self._algorithms:
                data = ComparisionData(alg, other)
                combination.append(data)
        return combination

    def prepare_args(self, data: ComparisionData):
        return (
            str(self._udpipe),
            data.algorithm.process,
            str(self._reference),
            str(data.other)
        )

    @staticmethod
    def process(args):
        udpipe, process_func, ref, other = args
        return process_func(udpipe, ref, other)
