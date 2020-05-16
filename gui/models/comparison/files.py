import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.models.roles import Roles
from gui.widgets.style import Colors


class ComparisonFilesModel(qc.QAbstractListModel):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._files: t.List[pl.Path] = []
        self._ref_file: t.Optional[pl.Path] = None
        self._show_paths = False

    @property
    def show_paths(self) -> bool:
        return self._show_paths

    @show_paths.setter
    def show_paths(self, value: bool):
        self._show_paths = value
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    @property
    def ref_file(self) -> t.Optional[pl.Path]:
        return self._ref_file

    @ref_file.setter
    def ref_file(self, value: t.Optional[pl.Path]):
        if value not in self._files:
            print(f'Path <{value}> not in model file paths')
            return
        self._ref_file = value
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    @property
    def exist_ref_file(self) -> t.Optional[pl.Path]:
        r = self._ref_file
        return r if r and r.exists() else None

    @property
    def other_files(self) -> t.List[pl.Path]:
        files = self._files.copy()
        if self._ref_file is not None:
            files.remove(self._ref_file)
        return files

    @property
    def exist_other_files(self) -> t.List[pl.Path]:
        files = self._files.copy()
        if self._ref_file is not None:
            files.remove(self._ref_file)
        return [f for f in files if f.exists()]

    def append_file(self, path: str):
        file = pl.Path(path)
        if file not in self._files:
            row = len(self._files)
            self.beginInsertRows(qc.QModelIndex(), row, row)
            self._files.append(file)
            self.endInsertRows()

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._files)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[pl.Path, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        file = self._files[row]

        is_file_exists = file.exists()
        is_ref_file = (file == self._ref_file)

        if qq.DisplayRole == role:
            file_name = file.name
            if self._show_paths:
                file_name = str(file)
            if is_ref_file:
                file_name += ' [Эталонный]'
            return file_name

        elif qq.TextColorRole == role:
            if not is_file_exists:
                return Colors.FG_RED

        elif qq.FontRole == role:
            font = qg.QFont()
            if not is_file_exists:
                font.setItalic(True)
            return font

        elif qq.BackgroundRole == role:
            if is_ref_file:
                return Colors.BG_GREEN

        elif qq.ToolTipRole == role:
            tool_tips = []
            if not is_file_exists:
                tool_tips.append('Файл не найден')
            if is_ref_file:
                tool_tips.append('Эталонный текст')
            return '\n'.join(tool_tips)

        elif Roles.SourceDataRole == role:
            return file

        return None

    def removeRows(self, row: int, count: int, parent: qc.QModelIndex = qc.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)

        for idx in range(row, row + count):
            file_path = self._files[idx]
            if self._ref_file == file_path:
                self._ref_file = None
            del self._files[idx]

        self.endRemoveRows()
        return True

    def clear(self):
        self.beginResetModel()
        self._files.clear()
        self._ref_file = None
        self.endResetModel()
