import typing as t

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq


class BaseProcessDialog(qw.QDialog):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        f |= qq.WindowMaximizeButtonHint | qq.WindowMinimizeButtonHint | qq.WindowCloseButtonHint
        f &= ~qq.WindowContextHelpButtonHint
        super().__init__(parent, f)

    @property
    def is_working(self) -> bool:
        return False

    def on_close_event(self, event: qg.QCloseEvent):
        event.accept()

    def closeEvent(self, event: qg.QCloseEvent):
        if self.is_working:
            result = qw.QMessageBox.question(self, 'Отмена операции', 'Прервать выполнение операции?')
            if qw.QMessageBox.Yes == result:
                self.on_close_event(event)
            else:
                event.ignore()
        else:
            event.accept()

    def exec_(self, *, hide_parent=True) -> int:
        parent = self.nativeParentWidget()
        if hide_parent:
            parent.hide()
        result = super().exec_()
        if hide_parent:
            parent.show()
        return result
