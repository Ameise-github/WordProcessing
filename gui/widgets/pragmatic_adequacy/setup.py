import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui.logic.pragmatic_adequacy.combinator import PragmaticAdequacyCombinator
from gui.models.common.text_files import TextFilesModel
from gui.models.common.udpipe import UDPipeFile
from gui.widgets import style
from gui.widgets.common.note_button import NoteButton
from gui.widgets.common.hseparator import HSeparator


class PragmaticAdequacySetup(qw.QWidget):
    def __init__(self, parent: t.Optional[qw.QWidget] = None, f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # [other]

        model = TextFilesModel()
        udpipe = UDPipeFile()

        # [widgets]

        comp_type_gbx = qw.QGroupBox('Сравнение')

        d_forward_rdb = qw.QRadioButton('Только прямое')
        d_forward_rdb.setChecked(True)
        d_reverse_rdb = qw.QRadioButton('Только обратное')
        d_both_rdb = qw.QRadioButton('Прямое и обратное')

        direction_bg = qw.QButtonGroup()
        direction_bg.addButton(d_forward_rdb, PragmaticAdequacyCombinator.FORWARD_ONLY)
        direction_bg.addButton(d_reverse_rdb, PragmaticAdequacyCombinator.REVERSE_ONLY)
        direction_bg.addButton(d_both_rdb, PragmaticAdequacyCombinator.BOTH)

        interlace_chb = qw.QCheckBox('Чересстрочное сравнение')

        separator_hs = HSeparator()
        run_btn = qw.QPushButton(style.icons.play_circle, 'Расчитать прагматическую адекватность')
        note_btn = NoteButton()

        # [connect]

        run_btn.clicked.connect(self._on_run)

        # [layout]

        comp_type_vbox = qw.QVBoxLayout()
        comp_type_vbox.addWidget(d_forward_rdb)
        comp_type_vbox.addWidget(d_reverse_rdb)
        comp_type_vbox.addWidget(d_both_rdb)
        comp_type_vbox.addWidget(interlace_chb)
        comp_type_gbx.setLayout(comp_type_vbox)

        hbox = qw.QHBoxLayout()
        hbox.addWidget(note_btn, 1)
        hbox.addWidget(run_btn, 0, qq.AlignRight)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(comp_type_gbx)
        vbox.addWidget(separator_hs)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # [fields]

        self._model = model
        self._udpipe = udpipe

        self._direction_bg = direction_bg
        self._interlace_chb = interlace_chb
        self._note_btn = note_btn


    @property
    def texts_model(self) -> TextFilesModel:
        return self._model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._model = value

    @property
    def udpipe_file(self) -> UDPipeFile:
        return self._udpipe

    @udpipe_file.setter
    def udpipe_file(self, value: UDPipeFile):
        self._udpipe = value

    def _on_run(self):
        try:
            files = self._model.items(exists_only=True)
            if not files:
                raise ValueError('Нечего сравнивать')

            udpipe_path = self.udpipe_file.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')
        except ValueError as e:
            self._note_btn.show_warn(e.args[0])
        else:
            self._note_btn.hide()

            combinator = PragmaticAdequacyCombinator()
            combinator.udpipe = udpipe_path
            combinator.direction = self._direction_bg.checkedId()
            combinator.text_files = files
            if self._interlace_chb.isChecked():
                combinator.interlace = self._model.checked(exists_only=True)

            # TODO test
            combinator.combine()
            for c, n in combinator.combination:
                print(f'{files.index(c)} : {files.index(n)}')
            print('=== === ===')
