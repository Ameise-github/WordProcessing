import sys
import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.logic.pragmatic_adequacy.thread import PragmaticAdequacyThread, PragmaticAdequacyData
from gui.models.pragmatic_adequacy.process import PragmaticAdequacyProcessModel, PragmaticAdequacyResult
from gui.widgets.common.process_dialog import BaseProcessDialog


class PragmaticAdequacyWindow(BaseProcessDialog):
    def __init__(self,
                 udpipe: t.Optional[pl.Path], text_files: t.List[pl.Path],
                 interlace: t.List[pl.Path], direction: int,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [other]

        model = PragmaticAdequacyProcessModel()
        thread = PragmaticAdequacyThread(udpipe, text_files, interlace, direction)

        # [widgets]

        result_tv = qw.QTableView()
        result_tv.setModel(model)
        result_tv.setSelectionMode(result_tv.SelectionMode.SingleSelection)

        hh = result_tv.horizontalHeader()
        hh.setSectionResizeMode(qw.QHeaderView.ResizeMode.Fixed)
        hh.setDefaultSectionSize(40)

        vh = result_tv.verticalHeader()
        vh.setSectionResizeMode(qw.QHeaderView.ResizeMode.Fixed)
        vh.setMinimumSectionSize(40)

        # [connect]

        thread.prepared.connect(self._on_prepared)
        thread.process_started.connect(self._on_process_started)
        thread.process_finished.connect(self._on_process_finished)
        thread.process_error.connect(self._on_process_error)
        thread.finished.connect(self._on_finished)

        # [layout]

        vbox = qw.QVBoxLayout()
        vbox.addWidget(result_tv)
        self.content_layout = vbox

        # [fields]

        self._thread = thread
        self._model = model
        self._text_files = text_files

        # [setup]

        self.setWindowTitle('Сравнение')
        self.progress_bar.setFormat('  %v из %m')

    def on_show(self):
        self._thread.start()

    def on_abort(self) -> bool:
        self._thread.abort()
        return True

    def _increment_progress(self, inc=1):
        value = self.progress_bar.value() + inc
        self.progress_bar.setValue(value)

    def _on_prepared(self, combinations: t.List[PragmaticAdequacyData]):
        self._model.set_source(self._text_files, combinations)
        self.progress_bar.setMaximum(len(combinations))
        self.update()

    def _on_process_started(self, data: PragmaticAdequacyData):
        self._model.assign_result(
            data.one, data.two,
            PragmaticAdequacyResult(PragmaticAdequacyResult.WORKING)
        )

    def _on_process_finished(self, data: PragmaticAdequacyData, result: float):
        self._model.assign_result(
            data.one, data.two,
            PragmaticAdequacyResult(PragmaticAdequacyResult.SUCCESS, result)
        )
        self._increment_progress()

    def _on_process_error(self, data: PragmaticAdequacyData, text: str):
        print(f'[ERROR] {data.one} => [{data.two}] => {text}', file=sys.stderr, flush=True)
        self._model.assign_result(
            data.one, data.two,
            PragmaticAdequacyResult(PragmaticAdequacyResult.ERROR, text)
        )
        self._increment_progress()

    def _on_finished(self):
        self.finish_him()
