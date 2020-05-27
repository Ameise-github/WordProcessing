import pathlib as pl

import PySide2.QtCore as qc
import PySide2.QtGui as qg

from gui.fs.icons import IconStorage
from gui.fs.style_sheets import StyleSheetStorage


class Colors:
    FG_RED = qg.QColor('#CC0000')
    BG_GREEN = qg.QColor('#DDFFC0')
    BG_ORANGE = qg.QColor('#FFDA77')
    WHITE = qg.QColor(255, 255, 255)


icons = IconStorage()
style_sheets = StyleSheetStorage()


def init():
    res_path = pl.Path(__file__).parent / '../resources'

    icons.load(res_path / 'icons', qc.QSize(24, 24))
    style_sheets.load(res_path / 'css')
