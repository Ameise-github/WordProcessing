import sys
import PySide2.QtWidgets as qw
from gui.widgets.comparison import ComparisonProcess
from gui.widgets import style


def main():
    app = qw.QApplication(sys.argv)
    app.setStyleSheet(style.STYLE_SHEET)

    w = ComparisonProcess()
    w.show()

    rc = app.exec_()


if __name__ == '__main__':
    main()
