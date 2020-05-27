import typing as t
import pathlib as pl


class StyleSheetStorage:
    def __init__(self):
        self._sheets: t.Dict[str, str] = {}

    def load(self, dir_path: pl.Path):
        # load
        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            if file.suffix.lower() != '.css':
                continue

            name = file.stem
            with file.open('r') as f:
                self._sheets[name.replace('-', '_')] = f.read()

    def __getattr__(self, item: str) -> str:
        sheet = self._sheets.get(item)
        if not sheet:
            raise AttributeError(f'CSS <{sheet}> not found')
        return sheet
