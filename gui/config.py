import pathlib as pl


def resolve(path: str) -> pl.Path:
    if not hasattr(resolve, 'module_path'):
        setattr(resolve, 'module_path', None)
        resolve.module_path = pl.Path(__file__).parent.absolute()

    return (resolve.module_path / path).resolve()


DEFAULT_UDPIPE_FILE = resolve('../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe')
DEFAULT_NLTK_FILE = resolve('../resource/data/trainText.tab')
