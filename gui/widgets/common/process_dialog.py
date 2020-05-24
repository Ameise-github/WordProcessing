import typing as t

import PySide2
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.widgets.common.timer import TimerLabel
from gui.widgets.common.hseparator import HSeparator


class BaseProcessDialog(qw.QDialog):
    PREPARING = 0
    WORKING = 1
    COMPLETION = 2
    DONE = 3

    aborting = qc.Signal()
    finished = qc.Signal()

    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        f |= qq.WindowMaximizeButtonHint | qq.WindowMinimizeButtonHint
        f &= ~qq.WindowContextHelpButtonHint & ~qq.WindowCloseButtonHint
        super().__init__(parent, f)

        # [widgets]

        content = qw.QWidget()

        timer_tl = TimerLabel()
        timer_tl.set_interval(500)

        process_pb = qw.QProgressBar()

        separator_hs = HSeparator()

        abort_btn = qw.QPushButton('Прервать')
        done_btn = qw.QPushButton('Готово')

        # [connect]

        abort_btn.clicked.connect(self._on_abort_clicked)
        done_btn.clicked.connect(self._on_done_clicked)

        # [states]

        work_state = qc.QState()
        abort_state = qc.QState()
        done_state = qc.QState()

        work_state.addTransition(self.aborting, abort_state)
        work_state.addTransition(self.finished, done_state)
        abort_state.addTransition(self.finished, done_state)

        work_state.assignProperty(process_pb, 'maximum', 0)
        work_state.assignProperty(process_pb, 'value', 0)
        work_state.assignProperty(done_btn, 'visible', False)

        abort_state.assignProperty(process_pb, 'minimum', 0)
        abort_state.assignProperty(process_pb, 'maximum', 0)
        abort_state.assignProperty(process_pb, 'value', 0)
        abort_state.assignProperty(abort_btn, 'enabled', False)

        done_state.assignProperty(timer_tl, 'work', False)
        done_state.assignProperty(process_pb, 'enabled', False)
        done_state.assignProperty(abort_btn, 'visible', False)
        done_state.assignProperty(done_btn, 'visible', True)

        machine = qc.QStateMachine()
        machine.addState(work_state)
        machine.addState(abort_state)
        machine.addState(done_state)
        machine.setInitialState(work_state)

        # [layout]

        progress_hbox = qw.QHBoxLayout()
        progress_hbox.addWidget(timer_tl)
        progress_hbox.addWidget(process_pb, 1)

        bottom_hbox = qw.QHBoxLayout()
        bottom_hbox.addStretch(1)
        bottom_hbox.addWidget(abort_btn, 0, qq.AlignRight)
        bottom_hbox.addWidget(done_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(content, 2)
        vbox.addLayout(progress_hbox)
        vbox.addWidget(separator_hs)
        vbox.addLayout(bottom_hbox)
        self.setLayout(vbox)

        # [fields]

        self._content = content
        self._timer_tl = timer_tl
        self._process_pb = process_pb
        self._cancel_btn = abort_btn
        self._ok_btn = done_btn

        self._machine = machine

        self._aborted = False

        # [setup]

        self.setMinimumSize(500, 500)
        self._machine.start()

    @property
    def progress_bar(self):
        return self._process_pb

    @property
    def content_layout(self) -> qw.QLayout:
        return self._content.layout()

    @content_layout.setter
    def content_layout(self, layout: qw.QLayout):
        layout.setMargin(0)
        self._content.setLayout(layout)

    @property
    def is_aborted(self):
        return self._aborted

    def showEvent(self, arg__1: qg.QShowEvent):
        self._timer_tl.set_work(True)
        self.on_show()

    def on_show(self):
        pass

    def exec_(self, *, hide_parent=True) -> int:
        parent = self.nativeParentWidget()
        if hide_parent:
            parent.hide()
        result = super().exec_()
        if hide_parent:
            parent.show()
        return result

    def abort(self):
        if self.on_abort():
            self._aborted = True
            self.aborting.emit()

    def _on_abort_clicked(self):
        result = qw.QMessageBox.question(self, 'Отмена операции', 'Прервать выполнение операции?')
        if qw.QMessageBox.Yes == result:
            self.abort()

    def on_abort(self) -> bool:
        raise NotImplementedError()

    def finish_him(self):
        self.finished.emit()

    def _on_done_clicked(self):
        self.close()
