from parsing.approximation_CT import approximation_CT
from parsing.text import Text


class MetricAnalysis:
    def __init__(self, trainTextUdpipe):
        self._text_standart: Text = None
        self._text: Text = None
        self.name = ""
        self.trainTextUdpipe: str = trainTextUdpipe

    def set_text_standart(self, path_file):
        self._text_standart = Text(path_file, self.trainTextUdpipe)

    def set_text(self, path_file):
        self._text = Text(path_file, self.trainTextUdpipe)

    def get_text_standart(self):
        return self._text_standart

    def get_text(self):
        return self._text

    def run(self):
        pass
