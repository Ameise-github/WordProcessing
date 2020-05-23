import typing as t
import pathlib as pl

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
import PySide2.QtWebEngineWidgets as qweb
from PySide2.QtCore import Qt as qq

from gui.logic.topics_definition.thread import TopicsDefinitionThread
from gui.models.common.udpipe import UDPipeFile


class TopicsDefinitionWindow(qw.QDialog):
    def __init__(self,
                 files: t.List[pl.Path], udpipe: UDPipeFile, optimal_topics: bool,
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        f |= qq.WindowMaximizeButtonHint | qq.WindowMinimizeButtonHint | qq.WindowCloseButtonHint
        f &= ~qq.WindowContextHelpButtonHint
        super().__init__(parent, f)

        # other

        thread = TopicsDefinitionThread(files, udpipe, optimal_topics)

        # widget

        webview = qweb.QWebEngineView()

        progress_pb = qw.QProgressBar()
        progress_pb.setMaximum(0)
        progress_pb.setMinimum(0)
        progress_pb.setTextVisible(False)

        # connect

        thread.error.connect(self._on_error)
        thread.finished.connect(self._on_finished)

        webview.loadStarted.connect(self._on_load_started)
        webview.loadProgress.connect(self._on_load_progress)
        webview.loadFinished.connect(self._on_load_finished)

        # layout

        vbox = qw.QVBoxLayout()
        vbox.addWidget(webview)
        vbox.addWidget(progress_pb)
        self.setLayout(vbox)

        # fields

        self._thread = thread

        self.webview = webview
        self.progress_pb = progress_pb

        # setup

        self.setMinimumSize(500, 500)
        self.setWindowTitle('Определение тематики')

    def showEvent(self, event: qg.QShowEvent):
        self._thread.start()

    def closeEvent(self, event: qg.QCloseEvent):
        if self._thread.isRunning():
            result = qw.QMessageBox.question(self, 'Отмена операции', 'Прервать операцию?')
            if qw.QMessageBox.Yes == result:
                self._thread.terminate()
                self._thread.wait()
            else:
                event.ignore()

        event.accept()

    def _on_error(self, msg: str):
        qw.QMessageBox.critical(self, 'Ошибка', msg)
        self.close()

    def _on_finished(self):
        self.webview.setHtml(self._thread.content)

    def _on_load_started(self):
        self.progress_pb.setMaximum(100)

    def _on_load_progress(self, progress: int):
        self.progress_pb.setValue(progress)

    def _on_load_finished(self, ok: bool):
        self.progress_pb.setVisible(False)
