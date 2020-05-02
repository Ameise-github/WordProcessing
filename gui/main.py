import sys
import PySide2.QtWidgets as qw
from gui.widgets.comparison import ComparisonSetupWidget


def main():
    app = qw.QApplication(sys.argv)

    w = ComparisonSetupWidget()
    w.show()

    rc = app.exec_()


if __name__ == '__main__':
    main()
