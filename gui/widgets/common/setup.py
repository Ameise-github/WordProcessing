import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.widgets.common.process_dialog import BaseProcessDialog


class BaseSetup(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

    def exec_dialog(self, dialog: BaseProcessDialog) -> int:
        self.hide()
        result = dialog.exec_()
        self.show()
        return result
