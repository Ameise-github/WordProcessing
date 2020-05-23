import typing as t

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc

from parsing.metric.base import BaseAlgorithm
from gui.models.checkable import BaseCheckableModel

AlgorithmList = t.List[BaseAlgorithm]


class ComparisonAlgorithmsModel(BaseCheckableModel[BaseAlgorithm]):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[BaseAlgorithm, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        algorithm = self._items[row]

        if qq.DisplayRole == role:
            return algorithm.name
        else:
            return super().data(index, role)

    @property
    def algorithms(self) -> AlgorithmList:
        return self._items.copy()

    @algorithms.setter
    def algorithms(self, value: AlgorithmList):
        self.beginResetModel()
        self._items = value.copy()
        self.endResetModel()