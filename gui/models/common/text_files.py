import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg

from gui.models.common.checkable import BaseCheckableModel
from gui.widgets.style import Colors


class TextFilesModel(BaseCheckableModel[pl.Path]):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._show_paths = False

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[pl.Path, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        file = self._items[row]
        not_exists = not file.exists()

        if qq.DisplayRole == role:
            if self._show_paths:
                return str(file)
            else:
                return file.name

        elif qq.TextColorRole == role:
            if not_exists:
                return Colors.FG_RED

        elif qq.FontRole == role:
            font = qg.QFont()
            if not_exists:
                font.setItalic(True)
            return font

        elif qq.ToolTipRole == role:
            tool_tips = []
            if not self._show_paths:
                tool_tips.append(str(file))
            if not_exists:
                tool_tips.append('Файл не найден')
            return '\n'.join(tool_tips)

        else:
            return super().data(index, role)

    @property
    def show_paths(self) -> bool:
        return self._show_paths

    @show_paths.setter
    def show_paths(self, value: bool):
        self._show_paths = value
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def append(self, paths: t.Iterable[str]):
        self.beginResetModel() # qc.QModelIndex(), 0, len(self._items) - 1
        paths_set = dict.fromkeys(map(pl.Path, paths))
        files_set = dict.fromkeys(self._items)
        files_set.update(paths_set)
        self._items = list(files_set.keys())
        self.endResetModel()

    def remove(self, paths: t.Iterable[str]):
        self.beginRemoveRows(qc.QModelIndex(), 0, len(self._items) - 1)
        paths_set = set(map(pl.Path, paths))
        files_set = set(self._items)
        for path in files_set.intersection(paths_set):
            self._items.remove(path)
            if path in self._checked:
                self._checked.remove(path)
        self.endRemoveRows()

    def move_up(self, index: qc.QModelIndex):
        if not index.isValid():
            return

        row = index.row()
        row_new = row - 1
        if 0 <= row_new < len(self._items):
            dummy_index = qc.QModelIndex()

            self.beginMoveRows(dummy_index, row, row, dummy_index, row_new)
            self._items[row], self._items[row_new] = self._items[row_new], self._items[row]
            self.endMoveRows()

    def move_down(self, index: qc.QModelIndex):
        if not index.isValid():
            return

        row = index.row()
        row_new = row + 1
        if 0 <= row_new < len(self._items):
            dummy_index = qc.QModelIndex()

            self.beginMoveRows(dummy_index, row, row, dummy_index, row_new + 1)
            self._items[row], self._items[row_new] = self._items[row_new], self._items[row]
            self.endMoveRows()

    def items(self, *, exists_only=False) -> t.List[pl.Path]:
        filtered = filter(
            lambda f: not exists_only or f.exists(),
            self._items
        )
        return list(filtered)

    def checked(self, *, exists_only=False) -> t.List[pl.Path]:
        filtered = filter(
            lambda f: not exists_only or f.exists(),
            self._checked
        )
        return list(filtered)
