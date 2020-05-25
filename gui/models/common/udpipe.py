import typing as t
import pathlib as pl

import PySide2.QtCore as qc

OptPath = t.Optional[pl.Path]


class UDPipeFile(qc.QObject):
    path_changed = qc.Signal(pl.Path, pl.Path)

    def __init__(self, path=pl.Path(), parent: qc.QObject = None):
        super(UDPipeFile, self).__init__(parent)

        self._path = path

    @property
    def path(self) -> OptPath:
        return self._path

    @path.setter
    def path(self, value: OptPath):
        old = self._path
        self._path = value
        self.path_changed.emit(old, value)

    def __str__(self):
        return str(self._path)
