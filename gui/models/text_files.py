import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.models.roles import Roles
from gui.widgets.style import Colors


class TextFilesModel(qc.QAbstractListModel):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._files: t.List[pl.Path] = []
        self._show_paths = False

    @property
    def show_paths(self) -> bool:
        return self._show_paths

    @show_paths.setter
    def show_paths(self, value: bool):
        self._show_paths = value
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def append(self, paths: t.Iterable[str]):
        self.beginInsertRows(qc.QModelIndex(), 0, len(self._files) - 1)
        paths_set = dict.fromkeys(map(pl.Path, paths))
        files_set = dict.fromkeys(self._files)
        files_set.update(paths_set)
        self._files = list(files_set.keys())
        self.endInsertRows()

    def remove(self, paths: t.Iterable[str]):
        self.beginRemoveRows(qc.QModelIndex(), 0, len(self._files) - 1)
        paths_set = set(map(pl.Path, paths))
        files_set = set(self._files)
        for path in files_set.intersection(paths_set):
            self._files.remove(path)
        self.endRemoveRows()

    def files(self, *, exists_only=False) -> t.List[pl.Path]:
        filtered = filter(
            lambda f: not exists_only or f.exists(),
            self._files
        )
        return list(filtered)

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._files)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[pl.Path, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        file = self._files[row]
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

        elif Roles.SourceDataRole == role:
            return file

        return None

    def removeRows(self, row: int, count: int, parent: qc.QModelIndex = qc.QModelIndex()) -> bool:
        try:
            removed = map(str, self._files[row:row + count])
            self.remove(removed)
        except IndexError:
            return False
        return True

    def clear(self):
        self.beginResetModel()
        self._files.clear()
        self.endResetModel()
