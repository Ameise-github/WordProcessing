import typing as t
import pathlib as pl

import PySide2
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from parsing.metric import BaseMetricAnalysis
from gui.logic.comparison import ComparisonCombinator, ComparisonWorker


class ComparisonProcess(qw.QDialog):
    def __init__(self, combinator: ComparisonCombinator,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        worker = ComparisonWorker(combinator)

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel(str(combinator.reference))

        result_tv = qw.QTableView()

        process_lbl = qw.QLabel('Выполнение:')
        process_value_lbl = qw.QLabel('подготовка')

        process_pb = qw.QProgressBar()
        process_pb.setMinimum(0)
        process_pb.setMaximum(0)
        process_pb.setFormat('   %v из %m')

        stop_btn = qw.QPushButton('Остановить')
        done_btn = qw.QPushButton('Готово')
        done_btn.setVisible(False)

        # connect

        worker.comparator.begin.connect(self.on_begin)
        worker.comparator.processing.connect(self.on_processing)
        worker.comparator.processed.connect(self.on_processed)
        worker.comparator.end.connect(self.on_end)
        worker.finished.connect(self.on_finished)
        stop_btn.clicked.connect(self.on_stop_clicked)
        done_btn.clicked.connect(self.on_done_clicked)

        # layout

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_lbl)
        ref_hbox.addWidget(ref_value_lbl, 1)

        process_hbox = qw.QHBoxLayout()
        process_hbox.addWidget(process_lbl)
        process_hbox.addWidget(process_value_lbl, 1)

        bottom_hbox = qw.QHBoxLayout()
        bottom_hbox.addStretch(1)
        bottom_hbox.addWidget(stop_btn, 0, qq.AlignRight)
        bottom_hbox.addWidget(done_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(ref_hbox)
        vbox.addWidget(result_tv)
        vbox.addWidget(process_lbl)
        vbox.addWidget(process_value_lbl)
        vbox.addWidget(process_pb)
        vbox.addLayout(bottom_hbox)

        # fields

        self.worker = worker
        self.process_pb = process_pb
        self.process_value_lbl = process_value_lbl
        self.stop_btn = stop_btn
        self.done_btn = done_btn

        # setup

        self.setMinimumWidth(650)
        self.setWindowTitle('Сравнение')
        self.setLayout(vbox)

    def showEvent(self, event: qg.QShowEvent):
        self.worker.run()
        super().showEvent(event)

    def closeEvent(self, event: qg.QCloseEvent):
        if self.worker.is_running():
            qw.QMessageBox.warning(self, '', 'Остановите процесс сравнения')
            event.ignore()
        else:
            event.accept()

    def on_begin(self):
        self.process_pb.setMaximum(self.worker.comparator.combinator.total())

    def on_processing(self, alg: BaseMetricAnalysis, file: pl.Path, number: int):
        self.process_value_lbl.setText(f'{alg.name}\n{file}')

    def on_processed(self, alg: BaseMetricAnalysis, file: pl.Path, number: int):
        self.process_pb.setValue(number)

    def on_end(self):
        self.stop_btn.setEnabled(False)

    def on_finished(self):
        self.stop_btn.setVisible(False)
        self.done_btn.setVisible(True)

    def on_stop_clicked(self):
        self.stop_btn.setEnabled(False)
        self.worker.stop()

    def on_done_clicked(self):
        self.close()




