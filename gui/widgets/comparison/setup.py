import typing as t
import PySide2.QtCore as qc
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
        file_remove_btn = qw.QPushButton('Удалить')
        file_remove_btn.setMinimumWidth(btn_min_width)
        files_show_path_cbx = qw.QCheckBox('Показать полный путь')
        files_clear_btn = qw.QPushButton('Очистить')
        files_clear_btn.setMinimumWidth(btn_min_width)

        ref_file_btn = qw.QPushButton('Выбрать эталонным')

        alg_gbx = qw.QGroupBox('Алгоритмы сравнений')
        alg_stochastic_cbx = qw.QCheckBox('Стохастический')
        alg_jaccard_cbx = qw.QCheckBox('Коэффициент Жаккара')
        alg_cossim_cbx = qw.QCheckBox('Косинусное сходство')

        alg_sep = qw.QFrame()
        alg_sep.setMinimumHeight(1)
        alg_sep.setFrameShape(qw.QFrame.StyledPanel)
        # alg_sep.setFrameShadow(qw.QFrame.Sunken)

        udp_lbl = qw.QLabel('Файл UDPipe модели:')
        udp_file_lned = qw.QLineEdit()
        udp_file_lned.setReadOnly(True)
        udp_file_lned.setPlaceholderText(settings.DEFAULT_UDPIPE_FILE.name)
        udp_add_btn = qw.QPushButton('Обзор...')
        udp_add_btn.setMinimumWidth(btn_min_width)

        opt_gbx = qw.QGroupBox('Опционально')
        opt_define_topic_cbx = qw.QCheckBox('Определить тематику')

        compare_btn = qw.QPushButton('Запуск')
        compare_btn.setMinimumWidth(btn_min_width)

        # connections

        file_add_btn.clicked.connect(self._file_add_act)
        file_remove_btn.clicked.connect(self._file_remove_act)
        files_show_path_cbx.clicked.connect(self._file_show_path_act)
        files_clear_btn.clicked.connect(self._files_clear_act)
        ref_file_btn.clicked.connect(self._ref_file_assign_act)
        udp_add_btn.clicked.connect(self._udp_set_file_act)

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

        files_vbox = qw.QVBoxLayout()
        files_vbox.addLayout(files_ctl_hbox)
        files_vbox.addWidget(files_lw, 1)
        files_vbox.addLayout(ref_file_hbox)
        files_vbox.addWidget(alg_gbx)
        files_vbox.addWidget(opt_gbx)
        files_vbox.addWidget(compare_btn, 0, qq.AlignRight)

        # setup

        self.setLayout(files_vbox)
        self.setWindowTitle('Анализ и сравнение текстов')

        # fields

        self.files_model = files_model

        self.dialog_add_text = dialog_add_text
        self.dialog_set_udp = dialog_set_udp

        self.files_lw = files_lw
        self.files_show_path_cbx = files_show_path_cbx

        self.udp_file_lned = udp_file_lned

    def _file_add_act(self):
        if self.dialog_add_text.exec_():
            files = self.dialog_add_text.selectedFiles()
            for f in files:
                self.files_model.append_file(f)

    def _file_remove_act(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            self.files_model.removeRows(idx.row(), 1)

    def _file_show_path_act(self):
        self.files_model.show_paths = self.files_show_path_cbx.isChecked()

    def _files_clear_act(self):
        if self.files_model.rowCount() <= 0:
            return
        res = qw.QMessageBox.question(self, 'Очистка списка', 'Очистить список файлов?')
        if res == qw.QMessageBox.Yes:
            self.files_model.clear()

    def _ref_file_assign_act(self):
        indexes: t.List[qc.QModelIndex] = self.files_lw.selectedIndexes()
        for idx in indexes:
            file = self.files_model.data(idx, Roles.DataKeyRole)
            self.files_model.ref_file = file

    def _udp_set_file_act(self):
        if self.dialog_set_udp.exec_():
            file = self.dialog_set_udp.selectedFiles()[0]
            self.udp_file_lned.setText(file)
