import typing as t
import pathlib as pl

import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

import gui.widgets.notification_server as ns
from gui.models.roles import Roles
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.models.comparison.algorithms import ComparisonAlgorithmsModel
from gui.models.proxy.text_files import TextFilesProxyModel
from gui.widgets import style
from gui.widgets.common.setup import BaseSetup
from gui.widgets.common.checkable_list import CheckableList
from gui.widgets.comparison.dialog import ComparisonDialog


class ComparisonSetup(BaseSetup):
    def __init__(self, parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__('Сравнение', 'Выполнить сравнение', parent, f)

        # [models]

        algorithms_model = ComparisonAlgorithmsModel()
        texts_model = TextFilesModel()

        texts_proxy_model = TextFilesProxyModel()
        texts_proxy_model.setSourceModel(texts_model)

        # [widgets]

        reference_lbl = qw.QLabel('Эталонный текст:')
        reference_cbx = qw.QComboBox()
        reference_cbx.setModel(texts_proxy_model)

        algorithms_lbl = qw.QLabel('Алгоритмы:')
        algorithms_chl = CheckableList()
        order_tb = algorithms_chl.toolbar
        algorithms_chl.model = algorithms_model

        info_act = qw.QAction(style.icons.info, 'Описание алгоритма')

        first_act = order_tb.actions()[0]
        order_tb.insertAction(first_act, info_act)
        order_tb.insertSeparator(first_act)

        # [connect]

        info_act.triggered.connect(self._on_algorithm_info)

        # [layout]

        vbox = qw.QVBoxLayout()
        vbox.addWidget(reference_lbl)
        vbox.addWidget(reference_cbx)
        vbox.addWidget(algorithms_lbl)
        vbox.addWidget(algorithms_chl)
        self.setLayout(vbox)

        # [fields]

        self._algorithms_model = algorithms_model
        self._texts_model = texts_model
        self._texts_proxy_model = texts_proxy_model

        self._algorithms_chl = algorithms_chl
        self._reference_cbx = reference_cbx

        self._udpipe_file = FilePath()

    @property
    def algorithms_model(self) -> ComparisonAlgorithmsModel:
        return self._algorithms_model

    @algorithms_model.setter
    def algorithms_model(self, value: ComparisonAlgorithmsModel):
        self._algorithms_model = value
        self._algorithms_chl.model = value

    @property
    def texts_model(self) -> TextFilesModel:
        return self._texts_model

    @texts_model.setter
    def texts_model(self, value: TextFilesModel):
        self._texts_model = value
        self._texts_proxy_model.setSourceModel(value)

    @property
    def udpipe_file(self) -> FilePath:
        return self._udpipe_file

    @udpipe_file.setter
    def udpipe_file(self, value: FilePath):
        self._udpipe_file = value

    def _on_algorithm_info(self):
        indexes: t.List[qc.QModelIndex] = self._algorithms_chl.list_view.selectedIndexes()
        if not indexes:
            return
        index = indexes[0]
        alg_name: str = index.data(qq.DisplayRole)
        alg_desc: str = index.data(Roles.DescriptionRole)
        qw.QMessageBox.information(self, f'Описание алгоритма: {alg_name}', alg_desc)

    def analysis(self):
        try:
            other_files = self._texts_model.checked(exists_only=True)

            ref_file: pl.Path = self._reference_cbx.currentData(Roles.SourceDataRole)
            if not ref_file or not ref_file.exists():
                raise ValueError('Эталонный текст недоступен')

            if ref_file in other_files:
                other_files.remove(ref_file)
            if not other_files:
                raise ValueError('Нечего сравнивать')

            checked_algs = self._algorithms_model.checked()
            if not checked_algs:
                raise ValueError('Не выбран алгоритм сравнения')

            udpipe_path = self._udpipe_file.path
            if not udpipe_path.exists():
                raise ValueError('Файл UDPipe недоступен')

        except ValueError as v:
            ns.global_server.notify(v.args[0])

        else:
            ns.global_server.clear()

            proc_w = ComparisonDialog(udpipe_path, checked_algs, ref_file, other_files, self)
            proc_w.exec_()
