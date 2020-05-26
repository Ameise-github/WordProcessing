import typing as t

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.widgets import style
from gui.widgets.notification_server import NotificationServer


class NoteButton(qw.QPushButton):
    def __init__(self, server: NotificationServer, parent: t.Optional[qw.QWidget] = None):
        pixmap = qw.QApplication.style().standardPixmap(qw.QStyle.SP_MessageBoxWarning)
        super().__init__(qg.QIcon(pixmap), '', parent)

        self.clicked.connect(self._on_click)
        server.notified.connect(self._on_notified)
        server.cleared.connect(self._on_click)

        self.setFlat(True)
        self.setStyleSheet(style.style_sheets.note_button)
        self.hide()

    def _on_notified(self, text: str):
        self.setText(text)
        self.show()

    def _on_click(self):
        self.hide()
