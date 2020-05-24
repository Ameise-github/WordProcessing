import typing as t

import PySide2.QtCore as qc
from PySide2.QtCore import Qt as qq
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

_FORMAT = 'HH:mm:ss'


class TimerLabel(qw.QLabel):
    def __init__(self, parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        timer = qc.QTimer()

        timer.timeout.connect(self._on_timeout)

        self._timer = timer
        self._elapsed = qc.QTime(0, 0)
        self._work = False

        self.setText(self._elapsed.toString(_FORMAT))

    def get_interval(self):
        return self._timer.interval()

    def set_interval(self, msec: int):
        self._timer.setInterval(msec)

    def is_work(self) -> bool:
        return self._work

    def set_work(self, enabled: bool):
        self._work = enabled
        if enabled:
            self._timer.start()
        else:
            self._timer.stop()

    interval = qc.Property(int, get_interval, set_interval)
    work = qc.Property(bool, is_work, set_work)

    def _on_timeout(self):
        self._elapsed = self._elapsed.addMSecs(self._timer.interval())
        self.setText(self._elapsed.toString(_FORMAT))
