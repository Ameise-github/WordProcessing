import typing as t
import pathlib as pl
import enum

import PySide2.QtCore as qc

from parsing.TextAnalysis import TextAnalysis
from gui.logic.common.pool_tread import BasePoolThread, Combination


class DataType(enum.Enum):
    MORPHOLOGY = 'morphology',
    SYNTAX = 'syntax'


class MorphSyntaxThread(BasePoolThread):
    def __init__(self,
                 nltk: pl.Path, udpipe: pl.Path, text: pl.Path, rus: bool,
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._nltk = nltk
        self._udpipe = udpipe
        self._text = text
        self._rus = rus

    def prepare(self) -> t.Any:
        return None

    def combine(self) -> t.Generator[Combination, None, None]:
        text_path = str(self._text)
        yield Combination(
            DataType.MORPHOLOGY,
            self._morphology,
            (str(self._nltk), text_path, self._rus)
        )
        yield Combination(
            DataType.SYNTAX,
            self._syntax,
            (str(self._udpipe), text_path)
        )

    @staticmethod
    def _morphology(nltk: str, text: str, rus: bool) -> list:
        analysis = TextAnalysis()
        result = analysis.morph_analysis(nltk, text, rus)
        return result

    @staticmethod
    def _syntax(udpipe: str, text: str) -> str:
        analysis = TextAnalysis()
        result = analysis.view_syntax_tree(text, udpipe)
        return result
