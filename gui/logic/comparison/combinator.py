import typing as t
import pathlib as pl
import PySide2.QtCore as qc
from gui.models.comparison.algorithms import AlgorithmList, BaseMetricAnalysis


class ComparisonCombinator(qc.QObject):
    def __init__(self, parent: qc.QObject = None):
        super().__init__(parent)

        self.files: t.List[pl.Path] = []
        self.reference: t.Optional[pl.Path] = None
        self.algorithms: AlgorithmList = []
        self.udpipe: t.Optional[pl.Path] = None

    def prepare(self):
        for alg in self.algorithms:
            alg.set_trainTextUdpipe(str(self.udpipe))
            alg.set_text_standart(str(self.reference))

    def total(self):
        return len(self.files) * len(self.algorithms)

    def combine(self) -> t.Tuple[BaseMetricAnalysis, pl.Path]:
        for file in self.files:
            for alg in self.algorithms:
                alg.set_text(str(file))
                yield alg, file
