import typing as t

import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.models.common.text_files import TextFilesModel
from gui.widgets import style
from gui.widgets.common.checkable_list import CheckableList


class TextFilesList(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [others]

        model = TextFilesModel()

        # dialogs

        dialog_add_text = qw.QFileDialog(self)
        dialog_add_text.setFileMode(qw.QFileDialog.ExistingFiles)
        dialog_add_text.setWindowTitle('Выберите файлы с текстом')
        dialog_add_text.setNameFilters(
            ['Текст (*.txt)', 'Все файлы (*.*)']
        )

        # widgets

        # files tool
        files_tb = qw.QToolBar('Управление файлами')
        files_tb.setIconSize(qc.QSize(16, 16))

        add_act = qw.QAction(style.icons.file_plus, 'Добавить файл', files_tb)
        delete_act = qw.QAction(style.icons.file_minus, 'Удалить файл', files_tb)
        show_path_act = qw.QAction(style.icons.code, 'Показать полный путь', files_tb)
        show_path_act.setCheckable(True)
        clear_act = qw.QAction(style.icons.x, 'Очистить список', files_tb)

        files_tb.addAction(add_act)
        files_tb.addAction(delete_act)
        files_tb.addSeparator()
        files_tb.addAction(show_path_act)
        files_tb.addSeparator()
        files_tb.addAction(clear_act)

        files_chl = CheckableList()
        order_tb = files_chl.toolbar

        up_act = qw.QAction(style.icons.arrow_up, 'Переместить выше', order_tb)
        down_act = qw.QAction(style.icons.arrow_down, 'Переместить вниз', order_tb)

        first_act = order_tb.actions()[0]
        order_tb.insertAction(first_act, up_act)
        order_tb.insertAction(first_act, down_act)
        order_tb.insertSeparator(first_act)

        # [connections]

        add_act.triggered.connect(self._on_add_file)
        delete_act.triggered.connect(self._on_remove_file)
        show_path_act.triggered.connect(self._on_show_path)
        clear_act.triggered.connect(self._on_clear)
        up_act.triggered.connect(self._on_move_up)
        down_act.triggered.connect(self._on_move_down)

        # layout

        vbox = qw.QVBoxLayout()
        vbox.addWidget(files_tb)
        vbox.addWidget(files_chl)
        self.setLayout(vbox)

        # fields

        self.dialog_add_text = dialog_add_text

        self._model = model
        self._files_chl = files_chl

    @property
    def model(self) -> TextFilesModel:
        return self._model

    @model.setter
    def model(self, value: TextFilesModel):
        self._model = value
        self._files_chl.model = value

    def _selected_index(self) -> qc.QModelIndex:
        indexes = self._files_chl.list_view.selectedIndexes()
        if not indexes:
            return qc.QModelIndex()
        return indexes[0]

    def _on_add_file(self):
        if self.dialog_add_text.exec_():
            files = self.dialog_add_text.selectedFiles()
            self._model.append(files)

    def _on_remove_file(self):
        indexes: t.List[qc.QModelIndex] = self._files_chl.list_view.selectedIndexes()
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

    def _on_move_up(self):
        idx = self._selected_index()
        self._model.move_up(idx)

    def _on_move_down(self):
        idx = self._selected_index()
        self._model.move_down(idx)
