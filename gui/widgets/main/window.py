import typing as t
import pathlib as pl

import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt as qq

from gui import config
from gui.models.comparison.algorithms import ComparisonAlgorithmsModel, AlgorithmList
from gui.models.common.text_files import TextFilesModel
from gui.models.common.file_path import FilePath
from gui.widgets.common.analysis_widget import AnalysisWidget
from gui.widgets.common.file_path_select import FilePathSelect
from gui.widgets.main.text_files_list import TextFilesList
from gui.widgets.comparison.setup import ComparisonSetup
from gui.widgets.topics_definition.setup import TopicsDefinitionSetup
from gui.widgets.pragmatic_adequacy.setup import PragmaticAdequacySetup
from gui.widgets.morphology_syntax.setup import MorphSyntaxSetup


class MainWindow(qw.QWidget):
    def __init__(self,
                 parent: t.Optional[qw.QWidget] = None,
                 f: qq.WindowFlags = qq.WindowFlags()):
        super().__init__(parent, f)

        # models

        texts_model = TextFilesModel()
        algorithms_model = ComparisonAlgorithmsModel()
        udpipe_file = FilePath(config.DEFAULT_UDPIPE_FILE)
        nltk_file = FilePath(config.DEFAULT_NLTK_FILE)

        # widgets

        udpipe_fps = FilePathSelect()
        udpipe_fps.default_path = config.DEFAULT_UDPIPE_FILE
        udpipe_fps.file = udpipe_file
        udpipe_fps.label.setText('UDPipe файл:')
        udpipe_fps.dialog.setNameFilters(['UDPipe модель (*.udpipe)', 'Все файлы (*.*)'])

        text_lbl = qw.QLabel('Файлы текстов:')
        text_man = TextFilesList()
        text_man.layout().setMargin(0)
        text_man.model = texts_model

        comparator_w = ComparisonSetup()
        comparator_w.algorithms_model = algorithms_model
        comparator_w.texts_model = texts_model
        comparator_w.udpipe_file = udpipe_file

        topics_definer_w = TopicsDefinitionSetup()
        topics_definer_w.texts_model = texts_model
        topics_definer_w.udpipe_file = udpipe_file

        pragmatic_w = PragmaticAdequacySetup()
        pragmatic_w.texts_model = texts_model
        pragmatic_w.udpipe_file = udpipe_file

        morph_syntax_w = MorphSyntaxSetup()
        morph_syntax_w.texts_model = texts_model
        morph_syntax_w.udpipe_file = udpipe_file
        morph_syntax_w.set_nltk_file(nltk_file, True)

        analysis_w = AnalysisWidget()
        analysis_w.add_setup(comparator_w)
        analysis_w.add_setup(topics_definer_w)
        analysis_w.add_setup(pragmatic_w)
        analysis_w.add_setup(morph_syntax_w)

        # layout

        vbox = qw.QVBoxLayout()
        vbox.addWidget(udpipe_fps)
        vbox.addWidget(text_lbl)
        vbox.addWidget(text_man)
        vbox.addWidget(analysis_w)
        self.setLayout(vbox)

        # fields

        self.texts_model = texts_model
        self.algorithms_model = algorithms_model
        self.udpipe_file = udpipe_file

        # setup

        self.setWindowTitle('Анализ и сравнение текстов')
        self.setMinimumSize(650, 400)

    @property
    def algorithms(self) -> AlgorithmList:
        return self.algorithms_model.algorithms

    @algorithms.setter
    def algorithms(self, value: AlgorithmList):
        self.algorithms_model.algorithms = value
