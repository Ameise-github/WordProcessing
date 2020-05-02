import typing as t
import pathlib as pl
from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from gui.models import Roles

REF_FILE_COLOR = qg.QColor.fromRgb(46, 139, 87)


class ComparisonFilesModel(qc.QAbstractListModel):
    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._files: t.List[str] = []
        self._ref_file: t.Optional[str] = None
        self._show_path = False

    @property
    def show_path(self) -> bool:
        return self._show_path

    @show_path.setter
    def show_path(self, value: bool):
        self._show_path = value
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def ref_file(self) -> str:
        return self._ref_file

    def set_ref_file(self, index: qc.QModelIndex) -> bool:
        if not index.isValid():
            return False
        self._ref_file = self.data(index, Roles.RawDataRole)
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
        return True

    def other_files(self) -> t.List[str]:
        if self._ref_file:
            files_copy = self._files.copy()
            files_copy.remove(self._ref_file)
            return files_copy
        return self._files

    def append_file(self, file_path: str):
        if file_path not in self._files:
            row = len(self._files)
            self.beginInsertRows(qc.QModelIndex(), row, row)
            self._files.append(file_path)
            self.endInsertRows()

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._files)

    def data(self, index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Union[pl.Path, t.Any]:
        if not index.isValid():
            return None

        row = index.row()
        file = self._files[row]

        if role == qq.DisplayRole:
            if self._show_path:
                return file
            else:
                return pl.Path(file).name
        elif role == qq.TextColorRole:
            if file == self._ref_file:
                return REF_FILE_COLOR
        elif role == qq.FontRole:
            if file == self._ref_file:
                font = qg.QFont()
                font.setBold(True)
                return font
        elif role == Roles.RawDataRole:
            return file

        return None

    def removeRows(self, row: int, count: int, parent: qc.QModelIndex = qc.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)

        for idx in range(row, row + count):
            file = self._files[idx]
            if self._ref_file == file:
                self._ref_file = None
            del self._files[idx]

        self.endRemoveRows()
        return True

    def clear(self):
        self.beginResetModel()
        self._files.clear()
        self._ref_file = None
        self.endResetModel()
