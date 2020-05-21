import sys
import pathlib as pl

import nltk
import parsing.metric as pm
import PySide2.QtWidgets as qw

from gui.logic.comparison.combinator import ComparisonCombinator
from gui.models.algorithms import AlgorithmList
from gui.widgets import style
from gui.widgets.window.main import Main
from gui.widgets.window.comparison import ComparisonProcess


def test_combinator(algorithms: AlgorithmList) -> ComparisonCombinator:
    c = ComparisonCombinator()
    c.algorithms = algorithms
    c.reference = pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt')
    c.others = [
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text2.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text3.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\theory.txt'),
    ]
    c.udpipe = pl.Path(
        r'C:\Development\Projects\WordProcessing\resource\trainModel\russian-syntagrus-ud-2.5-191206.udpipe'
    )

    return c


def exec_app(algorithms: AlgorithmList):
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    style.init()

    # wp = ComparisonProcess(test_combinator(algorithms))
    # wp.show()

    wm = Main()
    wm.algorithms = algorithms
    wm.show()

    return app.exec_()


def main():
    nltk.download('punkt')
    nltk.download('stopwords')

    algorithms = [
        pm.CosineSimilarityAlgorithm(),
        pm.JaccardAlgorithm(),
        pm.StochasticAlgorithm()
    ]

    rc = exec_app(algorithms)
    exit(rc)


if __name__ == '__main__':
    main()
