import typing as t
import pathlib as pl

from PySide2.QtCore import Qt as qq
import PySide2.QtCore as qc
import PySide2.QtGui as qg

from gui.logic.pragmatic_adequacy.thread import PragmaticAdequacyData
from gui.widgets.style import Colors


class PragmaticAdequacyResult:
    NONE = 'none'
    WORKING = 'working'
    ERROR = 'error'
    SUCCESS = 'success'

    def __init__(self, state=NONE, value=None):
        self.state = state
        self.value = value


_ResultDict = t.Dict[t.Tuple[pl.Path, pl.Path], PragmaticAdequacyResult]


class PragmaticAdequacyProcessModel(qc.QAbstractTableModel):

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        # [fields]

        self._text_files: t.List[pl.Path] = []
        self._results: _ResultDict = {}

    @property
    def text_files(self) -> t.List[pl.Path]:
        return self._text_files.copy()

    def set_source(self, text_files: t.List[pl.Path], combinations: t.List[PragmaticAdequacyData]):
        self.beginResetModel()
        self._text_files = text_files
        self._results = dict.fromkeys(
            map(tuple, combinations),
            PragmaticAdequacyResult()
        )
        self.endResetModel()

    def assign_result(self, one: pl.Path, two: pl.Path, result: PragmaticAdequacyResult) -> bool:
        self._results[one, two] = result
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
        return True

    def rowCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._text_files)

    def columnCount(self, parent: qc.QModelIndex = qc.QModelIndex()) -> int:
        return len(self._text_files)

    def headerData(self, section: int, orientation: qq.Orientation, role: int = qq.DisplayRole) -> t.Any:
        file = self._text_files[section]

        if qq.DisplayRole == role:
            return str(section + 1)

        elif qq.ToolTipRole == role:
            return str(file)

        return None

    def data(self, index: qc.QModelIndex = qc.QModelIndex(), role: int = qq.DisplayRole) -> t.Any:
        if not index.isValid():
            return None

        one = self._text_files[index.row()]
        two = self._text_files[index.column()]
        result = self._results.get((one, two))

        if not result:
            if qq.BackgroundRole == role:
                if one == two:
                    return qg.QColor.fromRgbF(0, 0, 0, 0.4)
                else:
                    return qg.QColor.fromRgbF(0, 0, 0, 0.2)

            elif qq.ToolTipRole == role:
                return 'Не сравнивается'

        else:
            if qq.TextAlignmentRole == role:
                return qq.AlignCenter

            if PragmaticAdequacyResult.WORKING == result.state:
                if qq.DisplayRole == role:
                    return '...'
                elif qq.BackgroundRole == role:
                    return Colors.BG_ORANGE
            elif PragmaticAdequacyResult.SUCCESS == result.state:
                if qq.DisplayRole == role:
                    return str(result.value)
