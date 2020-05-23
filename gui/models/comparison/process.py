import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.combinator import ComparisonCombinator
from gui.widgets.style import Colors


class ComparisonResult:
    NONE = 'none'
    WORKING = 'working'
    ERROR = 'error'
    SUCCESS = 'success'

    def __init__(self, state=NONE, value=None):
        self.state = state
        self.value = value


_ResultTable = t.Dict[t.Tuple[int, int], ComparisonResult]


class ComparisonProcessModel(qc.QAbstractTableModel):

    def __init__(self, combinator: ComparisonCombinator, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._combinator = combinator
        self._results: _ResultTable = {}

    @property
    def combinator(self) -> ComparisonCombinator:
        return self._combinator

    def assign_result(self, file: pl.Path, algorithm: BaseAlgorithm, result: ComparisonResult) -> bool:
        try:
            row = self._combinator.others.index(file)
            col = self._combinator.algorithms.index(algorithm)
        except ValueError:
            return False

        self._results[row, col] = result
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
        return True

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._combinator.others)

    def columnCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._combinator.algorithms)

    def headerData(self, section: int, orientation: qq.Orientation, role: int = qq.DisplayRole) -> t.Any:
        if qq.Orientation.Horizontal == orientation:
            algorithm = self._combinator.algorithms[section]

            if role in (qq.DisplayRole, qq.ToolTipRole):
                return algorithm.name

            # elif qq.SizeHintRole == role:
            #     fm = qw.QApplication.fontMetrics()
            #     style = qw.QApplication.style()
            #     margin = style.pixelMetric(qw.QStyle.PM_ButtonMargin)
            #     header_margin = qc.QSize(margin, margin) * 2
            #     rect = fm.boundingRect(algorithm.name)
            #     return rect.size() + header_margin

        elif qq.Orientation.Vertical == orientation:
            file = self._combinator.others[section]

            if qq.DisplayRole == role:
                return file.name

            elif qq.ToolTipRole == role:
                return str(file)

        return None

    def data(self, index: qc.QModelIndex = qc.QModelIndex(), role: int = qq.DisplayRole) -> t.Any:
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        result = self._results.get((row, col), ComparisonResult())

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
