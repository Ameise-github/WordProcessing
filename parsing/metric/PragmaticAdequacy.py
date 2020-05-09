from parsing.metric.MetricAnalysis import BaseMetricAnalysis
from parsing.text import Text


class PragmaticAdequacy(BaseMetricAnalysis):
    def __init__(self):
        super().__init__()
        self.name = "Показатель прагматической адекватности"

    def set_text_standart(self, path_file):
        ts = Text(path_file, self._trainTextUdpipe)
        ts.freq_dist_dic()
        ts.matrix_syntax()
        ts.get_entropy()
        self._text_standart = ts

    def set_text(self, path_file):
        t = Text(path_file, self._trainTextUdpipe)
        t.freq_dist_dic()
        t.matrix_syntax()
        t.get_entropy()
        self._text = t

    def run(self):
        text_old = self._text_standart
        text_new = self._text
        # разность значений информационной энтропии
        I = text_new.entropy - text_old.entropy

        return round(I, 3)