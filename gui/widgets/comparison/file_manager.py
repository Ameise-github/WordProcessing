import typing as t
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from gui.models.comparison import ComparisonFilesModel
from gui.models import Roles


class FileManager(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models
        model = ComparisonFilesModel()

        # dialogs

        dialog_add_text = qw.QFileDialog(self)
        dialog_add_text.setFileMode(qw.QFileDialog.ExistingFiles)
        dialog_add_text.setWindowTitle('Выберите файлы с текстом')
        dialog_add_text.setNameFilters(
            ['Текст (*.txt)', 'Все файлы (*.*)']
        )

        # widgets

        files_lv = qw.QListView()
        files_lv.setModel(model)

        add_btn = qw.QPushButton('Добавить...')
        add_btn.setIcon(qg.QIcon.fromTheme('list-add'))
        delete_btn = qw.QPushButton('Удалить')
        delete_btn.setIcon(qg.QIcon.fromTheme('list-remove'))
        show_path_cbx = qw.QCheckBox('Показать полный путь')
        clear_btn = qw.QPushButton('Очистить')
        clear_btn.setIcon(qg.QIcon.fromTheme('edit-clear'))

        ref_btn = qw.QPushButton('Выбрать эталонным')
        ref_btn.setIcon(qg.QIcon.fromTheme('go-up'))

        # connections

        add_btn.clicked.connect(self._on_add_file)
        delete_btn.clicked.connect(self._on_remove_file)
        show_path_cbx.clicked.connect(self._on_show_path)
        clear_btn.clicked.connect(self._on_clear)
        ref_btn.clicked.connect(self._on_assign_ref)

        # layout

        files_ctl_hbox = qw.QHBoxLayout()
        files_ctl_hbox.addWidget(add_btn)
        files_ctl_hbox.addWidget(delete_btn)
        files_ctl_hbox.addWidget(show_path_cbx)
        files_ctl_hbox.addStretch(1)
        files_ctl_hbox.addWidget(clear_btn)

        ref_hbox = qw.QHBoxLayout()
        ref_hbox.addWidget(ref_btn)
        ref_hbox.addStretch(1)

        vbox = qw.QVBoxLayout()
        vbox.setMargin(0)
        vbox.addLayout(files_ctl_hbox)
        vbox.addWidget(files_lv, 1)
        vbox.addLayout(ref_hbox)

        # fields

        self.dialog_add_text = dialog_add_text

        self._model = model

        self.files_lv = files_lv
        self.show_path_cbx = show_path_cbx

        # setup

        self.setLayout(vbox)

    @property
    def model(self) -> ComparisonFilesModel:
        return self._model

    @model.setter
    def model(self, value: ComparisonFilesModel):
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

    def _on_show_path(self):
        self._model.show_paths = self.show_path_cbx.isChecked()

    def _on_clear(self):
        if self._model.rowCount() <= 0:
            return
        res = qw.QMessageBox.question(self, 'Очистка списка', 'Очистить список файлов?')
        if res == qw.QMessageBox.Yes:
            self._model.clear()

    def _on_assign_ref(self):
        indexes: t.List[qc.QModelIndex] = self.files_lv.selectedIndexes()
        for idx in indexes:
            file = self._model.data(idx, Roles.DataKeyRole)
            self._model.ref_file = file
