import sys
import pathlib as pl

import nltk
import parsing.metric as pm
import PySide2.QtWidgets as qw

from gui.logic.comparison.combinator import ComparisonCombinator
from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets import style
from gui.widgets.comparison.process import ComparisonProcess
from gui.widgets.comparison.setup import ComparisonSetup


def test_combinator(algorithms: AlgorithmList) -> ComparisonCombinator:
    c = ComparisonCombinator()
    c.algorithms = algorithms
    c.reference = pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt')
    c.others = [
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text2.txt')
    ]
    c.udpipe = pl.Path(
        r'C:\Development\Projects\WordProcessing\resource\trainModel\russian-syntagrus-ud-2.5-191206.udpipe'
    )

    return c


def exec_app(algorithms: AlgorithmList):
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    # w = ComparisonProcess(test_combinator(algorithms))
    w = ComparisonSetup()
    w.algorithms = algorithms
    w.show()

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
