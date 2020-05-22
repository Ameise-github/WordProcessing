import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.models.roles import Roles
from gui.widgets.style import Colors

TItem = t.TypeVar('TItem')


class BaseListModel(qc.QAbstractListModel, t.Generic[TItem]):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._items: t.List[TItem] = []

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._items)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[TItem, t.Any]:
        row = index.row()
        item = self._items[row]

        if Roles.SourceDataRole == role:
            return item

        return None

    def removeRows(self, row: int, count: int, parent: qc.QModelIndex = qc.QModelIndex()) -> bool:
        try:
            removed = map(str, self._items[row:row + count])
            self.remove(removed)
        except IndexError:
            return False
        return True

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()
