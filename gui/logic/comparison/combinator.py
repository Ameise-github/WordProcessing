import typing as t
import pathlib as pl

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.models.algorithms import AlgorithmList


class ComparisonCombinator(qc.QObject):
    def __init__(self, parent: qc.QObject = None):
        super().__init__(parent)

        self.udpipe: t.Optional[pl.Path] = None
        self.algorithms: AlgorithmList = []
        self.reference: t.Optional[pl.Path] = None
        self.others: t.List[pl.Path] = []

    def total(self):
        return len(self.others) * len(self.algorithms)

    def combine(self) -> t.Tuple[pl.Path, BaseAlgorithm, pl.Path, pl.Path]:
        for other in self.others:
            for alg in self.algorithms:
                yield self.udpipe, alg, self.reference, other
