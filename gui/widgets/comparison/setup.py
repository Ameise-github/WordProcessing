import typing as t
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from gui.models.comparison import ComparisonFilesModel
from gui.models import Roles


class ComparisonSetupWidget(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qc.Qt.WindowFlags()):
        super().__init__(parent, f)

        # models
        files_model = ComparisonFilesModel()

        # widgets

        files_lw = qw.QListView()
        files_lw.setModel(files_model)

        file_add_btn = qw.QPushButton('Добавить')
        file_add_btn.setMinimumWidth(100)
        file_remove_btn = qw.QPushButton('Удалить')
        file_remove_btn.setMinimumWidth(100)
        files_show_path_cbx = qw.QCheckBox('Показать полный путь')
        files_clear_btn = qw.QPushButton('Очистить')
        files_clear_btn.setMinimumWidth(100)

        ref_file_btn = qw.QPushButton('Выбрать эталонным')

        # connections

        file_add_btn.clicked.connect(self._file_add_act)
        file_remove_btn.clicked.connect(self._file_remove_act)
        files_show_path_cbx.clicked.connect(self._file_show_path_act)
        files_clear_btn.clicked.connect(self._files_clear_act)
        ref_file_btn.clicked.connect(self._ref_file_assign_act)

        # layout

        files_ctl_hbox = qw.QHBoxLayout()
        files_ctl_hbox.addWidget(file_add_btn)
        files_ctl_hbox.addWidget(file_remove_btn)
        files_ctl_hbox.addWidget(files_show_path_cbx)
        files_ctl_hbox.addStretch(1)
        files_ctl_hbox.addWidget(files_clear_btn)

        ref_file_hbox = qw.QHBoxLayout()
        ref_file_hbox.addWidget(ref_file_btn)
        ref_file_hbox.addStretch(1)

        files_vbox = qw.QVBoxLayout()
        files_vbox.addLayout(files_ctl_hbox)
        files_vbox.addWidget(files_lw, 1)
        files_vbox.addLayout(ref_file_hbox)

        # setup

        self.setLayout(files_vbox)
        self.setWindowTitle('Анализ и сравнение текстов')

        # fields

        self.files_model = files_model

        self.files_lw = files_lw
        self.files_show_path_cbx = files_show_path_cbx

    def _file_add_act(self):
        files, _ = qw.QFileDialog.getOpenFileNames(
            self, 'Выберите файл с текстом', qc.QDir.homePath(), 'Текст (*.txt);;Все файлы (*.*)')

        if files:
            for f in files:
                self.files_model.append_file(f)

    def _file_remove_act(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            self.files_model.removeRows(idx.row(), 1)

    def _file_show_path_act(self):
        self.files_model.show_paths = self.files_show_path_cbx.isChecked()

    def _files_clear_act(self):
        res = qw.QMessageBox.question(self, 'Очистка списка', 'Очистить список файлов?')
        if res == qw.QMessageBox.Yes:
            self.files_model.clear()

    def _ref_file_assign_act(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            file = self.files_model.data(idx, Roles.DataKeyRole)
            self.files_model.ref_file = file
