import typing as t
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

# language=CSS
_STYLE_SHEET = """
QPushButton { 
    color: rgb(210,105,30); 
    text-align: left;
}
"""


class NoteButton(qw.QPushButton):
    def __init__(self, hide: bool = True, text: str = '', parent: t.Optional[qw.QWidget] = None):
        super().__init__(qg.QIcon(), text, parent)

        self.clicked.connect(self._on_click)

        self.setFlat(True)
        self.setStyleSheet(_STYLE_SHEET)

        if hide:
            self.hide()

    def show_warn(self, text: str):
        self.setIcon(qg.QIcon.fromTheme('dialog-warning'))
        self.setText(text)
        self.show()

    def _on_click(self):
        self.hide()
