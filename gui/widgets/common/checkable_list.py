import typing as t

import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.checkable import BaseCheckableModel
from gui.widgets import style


class CheckableList(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [other]

        model = BaseCheckableModel()

        # [widgets]

        check_tb = qw.QToolBar()
        check_tb.setOrientation(qq.Vertical)
        check_tb.setIconSize(qc.QSize(16, 16))

        check_act = qw.QAction(style.icons.check_square, 'Выбрать все', check_tb)
        uncheck_act = qw.QAction(style.icons.square, 'Отменить все', check_tb)
        invert_act = qw.QAction(style.icons.refresh_cw, 'Инвертировать', check_tb)

        check_tb.addAction(check_act)
        check_tb.addAction(uncheck_act)
        check_tb.addAction(invert_act)

        items_lv = qw.QListView()
        items_lv.setModel(model)

        # [connections]

        check_act.triggered.connect(self._on_check_all)
        uncheck_act.triggered.connect(self._on_uncheck_all)
        invert_act.triggered.connect(self._on_invert)

        # [layout]

        hbox = qw.QHBoxLayout()
        hbox.setMargin(0)
        hbox.addWidget(items_lv, 1)
        hbox.addWidget(check_tb)
        self.setLayout(hbox)

        # [fields]

        self._model = model
        self._check_tb = check_tb
        self._items_lv = items_lv

    def _on_check_all(self):
        self._model.check_all()

    def _on_uncheck_all(self):
        self._model.uncheck_all()

    def _on_invert(self):
        self._model.invert()

    @property
    def model(self) -> BaseCheckableModel:
        return self._model

    @model.setter
    def model(self, value: BaseCheckableModel):
        self._model = value
        self._items_lv.setModel(value)

    @property
    def toolbar(self):
        return self._check_tb

    @property
    def list_view(self):
        return self._items_lv
