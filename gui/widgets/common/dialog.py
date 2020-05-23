import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq


class BaseDialog(qw.QDialog):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        f |= qq.WindowMaximizeButtonHint | qq.WindowMinimizeButtonHint | qq.WindowCloseButtonHint
        f &= ~qq.WindowContextHelpButtonHint
        super().__init__(parent, f)
