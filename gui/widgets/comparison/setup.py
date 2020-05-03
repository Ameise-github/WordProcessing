import typing as t
import pathlib as pl
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from gui.models.comparison import ComparisonFilesModel
from gui.models import Roles
from gui import settings


class ComparisonSetupWidget(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qc.Qt.WindowFlags()):
        super().__init__(parent, f)

        btn_min_width = 100

        # models
        files_model = ComparisonFilesModel()

        # dialogs

        dialog_add_text = qw.QFileDialog(self)
        dialog_add_text.setFileMode(qw.QFileDialog.ExistingFiles)
        dialog_add_text.setWindowTitle('Выберите файлы с текстом')
        dialog_add_text.setNameFilters(
            ['Текст (*.txt)', 'Все файлы (*.*)']
        )

        dialog_set_udp = qw.QFileDialog(self)
        dialog_set_udp.setFileMode(qw.QFileDialog.ExistingFile)
        dialog_set_udp.setWindowTitle('Выберите файл UDPipe модели')
        dialog_set_udp.setNameFilters(
            ['UDPipe модель (*.udpipe)', 'Все файлы (*.*)']
        )

        # widgets

        files_lw = qw.QListView()
        files_lw.setModel(files_model)

        file_add_btn = qw.QPushButton('Добавить...')
        file_add_btn.setMinimumWidth(btn_min_width)
        file_add_btn.setIcon(qg.QIcon.fromTheme('list-add'))
        file_remove_btn = qw.QPushButton('Удалить')
        file_remove_btn.setMinimumWidth(btn_min_width)
        file_remove_btn.setIcon(qg.QIcon.fromTheme('list-remove'))
        files_show_path_cbx = qw.QCheckBox('Показать полный путь')
        files_clear_btn = qw.QPushButton('Очистить')
        files_clear_btn.setMinimumWidth(btn_min_width)
        files_clear_btn.setIcon(qg.QIcon.fromTheme('edit-clear'))

        ref_file_btn = qw.QPushButton('Выбрать эталонным')
        ref_file_btn.setIcon(qg.QIcon.fromTheme('go-up'))

        alg_gbx = qw.QGroupBox('Алгоритмы сравнений')
        alg_stochastic_cbx = qw.QCheckBox('Стохастический')
        alg_jaccard_cbx = qw.QCheckBox('Коэффициент Жаккара')
        alg_cossim_cbx = qw.QCheckBox('Косинусное сходство')

        alg_sep = qw.QFrame()
        alg_sep.setMinimumHeight(1)
        alg_sep.setFrameShape(qw.QFrame.StyledPanel)

        udp_lbl = qw.QLabel('Файл UDPipe модели:')
        udp_file_lned = qw.QLineEdit()
        udp_file_lned.setReadOnly(True)
        udp_file_lned.setPlaceholderText(settings.DEFAULT_UDPIPE_FILE.name)
        udp_add_btn = qw.QPushButton('Обзор...')
        udp_add_btn.setMinimumWidth(btn_min_width)
        udp_add_btn.setIcon(qg.QIcon.fromTheme('document-open'))

        opt_gbx = qw.QGroupBox('Опционально')
        opt_define_topic_cbx = qw.QCheckBox('Определить тематику')

        compare_btn = qw.QPushButton('Запуск')
        compare_btn.setMinimumWidth(btn_min_width)
        compare_btn.setIcon(qg.QIcon.fromTheme('system-run'))

        warning_btn = qw.QPushButton('Внимание!')
        warning_btn.setObjectName('warning-note')
        warning_btn.setFlat(True)
        warning_btn.setStyleSheet('QPushButton { color: rgb(210,105,30); text-align: left; }')
        warning_btn.setIcon(qg.QIcon.fromTheme('dialog-warning'))

        # connections

        file_add_btn.clicked.connect(self._on_add_file)
        file_remove_btn.clicked.connect(self._on_remove_file)
        files_show_path_cbx.clicked.connect(self._on_show_path_files)
        files_clear_btn.clicked.connect(self._on_clear_files)
        ref_file_btn.clicked.connect(self._on_assign_ref_file)
        udp_add_btn.clicked.connect(self._on_choose_udp_file)
        compare_btn.clicked.connect(self._on_run_comparison)
        warning_btn.clicked.connect(self._on_hide_warning)

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

        udp_file_hbox = qw.QHBoxLayout()
        udp_file_hbox.addWidget(udp_file_lned, 1)
        udp_file_hbox.addWidget(udp_add_btn)

        alg_vbox = qw.QVBoxLayout()
        alg_vbox.addWidget(alg_stochastic_cbx)
        alg_vbox.addWidget(alg_jaccard_cbx)
        alg_vbox.addWidget(alg_cossim_cbx)
        alg_vbox.addWidget(alg_sep)
        alg_vbox.addWidget(udp_lbl)
        alg_vbox.addLayout(udp_file_hbox)
        alg_vbox.addStretch(1)
        alg_gbx.setLayout(alg_vbox)

        opt_vbox = qw.QVBoxLayout()
        opt_vbox.addWidget(opt_define_topic_cbx)
        opt_vbox.addStretch(1)
        opt_gbx.setLayout(opt_vbox)

        bottom_hbox = qw.QHBoxLayout()
        bottom_hbox.addWidget(warning_btn, 1)
        bottom_hbox.addWidget(compare_btn, 0, qq.AlignRight)

        files_vbox = qw.QVBoxLayout()
        files_vbox.addLayout(files_ctl_hbox)
        files_vbox.addWidget(files_lw, 1)
        files_vbox.addLayout(ref_file_hbox)
        files_vbox.addWidget(alg_gbx)
        files_vbox.addWidget(opt_gbx)
        files_vbox.addLayout(bottom_hbox)

        # fields

        self.files_model = files_model

        self.dialog_add_text = dialog_add_text
        self.dialog_set_udp = dialog_set_udp

        self.files_lw = files_lw
        self.files_show_path_cbx = files_show_path_cbx

        self.alg_stochastic_cbx = alg_stochastic_cbx
        self.alg_jaccard_cbx = alg_jaccard_cbx
        self.alg_cossim_cbx = alg_cossim_cbx

        self.udp_file_lned = udp_file_lned

        self.warning_btn = warning_btn

        # setup

        self.setLayout(files_vbox)
        self.setWindowTitle('Анализ и сравнение текстов')

        self._on_hide_warning()

    def _show_warning(self, text: str):
        self.warning_btn.setText(text)
        self.warning_btn.show()

    def _on_add_file(self):
        if self.dialog_add_text.exec_():
            files = self.dialog_add_text.selectedFiles()
            for f in files:
                self.files_model.append_file(f)

    def _on_remove_file(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            self.files_model.removeRows(idx.row(), 1)

    def _on_show_path_files(self):
        self.files_model.show_paths = self.files_show_path_cbx.isChecked()

    def _on_clear_files(self):
        if self.files_model.rowCount() <= 0:
            return
        res = qw.QMessageBox.question(self, 'Очистка списка', 'Очистить список файлов?')
        if res == qw.QMessageBox.Yes:
            self.files_model.clear()

    def _on_assign_ref_file(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            file = self.files_model.data(idx, Roles.DataKeyRole)
            self.files_model.ref_file = file

    def _on_choose_udp_file(self):
        if self.dialog_set_udp.exec_():
            file = self.dialog_set_udp.selectedFiles()[0]
            self.udp_file_lned.setText(file)

    def _on_run_comparison(self):
        ref_file = self.files_model.exist_ref_file
        other_files = self.files_model.exist_other_files

        chk_stochastic = self.alg_stochastic_cbx.isChecked()
        chk_jaccard = self.alg_jaccard_cbx.isChecked()
        chk_cossim = self.alg_cossim_cbx.isChecked()

        udp_file = self.udp_file_lned.text()
        if not udp_file:
            udp_file = settings.DEFAULT_UDPIPE_FILE
        else:
            udp_file = pl.Path(udp_file)

        try:
            if not ref_file:
                if len(other_files) <= 1:
                    raise ValueError('Доступно менее двух текстов')
                raise ValueError('Эталонный текст недоступен')
            if not (chk_stochastic or chk_jaccard or chk_cossim):
                raise ValueError('Не выбран алгоритм сравнения')
            if not udp_file.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as v:
            self._show_warning(v.args[0])
            return
        self._on_hide_warning()

        # TODO показать окно выполнения

    def _on_hide_warning(self):
        self.warning_btn.hide()
