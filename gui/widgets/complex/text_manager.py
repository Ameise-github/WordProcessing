import typing as t

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.roles import Roles
from gui.models.text_files import TextFilesModel
from gui.widgets import style


class TextManager(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # other
        model = TextFilesModel()

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

        # connections

        add_act.triggered.connect(self._on_add_file)
        delete_act.triggered.connect(self._on_remove_file)
        show_path_act.triggered.connect(self._on_show_path)
        clear_act.triggered.connect(self._on_clear)

        # layout
        hbox = qw.QHBoxLayout()
        hbox.setMargin(0)
        hbox.addWidget(files_lv, 1)
        hbox.addWidget(toolbar)
        self.setLayout(hbox)

        # fields

        self.dialog_add_text = dialog_add_text
        self._model = model
        self.files_lv = files_lv

    @property
    def model(self) -> TextFilesModel:
        return self._model

    @model.setter
    def model(self, value: TextFilesModel):
        self._model = value
        self.files_lv.setModel(value)

    def _on_add_file(self):
        if self.dialog_add_text.exec_():
            files = self.dialog_add_text.selectedFiles()
            self._model.append(files)

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
