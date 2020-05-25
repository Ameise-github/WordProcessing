import sys
import pathlib as pl

import nltk
import parsing.metric as pm
import PySide2.QtWidgets as qw

from gui.logic.pragmatic_adequacy.combinator import PragmaticAdequacyCombinator
from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets import style
from gui.widgets.main.window import MainWindow
from gui.widgets.pragmatic_adequacy.window import PragmaticAdequacyWindow


def test_comparison_params(algorithms: AlgorithmList) -> dict:
    c = dict(
        algorithms=algorithms,
        reference=pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt'),
        others=[
            pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt'),
            pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text2.txt'),
            pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text3.txt'),
            pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\theory.txt'),
        ],
        udpipe=pl.Path(
            r'C:\Development\Projects\WordProcessing\resource\trainModel\russian-syntagrus-ud-2.5-191206.udpipe'
        )
    )

    return c


def test_pragmatic_adequacy_combinator() -> PragmaticAdequacyCombinator:
    c = PragmaticAdequacyCombinator()
    c.text_files = [
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text1.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text2.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\text3.txt'),
        pl.Path(r'C:\Development\Projects\WordProcessing\resource\data\theory.txt')
    ]
    c.interlace = c.text_files[-1::]
    c.udpipe = pl.Path(
        r'C:\Development\Projects\WordProcessing\resource\trainModel\russian-syntagrus-ud-2.5-191206.udpipe'
    )
    c.direction = PragmaticAdequacyCombinator.BOTH

    return c


def exec_app(algorithms: AlgorithmList):
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    style.init()

    # wp = ComparisonProcess(test_combinator(algorithms))
    # wp.show()

    # wp = PragmaticAdequacyWindow(test_pragmatic_adequacy_combinator())
    # wp.show()

    wm = MainWindow()
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
