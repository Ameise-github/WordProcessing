import typing as t

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.widgets.notification_server import NotificationServer

# language=CSS
_STYLE_SHEET = """
QPushButton { 
    text-align: left;
    border: 1px solid #FFD800;
    padding: 2px;
    background-color: #30FFD800;
}

QPushButton:hover { 
    background-color: #FFE97F;
}
"""


class NoteButton(qw.QPushButton):
    def __init__(self, server: NotificationServer, parent: t.Optional[qw.QWidget] = None):
        pixmap = qw.QApplication.style().standardPixmap(qw.QStyle.SP_MessageBoxWarning)
        super().__init__(qg.QIcon(pixmap), '', parent)

        self.clicked.connect(self._on_click)
        server.notified.connect(self._on_notified)
        server.cleared.connect(self._on_click)

        self.setFlat(True)
        self.setStyleSheet(_STYLE_SHEET)
        self.hide()

    def _on_notified(self, text: str):
        self.setText(text)
        self.show()

    def _on_click(self):
        self.hide()
