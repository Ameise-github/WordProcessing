from parsing.text import Text


class MetricAnalysis:
    def __init__(self):
        self._text_standart: Text = None
        self._text: Text = None
        self.name = ""
        self._trainTextUdpipe: str = ""

    def set_trainTextUdpipe(self, peth_trainTextUdpipe):
        self._trainTextUdpipe = peth_trainTextUdpipe

    def get_trainTextUdpipe(self):
        return self._trainTextUdpipe

    def set_text_standart(self, path_file):
        self._text_standart = Text(path_file, self._trainTextUdpipe)

    def set_text(self, path_file):
        self._text = Text(path_file, self._trainTextUdpipe)

    def get_text_standart(self):
        return self._text_standart

    def get_text(self):
        return self._text

    def run(self):
        pass
