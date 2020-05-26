import typing as t

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc


class MorphologyModel(qc.QAbstractTableModel):
    _HEADERS = ['№', 'Слово', 'Лемма', 'Часть речи', 'Теги']

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._results: t.List[tuple] = []

    def set_source(self, result: t.List[tuple]):
        self.beginResetModel()
        enumerate_result = [
            (i, *r) for i, r in enumerate(result, start=1)
        ]
        self._results = enumerate_result
        self.endResetModel()

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._results)

    def columnCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._HEADERS)

    def headerData(self, section: int, orientation: qq.Orientation, role: int = qq.DisplayRole) -> t.Any:
        if qq.Orientation.Horizontal == orientation:
            if qq.DisplayRole == role:
                return self._HEADERS[section]
        return None

    def data(self, index: qc.QModelIndex = qc.QModelIndex(), role: int = qq.DisplayRole) -> t.Any:
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        result = self._results[row]

        if qq.DisplayRole == role:
            return result[col]
