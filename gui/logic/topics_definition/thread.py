import typing as t
import pathlib as pl
import multiprocessing as mp
import multiprocessing.connection as mpc

import PySide2.QtCore as qc

from parsing.ThemsText import ThemsText
from gui.models.common.udpipe import UDPipeFile


class TopicsDefinitionThread(qc.QThread):
    error = qc.Signal(str)

    def __init__(self, files: t.List[pl.Path], udpipe: UDPipeFile, optimal_topics: bool,
                 parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._pool = mp.Pool()

        self._files = files
        self._udpipe = udpipe
        self._optimal_topics = optimal_topics

        self._content = None

    def run(self):
        files = list(map(str, self._files))
        udpipe = str(self._udpipe.path)

        try:
            receiver, sender = mp.Pipe()
            process = mp.Process(
                target=self._worker,
                args=(files, udpipe, self._optimal_topics, sender),
                daemon=False
            )
            process.start()
            self._content = receiver.recv()
            process.join()

        except BaseException as e:
            self._content = 'Error'
            self.error.emit(e.args[0])

    @property
    def content(self) -> str:
        return self._content

    @staticmethod
    def _define_topics(text_list: t.List[str], udpipe: str, optimal_topics: bool) -> str:
        topics_text = ThemsText(text_list, udpipe, optimal_topics)
        view_str, _ = topics_text.view_thems()
        return view_str

    @staticmethod
    def _worker(text_list: t.List[str], udpipe: str, optimal_topics: bool, sender: mpc.PipeConnection) -> None:
        result = TopicsDefinitionThread._define_topics(text_list, udpipe, optimal_topics)
        sender.send(result)
