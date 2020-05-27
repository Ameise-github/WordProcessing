import typing as t
import pathlib as pl

import PySide2.QtCore as qc
from PySide2.QtCore import Qt as qq
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.models.roles import Roles


class TextFilesProxyModel(qc.QIdentityProxyModel):
    def data(self, proxy_index: qc.QModelIndex, role: int = qq.DisplayRole) -> t.Any:
        if not proxy_index.isValid():
            return None

        text_file: str = super().data(proxy_index, Roles.SourceDataRole)

        if qq.DisplayRole == role:
            return pl.Path(text_file).name

        elif qq.CheckStateRole == role:
            return None

        elif qq.ForegroundRole == role:
            color: qg.QColor = super().data(proxy_index, qq.ForegroundRole)
            checked: qq.CheckState = super().data(proxy_index, qq.CheckStateRole)
            if not color:
                color = qw.QApplication.palette().color(qg.QPalette.Foreground)
            if qq.Unchecked == checked:
                color.setAlphaF(0.4)
            return color

        else:
            return super().data(proxy_index, role)
