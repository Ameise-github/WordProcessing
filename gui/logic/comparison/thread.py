import typing as t
import pathlib as pl

import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.logic.common.pool_tread import BasePoolThread, Combination
from gui.models.comparison.algorithms import AlgorithmList

ComparisionData = t.Tuple[BaseAlgorithm, pl.Path]


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

    def prepare(self) -> t.Any:
        return len(self._algorithms) * len(self._others)

    def combine(self) -> t.Generator[Combination, None, None]:
        for other in self._others:
            for alg in self._algorithms:
                yield Combination(
                    (alg, other),
                    alg.process,
                    map(str, (self._udpipe, self._reference, other))
                )
