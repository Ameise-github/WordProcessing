import typing as t
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq


class ComparisonProcess(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models

        # widgets

        ref_lbl = qw.QLabel('Эталонный текст:')
        ref_value_lbl = qw.QLabel('файл')

        result_tv = qw.QTableView()

        process_lbl = qw.QLabel('Выполнение:')
        process_value_lbl = qw.QLabel('описание операции')

        process_pb = qw.QProgressBar()
        process_pb.setValue(75)

        stop_btn = qw.QPushButton('Остановить')
        done_btn = qw.QPushButton('Готово')

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

        # setup

        self.setWindowTitle('Сравнение')
        self.setLayout(vbox)

    def closeEvent(self, event: qg.QCloseEvent):
        # TODO завершение потока выполнения
        super().closeEvent(event)
