import pathlib as pl

_module_path = pl.Path(__file__).parent.absolute()

DEFAULT_UDPIPE_FILE = (_module_path / '../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe').resolve()
