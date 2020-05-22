import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.models.list import BaseListModel
from gui.models.roles import Roles
from gui.widgets.style import Colors

TItem = t.TypeVar('TItem')


class BaseCheckableModel(BaseListModel[TItem]):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._selected: t.List[TItem] = []

    def flags(self, index: qc.QModelIndex) -> qq.ItemFlags:
        default_flags = super().flags(index)
        if index.isValid():
            return default_flags | qq.ItemIsUserCheckable
        return default_flags

    def setData(self, index: qc.QModelIndex, value: t.Any, role: int = qq.CheckStateRole) -> bool:
        if not (index.isValid() or role == qq.CheckStateRole):
            return False

        item = index.data(Roles.SourceDataRole)

        if value == qq.Checked:
            self._selected.append(item)
        else:
            self._selected.remove(item)

        return True

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[TItem, t.Any]:
        row = index.row()
        item = self._items[row]

        if qq.CheckStateRole == role:
            return self.check_state(item)
        else:
            return super().data(index, role)

    def checked(self) -> t.List[TItem]:
        return self._selected.copy()

    def check_state(self, item: TItem) -> qq.CheckState:
        return qq.Checked if item in self._selected else qq.Unchecked

    def invert(self):
        items_set = set(self._items)
        inverted_set = items_set.difference(self._selected)
        self._selected = list(inverted_set)
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def check_all(self):
        self._selected = self._items.copy()
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def uncheck_all(self):
        self._selected.clear()
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self._selected.clear()
        self.endResetModel()
