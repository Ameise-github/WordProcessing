import typing as t

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.roles import Roles
from gui.models.texts import TextsModel
from gui.widgets import style


class TextManager(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other
        model = TextsModel()

        toolbar_style = qw.QStyleOptionToolBar()

        # dialogs

        dialog_add_text = qw.QFileDialog(self)
        dialog_add_text.setFileMode(qw.QFileDialog.ExistingFiles)
        dialog_add_text.setWindowTitle('Выберите файлы с текстом')
        dialog_add_text.setNameFilters(
            ['Текст (*.txt)', 'Все файлы (*.*)']
        )

        # widgets

        toolbar = qw.QToolBar('Действия над списком')
        toolbar.setOrientation(qq.Vertical)
        # toolbar.setIconSize(qc.QSize(16, 16))

        add_act = qw.QAction(style.icons.file_plus, 'Добавить файл', toolbar)
        delete_act = qw.QAction(style.icons.file_minus, 'Удалить файл', toolbar)
        show_path_act = qw.QAction(style.icons.code, 'Показать полный путь', toolbar)
        show_path_act.setCheckable(True)
        clear_act = qw.QAction(style.icons.x_circle, 'Очистить список', toolbar)

        toolbar.addAction(add_act)
        toolbar.addAction(delete_act)
        toolbar.addSeparator()
        toolbar.addAction(show_path_act)
        toolbar.addSeparator()
        toolbar.addAction(clear_act)

        files_lv = qw.QListView()
        files_lv.setModel(model)

        ref_btn = qw.QPushButton('Выбрать эталонным')
        ref_btn.setIcon(qg.QIcon.fromTheme('go-up'))

        # connections

        add_act.triggered.connect(self._on_add_file)
        delete_act.triggered.connect(self._on_remove_file)
        show_path_act.triggered.connect(self._on_show_path)
        clear_act.triggered.connect(self._on_clear)

        ref_btn.clicked.connect(self._on_assign_ref)

        # layout

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_btn)
        ref_hbox.addStretch(1)

        hbox = qw.QHBoxLayout()
        hbox.addWidget(files_lv, 1)
        hbox.addWidget(toolbar)

        vbox = qw.QVBoxLayout()
        vbox.setMargin(0)
        vbox.addLayout(hbox)
        vbox.addLayout(ref_hbox)

        # fields

        self.dialog_add_text = dialog_add_text

        self._model = model

        self.files_lv = files_lv

        # setup

        self.setLayout(vbox)

    @property
    def model(self) -> TextsModel:
        return self._model

    @model.setter
    def model(self, value: TextsModel):
        self._model = value
        self.files_lv.setModel(value)

    def _on_add_file(self):
        if self.dialog_add_text.exec_():
            files = self.dialog_add_text.selectedFiles()
            for f in files:
                self._model.append_file(f)

    def _on_remove_file(self):
        indexes: t.List[qc.QModelIndex] = self.files_lv.selectedIndexes()
        for idx in indexes:
            self._model.removeRows(idx.row(), 1)

    def _on_show_path(self, checked: bool):
        self._model.show_paths = checked

    def _on_clear(self):
        if self._model.rowCount() <= 0:
            return
        res = qw.QMessageBox.question(self, 'Очистка списка', 'Очистить список файлов?')
        if res == qw.QMessageBox.Yes:
            self._model.clear()

    def _on_assign_ref(self):
        indexes: t.List[qc.QModelIndex] = self.files_lv.selectedIndexes()
        for idx in indexes:
            file = self._model.data(idx, Roles.SourceDataRole)
            self._model.ref_file = file
