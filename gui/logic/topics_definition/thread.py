import typing as t
import pathlib as pl

import PySide2.QtCore as qc

from parsing.ThemsText import ThemsText
from gui.logic.common.pool_tread import BasePoolThread, Combination
from gui.models.common.udpipe import UDPipeFile


class TopicsDefinitionThread(BasePoolThread):
    def __init__(self, files: t.List[pl.Path], udpipe: UDPipeFile, optimal_topics: bool,
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._files = files
        self._udpipe = udpipe
        self._optimal_topics = optimal_topics

    def prepare(self) -> t.Any:
        return None

    def combine(self) -> list:
        yield Combination(
            None,
            self._process,
            (str(self._udpipe), list(map(str, self._files)), self._optimal_topics)
        )

    @staticmethod
    def _process(udpipe, files, optimal_topics):
        topics_text = ThemsText(files, udpipe, optimal_topics)
        view_str, _ = topics_text.view_thems()
        return view_str
