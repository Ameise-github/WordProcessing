import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq


class BaseSetup(qw.QWidget):
    def __init__(self, name: str, action_text: str,
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [field]

        self._name = name
        self._act_text = action_text

    @property
    def name(self):
        return self._name

    @property
    def action_text(self):
        return self._act_text

    def analysis(self):
        raise NotImplementedError()
