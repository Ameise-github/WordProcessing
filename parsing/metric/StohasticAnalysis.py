import math

from parsing.approximation_CT import approximation_CT
from parsing.metric.MetricAnalysis import BaseMetricAnalysis
from parsing.text import Text


class StohasticAnalysis(BaseMetricAnalysis):
    def __init__(self):
        super().__init__()
        self.name = "Критерий стохастического подобия"

    def set_text_standart(self, path_file):
        ts = Text(path_file, self._trainTextUdpipe)
        ts.freq_dist_dic()
        ts.matrix_syntax()
        ts.get_entropy()
        ts.CT = approximation_CT(ts.entropy, ts.entropy2, ts.entropy3)
        self._text_standart = ts

    def set_text(self, path_file):
        t = Text(path_file, self._trainTextUdpipe)
        t.freq_dist_dic()
        t.matrix_syntax()
        t.get_entropy()
        t.CT = approximation_CT(t.entropy, t.entropy2,t.entropy3)
        self._text = t

    def run(self):
        """
        вычисление стахостического подобия текстов
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Вычисление коэфициента подобия(степени схожести)
        # для отчета
        # f_s = text_standart.CT.return_f()
        # f = get_text.CT.return_f()
        # ff = (f_s - f)**2
        # intgrl = integrate(ff, (abc.t, -oo, oo))
        # # print(intgrl.doit(), intgrl.evalf())
        # if(intgrl != 0 ):
        #     d = math.sqrt(intgrl)
        #     p = 1 - d
        #     print(intgrl, d, p)

        # для рассчета
        ts = self.get_text_standart()
        t = self.get_text()
        standrt = (ts.CT.C1 * ts.CT.T1) + (ts.CT.C2 * ts.CT.T2)
        tmp = (t.CT.C1 * t.CT.T1) + (t.CT.C2 * t.CT.T2)
        d = math.sqrt(math.pow((standrt - tmp), 2))
        p = 1 - d
        if (p < 0):
            t.p = 0.01
        else:
            t.p = round(p, 2)
            # проверка
            # print("tmp = {}; d = {}; p = {}".format(tmp, d, round(p, 2)))