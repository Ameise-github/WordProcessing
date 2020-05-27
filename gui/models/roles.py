from PySide2.QtCore import Qt as qq


def _auto(x):
    return qq.UserRole + x


class Roles:
    SourceDataRole = _auto(1)
    DescriptionRole = _auto(2)
