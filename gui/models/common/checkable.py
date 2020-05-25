import typing as t

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc

from gui.models.common.list import BaseListModel
from gui.models.roles import Roles

TItem = t.TypeVar('TItem')


class BaseCheckableModel(BaseListModel[TItem]):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._checked: t.List[TItem] = []

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
            self._checked.append(item)
        else:
            self._checked.remove(item)

        return True

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[TItem, t.Any]:
        row = index.row()
        item = self._items[row]

        if qq.CheckStateRole == role:
            return self.check_state(item)
        else:
            return super().data(index, role)

    def checked(self) -> t.List[TItem]:
        return self._checked.copy()

    def check_state(self, item: TItem) -> qq.CheckState:
        return qq.Checked if item in self._checked else qq.Unchecked

    def invert(self):
        items_set = set(self._items)
        inverted_set = items_set.difference(self._checked)
        self._checked = list(inverted_set)
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def check_all(self):
        self._checked = self._items.copy()
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def uncheck_all(self):
        self._checked.clear()
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self._checked.clear()
        self.endResetModel()
