import sys
import typing as t
import pathlib as pl

import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from parsing.metric.base import BaseAlgorithm
from gui.logic.comparison.combinator import ComparisonCombinator
from gui.logic.comparison.thread import ComparisionThread
from gui.models.process import ComparisonProcessModel
from gui.widgets.common.timer import TimerLabel
from gui.widgets.common.hseparator import HSeparator


class ComparisonProcess(qw.QDialog):
    def __init__(self, combinator: ComparisonCombinator,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        model = ComparisonProcessModel(combinator)
        thread = ComparisionThread(model, self)

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel(str(combinator.reference))

        result_tv = qw.QTableView()
        result_tv.setModel(model)
        result_tv.setSelectionMode(result_tv.SelectionMode.SingleSelection)

        timer_lbl = TimerLabel()
        timer_lbl.interval = 500

        process_pb = qw.QProgressBar()
        process_pb.setMinimum(0)
        process_pb.setMaximum(combinator.total())
        process_pb.setValue(0)
        process_pb.setFormat('  %v из %m')

        separator_hs = HSeparator()

        stop_btn = qw.QPushButton('Остановить')
        done_btn = qw.QPushButton('Готово')
        done_btn.setVisible(False)

        # connect

        thread.process_finished.connect(self.on_process_finished)
        thread.error.connect(self.on_error)
        thread.finished.connect(self.on_finished)
        stop_btn.clicked.connect(self.on_stop_clicked)
        done_btn.clicked.connect(self.on_done_clicked)

        # layout

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_lbl)
        ref_hbox.addWidget(ref_value_lbl, 1)

        progress_hbox = qw.QHBoxLayout()
        progress_hbox.addWidget(timer_lbl)
        progress_hbox.addWidget(process_pb, 1)

        bottom_hbox = qw.QHBoxLayout()
        bottom_hbox.addStretch(1)
        bottom_hbox.addWidget(stop_btn, 0, qq.AlignRight)
        bottom_hbox.addWidget(done_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(ref_hbox)
        vbox.addWidget(result_tv)
        vbox.addLayout(progress_hbox)
        vbox.addWidget(separator_hs)
        vbox.addLayout(bottom_hbox)

        # fields

        self.thread = thread
        self.timer_lbl = timer_lbl
        self.process_pb = process_pb
        self.stop_btn = stop_btn
        self.done_btn = done_btn

        self._schedule_close = False  # плановое закрытие окна после отмены операции

        # setup

        self.setMinimumWidth(650)
        self.setWindowTitle('Сравнение')
        self.setLayout(vbox)

    def increment_progress(self, inc=1):
        value = self.process_pb.value() + inc
        self.process_pb.setValue(value)

    def showEvent(self, event: qg.QShowEvent):
        self.timer_lbl.start()
        self.thread.start()

    def closeEvent(self, event: qg.QCloseEvent):
        if self.thread.isRunning():
            result = qw.QMessageBox.question(self, 'Отмена операции', 'Прервать сравнение?')
            if qw.QMessageBox.Yes == result:
                self.on_stop_clicked()
            else:
                event.ignore()

        event.accept()

    def on_process_finished(self, alg: BaseAlgorithm, other: pl.Path, result: int):
        self.increment_progress()

    def on_error(self, alg: BaseAlgorithm, other: pl.Path, text: str):
        self.increment_progress()
        print(f'[ERROR] {other} => [{alg}] => {text}', file=sys.stderr, flush=True)

    def on_finished(self):
        self.timer_lbl.stop()
        self.stop_btn.setVisible(False)
        self.done_btn.setVisible(True)

    def on_stop_clicked(self):
        self.stop_btn.setEnabled(False)
        self.thread.terminate()

    def on_done_clicked(self):
        self.close()
