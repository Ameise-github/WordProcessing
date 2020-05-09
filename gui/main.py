import sys
import PySide2.QtWidgets as qw
from gui.widgets.comparison import ComparisonProcess
from gui.models.comparison import AlgorithmList
from gui.widgets import style
import parsing.metric as pm


def get_algorithms() -> AlgorithmList:
    return [
        pm.CosineSimilarity(),
        pm.MetricJaccard(),
        pm.StohasticAnalysis()
    ]


def main():
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    w = ComparisonProcess()
    # w = ComparisonSetup()
    # w.algorithms = get_algorithms()
    w.show()

    rc = app.exec_()


if __name__ == '__main__':
    main()
