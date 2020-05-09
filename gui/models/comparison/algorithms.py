import typing as t
from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from gui.models import Roles

from parsing.metric.MetricAnalysis import MetricAnalysis

AlgorithmList = t.List[MetricAnalysis]


class ComparisonAlgorithmsModel(qc.QAbstractListModel):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._algorithms: AlgorithmList = []
        self._selected: AlgorithmList = []

    @property
    def algorithms(self) -> AlgorithmList:
        return self._algorithms.copy()

    @algorithms.setter
    def algorithms(self, value: AlgorithmList):
        self.beginResetModel()
        self._algorithms = value.copy()
        self.endResetModel()

    def checked_algorithms(self) -> AlgorithmList:
        return self._selected.copy()

    def flags(self, index: qc.QModelIndex) -> qq.ItemFlags:
        default_flags = super(ComparisonAlgorithmsModel, self).flags(index)
        if index.isValid():
            return (default_flags | qq.ItemIsUserCheckable)
        return super().flags(index)

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._algorithms)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[MetricAnalysis, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        algorithm = self._algorithms[row]

        if qq.DisplayRole == role:
            return algorithm.name

        elif Roles.DataKeyRole == role:
            return algorithm

        elif qq.CheckStateRole == role:
            return qq.Checked if algorithm in self._selected else qq.Unchecked

        return None

    def setData(self, index: qc.QModelIndex, value: t.Any, role: int = qq.CheckStateRole) -> bool:
        if not (index.isValid() or role == qq.CheckStateRole):
            return False

        algorithm = self.data(index, Roles.DataKeyRole)

        if value == qq.Checked:
            self._selected.append(algorithm)
        else:
            self._selected.remove(algorithm)

        return True
