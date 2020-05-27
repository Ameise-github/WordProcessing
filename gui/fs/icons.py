import typing as t
import pathlib as pl

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtSvg as svg

from gui.exception import LoadError


class IconStorage:
    def __init__(self):
        self._icons: t.Dict[str, qg.QIcon] = {}

    def load(self, dir_path: pl.Path, size: qc.QSize):
        # load
        name2render_dict: t.Dict[str, svg.QSvgRenderer] = {}

        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            if file.suffix.lower() != '.svg':
                continue

            render = svg.QSvgRenderer(str(file))

            if not render.isValid():
                raise LoadError('Invalid SVG')

            name2render_dict[file.stem] = render

        # draw
        pixmap = qg.QImage(size, qg.QImage.Format_ARGB32)
        painter = qg.QPainter()
        name2icon_dict: t.Dict[str, qg.QIcon] = {}

        for name, render in name2render_dict.items():
            painter.begin(pixmap)
            painter.save()
            painter.setCompositionMode(qg.QPainter.CompositionMode_Clear)
            painter.fillRect(pixmap.rect(), qc.Qt.transparent)
            painter.restore()
            render.render(painter)
            painter.end()

            icon = qg.QIcon(qg.QPixmap.fromImage(pixmap))
            name2icon_dict[name.replace('-', '_')] = icon

        # result
        self._icons = name2icon_dict

    def __getattr__(self, item: str) -> qg.QIcon:
        icon = self._icons.get(item)
        if not icon:
            raise AttributeError(f'Icon <{item}> not found')
        return icon
