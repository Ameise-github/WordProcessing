import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
import PySide2.QtWebEngineWidgets as qweb
from PySide2.QtCore import Qt as qq

from gui.logic.morphology_syntax.thread import MorphSyntaxThread, DataType
from gui.models.morphology_syntax.morphology import MorphologyModel
from gui.widgets.common.process_dialog import BaseProcessDialog


class MorphSyntaxDialog(BaseProcessDialog):
    def __init__(self,
                 nltk: pl.Path, udpipe: pl.Path, text: pl.Path, rus: bool,
                 parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = MorphologyModel()
        thread = MorphSyntaxThread(nltk, udpipe, text, rus)

        # widget

        morph_tv = qw.QTableView()
        morph_tv.setModel(model)
        morph_tv.setSelectionMode(morph_tv.SelectionMode.SingleSelection)

        syntax_wv = qweb.QWebEngineView()

        syntax_frame = qw.QFrame()
        syntax_frame.setFrameShape(qw.QFrame.StyledPanel)

        tabs = qw.QTabWidget()
        tabs.addTab(morph_tv, 'Морфология')
        tabs.addTab(syntax_frame, 'Синтаксис')

        # connect

        thread.process_finished.connect(self._on_process_finished)
        thread.process_error.connect(self._on_process_error)

        syntax_wv.loadProgress.connect(self._on_load_progress)
        syntax_wv.loadFinished.connect(self._on_load_finished)

        # layout

        wv_vbox = qw.QVBoxLayout()
        wv_vbox.setMargin(0)
        wv_vbox.addWidget(syntax_wv)
        syntax_frame.setLayout(wv_vbox)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(tabs)
        self.content_layout = vbox

        # fields

        self._model = model
        self._thread = thread
        self._syntax_wv = syntax_wv

        self._morph_progress = 0

        # setup

        self.setWindowTitle('Морфология и Синтаксис')
        self.progress_bar.setMaximum(200)  # Morph and Syntax

    def on_show(self):
        self._thread.start()

    def on_abort(self) -> bool:
        if self._thread.isRunning():
            self._thread.terminate()
            self._thread.wait()
        else:
            self._syntax_wv.stop()
        return True

    def _on_process_finished(self, data: DataType, result: t.Union[str, list]):
        if not self.is_aborted:
            if data is DataType.MORPHOLOGY:
                self._model.set_source(result)
                self._morph_progress = 100
                self.progress_value += 100
            elif data is DataType.SYNTAX:
                self._syntax_wv.setHtml(result)
        else:
            self.finish_him()

    def _on_process_error(self, data: DataType, text: str):
        qw.QMessageBox.critical(self, 'Ошибка', text)

    def _on_load_progress(self, progress: int):
        self.progress_value = self._morph_progress + progress

    def _on_load_finished(self, ok: bool):
        self.finish_him()
