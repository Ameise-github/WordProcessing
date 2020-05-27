import typing as t
import pathlib as pl

import PySide2.QtCore as qc

from parsing.ThemsText import ThemsText
from gui.logic.common.pool_tread import BasePoolThread, Combination
from gui.models.common.file_path import FilePath


class TopicsDefinitionThread(BasePoolThread):
    def __init__(self, files: t.List[pl.Path], udpipe: pl.Path, optimal_topics: bool,
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
        view_str, lda_model = topics_text.view_thems()
        list_topics_doc = topics_text.topics_document(lda_model)
        return view_str, list_topics_doc
