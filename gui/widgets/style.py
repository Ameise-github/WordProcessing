import pathlib as pl

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from gui.fs.icons import IconStorage

STYLE_SHEET = """
QPushButton {
    min-width: 100px
}
"""


class Colors:
    FG_RED = qg.QColor('#CC0000')
    BG_GREEN = qg.QColor('#DDFFC0')
    BG_ORANGE = qg.QColor('#FFDA77')
    WHITE = qg.QColor(255, 255, 255)


icons = IconStorage()


def init():
    icons.load(pl.Path(__file__).parent / '../../resource/icons', qc.QSize(24, 24))
