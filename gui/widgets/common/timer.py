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

        timer.timeout.connect(self.on_timeout)

        self._timer = timer
        self._elapsed = qc.QTime(0, 0)

        self.setText(self._elapsed.toString(_FORMAT))

    @property
    def interval(self):
        return self._timer.interval()

    @interval.setter
    def interval(self, msec: int):
        self._timer.setInterval(msec)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def on_timeout(self):
        self._elapsed = self._elapsed.addMSecs(self._timer.interval())
        self.setText(self._elapsed.toString(_FORMAT))
