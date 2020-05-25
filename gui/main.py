import sys

import nltk
import parsing.metric as pm
import PySide2.QtWidgets as qw

from gui.models.comparison.algorithms import AlgorithmList
from gui.widgets import style
from gui.widgets.main.window import MainWindow


def exec_app(algorithms: AlgorithmList):
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    style.init()

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
