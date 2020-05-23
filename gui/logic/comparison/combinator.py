import typing as t
import pathlib as pl

from parsing.metric.base import BaseAlgorithm
from gui.models.comparison.algorithms import AlgorithmList


class ComparisonCombinator:
    def __init__(self):
        self.udpipe: t.Optional[pl.Path] = None
        self.algorithms: AlgorithmList = []
        self.reference: t.Optional[pl.Path] = None
        self.others: t.List[pl.Path] = []

    def combine(self) -> t.List[t.Tuple[BaseAlgorithm, pl.Path]]:
        combination = []
        for other in self.others:
            for alg in self.algorithms:
                combination.append((alg, other))
        return combination
