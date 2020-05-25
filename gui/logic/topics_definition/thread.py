import typing as t
import pathlib as pl

import PySide2.QtCore as qc

from parsing.ThemsText import ThemsText
from gui.logic.common.pool_tread import BasePoolThread
from gui.models.common.udpipe import UDPipeFile


class TopicsDefinitionThread(BasePoolThread):
    def __init__(self, files: t.List[pl.Path], udpipe: UDPipeFile, optimal_topics: bool,
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._files = files
        self._udpipe = udpipe
        self._optimal_topics = optimal_topics

    def combine(self) -> list:
        return [None]

    def prepare_args(self, data: None):
        return (
            list(map(str, self._files)),
            str(self._udpipe),
            self._optimal_topics
        )

    @staticmethod
    def process(args: object) -> object:
        files, udpipe, optimal_topics = args
        topics_text = ThemsText(files, udpipe, optimal_topics)
        view_str, _ = topics_text.view_thems()
        return view_str
