import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

import gui.widgets.notification_server as ns
from gui.widgets import style
from gui.widgets.common.setup import BaseSetup
from gui.widgets.common.note_button import NoteButton


class AnalysisWidget(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # widget

        tabs = qw.QTabWidget()
        note_btn = NoteButton(ns.global_server)
        button = qw.QPushButton(style.icons.play_circle, 'null')

        # connect

        tabs.currentChanged.connect(self._on_tab_changed)
        button.clicked.connect(self._on_button_clicked)

        # layout

        hbox = qw.QHBoxLayout()
        hbox.addWidget(note_btn, 1)
        hbox.addWidget(button, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.setMargin(0)
        vbox.addWidget(tabs, 1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # field

        self._tabs = tabs
        self._button = button

    def add_setup(self, widget: BaseSetup):
        self._tabs.addTab(widget, widget.name)

    def _on_tab_changed(self, index: int):
        setup_w: BaseSetup = self._tabs.widget(index)
        self._button.setText(setup_w.action_text)

    def _on_button_clicked(self):
        setup_w: BaseSetup = self._tabs.currentWidget()
        setup_w.analysis()
