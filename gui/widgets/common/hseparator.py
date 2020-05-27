import typing as t

from PySide2.QtCore import Qt as qq
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class HSeparator(qw.QFrame):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # setup

        self.setMinimumHeight(1)
        self.setFrameShape(qw.QFrame.StyledPanel)
