import typing as t
import pathlib as pl
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq
from gui.widgets import NoteButton
from gui.widgets.comparison.file_manager import FileManager
from gui import settings


class ComparisonSetup(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # dialogs

        dialog_set_udp = qw.QFileDialog(self)
        dialog_set_udp.setFileMode(qw.QFileDialog.ExistingFile)
        dialog_set_udp.setWindowTitle('Выберите файл UDPipe модели')
        dialog_set_udp.setNameFilters(
            ['UDPipe модель (*.udpipe)', 'Все файлы (*.*)']
        )

        # widgets

        file_man = FileManager()

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
        udp_add_btn.setIcon(qg.QIcon.fromTheme('document-open'))

        opt_gbx = qw.QGroupBox('Опционально')
        opt_define_topic_cbx = qw.QCheckBox('Определить тематику')

        compare_btn = qw.QPushButton('Запуск')
        compare_btn.setIcon(qg.QIcon.fromTheme('system-run'))

        note_btn = NoteButton()

        # connections

        udp_add_btn.clicked.connect(self._on_choose_udp_file)
        compare_btn.clicked.connect(self._on_run_comparison)

        # layout

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
        bottom_hbox.addWidget(note_btn, 1)
        bottom_hbox.addWidget(compare_btn, 0, qq.AlignRight)

        files_vbox = qw.QVBoxLayout()
        files_vbox.addWidget(file_man)
        files_vbox.addWidget(alg_gbx)
        files_vbox.addWidget(opt_gbx)
        files_vbox.addLayout(bottom_hbox)

        # fields

        self.dialog_set_udp = dialog_set_udp

        self.file_man = file_man

        self.alg_stochastic_cbx = alg_stochastic_cbx
        self.alg_jaccard_cbx = alg_jaccard_cbx
        self.alg_cossim_cbx = alg_cossim_cbx

        self.udp_file_lned = udp_file_lned

        self.note_btn = note_btn

        # setup

        self.setLayout(files_vbox)
        self.setWindowTitle('Анализ и сравнение текстов')

    def _on_choose_udp_file(self):
        if self.dialog_set_udp.exec_():
            file = self.dialog_set_udp.selectedFiles()[0]
            self.udp_file_lned.setText(file)

    def _on_run_comparison(self):
        ref_file = self.file_man.model.exist_ref_file
        other_files = self.file_man.model.exist_other_files

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
            self.note_btn.show_warn(v.args[0])
            return

        self.note_btn.hide()

        # TODO показать окно выполнения
        qw.QMessageBox.information(self, '', 'Типа выполнение')
