import typing as t
import pathlib as pl
import PySide2.QtCore as qc
from gui.models.comparison.algorithms import BaseMetricAnalysis
from gui.logic.comparison.combinator import ComparisonCombinator


class Comparator(qc.QObject):
    begin = qc.Signal()
    end = qc.Signal()
    processing = qc.Signal(BaseMetricAnalysis, pl.Path, int)
    processed = qc.Signal(BaseMetricAnalysis, pl.Path, int)

    def __init__(self, combinator: ComparisonCombinator, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self.combinator = combinator

    def compare(self):
        self.combinator.prepare()
        self.begin.emit()
        for number, (alg, file) in enumerate(self.combinator.combine(), 1):
            self.processing.emit(alg, file, number)
            alg.run()
            self.processed.emit(alg, file, number)
        self.end.emit()


class ComparisonWorker(qc.QObject):
    finished = qc.Signal()

    def __init__(self, combinator: ComparisonCombinator, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        thread = qc.QThread()
        thread.setObjectName('ComparisonWorkerThread')
        comparator = Comparator(combinator)
        comparator.moveToThread(thread)
        comparator.end.connect(thread.quit)

        thread.started.connect(comparator.compare)
        thread.finished.connect(self.finished)

        self.comparator = comparator
        self._thread = thread

    def run(self):
        self._thread.start()

    def stop(self):
        self._thread.terminate()

    def is_running(self):
        return self._thread.isRunning()
