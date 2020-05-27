import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
import PySide2.QtWebEngineWidgets as qweb
from PySide2.QtCore import Qt as qq

from gui.logic.topics_definition.thread import TopicsDefinitionThread
from gui.models.topics_definition.topics import TopicDefinitionModel
from gui.widgets.common.process_dialog import BaseProcessDialog


class TopicsDefinitionDialog(BaseProcessDialog):
    def __init__(self,
                 files: t.List[pl.Path], udpipe: pl.Path, optimal_topics: bool,
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = TopicDefinitionModel()
        thread = TopicsDefinitionThread(files, udpipe, optimal_topics)

        # widget

        webview = qweb.QWebEngineView()

        frame = qw.QFrame()
        frame.setFrameShape(qw.QFrame.StyledPanel)

        table_tv = qw.QTableView()
        table_tv.setModel(model)

        splitter = qw.QSplitter(qq.Horizontal)
        splitter.addWidget(frame)
        splitter.addWidget(table_tv)
        splitter.setOpaqueResize(False)
        splitter.setSizes([999999, 999999])

        # connect

        thread.process_finished.connect(self._on_process_finished)
        thread.process_error.connect(self._on_process_error)

        webview.loadStarted.connect(self._on_load_started)
        webview.loadProgress.connect(self._on_load_progress)
        webview.loadFinished.connect(self._on_load_finished)

        # layout

        wv_vbox = qw.QVBoxLayout()
        wv_vbox.setMargin(0)
        wv_vbox.addWidget(webview)
        frame.setLayout(wv_vbox)

        hbox = qw.QHBoxLayout()
        hbox.addWidget(splitter)
        self.content_layout = hbox

        # fields
        self._model = model
        self._thread = thread

        self._webview = webview

        # setup

        self.setWindowTitle('Определение тематики')
        self.progress_bar.setRange(0, 0)
        self._thread.start()

    def on_abort(self) -> bool:
        if self._thread.isRunning():
            self._thread.terminate()
            self._thread.wait()
        else:
            self._webview.stop()
        return True

    def _on_process_finished(self, data: None, result: str):
        if not self.is_aborted:
            html, table = result
            self._model.set_source(table)
            self._webview.setHtml(html)
        else:
            self.finish_him()

    def _on_process_error(self, data: None, text: str):
        qw.QMessageBox.critical(self, 'Ошибка', text)
        self.abort()

    def _on_load_started(self):
        self.progress_bar.setMaximum(100)

    def _on_load_progress(self, progress: int):
        self.progress_bar.setValue(progress)

    def _on_load_finished(self, ok: bool):
        self.finish_him()
