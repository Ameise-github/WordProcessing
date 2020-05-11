import sys
import pathlib as pl
import PySide2.QtWidgets as qw
import nltk
import parsing.metric as pm
from gui.widgets.comparison import ComparisonProcess, ComparisonSetup
from gui.models.comparison import AlgorithmList
from gui.widgets import style
from gui.logic.comparison import ComparisonCombinator


def test_combinator(algorithms: AlgorithmList) -> ComparisonCombinator:
    c = ComparisonCombinator()
    c.algorithms = algorithms
    c.reference = pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt')
    c.files = [
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
        pm.CosineSimilarity(),
        pm.MetricJaccard(),
        pm.StohasticAnalysis()
    ]

    rc = exec_app(algorithms)
    exit(rc)


if __name__ == '__main__':
    main()
