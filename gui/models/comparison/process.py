import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.thread import ComparisionData
from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets.style import Colors


class ComparisonResult:
    NONE = 'none'
    WORKING = 'working'
    ERROR = 'error'
    SUCCESS = 'success'

    def __init__(self, state=NONE, value=None):
        self.state = state
        self.value = value


_ResultTable = t.Dict[t.Tuple[BaseAlgorithm, pl.Path], ComparisonResult]


class ComparisonProcessModel(qc.QAbstractTableModel):

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._algorithms: AlgorithmList = []
        self._text_files: t.List[pl.Path] = []
        self._results: _ResultTable = {}

    def set_source(self, algorithms: AlgorithmList, others: t.List[pl.Path], combinations: t.List[ComparisionData]):
        self.beginResetModel()
        self._algorithms = algorithms
        self._text_files = others
        self._results = dict.fromkeys(
            map(tuple, combinations),
            ComparisonResult()
        )
        self.endResetModel()

    def assign_result(self, algorithm: BaseAlgorithm, file: pl.Path,  result: ComparisonResult) -> bool:
        self._results[algorithm, file] = result
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
        return True

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._text_files)

    def columnCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._algorithms)

    def headerData(self, section: int, orientation: qq.Orientation, role: int = qq.DisplayRole) -> t.Any:
        if qq.Orientation.Horizontal == orientation:
            algorithm = self._algorithms[section]

            if role in (qq.DisplayRole, qq.ToolTipRole):
                return algorithm.name

        elif qq.Orientation.Vertical == orientation:
            file = self._text_files[section]

            if qq.DisplayRole == role:
                return file.name

            elif qq.ToolTipRole == role:
                return str(file)

        return None

    def data(self, index: qc.QModelIndex = qc.QModelIndex(), role: int = qq.DisplayRole) -> t.Any:
        if not index.isValid():
            return None

        algorithm = self._algorithms[index.column()]
        other = self._text_files[index.row()]
        result = self._results[algorithm, other]

        if qq.TextAlignmentRole == role:
            return qq.AlignCenter

        if ComparisonResult.WORKING == result.state:
            if qq.DisplayRole == role:
                return 'в процессе'
            elif qq.BackgroundRole == role:
                return Colors.BG_ORANGE
        elif ComparisonResult.SUCCESS == result.state:
            if qq.DisplayRole == role:
                return str(result.value)
