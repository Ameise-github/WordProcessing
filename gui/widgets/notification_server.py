import typing as t

import PySide2.QtCore as qc


class NotificationServer(qc.QObject):
    notified = qc.Signal(str)
    cleared = qc.Signal()

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

    def notify(self, text: str):
        self.notified.emit(text)

    def clear(self):
        self.cleared.emit()


global_server = NotificationServer()
"""Общий сервер уведомлений"""
