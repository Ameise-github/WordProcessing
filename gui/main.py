import sys
import PySide2.QtWidgets as qw
from gui.models.comparison import AlgorithmList
from gui.widgets.comparison import ComparisonSetup
from gui.widgets import style


def get_algorithms() -> AlgorithmList:
    return []


def main():
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    w = ComparisonSetup()
    w.algorithms = get_algorithms()
    w.show()

    rc = app.exec_()


if __name__ == '__main__':
    main()
