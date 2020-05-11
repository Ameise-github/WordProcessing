import typing as t
import pathlib as pl

import PySide2
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from parsing.metric import BaseAlgorithm
from gui.logic.comparison import ComparisonCombinator, ComparisionThread


class ComparisonProcess(qw.QDialog):
    def __init__(self, combinator: ComparisonCombinator,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other

        thread = ComparisionThread(combinator, self)

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel(str(combinator.reference))

        result_tv = qw.QTableView()

        process_pb = qw.QProgressBar()
        process_pb.setMinimum(0)
        process_pb.setMaximum(combinator.total())
        process_pb.setValue(0)
        process_pb.setFormat('  %v из %m')

        stop_btn = qw.QPushButton('Остановить')
        done_btn = qw.QPushButton('Готово')
        done_btn.setVisible(False)

        # connect

        thread.processed.connect(self.on_processed)
        thread.error.connect(self.on_error)
        thread.finished.connect(self.on_finished)
        stop_btn.clicked.connect(self.on_stop_clicked)
        done_btn.clicked.connect(self.on_done_clicked)

        # layout

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_lbl)
        ref_hbox.addWidget(ref_value_lbl, 1)

        bottom_hbox = qw.QHBoxLayout()
        bottom_hbox.addStretch(1)
        bottom_hbox.addWidget(stop_btn, 0, qq.AlignRight)
        bottom_hbox.addWidget(done_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addLayout(ref_hbox)
        vbox.addWidget(result_tv)
        vbox.addWidget(process_pb)
        vbox.addLayout(bottom_hbox)

        # fields

        self.thread = thread
        self.process_pb = process_pb
        self.stop_btn = stop_btn
        self.done_btn = done_btn

        # setup

        self.setMinimumWidth(650)
        self.setWindowTitle('Сравнение')
        self.setLayout(vbox)

    def showEvent(self, event: qg.QShowEvent):
        self.thread.start()
        super().showEvent(event)

    def closeEvent(self, event: qg.QCloseEvent):
        if self.thread.isRunning():
            qw.QMessageBox.warning(self, '', 'Выполняется процесс сравнения')
            event.ignore()
        else:
            event.accept()

    def on_processed(self, alg: BaseAlgorithm, other: pl.Path, result: int):
        value = self.process_pb.value() + 1
        self.process_pb.setValue(value)
        print(f'{other} => [{alg}] => {result}')

    def on_error(self, alg: BaseAlgorithm, other: pl.Path, text: str):
        value = self.process_pb.value() + 1
        self.process_pb.setValue(value)
        print(f'{other} ==[ERROR]=> [{alg}] => {text}')

    def on_finished(self):
        self.stop_btn.setVisible(False)
        self.done_btn.setVisible(True)

    def on_stop_clicked(self):
        self.stop_btn.setEnabled(False)
        self.thread.terminate()

    def on_done_clicked(self):
        self.close()




