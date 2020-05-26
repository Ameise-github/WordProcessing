import typing as t

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

import gui.widgets.notification_server as ns
from gui.logic.pragmatic_adequacy.thread import PragmaticAdequacyThread
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.widgets.common.setup import BaseSetup
from gui.widgets.pragmatic_adequacy.window import PragmaticAdequacyWindow


class PragmaticAdequacySetup(BaseSetup):
    def __init__(self, parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__('Прагматическая адекватность', 'Расчитать адекватность', parent, f)

        # [other]

        model = TextFilesModel()
        udpipe = FilePath()

        # [widgets]

        comp_type_gbx = qw.QGroupBox('Сравнение')

        d_forward_rdb = qw.QRadioButton('Только прямое')
        d_forward_rdb.setChecked(True)
        d_reverse_rdb = qw.QRadioButton('Только обратное')
        d_both_rdb = qw.QRadioButton('Прямое и обратное')

        direction_bg = qw.QButtonGroup()
        direction_bg.addButton(d_forward_rdb, PragmaticAdequacyThread.FORWARD_ONLY)
        direction_bg.addButton(d_reverse_rdb, PragmaticAdequacyThread.REVERSE_ONLY)
        direction_bg.addButton(d_both_rdb, PragmaticAdequacyThread.BOTH)

        interlace_chb = qw.QCheckBox('Чересстрочное сравнение')

        # [layout]

        comp_type_vbox = qw.QVBoxLayout()
        comp_type_vbox.addWidget(d_forward_rdb)
        comp_type_vbox.addWidget(d_reverse_rdb)
        comp_type_vbox.addWidget(d_both_rdb)
        comp_type_vbox.addWidget(interlace_chb)
        comp_type_gbx.setLayout(comp_type_vbox)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(comp_type_gbx)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # [fields]

        self._model = model
        self._udpipe = udpipe

        self._direction_bg = direction_bg
        self._interlace_chb = interlace_chb

    @property
    def texts_model(self) -> TextFilesModel:
        return self._model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._model = value

    @property
    def udpipe_file(self) -> FilePath:
        return self._udpipe

    @udpipe_file.setter
    def udpipe_file(self, value: FilePath):
        self._udpipe = value

    def analysis(self):
        try:
            files = self._model.items(exists_only=True)
            if not files:
                raise ValueError('Нечего сравнивать')

            udpipe_path = self.udpipe_file.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')

        except ValueError as v:
            ns.global_server.notify(v.args[0])

        else:
            ns.global_server.clear()

            interlace = self._model.checked(exists_only=True) if self._interlace_chb.isChecked() else []

            proc_w = PragmaticAdequacyWindow(udpipe_path, files, interlace, self._direction_bg.checkedId(), self)
            proc_w.exec_()
